# Thống Discord Bot

Bot Discord cá nhân của Thống với phong cách trò chuyện trẻ trung, hài hước và châm biếm.

## Tính năng

- Trả lời các câu hỏi về thông tin cá nhân
- Chỉ giao tiếp bằng tiếng Việt
- Phong cách trò chuyện vui vẻ, trẻ trung
- Trả lời "Tôi bị ngu" cho các câu hỏi không hiểu hoặc không phải tiếng Việt

## Yêu cầu

- Python 3.8 trở lên
- Discord.py
- python-dotenv

## Cách cài đặt

1. Clone repository này về máy
2. Cài đặt các thư viện cần thiết:
```bash
pip install discord.py python-dotenv
```
3. Tạo file `.env` và thêm Discord bot token của bạn:
```
DISCORD_TOKEN=your_discord_bot_token_here
```
4. Chạy bot:
```bash
python bot.py
```

## Cách sử dụng

1. Thêm bot vào server Discord của bạn
2. Bot sẽ tự động phản hồi mọi tin nhắn trong các kênh mà nó có quyền truy cập
3. Bot sẽ:
   - Trả lời các câu hỏi về thông tin cá nhân
   - Phản hồi với phong cách trẻ trung, hài hước
   - Trả lời "Tôi bị ngu" cho tin nhắn không phải tiếng Việt
   - Có các câu trả lời ngẫu nhiên cho những câu hỏi không khớp mẫu

## Lưu ý

- Đảm bảo bot có quyền đọc và gửi tin nhắn trong các kênh
- Không chia sẻ file `.env` chứa token của bot
- Bot chỉ giao tiếp bằng tiếng Việt

# Discord Bot Deployment Guide

## Cách deploy lên RunPod

1. Đăng ký tài khoản tại [RunPod](https://www.runpod.io/)

2. Tạo file `.env` với token Discord của bạn:
```
DISCORD_TOKEN=your_discord_token_here
```

3. Build Docker image:
```bash
docker build -t discord-bot .
```

4. Đăng nhập vào RunPod và làm theo các bước sau:

   - Tạo một pod mới (chọn container type là "Basic GPU")
   - Upload Docker image lên RunPod container registry
   - Deploy pod với image đã upload
   - Thêm environment variable DISCORD_TOKEN trong pod settings

## Lưu ý

- Đảm bảo `.env` file đã được thêm vào `.gitignore`
- Kiểm tra logs trong RunPod để xác nhận bot đang chạy
- Nên sử dụng pod với cấu hình nhỏ nhất có thể vì bot không cần nhiều tài nguyên 

## Cách deploy miễn phí

### 1. Deploy lên Render.com (Khuyến nghị)

1. Đăng ký tài khoản tại [Render](https://render.com)
2. Kết nối repository GitHub của bạn với Render
3. Chọn "New Web Service"
4. Cấu hình:
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
5. Thêm environment variable:
   - Key: `DISCORD_TOKEN`
   - Value: Token của bot Discord của bạn
6. Click "Create Web Service"

### 2. Deploy lên Replit (Lựa chọn thay thế)

1. Đăng ký tài khoản tại [Replit](https://replit.com)
2. Tạo một Repl mới với template Python
3. Upload code của bot lên
4. Tạo file `.env` và thêm Discord token
5. Chạy bot bằng cách click "Run"
6. Để giữ bot luôn hoạt động:
   - Sử dụng UptimeRobot để ping Repl URL mỗi 5 phút
   - Hoặc nâng cấp lên Replit Hacker Plan để có uptime tốt hơn

### 3. Deploy lên Railway.app (Lựa chọn thay thế)

1. Đăng ký tài khoản tại [Railway](https://railway.app)
2. Kết nối với GitHub repository
3. Tạo project mới
4. Thêm environment variable `DISCORD_TOKEN`
5. Railway sẽ tự động deploy khi bạn push code

## So sánh các nền tảng hosting miễn phí:

1. **Render.com**
   - ✅ 750 giờ miễn phí mỗi tháng
   - ✅ Không yêu cầu thẻ tín dụng
   - ✅ Setup đơn giản
   - ✅ Uptime ổn định

2. **Replit**
   - ✅ Hoàn toàn miễn phí
   - ✅ Có IDE trực tuyến
   - ❌ Cần trick để duy trì uptime
   - ❌ Có thể bị lag

3. **Railway.app**
   - ✅ $5 credit miễn phí mỗi tháng
   - ✅ Setup dễ dàng
   - ❌ Yêu cầu GitHub account
   - ❌ Giới hạn sau khi hết credit

## Lưu ý quan trọng

- Không bao giờ commit file `.env` chứa token
- Nên setup monitoring để theo dõi uptime của bot
- Với Replit, nên sử dụng UptimeRobot để giữ bot luôn hoạt động
- Backup code thường xuyên
- Kiểm tra logs định kỳ để đảm bảo bot hoạt động ổn định 