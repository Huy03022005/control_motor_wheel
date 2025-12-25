import cv2
import mediapipe as mp
import math
import numpy as np
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# --- CẤU HÌNH INFLUXDB ---
url = "http://localhost:8086" # Thay bằng URL InfluxDB của bạn
token = "9V97H6B0YyA7FywV_F4uHRVo44pSGUlSR9kzRNa-1OuTBHxON9AYucUB2PpYBtI2hFzW7R1EcsA5gX_HM7zb8Q=="          # Thay bằng Token của bạn
org = "my_org"              # Thay bằng tên Organization
bucket = "wheel_data"        # Thay bằng tên Bucket (ví dụ: WheelControl)

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# --- KHỞI TẠO NHẬN DIỆN TAY ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success: break

    percent = 0
    bar_height = 400
    image = cv2.flip(image, 1)
    h, w, c = image.shape
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            thumb = hand_landmarks.landmark[4]
            index = hand_landmarks.landmark[8]
            cx, cy = int(thumb.x * w), int(thumb.y * h)
            ix, iy = int(index.x * w), int(index.y * h)

            # Vẽ đường thẳng nối giữa ngón cái và ngón trỏ
            cv2.line(image, (cx, cy), (ix, iy), (255, 0, 255), 3) 

            # Vẽ thêm 2 vòng tròn nhỏ ở đầu ngón để nhìn cho chuyên nghiệp hơn
            cv2.circle(image, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(image, (ix, iy), 10, (255, 0, 255), cv2.FILLED)

            distance = math.hypot(ix - cx, iy - cy)
            percent = int(np.interp(distance, [20, 200], [0, 100]))
            bar_height = np.interp(distance, [20, 200], [400, 150])

            # --- GỬI DỮ LIỆU LÊN INFLUXDB ---
            # Tạo một point dữ liệu cho tốc độ bánh xe
            point = Point("wheel_speed") \
                .tag("device", "hand_controller") \
                .field("speed_percent", float(percent))
            
            try:
                write_api.write(bucket=bucket, org=org, record=point)
            except Exception as e:
                print(f"Lỗi gửi InfluxDB: {e}")

    # Vẽ giao diện
    cv2.rectangle(image, (50, 150), (85, 400), (255, 255, 255), 3)
    cv2.rectangle(image, (50, int(bar_height)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(image, f'SPEED: {percent}%', (40, 450), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    cv2.imshow('Wheel Speed Controller', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()