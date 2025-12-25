#tải influxDB trên powershell
# 1. Tạo thư mục InfluxDB ở ổ E
New-Item -ItemType Directory -Force -Path "E:\influxdb"
cd "E:\influxdb"

# 2. Tải file
wget https://download.influxdata.com/influxdb/releases/v2.7.12/influxdb2-2.7.12-windows.zip -UseBasicParsing -OutFile influxdb2-2.7.12-windows.zip

# 3. Giải nén
Expand-Archive .\influxdb2-2.7.12-windows.zip -DestinationPath "E:\influxdb" 

# 4. Chuyển file ra ngoài thư mục gốc E:\influxdb
Move-Item -Path "E:\influxdb\influxdb2-2.7.5-windows-amd64\*" -Destination "E:\influxdb"

# 5. Dọn dẹp file thừa
Remove-Item -Path "E:\influxdb\influxdb.zip"
Remove-Item -Path "E:\influxdb\influxdb2-2.7.5-windows-amd64" -Recurse


# cách chạy
## Bây giờ, bạn mở trình duyệt (Chrome/Edge) và làm theo các bước sau:

## Truy cập: http://localhost:8086

## Nhấn Get Started.

## Thiết lập các thông số (Hãy ghi chép lại để dán vào Python):

## Username: admin (hoặc tên bạn muốn).

## Password: admin12345 (phải có ít nhất 8 ký tự).

## Initial Organization Name: my_org

## Initial Bucket Name: wheel_data

## Sau khi nhấn Continue, hệ thống sẽ cung cấp cho bạn một mã Operator Token. Hãy nhấn Copy to Clipboard.


Lưu ý quan trọng:
Không tắt cửa sổ PowerShell đang chạy .\influxd.exe. Nếu tắt, file Python sẽ báo lỗi không kết nối được server.

Nếu bạn muốn dữ liệu lưu vào ổ E thay vì ổ C (như trong log của bạn đang hiện C:\Users\nguye\...), lần sau hãy khởi động bằng lệnh: .\influxd.exe --engine-path="E:\influxdb\data" --bolt-path="E:\influxdb\influxd.bolt"


#chạy chỉ cần bấm run in terminal ( chạy file hand_to_influxdb)