import cv2
import mediapipe as mp
import math

# Khởi tạo MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Khởi tạo webcam
cap = cv2.VideoCapture(0)

# Hàm tính khoảng cách giữa hai điểm
def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

# Hàm kiểm tra ngón tay có giơ lên hay không
def is_finger_up(hand_landmarks, finger_tip, finger_pip, finger_mcp, wrist=None, is_thumb=False):
    """
    Kiểm tra xem ngón tay có giơ lên hay không
    - Đối với ngón cái: so sánh với cổ tay
    
    - Đối với các ngón khác: so sánh với khớp MCP
    """
    if is_thumb:
        # So sánh ngón cái với cổ tay
        return finger_tip.y < wrist.y
    else:
        # So sánh các ngón khác với khớp MCP
        return finger_tip.y < finger_mcp.y

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Không thể đọc từ webcam")
            continue
        
        # Chuyển đổi BGR sang RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Xử lý ảnh để nhận diện bàn tay
        results = hands.process(image_rgb)
        
        # Chuyển đổi RGB sang BGR để hiển thị bằng OpenCV
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        
        # Vẽ landmarks nếu phát hiện bàn tay
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Vẽ landmarks và kết nối
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                
                # Lấy kích thước ảnh
                h, w, _ = image.shape
                
                # Lấy các điểm landmarks cần thiết
                landmarks = hand_landmarks.landmark
                
                # Điểm landmarks cho 2 ngón tay đầu tiên (ngón cái và ngón trỏ)
                thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
                thumb_ip = landmarks[mp_hands.HandLandmark.THUMB_IP]
                thumb_mcp = landmarks[mp_hands.HandLandmark.THUMB_MCP]
                thumb_cmc = landmarks[mp_hands.HandLandmark.THUMB_CMC]
                
                index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_pip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP]
                index_mcp = landmarks[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                
                # Cổ tay
                wrist = landmarks[mp_hands.HandLandmark.WRIST]
                
                # Kiểm tra xem 2 ngón tay có giơ lên không
                thumb_up = is_finger_up(hand_landmarks, thumb_tip, thumb_ip, thumb_mcp, wrist, is_thumb=True)
                index_up = is_finger_up(hand_landmarks, index_tip, index_pip, index_mcp)
                
                # Vẽ vòng tròn và thông tin cho 2 ngón tay
                fingers_info = []
                
                # Ngón cái
                thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
                thumb_color = (0, 255, 0) if thumb_up else (0, 0, 255)
                cv2.circle(image, (thumb_x, thumb_y), 10, thumb_color, -1)
                cv2.putText(image, f'Thumb: {"UP" if thumb_up else "DOWN"}', 
                           (thumb_x - 50, thumb_y - 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, thumb_color, 2)
                fingers_info.append(f"Thumb: {'UP' if thumb_up else 'DOWN'}")
                
                # Ngón trỏ
                index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)
                index_color = (0, 255, 0) if index_up else (0, 0, 255)
                cv2.circle(image, (index_x, index_y), 10, index_color, -1)
                cv2.putText(image, f'Index: {"UP" if index_up else "DOWN"}', 
                           (index_x - 50, index_y - 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, index_color, 2)
                fingers_info.append(f"Index: {'UP' if index_up else 'DOWN'}")
                
                # Tính khoảng cách giữa ngón cái và ngón trỏ
                distance = calculate_distance(thumb_tip, index_tip)
                distance_px = distance * w  # Chuyển đổi sang pixel
                
                # Vẽ đường nối giữa 2 ngón tay
                cv2.line(image, (thumb_x, thumb_y), (index_x, index_y), (255, 255, 0), 2)
                
                # Hiển thị khoảng cách
                mid_x = (thumb_x + index_x) // 2
                mid_y = (thumb_y + index_y) // 2
                cv2.putText(image, f'Distance: {distance_px:.1f}px', 
                           (mid_x - 60, mid_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                
                # Hiển thị trạng thái tổng hợp
                status_y = 30
                cv2.putText(image, "Two Finger Detection Status:", 
                           (10, status_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                for i, info in enumerate(fingers_info):
                    status_y += 30
                    cv2.putText(image, info, 
                               (20, status_y), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Hiển thị trạng thái cả hai ngón cùng giơ lên
                if thumb_up and index_up:
                    cv2.putText(image, "TWO FINGERS UP!", 
                               (w // 2 - 100, 50), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                
                # Thêm hướng dẫn
                cv2.putText(image, "Press 'q' to quit", 
                           (w - 200, h - 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        
        # Hiển thị kết quả
        cv2.imshow('Two Finger Detection (Thumb + Index)', image)
        
        # Thoát khi nhấn 'q'
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()