import express from "express"
//nhập thư viện express vào dự án để sử dụng các tính năng server

import routers from "./routes/routers.js";
// Nhập file cấu hình các tuyến đường (routes) từ thư mục khác

const app = express();
// khởi tạo một đối tượng express

app.use("/api", routers)
// Gắn (mount) các tuyến đường từ file routers.js vào tiền tố "/api"
// Ví dụ: Nếu trong routers.js có route "/", người dùng sẽ truy cập qua "http://localhost:5001/api/"

app.listen(5001, ()=>{
    // ra lệnh cho server lắng nghe các yêu vầu kết nối tại cổng 
    console.log("server đã chạy trên cổng 5001");
})


