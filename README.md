# Thống Discord Bot

Bot Discord cá nhân của Thống với phong cách trò chuyện trẻ trung, hài hước và châm biếm.

## Tính năng

- **AI-Powered Responses**: Sử dụng AI model (Groq/Hugging Face) để trả lời thông minh
- **Valorant Match Tracking**: Theo dõi và thông báo khi người chơi bắt đầu trận đấu Valorant
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
RIOT_API_KEY=your_riot_api_key_here  # Bắt buộc cho tính năng theo dõi Valorant
RIOT_REGION=ap  # Khu vực: ap (Asia Pacific), na, eu, kr, etc.
```

4. Lấy API keys:
   - **Groq API key** (miễn phí):
     - Đăng ký tại [Groq Console](https://console.groq.com/)
     - Tạo API key mới
     - Copy và thêm vào file `.env`
   - **Riot Games API key** (miễn phí, bắt buộc cho Valorant tracking):
     - Đăng ký tại [Riot Developer Portal](https://developer.riotgames.com/)
     - Tạo API key mới
     - **Lưu ý**: API key có giới hạn rate limit (100 requests mỗi 2 phút cho development key)
     - Copy và thêm vào file `.env`

5. Chạy bot:
```bash
python bot.py
```

## Cách sử dụng

1. Thêm bot vào server Discord của bạn
2. Bot sẽ tự động phản hồi **tất cả tin nhắn** trong các kênh mà nó có quyền truy cập
3. Bot sẽ:
   - Sử dụng AI để trả lời các câu hỏi một cách thông minh
   - Trả lời các câu hỏi về thông tin cá nhân từ `prompts.txt`
   - Phản hồi với phong cách trẻ trung, hài hước, châm biếm
   - Trả lời "Tôi bị ngu" cho tin nhắn không phải tiếng Việt hoặc không hiểu
   - Tự động tùy chỉnh phong cách dựa trên nội dung trong `prompts.txt`

**Lưu ý:** Bot sẽ phản hồi mọi tin nhắn (trừ tin nhắn từ chính bot). Đảm bảo bot chỉ có quyền truy cập vào các kênh bạn muốn bot hoạt động.

## Tính năng theo dõi Valorant

Bot có thể tự động theo dõi và thông báo khi người chơi bắt đầu/kết thúc trận đấu Valorant, kèm theo thống kê chi tiết và nhận xét AI bằng tiếng Việt.

### Cách sử dụng:

1. **Liên kết tài khoản Discord với Riot (Khuyến nghị - Tự động theo dõi):**
   ```
   !link riot <TênRiot> <TagRiot>
   ```
   Ví dụ: `!link riot PlayerName 1234`
   
   Sau khi liên kết, bot sẽ **tự động** theo dõi khi bạn bắt đầu chơi Valorant (qua Discord presence).

2. **Thêm người chơi vào danh sách theo dõi (Thủ công):**
   ```
   !track valorant <TênRiot> <TagRiot>
   ```
   Ví dụ: `!track valorant PlayerName 1234`

3. **Xóa người chơi khỏi danh sách theo dõi:**
   ```
   !untrack valorant
   ```

4. **Đặt kênh thông báo** (cần quyền Administrator):
   ```
   !set valorant channel
   ```
   Lệnh này sẽ đặt kênh hiện tại làm kênh nhận thông báo khi có trận đấu mới.

5. **Xem danh sách người chơi được theo dõi:**
   ```
   !list tracked
   ```

### Tính năng tự động:

- **Tự động phát hiện khi bắt đầu chơi**: Khi bạn liên kết tài khoản và bắt đầu chơi Valorant, bot sẽ tự động theo dõi bạn
- **Thông báo khi bắt đầu trận đấu**: Bot sẽ thông báo khi bạn vào trận đấu
- **Thống kê sau khi kết thúc**: Khi trận đấu kết thúc, bot sẽ gửi:
  - Kết quả trận đấu (Thắng/Thua, tỷ số)
  - K/D/A, điểm số, sát thương
  - Agent sử dụng, headshot %
  - **Nhận xét AI tự động** bằng tiếng Việt dựa trên thống kê

### Lưu ý:
- Bot sẽ tự động kiểm tra mỗi 30 giây để phát hiện trận đấu mới
- Cần có Riot Games API key hợp lệ trong file `.env`
- **Quan trọng**: Riot Games API cho Valorant yêu cầu Production API key. Development key (personal key) có thể không có quyền truy cập vào Valorant API endpoints. Bạn cần:
  1. Đăng ký tại [Riot Developer Portal](https://developer.riotgames.com/)
  2. Nộp đơn xin Production API key với mô tả dự án của bạn
  3. Chờ Riot Games phê duyệt
- API key có giới hạn rate limit (100 requests/2 phút cho development key, cao hơn cho production key)
- Bot sẽ gửi thông báo khi phát hiện người chơi bắt đầu trận đấu mới
- Region mặc định là `ap` (Asia Pacific). Có thể thay đổi trong `.env` với `RIOT_REGION`

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

### ⚠️ Render.com (Không khuyến nghị)

**Vấn đề:**
- ❌ Render **KHÔNG còn hỗ trợ Background Workers miễn phí**
- ❌ Background Workers yêu cầu paid plan ($7/tháng)
- ❌ Chỉ có Web Services miễn phí (không phù hợp cho Discord bots)

**Khuyến nghị:** Sử dụng **Fly.io** hoặc **Replit** thay vì Render cho Discord bots miễn phí.

### 1. Deploy lên Fly.io (Khuyến nghị nhất - Hoàn toàn miễn phí)

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

### 2. Deploy lên Replit (Khuyến nghị thứ 2 - Hoàn toàn miễn phí)

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

### 3. Deploy lên Railway.app (Có giới hạn)

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
| **Fly.io** | 3 VMs miễn phí | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **Production - Khuyến nghị nhất** |
| **Replit** | Unlimited | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **Development/Testing - Khuyến nghị** |
| **Railway.app** | $5 credit/tháng | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Quick deploy |
| **Render.com** | Web Service only | ⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ Không khuyến nghị cho bots |

### Chi tiết:

1. **Fly.io** 🏆 **Khuyến nghị nhất cho Production**
   - ✅ 3 VMs miễn phí (shared-cpu-1x, 256MB RAM)
   - ✅ Không yêu cầu thẻ tín dụng
   - ✅ Uptime rất ổn định
   - ✅ Global edge network
   - ✅ Không bị sleep
   - ⚠️ Cần CLI để setup

2. **Replit** 🥈 **Khuyến nghị cho Development**
   - ✅ Hoàn toàn miễn phí
   - ✅ Có IDE trực tuyến
   - ✅ Setup cực kỳ dễ
   - ❌ Cần trick để duy trì uptime (UptimeRobot)
   - ❌ Có thể bị lag
   - ⚠️ Tốt cho testing, có thể dùng cho production với UptimeRobot

3. **Railway.app**
   - ✅ $5 credit miễn phí mỗi tháng
   - ✅ Setup dễ dàng
   - ✅ Auto-deploy từ GitHub
   - ❌ Yêu cầu GitHub account
   - ❌ Giới hạn sau khi hết credit
   - ⚠️ Có thể cần thanh toán sau khi hết credit

4. **Render.com** ⚠️ **Không khuyến nghị**
   - ❌ Không còn hỗ trợ Background Workers miễn phí
   - ❌ Chỉ có Web Services (không phù hợp cho Discord bots)
   - ❌ Background Workers yêu cầu paid plan ($7/tháng)

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