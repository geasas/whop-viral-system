# API_CONTRACT.md — Whop + TikTok + Instagram + YouTube API

> **كل ما تحتاجه للتعامل مع الـ 4 APIs الرسمية.**
>
> Tokens + Endpoints + Scopes + Examples + Rate Limits.

---

## 1. Whop API

### 1.1 الـ Endpoints الأساسية

| الـ Endpoint | الطريقة | الوظيفة |
|--------------|--------|---------|
| `https://api.whop.com/api/v1/bounties` | GET | استعراض كل bounties |
| `https://api.whop.com/api/v1/bounties/{id}` | GET | تفاصيل bounty |
| `https://api.whop.com/api/v1/bounty_submissions` | POST | تسليم clip |
| `https://api.whop.com/api/v1/bounty_submissions/{id}` | GET | حالة التسليم |
| `https://api.whop.com/api/v1/me` | GET | معلومات المستخدم |
| `https://api.whop.com/api/v1/payouts` | GET | استعراض payouts |

### 1.2 الـ Authentication

```bash
# Bearer token in headers
curl -H "Authorization: Bearer $WHOP_BEARER_TOKEN" \
     https://api.whop.com/api/v1/bounties
```

### 1.3 استعراض الـ Bounties (مثال)

```bash
# استعراض كل bounties
curl -X GET \
  -H "Authorization: Bearer $WHOP_BEARER_TOKEN" \
  "https://api.whop.com/api/v1/bounties?expanded=true" | jq

# استعراض bounty معينة
curl -X GET \
  -H "Authorization: Bearer $WHOP_BEARER_TOKEN" \
  "https://api.whop.com/api/v1/bounties/bnty_xxx" | jq
```

### 1.4 تسليم clip

```bash
curl -X POST \
  -H "Authorization: Bearer $WHOP_BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "bounty_id": "bnty_xxx",
    "deliverable_type": "multi_link",
    "links": ["https://tiktok.com/@user/video/123", "https://instagram.com/reel/abc"],
    "notes": "Auto-generated viral clip"
  }' \
  https://api.whop.com/api/v1/bounty_submissions
```

### 1.5 متابعة حالة التسليم

```bash
curl -X GET \
  -H "Authorization: Bearer $WHOP_BEARER_TOKEN" \
  "https://api.whop.com/api/v1/bounty_submissions/sub_xxx"
```

الـ status: `entry.approved`, `entry.rejected`, `entry.review`.

### 1.6 Whop CLI (Optional)

```bash
# Install
curl -fsSL https://whop.com/install.sh | sh

# List bounties
whop bounties list --category=all --sort=rate_per_1k

# Submit
whop bounties submit --bounty-id bnty_xxx --links "..."

# Status
whop bounties status --submission-id sub_xxx
```

### 1.7 الـ Rate Limits
- 60 request/minute per token.
- 1000 request/hour per app.
- Pagination: 50 per page.

### 1.8 SDKs الرسمية
- TypeScript: `npm install @whop/api`
- Python: `pip install whop-python`
- Ruby: `gem install whop`

### 1.9 MCP Servers (للـ AI agents)
```bash
# Claude Desktop / Cursor / Grok integration
whop mcp install
# Adds Whop MCP server to ~/.config/claude/mcp.json
```

### 1.10 الـ Webhooks (لا توجد للـ bounties — polling مطلوب)
```python
# polling كل ساعة
import time
while True:
    submissions = get_bounty_submissions()
    for s in submissions:
        if s['status'] == 'entry.review':
            # wait
            continue
        elif s['status'] == 'entry.approved':
            log_to_worklog(s, 'approved')
        elif s['status'] == 'entry.rejected':
            log_to_worklog(s, 'rejected')
    time.sleep(3600)
```

---

## 2. TikTok Content Posting API v2

### 2.1 الـ Endpoints

| الـ Endpoint | الطريقة | الوظيفة |
|--------------|--------|---------|
| `https://open.tiktokapis.com/v2/oauth/token/` | POST | تبديل code لـ access_token |
| `https://open.tiktokapis.com/v2/user/info/` | GET | معلومات المستخدم |
| `https://open.tiktokapis.com/v2/post/publish/video/init/` | POST | بدء رفع فيديو |
| `https://open.tiktokapis.com/v2/post/publish/status/fetch/` | POST | حالة النشر |
| `https://open.tiktokapis.com/v2/post/publish/video/mp4/upload/` | POST | رفع الفيديو MP4 |

### 2.2 الـ Authentication (OAuth 2.0)

```python
# Step 1: redirect user to authorization URL
auth_url = f"https://www.tiktok.com/v2/auth/authorize/?client_key={CLIENT_KEY}&scope=video.publish&response_type=code&redirect_uri={REDIRECT_URI}"

# Step 2: exchange code for access_token
import requests
resp = requests.post("https://open.tiktokapis.com/v2/oauth/token/", data={
    "client_key": CLIENT_KEY,
    "client_secret": CLIENT_SECRET,
    "code": CODE,
    "grant_type": "authorization_code",
    "redirect_uri": REDIRECT_URI,
})
tokens = resp.json()
# {"access_token": "...", "refresh_token": "...", "expires_in": 86400}
```

### 2.3 Refresh Token (each 24h)

```python
resp = requests.post("https://open.tiktokapis.com/v2/oauth/refresh_token/", data={
    "client_key": CLIENT_KEY,
    "client_secret": CLIENT_SECRET,
    "refresh_token": REFRESH_TOKEN,
    "grant_type": "refresh_token",
})
new_tokens = resp.json()
# Save to .env: TIKTOK_ACCESS_TOKEN, TIKTOK_REFRESH_TOKEN
```

### 2.4 نشر فيديو (Direct Post)

```python
# Step 1: Initialize upload
init_resp = requests.post(
    "https://open.tiktokapis.com/v2/post/publish/video/init/",
    headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    json={
        "post_info": {
            "title": "Amazing viral clip!",
            "privacy_level": "PUBLIC_TO_EVERYONE",
            "disable_comment": False,
            "disable_duet": False,
            "disable_stitch": False,
            "video_cover_timestamp_ms": 1000,
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": 1234567,
            "chunk_size": 5242880,
            "total_chunk_count": 1,
        }
    }
)
publish_id = init_resp.json()['data']['publish_id']
upload_url = init_resp.json()['data']['upload_url']

# Step 2: Upload chunks
with open("final.mp4", "rb") as f:
    chunk = f.read(5242880)
    requests.post(upload_url, data=chunk, headers={"Content-Range": "bytes 0-5242879/1234567"})

# Step 3: Check status
status_resp = requests.post(
    "https://open.tiktokapis.com/v2/post/publish/status/fetch/",
    headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    json={"publish_id": publish_id}
)
```

### 2.5 الـ Scopes المطلوبة

| Scope | الوظيفة |
|-------|---------|
| `video.publish` | Direct Post (public) — يحتاج audit |
| `video.upload` | Draft only — بدون audit |
| `user.info.basic` | معلومات المستخدم الأساسية |

### 2.6 الـ Rate Limits
- 600 requests/minute per app.
- 1 publish request per second.
- Max video size: 287MB.
- Max video duration: 10 minutes (35 minutes for verified).

### 2.7 الـ Audit Process
- TikTok يتطلب audit لكل app ينشر public content.
- يأخذ 4-6 أسابيع.
- يتضمن: business verification + sample videos.
- بعد الموافقة: نشر مباشر دون manual review.
- **أثناء الانتظار**: استخدم `video.upload` (Draft mode) + نشر يدوي من TikTok app.

### 2.8 الـ Webhooks (Recommended)

```python
# تكوين webhook endpoint
@app.route("/webhooks/tiktok", methods=["POST"])
def tiktok_webhook():
    event = request.json
    if event["event"] == "video.publish.complete":
        video_id = event["data"]["video_id"]
        # Update state.json
    return "", 200
```

---

## 3. Instagram Graph API

### 3.1 الـ Endpoints

| الـ Endpoint | الطريقة | الوظيفة |
|--------------|--------|---------|
| `https://graph.instagram.com/v21.0/{ig-user-id}/media` | POST | إنشاء container |
| `https://graph.instagram.com/v21.0/{container-id}` | GET | حالة container |
| `https://graph.instagram.com/v21.0/{ig-user-id}/media_publish` | POST | نشر الـ container |
| `https://graph.instagram.com/v21.0/{ig-user-id}` | GET | معلومات المستخدم |
| `https://graph.instagram.com/v21.0/{ig-user-id}/insights` | GET | analytics |

### 3.2 الـ Authentication (Long-Lived Token)

```bash
# Step 1: Get short-lived token from OAuth
# https://www.facebook.com/v21.0/dialog/oauth?client_id=APP_ID&redirect_uri=...&scope=instagram_business_basic,instagram_business_content_publish

# Step 2: Exchange for long-lived (60 days)
curl "https://graph.facebook.com/v21.0/oauth/access_token?grant_type=fb_exchange_token&client_id=APP_ID&client_secret=APP_SECRET&fb_exchange_token=SHORT_TOKEN"

# Step 3: Get IG user ID
curl "https://graph.instagram.com/v21.0/me?access_token=LONG_TOKEN"
```

### 3.3 نشر Reel (3-step Flow)

```python
import requests

# Step 1: Create media container
resp = requests.post(
    f"https://graph.instagram.com/v21.0/{IG_USER_ID}/media",
    data={
        "media_type": "REELS",
        "video_url": "https://your-cdn.com/video.mp4",  # must be public URL
        "caption": "Amazing viral clip! #motivation #business",
        "access_token": ACCESS_TOKEN,
    }
)
container_id = resp.json()["id"]

# Step 2: Poll status (wait for "FINISHED")
while True:
    status_resp = requests.get(
        f"https://graph.instagram.com/v21.0/{container_id}",
        params={"access_token": ACCESS_TOKEN}
    )
    if status_resp.json()["status"] == "FINISHED":
        break
    elif status_resp.json()["status"] == "ERROR":
        raise Exception(status_resp.json())
    time.sleep(5)

# Step 3: Publish
publish_resp = requests.post(
    f"https://graph.instagram.com/v21.0/{IG_USER_ID}/media_publish",
    data={
        "creation_id": container_id,
        "access_token": ACCESS_TOKEN,
    }
)
media_id = publish_resp.json()["id"]
```

### 3.4 الـ Scopes (Instagram API with Instagram Login)

| Scope | الوظيفة |
|-------|---------|
| `instagram_business_basic` | معلومات أساسية |
| `instagram_business_content_publish` | نشر محتوى |
| `instagram_business_manage_comments` | إدارة تعليقات |
| `instagram_business_manage_messages` | إدارة رسائل |

### 3.5 الـ Rate Limits
- 25 posts/24h per account.
- 200 API calls/hour per app.
- Video URL must be public (cannot be local file).
- Max video: 100MB / 90 seconds (REELS), or 60 minutes (VIDEO).

### 3.6 Refresh Token (each 50 days)

```python
resp = requests.get(
    "https://graph.instagram.com/refresh_access_token",
    params={
        "grant_type": "ig_refresh_token",
        "access_token": ACCESS_TOKEN,
    }
)
new_token = resp.json()["access_token"]
# 60 days new expiry
```

### 3.7 الـ Insights (Analytics)

```python
resp = requests.get(
    f"https://graph.instagram.com/v21.0/{media_id}/insights",
    params={
        "metric": "views,reach,likes,comments,shares,saves,profile_visits,follows",
        "access_token": ACCESS_TOKEN,
    }
)
insights = resp.json()
```

---

## 4. YouTube Data API v3

### 4.1 الـ Endpoints

| الـ Endpoint | الطريقة | الوظيفة |
|--------------|--------|---------|
| `https://www.googleapis.com/upload/youtube/v3/videos` | POST | رفع فيديو |
| `https://www.googleapis.com/youtube/v3/videos` | GET | معلومات فيديو |
| `https://www.googleapis.com/youtube/v3/videos` | PUT | تحديث metadata |
| `https://www.googleapis.com/youtube/v3/search` | GET | بحث |
| `https://www.googleapis.com/youtube/v3/channels` | GET | معلومات قناة |
| `https://youtubeanalytics.googleapis.com/v2/reports` | GET | analytics |

### 4.2 الـ Authentication (OAuth 2.0)

```python
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Scopes
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# OAuth flow
flow = InstalledAppFlow.from_client_secrets_file(
    "client_secret.json",
    SCOPES
)
creds = flow.run_local_server(port=8080)

# Save token for future use
with open("token.json", "w") as f:
    f.write(creds.to_json())

# Build service
youtube = build("youtube", "v3", credentials=creds)
```

### 4.3 رفع فيديو (Short)

```python
request_body = {
    "snippet": {
        "title": "Amazing viral clip!",
        "description": "Subscribe for more! #shorts #motivation",
        "tags": ["shorts", "motivation", "business"],
        "categoryId": "24",  # Entertainment
    },
    "status": {
        "privacyStatus": "public",
        "selfDeclaredMadeForKids": False,
        "containsSyntheticMedia": False,  # set True if AI-generated
    }
}

media = MediaFileUpload("final.mp4", chunksize=5*1024*1024, resumable=True)
response = youtube.videos().insert(
    part="snippet,status",
    body=request_body,
    media_body=media
).execute()

video_id = response["id"]
video_url = f"https://youtube.com/shorts/{video_id}"
```

### 4.4 الـ Quota System

- Default: 10,000 quota units/day per project.
- Each upload costs: 1600 units.
- Each search costs: 100 units.
- Each list costs: 1 unit.
- → Max ~6 uploads/day per project.

### 4.5 الـ API Audit (App Verification)

- YouTube يتطلب audit للـ apps الـ تنشر public videos.
- يأخذ 4-6 أسابيع (نفس TikTok).
- خلال الانتظار: رفع يدوي من YouTube Studio.

### 4.6 الـ Analytics (YouTube Analytics API)

```python
from googleapiclient.discovery import build

youtube_analytics = build("youtubeAnalytics", "v2", credentials=creds)

resp = youtube_analytics.reports().query(
    startDate="2026-09-01",
    endDate="2026-09-30",
    metrics="views,estimatedMinutesWatched,averageViewDuration,subscribersGained,likes,dislikes,comments,shares",
    dimensions="day",
    ids=f"channel=={CHANNEL_ID}",
).execute()

for row in resp["rows"]:
    date, views, minutes, avg_duration, subs, likes, dislikes, comments, shares = row
```

---

## 5. الـ Common Patterns (للـ 4 APIs)

### 5.1 Retry Logic

```python
# _common.py
from time import sleep
import requests

def with_retry(fn, max_retries=3, backoff=2.0):
    for attempt in range(max_retries):
        try:
            return fn()
        except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
            if hasattr(e, 'response') and e.response.status_code in [429, 500, 502, 503]:
                sleep(backoff ** attempt)
                continue
            raise
    raise MaxRetriesExceeded
```

### 5.2 Token Refresh

```python
# _common.py
def refresh_all_tokens():
    refresh_tiktok_token()
    refresh_instagram_token()
    # YouTube token.json auto-refreshes via google-auth
    
def check_tokens():
    """Check if all tokens valid. Return dict."""
    return {
        "tiktok": check_tiktok_token(),
        "instagram": check_instagram_token(),
        "youtube": check_youtube_token(),
        "whop": check_whop_token(),
    }
```

### 5.3 State Management

```python
# _common.py
import json
from pathlib import Path

STATE_FILE = "state.json"

def load_state():
    if Path(STATE_FILE).exists():
        return json.loads(Path(STATE_FILE).read_text())
    return {"videos": {}, "last_run": None}

def save_state(state):
    Path(STATE_FILE).write_text(json.dumps(state, indent=2, default=str))

def update_state(video_id, platform, post_id, post_url, status):
    state = load_state()
    state["videos"].setdefault(video_id, {})
    state["videos"][video_id][platform] = {
        "id": post_id,
        "url": post_url,
        "status": status,
        "timestamp": datetime.utcnow().isoformat(),
    }
    state["last_run"] = datetime.utcnow().isoformat()
    save_state(state)
```

### 5.4 Logging

```python
# _common.py
import logging

logger = logging.getLogger("whop-viral")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"logs/{date.today()}.log"),
        logging.StreamHandler(),
    ]
)

def log_to_worklog(task_id, agent, task, work_log, stage_summary):
    """Append to worklog.md"""
    entry = f"""
---
Task ID: {task_id}
Agent: {agent}
Task: {task}

Work Log:
{work_log}

Stage Summary:
{stage_summary}
"""
    with open("worklog.md", "a") as f:
        f.write(entry)
```

---

## 6. الـ Webhooks (Where Available)

### 6.1 TikTok Webhooks
- Configure: TikTok Developers → App → Webhooks.
- Events: `video.publish.complete`, `video.publish.failed`.
- Endpoint: HTTPS required.

### 6.2 Instagram Webhooks (via Meta)
- Configure: Facebook App → Webhooks.
- Events: `feed`, `permissions`, `ratings`.
- Note: No real-time video analytics webhook (use polling).

### 6.3 YouTube Push Notifications (PubSubHubbub)
- Subscribe to channel feeds.
- Notifications for new videos.
- Not for analytics (use polling).

### 6.4 Whop Webhooks
- ⚠️ No webhooks for bounty_submissions.
- Use polling (every hour).

---

## 7. الـ Errors Common to All APIs

| Code | المعنى | الحل |
|------|---------|------|
| 401 Unauthorized | Token expired/invalid | Refresh + retry |
| 403 Forbidden | Scope missing or audit pending | Check scopes + audit |
| 429 Too Many Requests | Rate limit | Backoff retry |
| 500/502/503 | Server error | Retry after 30s |
| 400 Bad Request | Invalid params | Check body |

---

## 8. الـ API Status Check (Health Check)

```python
# scripts/check_tokens.py
def check_all_apis():
    results = {}
    
    # TikTok
    try:
        resp = requests.get(
            "https://open.tiktokapis.com/v2/user/info/",
            headers={"Authorization": f"Bearer {TIKTOK_ACCESS_TOKEN}"}
        )
        results["tiktok"] = "✓" if resp.status_code == 200 else f"✗ ({resp.status_code})"
    except Exception as e:
        results["tiktok"] = f"✗ ({e})"
    
    # Instagram
    try:
        resp = requests.get(
            f"https://graph.instagram.com/v21.0/{IG_USER_ID}",
            params={"fields": "username,followers_count", "access_token": IG_TOKEN}
        )
        results["instagram"] = "✓" if resp.status_code == 200 else f"✗ ({resp.status_code})"
    except Exception as e:
        results["instagram"] = f"✗ ({e})"
    
    # YouTube
    try:
        # Use cached credentials
        youtube = build("youtube", "v3", credentials=creds)
        resp = youtube.channels().list(part="snippet", mine=True).execute()
        results["youtube"] = "✓" if resp.get("items") else "✗"
    except Exception as e:
        results["youtube"] = f"✗ ({e})"
    
    # Whop
    try:
        resp = requests.get(
            "https://api.whop.com/api/v1/me",
            headers={"Authorization": f"Bearer {WHOP_TOKEN}"}
        )
        results["whop"] = "✓" if resp.status_code == 200 else f"✗ ({resp.status_code})"
    except Exception as e:
        results["whop"] = f"✗ ({e})"
    
    return results

if __name__ == "__main__":
    results = check_all_apis()
    for api, status in results.items():
        print(f"{api}: {status}")
```

---

## 9. الـ Security Notes

### 9.1 Token Storage
- ✅ في `.env` (لا يُرفع لـ git).
- ✅ كل token بصلاحية محدودة (least privilege).
- ✅ Refresh تلقائي (لا يدوي).
- ❌ لا تخزّن في الـ code.
- ❌ لا في الـ logs.
- ❌ لا في الـ error messages للمستخدم.

### 9.2 Webhook Security
- ✅ تحقق من signature (TikTok: `X-TikTok-Notification-Signature`, Meta: `X-Hub-Signature-256`).
- ✅ استخدم HTTPS فقط.
- ✅ عامل الـ webhook كـ untrusted (validate كل شي).

### 9.3 Rate Limiting
- ✅ احترم rate limits.
- ✅ استخدم backoff exponential.
- ✅ Cache what you can.

---

## 10. الـ Quick Test Script

```bash
# Test all APIs
python scripts/check_tokens.py

# Sample output:
# tiktok: ✓
# instagram: ✓
# youtube: ✓
# whop: ✓
```

إذا كلها ✓، النظام جاهز للتشغيل.
