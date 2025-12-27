# Thống Discord Bot

Bot Discord cá nhân của Thống với phong cách trò chuyện trẻ trung, hài hước và châm biếm.

## Tính năng

- **AI-Powered Responses**: Sử dụng AI model (Groq/Hugging Face) để trả lời thông minh
- Trả lời các câu hỏi về thông tin cá nhân dựa trên `prompts.txt`
- Chỉ giao tiếp bằng tiếng Việt
- Phong cách trò chuyện vui vẻ, trẻ trung, châm biếm
- Trả lời "Tôi bị ngu" cho các câu hỏi không hiểu hoặc không phải tiếng Việt
- Tự động tải cấu hình từ file `prompts.txt`

## Yêu cầu

- Python 3.8 trở lên (khuyến nghị Python 3.13+)
- Discord.py
- python-dotenv
- Groq API key (miễn phí) hoặc Hugging Face API key (tùy chọn)

## Cách cài đặt

1. Clone repository này về máy
2. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

3. Tạo file `.env` và thêm các thông tin sau:
```
DISCORD_TOKEN=your_discord_bot_token_here
GROQ_API_KEY=your_groq_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here  # Tùy chọn, chỉ cần nếu muốn dùng Hugging Face
```

4. Lấy Groq API key (miễn phí):
   - Đăng ký tại [Groq Console](https://console.groq.com/)
   - Tạo API key mới
   - Copy và thêm vào file `.env`

5. Chạy bot:
```bash
python bot.py
```

## Cách sử dụng

1. Thêm bot vào server Discord của bạn
2. Gửi tin nhắn bắt đầu bằng `!thong` để bot phản hồi
3. Bot sẽ:
   - Sử dụng AI để trả lời các câu hỏi một cách thông minh
   - Trả lời các câu hỏi về thông tin cá nhân từ `prompts.txt`
   - Phản hồi với phong cách trẻ trung, hài hước, châm biếm
   - Trả lời "Tôi bị ngu" cho tin nhắn không phải tiếng Việt hoặc không hiểu
   - Tự động tùy chỉnh phong cách dựa trên nội dung trong `prompts.txt`

## Cấu hình AI

Bot sử dụng file `prompts.txt` để cấu hình phong cách và thông tin cá nhân. Bạn có thể chỉnh sửa file này để thay đổi:
- Thông tin cá nhân (tên, quê quán, trường học, v.v.)
- Phong cách trả lời (đùa cợt, trẻ trung, châm biếm)
- Các quy tắc xử lý tin nhắn

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

> 📖 **Xem hướng dẫn chi tiết:** [DEPLOYMENT.md](DEPLOYMENT.md) - Hướng dẫn đầy đủ về cách deploy bot lên các nền tảng miễn phí

### 1. Deploy lên Render.com (Khuyến nghị - Hoàn toàn miễn phí)

**Render.com** là lựa chọn tốt nhất cho bot Discord vì:
- ✅ 750 giờ miễn phí mỗi tháng (đủ cho 24/7)
- ✅ Không yêu cầu thẻ tín dụng
- ✅ Uptime ổn định
- ✅ Tự động deploy từ GitHub

**Cách deploy:**

**Cách 1: Sử dụng render.yaml (Khuyến nghị)**
1. Đảm bảo file `render.yaml` đã có trong repository
2. Đăng ký tại [Render](https://render.com)
3. Kết nối repository GitHub của bạn
4. Chọn "New" → "Blueprint"
5. Render sẽ tự động detect `render.yaml` và cấu hình
6. Thêm các environment variables:
   - `DISCORD_TOKEN`: Token của bot Discord
   - `GROQ_API_KEY`: API key từ Groq (miễn phí)
   - `HUGGINGFACE_API_KEY`: (Tùy chọn) API key từ Hugging Face
7. Click "Apply" để deploy

**Cách 2: Deploy thủ công**
1. Đăng ký tại [Render](https://render.com)
2. Kết nối repository GitHub
3. Chọn "New" → "Background Worker"
4. Cấu hình:
   - **Name**: discord-bot
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
5. Thêm environment variables:
   - `DISCORD_TOKEN`: Token của bot Discord
   - `GROQ_API_KEY`: API key từ Groq
   - `HUGGINGFACE_API_KEY`: (Tùy chọn) API key từ Hugging Face
6. Chọn "Free" plan
7. Click "Create Background Worker"

### 2. Deploy lên Fly.io (Miễn phí - Khuyến nghị thứ 2)

**Fly.io** cung cấp:
- ✅ 3 VMs miễn phí (shared-cpu-1x, 256MB RAM)
- ✅ Không yêu cầu thẻ tín dụng
- ✅ Uptime ổn định
- ✅ Deploy dễ dàng

**Cách deploy:**
1. Cài đặt Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Đăng ký tại [Fly.io](https://fly.io)
3. Login: `fly auth login`
4. Tạo app: `fly launch` (chọn region gần bạn)
5. Thêm secrets:
   ```bash
   fly secrets set DISCORD_TOKEN=your_token
   fly secrets set GROQ_API_KEY=your_key
   ```
6. Deploy: `fly deploy`

### 3. Deploy lên Replit (Lựa chọn thay thế)

1. Đăng ký tài khoản tại [Replit](https://replit.com)
2. Tạo một Repl mới với template Python
3. Upload code của bot lên
4. Tạo file `.env` và thêm:
   ```
   DISCORD_TOKEN=your_token
   GROQ_API_KEY=your_key
   ```
5. Chạy bot bằng cách click "Run"
6. Để giữ bot luôn hoạt động:
   - Sử dụng [UptimeRobot](https://uptimerobot.com) để ping Repl URL mỗi 5 phút
   - Hoặc nâng cấp lên Replit Hacker Plan để có uptime tốt hơn

### 4. Deploy lên Railway.app (Có giới hạn)

1. Đăng ký tài khoản tại [Railway](https://railway.app)
2. Kết nối với GitHub repository
3. Tạo project mới → "New Project" → "Deploy from GitHub repo"
4. Thêm environment variables:
   - `DISCORD_TOKEN`
   - `GROQ_API_KEY`
   - `HUGGINGFACE_API_KEY` (tùy chọn)
5. Railway sẽ tự động deploy khi bạn push code

**Lưu ý**: Railway cung cấp $5 credit miễn phí mỗi tháng, sau đó cần thanh toán.

## So sánh các nền tảng hosting miễn phí:

| Platform | Free Tier | Uptime | Setup | Best For |
|----------|-----------|--------|-------|----------|
| **Render.com** | 750 giờ/tháng | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **Khuyến nghị nhất** |
| **Fly.io** | 3 VMs miễn phí | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Production apps |
| **Replit** | Unlimited | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Development/Testing |
| **Railway.app** | $5 credit/tháng | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Quick deploy |

### Chi tiết:

1. **Render.com** ⭐ **Khuyến nghị nhất**
   - ✅ 750 giờ miễn phí mỗi tháng (đủ cho 24/7)
   - ✅ Không yêu cầu thẻ tín dụng
   - ✅ Setup đơn giản với render.yaml
   - ✅ Uptime ổn định
   - ✅ Auto-deploy từ GitHub

2. **Fly.io**
   - ✅ 3 VMs miễn phí (shared-cpu-1x, 256MB RAM)
   - ✅ Không yêu cầu thẻ tín dụng
   - ✅ Uptime rất ổn định
   - ✅ Global edge network
   - ⚠️ Cần CLI để setup

3. **Replit**
   - ✅ Hoàn toàn miễn phí
   - ✅ Có IDE trực tuyến
   - ✅ Setup cực kỳ dễ
   - ❌ Cần trick để duy trì uptime (UptimeRobot)
   - ❌ Có thể bị lag
   - ⚠️ Tốt cho testing, không khuyến nghị cho production

4. **Railway.app**
   - ✅ $5 credit miễn phí mỗi tháng
   - ✅ Setup dễ dàng
   - ✅ Auto-deploy từ GitHub
   - ❌ Yêu cầu GitHub account
   - ❌ Giới hạn sau khi hết credit
   - ⚠️ Có thể cần thanh toán sau khi hết credit

## Lưu ý quan trọng khi deploy

### Environment Variables cần thiết:
Khi deploy, bạn cần thêm các environment variables sau:
- `DISCORD_TOKEN`: Token của bot Discord (bắt buộc)
- `GROQ_API_KEY`: API key từ Groq (bắt buộc cho AI features)
- `HUGGINGFACE_API_KEY`: API key từ Hugging Face (tùy chọn, chỉ cần nếu muốn dùng Hugging Face)

### Security:
- ❌ **KHÔNG BAO GIỜ** commit file `.env` chứa token
- ✅ Thêm `.env` vào `.gitignore`
- ✅ Sử dụng environment variables trên hosting platform
- ✅ Không chia sẻ API keys

### Monitoring:
- Nên setup monitoring để theo dõi uptime của bot
- Với Replit, sử dụng [UptimeRobot](https://uptimerobot.com) để ping URL mỗi 5 phút
- Kiểm tra logs định kỳ để đảm bảo bot hoạt động ổn định

### Backup:
- Backup code thường xuyên
- Lưu trữ API keys ở nơi an toàn
- Có thể sử dụng GitHub để backup code tự động 