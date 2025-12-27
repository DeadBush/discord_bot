# Hướng dẫn Deploy Bot Discord Miễn Phí

## Tổng quan

Bot Discord này có thể được host hoàn toàn miễn phí trên nhiều nền tảng. Tài liệu này hướng dẫn chi tiết cách deploy.

## Yêu cầu trước khi deploy

1. **Discord Bot Token**
   - Tạo bot tại [Discord Developer Portal](https://discord.com/developers/applications)
   - Copy bot token

2. **Groq API Key** (Miễn phí)
   - Đăng ký tại [Groq Console](https://console.groq.com/)
   - Tạo API key mới
   - Hoàn toàn miễn phí, không cần thẻ tín dụng

3. **GitHub Repository** (Khuyến nghị)
   - Push code lên GitHub
   - Giúp auto-deploy dễ dàng hơn

## Các nền tảng hosting miễn phí

### ⚠️ Render.com (Không khuyến nghị cho Discord bots)

**Vấn đề:**
- ❌ Render **KHÔNG còn hỗ trợ Background Workers miễn phí**
- ❌ Chỉ có Web Services miễn phí (không phù hợp cho Discord bots)
- ❌ Background Workers yêu cầu paid plan ($7/tháng)

**Nếu vẫn muốn thử Render (Web Service):**
1. Deploy như Web Service (không phải Background Worker)
2. Bot có thể bị sleep sau 15 phút không hoạt động
3. Có thể gặp rate limiting issues

**Khuyến nghị:** Sử dụng **Fly.io** hoặc **Replit** thay vì Render cho Discord bots miễn phí.

---

### 🏆 Fly.io (Khuyến nghị nhất - Hoàn toàn miễn phí)

**Ưu điểm:**
- ✅ 3 VMs miễn phí
- ✅ Uptime rất ổn định
- ✅ Global edge network
- ✅ Không sleep như Render

**Cách deploy:**

1. **Cài đặt Fly CLI:**
   ```bash
   # Windows (PowerShell)
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   
   # Mac/Linux
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login:**
   ```bash
   fly auth login
   ```

3. **Tạo app:**
   ```bash
   fly launch
   ```
   - Chọn region gần bạn (ví dụ: `hkg` cho Hong Kong)
   - Chọn "No" khi hỏi về database

4. **Thêm secrets:**
   ```bash
   fly secrets set DISCORD_TOKEN=your_token
   fly secrets set GROQ_API_KEY=your_key
   ```

5. **Deploy:**
   ```bash
   fly deploy
   ```

6. **Kiểm tra logs:**
   ```bash
   fly logs
   ```

---

### 🥈 Replit (Dễ nhất - Hoàn toàn miễn phí)

**Ưu điểm:**
- ✅ Hoàn toàn miễn phí
- ✅ Có IDE trực tuyến
- ✅ Setup cực kỳ dễ

**Nhược điểm:**
- ❌ Cần trick để giữ bot chạy 24/7
- ❌ Có thể bị lag

**Cách deploy:**

1. Đăng ký tại [Replit](https://replit.com)
2. Tạo Repl mới → "Import from GitHub"
3. Chọn repository của bạn
4. Tạo file `.env`:
   ```
   DISCORD_TOKEN=your_token
   GROQ_API_KEY=your_key
   ```
5. Click "Run"
6. **Giữ bot chạy 24/7:**
   - Đăng ký [UptimeRobot](https://uptimerobot.com) (miễn phí)
   - Thêm monitor mới → HTTP(s)
   - URL: `https://your-repl-name.your-username.repl.co`
   - Interval: 5 phút
   - Bot sẽ không bị sleep

---

### 🚂 Railway.app

**Ưu điểm:**
- ✅ $5 credit miễn phí/tháng
- ✅ Auto-deploy từ GitHub
- ✅ Setup dễ dàng

**Nhược điểm:**
- ❌ Có thể cần thanh toán sau khi hết credit
- ❌ Giới hạn sau $5

**Cách deploy:**

1. Đăng ký tại [Railway](https://railway.app)
2. "New Project" → "Deploy from GitHub repo"
3. Chọn repository
4. Thêm environment variables:
   - `DISCORD_TOKEN`
   - `GROQ_API_KEY`
5. Railway tự động deploy

---

## So sánh nhanh

| Platform | Free Tier | Uptime | Setup | Tốt cho |
|----------|-----------|--------|-------|---------|
| **Fly.io** | 3 VMs | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **Production - Khuyến nghị** |
| **Replit** | Unlimited | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **Testing/Development - Khuyến nghị** |
| **Railway** | $5/tháng | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Quick deploy |
| **Render** | Web Service only | ⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ Không khuyến nghị cho bots |

## Troubleshooting

### Bot không chạy trên Render
- Kiểm tra logs trong Render dashboard
- Đảm bảo đã thêm đầy đủ environment variables
- Kiểm tra bot token có đúng không

### Bot bị disconnect thường xuyên
- Render free tier có thể sleep, đây là bình thường
- Bot sẽ tự động reconnect khi có tin nhắn
- Nếu cần uptime tốt hơn, dùng Fly.io

### Lỗi "ModuleNotFoundError"
- Đảm bảo `requirements.txt` có đầy đủ dependencies
- Kiểm tra build logs trên hosting platform

### API rate limit
- Groq có rate limit cao, thường không gặp vấn đề
- Nếu gặp, có thể thêm Hugging Face API key làm fallback

## Monitoring

Khuyến nghị setup monitoring để theo dõi bot:

1. **UptimeRobot** (Miễn phí)
   - Monitor HTTP endpoint (nếu có)
   - Hoặc ping bot qua Discord

2. **Logs**
   - Kiểm tra logs định kỳ trên hosting platform
   - Tìm lỗi và fix kịp thời

## Backup

- ✅ Push code lên GitHub (tự động backup)
- ✅ Lưu API keys ở nơi an toàn (password manager)
- ✅ Export environment variables định kỳ

## Security Checklist

- [ ] `.env` đã được thêm vào `.gitignore`
- [ ] Không commit API keys vào GitHub
- [ ] Sử dụng environment variables trên hosting
- [ ] Bot token được bảo mật
- [ ] Review code trước khi deploy

---

**Khuyến nghị:** Sử dụng **Render.com** cho production vì uptime tốt và setup đơn giản nhất.

