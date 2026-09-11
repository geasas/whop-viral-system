# SYSTEM.md — البنية الكاملة + التشغيل

> **هذا الملف يشرح بنية النظام من ناحية معمارية + كيفية التشغيل الفعلي + الـ stack التقني.**

---

## 1. المعمارية (Architecture)

### 1.1 الـ Layers السبعة (من أعلى لأسفل)

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 7: Strategic Minds (7 sub-agents)                   │
│  Sima Yi + Cao Cao + Guo Jia + Liu Bei + Dong Zhuo +       │
│  Lu Bu + Yuan Fang                                          │
├─────────────────────────────────────────────────────────────┤
│  Layer 6: Orchestration (daily_pipeline.sh + cron)         │
│  cron 06:00 → 22:00، 7 agents + scripts                    │
├─────────────────────────────────────────────────────────────┤
│  Layer 5: Publishing APIs                                   │
│  TikTok Content Posting API v2                              │
│  Instagram Graph API (container → poll → publish)           │
│  YouTube Data API v3 (OAuth 2.0)                            │
│  Whop bounty_submissions API                               │
├─────────────────────────────────────────────────────────────┤
│  Layer 4: Quality Gates                                     │
│  halal_check.py (5-بند) — must PASS before publish          │
│  retention_scorecard.py (6-بند) — must PASS ≥5/6            │
├─────────────────────────────────────────────────────────────┤
│  Layer 3: Editing Pipeline                                  │
│  FFmpeg (Double Zoom, B-roll, Beat Sync, J-Cut)            │
│  MoviePy + ffmpeg-python (programmatic editing)             │
│  Whisper captions (Alex Hormozi style)                      │
│  auto-editor + librosa (silence removal + beat detect)     │
├─────────────────────────────────────────────────────────────┤
│  Layer 2: Acquisition                                      │
│  yt-dlp (download source videos)                            │
│  faster-whisper (transcribe + word-level timestamps)        │
│  Whop API (browse bounties)                                 │
├─────────────────────────────────────────────────────────────┤
│  Layer 1: Foundation                                        │
│  Python 3.10+ + FFmpeg 7+ + yt-dlp + Whisper models        │
│  + Whop CLI + native APIs SDKs                              │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 الـ Data Flow (دورة حياة الفيديو)

```
1. Whop bounties (browse) ─────────┐
2. Download source (yt-dlp)        │
3. Transcribe (faster-whisper)     │
4. Auto-edit (silence + cuts)      │  ← ينتج 3-5 segments
5. Viral-edit per segment:         │
   ├─ B-roll overlay              │
   ├─ Double zoom                │
   ├─ Beat sync                  │
   ├─ Captions                  │
   └─ Pattern interrupt          │
6. halal_check (5-بند)             │  ← gate: must PASS
7. retention_scorecard (6-بند)    │  ← gate: must ≥5/6
8. Publish: TikTok + IG + YT      │  ← parallel via 3 APIs
9. Submit to Whop bounty          │  ← with link + analytics
10. Track analytics daily         │
11. Update worklog + state.json   │
12. A/B/C hooks analysis         │  ← Yuan Fang loop
```

### 1.3 الـ State Management

كل سكربت يقرأ/يكتب state في `state.json`:

```json
{
  "last_run": "2026-09-11T15:30:00",
  "videos_processed": ["vid_001", "vid_002"],
  "videos_published": {
    "vid_001": {
      "tiktok": {"id": "...", "url": "...", "status": "published"},
      "instagram": {"id": "...", "url": "...", "status": "published"},
      "youtube": {"id": "...", "url": "...", "status": "published"},
      "whop_bounty": {"id": "...", "status": "submitted"}
    }
  },
  "analytics": {
    "vid_001": {
      "views": 8500,
      "shares": 200,
      "saves": 180,
      "retention_30s": 0.65,
      "share_rate": 0.0235
    }
  }
}
```

`_common.py` يدير كل الـ state reads/writes.

---

## 2. التشغيل الفعلي (Production Setup)

### 2.1 متطلبات النظام

| المتطلب | الإصدار | لماذا |
|---------|---------|-------|
| OS | Linux/macOS/WSL | FFmpeg + cron support |
| Python | 3.10+ | for type hints + faster-whisper |
| FFmpeg | 7.0+ | for all video processing |
| RAM | 8GB+ (16GB مثالي) | Whisper + Stable Diffusion |
| Disk | 50GB+ free | for video cache + Whisper models |
| GPU | Optional (CUDA/Metal) | faster Whisper + SD inference |
| Internet | مستقر | للـ APIs |

### 2.2 التثبيت

```bash
# 1. استنساخ المستودع
git clone https://github.com/geasas/whop-viral-system.git
cd whop-viral-system

# 2. تشغيل setup
bash scripts/setup.sh
# - يفحص Python/FFmpeg/yt-dlp
# - يثبت: pip install -r scripts/requirements.txt
# - ينزّل Whisper models (tiny/base)
# - ينشئ .env من .env.template

# 3. ملء الـ credentials
nano .env
# - TIKTOK_CLIENT_KEY=...
# - TIKTOK_CLIENT_SECRET=...
# - TIKTOK_ACCESS_TOKEN=...
# - INSTAGRAM_ACCESS_TOKEN=...
# - INSTAGRAM_USER_ID=...
# - YOUTUBE_CLIENT_SECRET_JSON=/path/to/client_secret.json
# - WHOP_API_KEY=...
# - WHOP_BEARER_TOKEN=...

# 4. اختبار التثبيت
python scripts/download_source.py --help
python scripts/transcribe.py --help
python scripts/viral_edit.py --help
```

### 2.3 تفعيل الـ APIs (مرة واحدة)

#### TikTok Content Posting API
1. اذهب إلى https://developers.tiktok.com/
2. أنشئ تطبيق جديد (App type: "Web").
3. أضف redirect URI: `https://yourdomain.com/callback`.
4. اطلب النطاقات: `video.publish`, `video.upload`.
5. انتظر الموافقة (4-6 أسابيع للـ audit).
6. احفظ `client_key` + `client_secret` في `.env`.

#### Instagram Graph API
1. https://developers.facebook.com/apps/ → إنشاء app جديد.
2. Add Product: Instagram.
3. أضف منتج "Instagram API with Instagram Login".
4. اطلب النطاقات: `instagram_business_basic`, `instagram_business_content_publish`, `instagram_business_manage_comments`, `instagram_business_manage_messages`.
5. اربط حساب Instagram business account.
6. احصل على `access_token` (long-lived, 60 day) + `ig_user_id`.

#### YouTube Data API v3
1. https://console.cloud.google.com/ → إنشاء project.
2. Enable "YouTube Data API v3".
3. إنشاء OAuth 2.0 credentials (Application type: Desktop).
4. تنزيل `client_secret.json`.
5. أول تشغيل: يطلب تصريح، يحفظ `token.json`.

#### Whop API
1. https://whop.com → Settings → Developer.
2. إنشاء API key (Bearer token).
3. (اختياري) تنزيل Whop CLI: `curl -fsSL https://whop.com/install.sh | sh`.
4. سجل الـ bounty submissions عبر `POST /api/v1/bounty_submissions`.

### 2.4 إعداد الحسابات الثانوية (Trial Mode)

```bash
# 1. إنشاء حسابات ثانوية بنفس الـ niche
# 2. نشر يومي على الثانوي فقط
# 3. مراقبة median views آخر 50 فيديو
# 4. نقل للرئيسي فقط عند:
#    - median ≥ 2x حساب رئيسي → نقل + استمرار
#    - median ≥ 3x → استثمار بـ Paid لاحقاً
```

### 2.5 تفعيل الـ cron اليومي

```bash
# 1. افتح crontab
crontab -e

# 2. أضف:
0 6 * * * cd /path/to/whop-viral-system && bash scripts/daily_pipeline.sh >> logs/cron-$(date +\%Y\%m\%d).log 2>&1

# 3. احفظ
```

الساعة 06:00 (UTC timezone matching جمهور US/Europe) تشغّل:
- download → transcribe → auto_edit → viral_edit → halal_check → scorecard → publish_* → submit_whop → analytics.

---

## 3. الـ Stack التقني بالتفصيل

### 3.1 Python Libraries (`scripts/requirements.txt`)

```
# Core
python-dotenv>=1.0.0
requests>=2.31.0
httpx>=0.25.0
pydantic>=2.0.0

# Video/Audio
ffmpeg-python>=0.2.0
moviepy>=2.0.0
opencv-python-headless>=4.10.0
Pillow>=10.0.0
imageio-ffmpeg>=0.5.0

# AI/ML
faster-whisper>=1.0.0
openai-whisper>=20231117
torch>=2.0.0  # for whisper GPU
librosa>=0.10.0
numpy>=1.24.0
scipy>=1.11.0

# APIs
google-api-python-client>=2.100.0
google-auth-oauthlib>=1.1.0
google-auth-httplib2>=0.2.0
tiktok-api-python>=0.5.0  # unofficial

# Download
yt-dlp>=2024.0.0

# Utils
tqdm>=4.65.0
rich>=13.0.0
python-logging-loki>=0.5.0
```

### 3.2 External Tools

| الأداة | التثبيت | الاستخدام |
|--------|---------|---------|
| FFmpeg 7+ | `apt install ffmpeg` / `brew install ffmpeg` | كل المونتاج |
| yt-dlp | `pip install yt-dlp` | download source videos |
| auto-editor | `pip install auto-editor` | silence removal |
| Whop CLI | `curl -fsSL https://whop.com/install.sh \| sh` | bounty submissions |
| stable-diffusion WebUI | `git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui` | B-roll generation |

### 3.3 نماذج Whisper

| النموذج | الحجم | السرعة | الدقة | الاستخدام |
|---------|------|--------|-------|----------|
| tiny | 75MB | أسرع | أدنى | preview / سريع |
| base | 145MB | سريع | جيد | افتراضي |
| small | 488MB | متوسط | جيد جداً | عربي + إنجليزي |
| medium | 1.5GB | بطيء | ممتاز | للمحتوى الإنجليزي الصعب |
| large-v3 | 3GB | بطيء جداً | أعلى | لمحتوى عربي صعب |

### 3.4 الـ Audio الـ حلال (مجاني)

| المصدر | الرابط | المحتوى |
|--------|--------|---------|
| mp3quran.net | https://mp3quran.net | قرآن مرتّل |
| assabile.com | https://www.assabile.com | أناشيد بلا آلات |
| alafasy.tv | https://www.alafasy.tv | مشاريع العفاسي |
| anasheed-radio | https://anasheed.radio | راديو أناشيد |
| NoCopyrightSounds | https://ncs.io | إيقاع بلا حقوق (لكن فيه موسيقى — تجنب) |

---

## 4. الـ Cron اليومي بالتفصيل

### 4.1 الجدول الزمني (UTC)

| الساعة (UTC) | المهمة | العقل المسؤول |
|--------------|-------|----------------|
| 06:00 | state review + worklog قراءة | Sima Yi |
| 07:00 | pipeline health check | Cao Cao |
| 08:00 | browse Whop bounties + اختيار | Guo Jia |
| 09:00 | halal_check على المحتوى المختار | Liu Bei |
| 10:00 | timing + niche alignment + narrative | Dong Zhuo |
| 11:00 | الحملة الكبرى (إن وُجدت فرصة 10×) | Lu Bu |
| 12:00 | A/B/C نتائج اليوم السابق + توصيات | Yuan Fang |
| 15:00-18:00 | التنفيذ (download → publish) | كل العقول بالتوازي |
| 22:00 | analytics + worklog تحديث | Cao Cao |

### 4.2 الـ daily_pipeline.sh (المختصر)

```bash
#!/bin/bash
set -e
cd "$(dirname "$0")/.."

LOG=logs/$(date +%Y%m%d).log
mkdir -p logs

# 1. اختر فيديو اليوم
CAMPAIGN_URL=$(python scripts/select_daily_campaign.py)
echo "[$(date)] Campaign: $CAMPAIGN_URL" >> $LOG

# 2. تحميل
python scripts/download_source.py --url "$CAMPAIGN_URL" --out /tmp/raw.mp4

# 3. transcription
python scripts/transcribe.py --input /tmp/raw.mp4 --out /tmp/transcript.json

# 4. auto-edit (يكتشف segments)
python scripts/auto_edit.py --input /tmp/raw.mp4 --transcript /tmp/transcript.json --out /tmp/clips/

# 5. لكل clip، viral-edit
for clip in /tmp/clips/*.mp4; do
  python scripts/viral_edit.py --segment "$clip" --broll assets/broll/ --audio assets/nasheed/ --out /tmp/final_$(basename $clip)
  
  # 6. Halal gate
  python scripts/halal_check.py --video /tmp/final_*.mp4 || { echo "[$(date)] Halal check FAILED" >> $LOG; continue; }
  
  # 7. Retention scorecard
  python scripts/retention_scorecard.py --video /tmp/final_*.mp4 || { echo "[$(date)] Scorecard FAILED" >> $LOG; continue; }
  
  # 8. Publish
  python scripts/publish_tiktok.py --video /tmp/final_*.mp4 --caption "$(python scripts/gen_caption.py)" &
  python scripts/publish_instagram.py --video /tmp/final_*.mp4 --caption "..." &
  python scripts/publish_youtube.py --video /tmp/final_*.mp4 --title "..." &
  wait
  
  # 9. Submit to Whop bounty
  python scripts/submit_whop_bounty.py --video /tmp/final_*.mp4 --bounty "$CAMPAIGN_URL"
done

# 10. Analytics
python scripts/analytics_dashboard.py --date $(date +%Y-%m-%d) >> $LOG
```

---

## 5. الـ Error Handling + Resilience

### 5.1 الـ Retry Logic

`_common.py` يوفر:
```python
def with_retry(fn, max_retries=3, backoff=2.0):
    """Retry على 429, 500, timeout"""
    for attempt in range(max_retries):
        try:
            return fn()
        except (RateLimitError, ServerError, TimeoutError) as e:
            sleep(backoff ** attempt)
    raise MaxRetriesExceeded
```

### 5.2 الـ Logging

كل سكربت يكتب في:
- `logs/{date}.log` — مفصل
- `logs/errors.log` — أخطاء فقط
- `worklog.md` — ملخص

### 5.3 الـ Token Refresh

`_common.py`:
- TikTok access token: 24 hour، refresh تلقائي.
- Instagram long-lived token: 60 day، refresh كل 50 day.
- YouTube: token.json يُحدّث تلقائياً.

---

## 6. الـ Monitoring والـ Alerts

### 6.1 الـ Health Check يومي

```bash
python scripts/health_check.py
# - فحص API tokens (valid)
# - فحص state.json (not corrupted)
# - فحص disk space
# - فحص logs آخر 24 ساعة للأخطاء
# - فحص whisper models (downloaded)
```

### 6.2 الـ KPIs اليومية

`analytics_dashboard.py` يخرج:
```json
{
  "date": "2026-09-11",
  "videos_published": 4,
  "total_views": 12500,
  "avg_view_rate": 0.78,
  "avg_retention_30s": 0.52,
  "share_rate": 0.018,
  "save_rate": 0.022,
  "whop_submissions": 3,
  "whop_approved": 1,
  "estimated_revenue_today": 12.50,
  "mrr": 287.50
}
```

### 6.3 الـ Alert (إن فشل)

```python
# _common.py
def alert(message: str, severity: str = "warning"):
    """يطبع في logs + (اختياري) Telegram bot"""
    if severity == "critical":
        # 1. اطبع في errors.log
        # 2. اوقف الـ pipeline
        # 3. (إن لزم) أرسل Telegram
```

---

## 7. الـ Backup والـ Recovery

### 7.1 الـ Daily Backup

```bash
# في cron 23:00:
0 23 * * * tar -czf /backup/whop-system-$(date +\%Y\%m\%d).tar.gz /path/to/whop-viral-system/{state.json,worklog.md,logs}
```

### 7.2 الـ Recovery

```bash
# 1. استرجع backup
tar -xzf /backup/whop-system-20260910.tar.gz -C /

# 2. تحقق من state
python scripts/health_check.py --verify-state

# 3. أعد المحاولة للمهمة الفاشلة
python scripts/{failed_script}.py --resume-from state.json
```

---

## 8. التطوير والتوسيع

### 8.1 إضافة عقل جديد
1. أنشئ `minds/{new_mind}.md` بـ: worldview, signature_move, blind_spots, when_to_activate, prompt.
2. أضفه في `AGENTS.md` §1.
3. أضف وزنه في `MASTER.md` §3.
4. أضفه في `daily_pipeline.sh` إن لزم.

### 8.2 إضافة منصة جديدة (مثلاً: Snapchat)
1. أنشئ `scripts/publish_snapchat.py`.
2. اتبع نفس interface: `Publish(video, caption, hashtags) -> PostResult`.
3. أضفها في `daily_pipeline.sh`.
4. حدّث `analytics_dashboard.py` لجلب analytics منها.

### 8.3 إضافة أدوات AI جديدة
1. أضفها في `scripts/requirements.txt`.
2. أكمل الـ interface في `_common.py`.
3. وثّق في `TOOLS.md`.

---

## 9. الـ Security Best Practices

### 9.1 الـ API Tokens
- لا تُرفع لـ GitHub أبداً (`.gitignore` يستثني `.env`).
- استخدم environment variables أو secret manager.
- rotate كل 90 يوم.

### 9.2 الـ Account Safety
- لا تسجل دخول يومياً بكلمة مرور — استخدم API.
- لا تستخدم بوتات followers / engagement.
- لا تنشر أكثر من 5 فيديوهات/يوم/حساب.
- اترك 2+ ساعة بين النشرات.

### 9.3 الـ Content Safety
- لا تقت من قنوات بها محتوى محرم.
- راجع الفيديو قبل النشر (AI may hallucinate).
- استخدم `halal_check.py` قبل كل نشر.

---

## 10. الـ Performance Optimization

### 10.1 الـ Parallelism
- الـ download + transcribe: متسلسلة (تعتمد على بعض).
- الـ viral_edit per clip: متوازية (3-5 clips بالتوازي).
- الـ publish (3 منصات): متوازية دائماً.

### 10.2 الـ Caching
- Whisper models: نزّل مرة واحدة، cache في `~/.cache/whisper/`.
- B-roll: cache في `assets/broll/` للاستخدام المتكرر.
- Captions templates: cache في `assets/captions/`.

### 10.3 الـ GPU Acceleration
- Whisper: استخدم `device='cuda'` أو `device='metal'`.
- FFmpeg: استخدم `-hwaccel cuda` أو `videotoolbox`.
- Stable Diffusion: استخدم GPU لـ inference أسرع بـ 10×.

---

## 11. الـ Maintenance

### 11.1 الـ Weekly Review
- تحديث الـ niche إن لزم (Dong Zhuo).
- مراجعة الـ bounties المتاحة (Guo Jia).
- تحديث الـ hooks الفائزة (Yuan Fang).
- مراجعة الـ halal checklist (Liu Bei).

### 11.2 الـ Monthly Review
- تحديث الأهداف (Sima Yi).
- مراجعة MRR (Cao Cao).
- تحديث الـ Strategy.md + KPIs.
- مراجعة شروط المنصات الجديدة (Cao Cao).

### 11.3 الـ Quarterly Review
- تحديث الـ 12-month plan.
- مراجعة الـ ethics + الحلال.
- تحديث الـ repository + release new version.
