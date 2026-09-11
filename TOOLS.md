# TOOLS.md — الأدوات + Setup الكامل

> **دليل تثبيت + إعداد كل أدوات النظام. ميزانية $0 (open-source بالكامل).**

---

## 1. متطلبات النظام

### 1.1 Hardware
| المتطلب | الحد الأدنى | الموصى |
|---------|------------|--------|
| OS | Linux (Ubuntu 22.04+ / WSL2) | macOS / Linux native |
| RAM | 8GB | 16GB-32GB (لـ Whisper medium/large) |
| Disk | 50GB free | 200GB+ (لـ video cache + models) |
| GPU | Optional | NVIDIA 8GB+ (لـ Whisper GPU + Stable Diffusion) |
| Internet | 10Mbps | 100Mbps+ (لـ uploads) |

### 1.2 Software
| المتطلب | الإصدار | لماذا |
|---------|---------|-------|
| Python | 3.10+ | for type hints + faster-whisper |
| FFmpeg | 7.0+ | كل المونتاج |
| Node.js | 18+ | للـ Whop CLI (اختياري) |
| Git | 2.30+ | لاستنساخ المستودع |
| yt-dlp | 2024.0.0+ | تحميل الفيديوهات |

---

## 2. التثبيت (Setup Script)

### 2.1 تشغيل setup.sh

```bash
# 1. استنساخ المستودع
git clone https://github.com/geasas/whop-viral-system.git
cd whop-viral-system

# 2. تشغيل setup
chmod +x scripts/setup.sh
bash scripts/setup.sh
```

### 2.2 ما يفعله setup.sh

1. **يفحص النظام** (OS, Python, FFmpeg, RAM, disk).
2. **يثبت Python dependencies**:
   ```bash
   pip install -r scripts/requirements.txt
   ```
3. **يثبت FFmpeg** (إن لم يكن موجوداً):
   ```bash
   sudo apt install ffmpeg  # Linux
   brew install ffmpeg      # macOS
   ```
4. **يثبت yt-dlp**:
   ```bash
   pip install yt-dlp
   ```
5. **ينزّل Whisper models**:
   ```bash
   python -c "from faster_whisper import WhisperModel; WhisperModel('tiny', device='cpu')"
   python -c "from faster_whisper import WhisperModel; WhisperModel('base', device='cpu')"
   ```
6. **ينشئ .env من .env.template**:
   ```bash
   cp scripts/.env.template .env
   ```
7. **ينشئ المجلدات**:
   ```bash
   mkdir -p logs assets/broll assets/nasheed assets/templates
   ```
8. **يفحص التثبيت**:
   ```bash
   python scripts/health_check.py
   ```

### 2.3 إعداد يدوي (إن لزم)

#### Python 3.10+
```bash
# Ubuntu
sudo apt update && sudo apt install python3.10 python3.10-venv python3-pip
python3.10 -m venv venv
source venv/bin/activate

# macOS
brew install python@3.10
python3.10 -m venv venv
source venv/bin/activate
```

#### FFmpeg 7+
```bash
# Ubuntu
sudo apt install ffmpeg
ffmpeg -version  # should show 7.x

# macOS
brew install ffmpeg
```

#### yt-dlp
```bash
pip install -U yt-dlp
yt-dlp --version  # 2024.0.0+
```

#### Whisper models (manual)
```bash
# نزل يدوياً (optional — auto-download on first use)
mkdir -p ~/.cache/whisper
wget -P ~/.cache/whisper/ https://huggingface.co/Systran/faster-whisper-tiny/resolve/main/model.bin
wget -P ~/.cache/whisper/ https://huggingface.co/Systran/faster-whisper-base/resolve/main/model.bin
# للـ Arabic: استخدم small أو medium
```

---

## 3. الـ .env.template

```bash
# =================================
# TikTok Content Posting API
# =================================
TIKTOK_CLIENT_KEY=your_client_key_here
TIKTOK_CLIENT_SECRET=your_client_secret_here
TIKTOK_ACCESS_TOKEN=your_access_token_here  # refreshes every 24h
TIKTOK_REFRESH_TOKEN=your_refresh_token_here
TIKTOK_OPEN_ID=your_open_id_here

# =================================
# Instagram Graph API
# =================================
INSTAGRAM_ACCESS_TOKEN=your_ig_token_here  # long-lived 60 days
INSTAGRAM_USER_ID=your_ig_user_id_here
INSTAGRAM_APP_ID=your_meta_app_id_here
INSTAGRAM_APP_SECRET=your_meta_app_secret_here

# =================================
# YouTube Data API v3
# =================================
YOUTUBE_CLIENT_SECRET_JSON=/path/to/client_secret.json
YOUTUBE_TOKEN_JSON=/path/to/token.json  # auto-generated on first OAuth
YOUTUBE_CHANNEL_ID=your_channel_id_here

# =================================
# Whop API
# =================================
WHOP_API_KEY=your_whop_api_key_here
WHOP_BEARER_TOKEN=your_whop_bearer_token_here
WHOP_USER_ID=your_whop_user_id_here
WHOP_CLI_PATH=/usr/local/bin/whop  # optional CLI

# =================================
# B-Roll Sources (free APIs)
# =================================
PEXELS_API_KEY=your_pexels_key_here  # free at pexels.com/api
PIXABAY_API_KEY=your_pixabay_key_here  # free at pixabay.com/api

# =================================
# Optional: AI Image Generation
# =================================
STABLE_DIFFUSION_WEBUI_URL=http://127.0.0.1:7860  # local AUTOMATIC1111
STABLE_DIFFUSION_MODEL=v1-5-pruned-emaonly.safetensors

# =================================
# System
# =================================
LOG_LEVEL=INFO
STATE_FILE=state.json
CACHE_DIR=.cache
WHISPER_MODEL=small  # tiny|base|small|medium|large
WHISPER_DEVICE=cpu   # cpu|cuda|metal
```

---

## 4. الـ Stack الكامل (10 طبقات)

| Layer | الأداة | الإصدار | الوظيفة | البديل (إن فشل) |
|-------|--------|---------|---------|------------------|
| 1. Download | yt-dlp | 2024.0+ | تحميل فيديوهات | youtube-dl (slower) |
| 2. Transcribe | faster-whisper | 1.0+ | word timestamps | openai-whisper (slower) |
| 3. Auto-edit | auto-editor + librosa | 29+ / 0.10+ | silence + beats | FFmpeg silenceremove |
| 4. Edit | FFmpeg + moviepy | 7+/2.0+ | مونتاج + تأثيرات | DaVinci Resolve (manual) |
| 5. Captions | Whisper + drawtext | - | كارترايدج | SubtitleEdit (manual) |
| 6. B-Roll | Pexels API + Pixabay | - | لقطات داعمة | Stable Diffusion (local) |
| 7. Halal Check | Python (custom) | - | 5-بند gate | manual review |
| 8. Score | Python (custom) | - | 6-بند gate | manual review |
| 9. Publish | TikTok/IG/YT APIs | - | نشر يومي | manual upload |
| 10. Analytics | Python (custom) | - | KPIs يومي | manual dashboard |
| 11. Whop | Whop CLI + API | - | تسليم bounties | manual submission |

---

## 5. تفعيل الـ APIs (Step-by-Step)

### 5.1 TikTok Content Posting API

1. اذهب إلى https://developers.tiktok.com/.
2. أنشئ حساب مطور.
3. أنشئ تطبيق جديد (App type: "Web").
4. املأ:
   - App name: "Whop Viral Bot"
   - Description: "Automated short video publishing via official API"
   - Categories: "Tools and Utilities"
   - Redirect URI: `https://yourdomain.com/callback` (أو `http://localhost:8080/callback` للـ testing).
5. اطلب النطاقات:
   - `video.publish` (Direct Post + audit)
   - `video.upload` (Draft + no audit)
6. احفظ `client_key` و `client_secret`.
7. **انتظر الموافقة (App Review)** — يأخذ 4-6 أسابيع للـ audit.
8. بعد الموافقة، احصل على `access_token` عبر OAuth flow.
9. ضع الـ tokens في `.env`.

### 5.2 Instagram Graph API

1. اذهب إلى https://developers.facebook.com/apps/.
2. أنشئ تطبيق جديد (App type: "Business").
3. أضف Product: "Instagram".
4. اختر "Instagram API with Instagram Login".
5. اطلب النطاقات:
   - `instagram_business_basic`
   - `instagram_business_content_publish`
   - `instagram_business_manage_comments`
   - `instagram_business_manage_messages`
6. اربط حساب Instagram Business account (يجب أن يكون business/creator).
7. احصل على `access_token` (long-lived, 60 day).
8. احصل على `ig_user_id`.
9. ضع القيم في `.env`.
10. **OAuth flow للحصول على long-lived token**:
    ```bash
    curl -X GET "https://graph.facebook.com/v21.0/oauth/access_token" \
      -d "grant_type=fb_exchange_token" \
      -d "client_id=$INSTAGRAM_APP_ID" \
      -d "client_secret=$INSTAGRAM_APP_SECRET" \
      -d "fb_exchange_token=$SHORT_LIVED_TOKEN"
    ```

### 5.3 YouTube Data API v3

1. اذهب إلى https://console.cloud.google.com/.
2. أنشئ مشروع جديد.
3. Enable "YouTube Data API v3" (APIs & Services → Library → search).
4. أنشئ credentials (OAuth 2.0 Client ID):
   - Application type: "Desktop app".
   - Name: "Whop Viral Bot".
5. تنزيل `client_secret.json`.
6. ضعه في `/path/to/.credentials/client_secret.json`.
7. ضع الـ path في `.env`.
8. أول تشغيل:
   ```bash
   python scripts/publish_youtube.py --auth  # يطلب تصريح في browser
   ```
9. يحفظ `token.json` تلقائياً (يستخدم تلقائياً في الأيام التالية).
10. **API Audit**: YouTube يتطلب audit للـ apps الـ تنشر public videos. تقدّم بـ request في https://developers.google.com/youtube/v3/guides/quota_and_compliance_audition.

### 5.4 Whop API

1. اذهب إلى https://whop.com → سجّل دخول.
2. Settings → Developer.
3. أنشئ API key.
4. احفظ `Bearer token`.
5. (اختياري) تنزيل Whop CLI:
   ```bash
   curl -fsSL https://whop.com/install.sh | sh
   ```
6. ضع القيم في `.env`.

### 5.5 Pexels + Pixabay (لـ B-roll)

#### Pexels
1. https://www.pexels.com/api/ → Sign up.
2. احصل على API key (مجاني، 200 req/hour).
3. ضع في `.env`: `PEXELS_API_KEY=...`

#### Pixabay
1. https://pixabay.com/api/docs/ → Sign up.
2. احصل على API key (مجاني).
3. ضع في `.env`: `PIXABAY_API_KEY=...`

### 5.6 (Optional) Stable Diffusion WebUI

1. استنساخ:
   ```bash
   git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
   cd stable-diffusion-webui
   ./webui.sh
   ```
2. ينزّل الـ models تلقائياً (~5GB).
3. تشغيل على `http://127.0.0.1:7860`.
4. ضع في `.env`: `STABLE_DIFFUSION_WEBUI_URL=http://127.0.0.1:7860`.

---

## 6. الأوامر المفيدة (Cheat Sheet)

### 6.1 معالجة فيديو

```bash
# تحميل فيديو
yt-dlp -f "best[ext=mp4]" "https://youtube.com/watch?v=xxx" -o raw.mp4

# Transcription
python scripts/transcribe.py --input raw.mp4 --out transcript.json

# Auto-edit
python scripts/auto_edit.py --input raw.mp4 --transcript transcript.json --out clips/

# Viral-edit
python scripts/viral_edit.py --segment clips/clip_01.mp4 --broll assets/broll/ --audio assets/nasheed/track_01.mp3 --out final.mp4

# Halal check
python scripts/halal_check.py final.mp4

# Scorecard
python scripts/retention_scorecard.py final.mp4

# Publish
python scripts/publish_tiktok.py --video final.mp4 --caption "..."
```

### 6.2 FFmpeg مباشرة

```bash
# Double Zoom (91% → 100% → 109% every 5s)
ffmpeg -i input.mp4 -vf "scale=1090:1936,zoompan=z='if(gt(on,1),min(zoom+0.002,1.1),1)':d=150:s=1080x1920" output.mp4

# B-roll overlay between 2-5s
ffmpeg -i main.mp4 -i broll.mp4 -filter_complex "[1:v]scale=1080:1920[b];[0:v][b]overlay=enable='between(t,2,5)'" output.mp4

# Captions burn-in
ffmpeg -i input.mp4 -vf "subtitles=captions.ass:force_style='Fontsize=24,Outline=2'" output.mp4

# J-Cut (audio 0.5s before video)
ffmpeg -i input.mp4 -af "adelay=500|500" -c:v copy output.mp4

# Beat detection (librosa)
python -c "import librosa; y,sr=librosa.load('audio.mp3'); tempo,beats=librosa.beat.beat_track(y,sr); print(f'Tempo: {tempo}')"

# Silence removal
ffmpeg -i input.mp4 -af "silenceremove=stop_periods=-1:stop_duration=0.3:stop_threshold=-40dB" output.mp4
```

### 6.3 مراقبة النظام

```bash
# Health check
python scripts/health_check.py

# Tokens check
python scripts/check_tokens.py

# Analytics يومي
python scripts/analytics_dashboard.py --date $(date +%Y-%m-%d)

# Whop bounty browse
whop bounties list --category=all --sort=rate_per_1k

# Cron log آخر 24h
tail -100 logs/cron-$(date +%Y%m%d).log
```

---

## 7. الـ Performance Tuning

### 7.1 GPU Acceleration للـ Whisper
```bash
# تثبيت CUDA toolkit
sudo apt install nvidia-cuda-toolkit

# تثبيت PyTorch with CUDA
pip install torch --index-url https://download.pytorch.org/whl/cu118

# استخدام GPU في Whisper
python scripts/transcribe.py --input raw.mp4 --device cuda --model small
# 5x faster than CPU
```

### 7.2 FFmpeg Hardware Encoding
```bash
# NVIDIA NVENC
ffmpeg -i input.mp4 -c:v h264_nvenc -preset p6 -b:v 5M output.mp4

# Apple VideoToolbox
ffmpeg -i input.mp4 -c:v h264_videotoolbox -b:v 5M output.mp4

# Intel QuickSync
ffmpeg -i input.mp4 -c:v h264_qsv -b:v 5M output.mp4
```

### 7.3 Parallel Processing
```bash
# شغل 5 فيديوهات بالتوازي
for clip in clips/*.mp4; do
  python scripts/viral_edit.py --segment "$clip" &
done
wait
```

---

## 8. الـ Maintenance

### 8.1 تحديث المكتبات
```bash
# كل أسبوع
pip install -U -r scripts/requirements.txt
yt-dlp -U
```

### 8.2 تنظيف الـ cache
```bash
# كل أسبوع
rm -rf /tmp/clips/* /tmp/final_* /tmp/raw_*
find .cache/ -mtime +30 -delete
```

### 8.3 Backup
```bash
# كل يوم (cron 23:00)
0 23 * * * tar -czf /backup/whop-$(date +\%Y\%m\%d).tar.gz /path/to/whop-viral-system/{state.json,worklog.md,logs,.env}
```

---

## 9. الـ Troubleshooting

### 9.1 FFmpeg Errors
```bash
# "Codec not found"
sudo apt install libavcodec-extra

# "No GPU"
sudo apt install nvidia-driver-535
```

### 9.2 Whisper Errors
```bash
# "Model not found"
# Download manually:
huggingface-cli download Systran/faster-whisper-small

# "Out of memory"
# Use smaller model:
python scripts/transcribe.py --input raw.mp4 --model tiny
```

### 9.3 API Errors
```bash
# TikTok 401
# Refresh access token
python scripts/_common.py refresh-tiktok-token

# Instagram 403
# Re-authorize app
# https://developers.facebook.com/tools/explorer/

# YouTube 403 (quota exceeded)
# Wait until midnight Pacific time (resets daily)
# Or request quota increase
```

### 9.4 Whop API Errors
```bash
# 404 on bounty
python scripts/whop_bounty_status.py --submission-id $ID --verbose

# 401 unauthorized
# Refresh bearer token
# Settings → Developer → Rotate key
```

---

## 10. الـ Cloud Deployment (Optional)

### 10.1 VPS Setup (DigitalOcean / Hetzner / Linode)
```bash
# VPS specs: 4 vCPU, 8GB RAM, 160GB SSD, $10-20/month

# SSH login
ssh root@your-vps

# Clone repo
git clone https://github.com/geasas/whop-viral-system.git
cd whop-viral-system

# Setup
bash scripts/setup.sh

# Configure .env
nano .env

# Set up cron
crontab -e
# Add: 0 6 * * * cd /root/whop-viral-system && bash scripts/daily_pipeline.sh
```

### 10.2 Docker (Optional)
```dockerfile
# Dockerfile
FROM python:3.10-slim

RUN apt-get update && apt-get install -y ffmpeg git
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["bash", "scripts/daily_pipeline.sh"]
```

### 10.3 الـ Cost Estimate (VPS route)
- VPS: $10-20/شهر
- Domain (optional): $10-15/سنة
- Total: $11-21/شهر

إذا استخدمت جهازك الشخصي = $0/شهر (بدون VPS).

---

## 11. الـ Security Best Practices

### 11.1 الـ API Tokens
- ✅ لا تُرفع لـ GitHub (`.gitignore` يشمل `.env`).
- ✅ استخدم environment variables.
- ✅ Rotate كل 90 يوم.
- ✅ لا تخزّنها في الـ code نفسه.

### 11.2 الـ Account Safety
- ✅ لا تسجل دخول يدوي بـ باسورد يومياً — استخدم API.
- ✅ لا تستخدم بوتات followers.
- ✅ لا تنشر أكثر من 5 فيديوهات/يوم/حساب.
- ✅ اترك 2+ ساعات بين النشرات.
- ✅ استخدم VPN/different IPs لكل حساب (لتفادي linkage).

### 11.3 الـ Content Safety
- ✅ لا تقت من قنوات بها محتوى محرم.
- ✅ راجع الفيديو قبل النشر.
- ✅ استخدم `halal_check.py` قبل كل نشر.
- ✅ استخدم `retention_scorecard.py` قبل كل نشر.

---

## 12. الـ Quick Start (Copy-Paste)

```bash
# 1. Setup
git clone https://github.com/geasas/whop-viral-system.git
cd whop-viral-system
bash scripts/setup.sh

# 2. Fill credentials
nano .env
# Fill in: TIKTOK_*, INSTAGRAM_*, YOUTUBE_*, WHOP_*

# 3. First run (manual)
python scripts/health_check.py
python scripts/browse_whop_bounties.py  # pick a bounty

# 4. Run daily pipeline (manual first time)
bash scripts/daily_pipeline.sh

# 5. Set up cron (after verifying works)
crontab -e
# Add: 0 6 * * * cd /path/to/whop-viral-system && bash scripts/daily_pipeline.sh >> logs/cron.log 2>&1

# 6. Monitor
tail -f logs/cron.log
```
