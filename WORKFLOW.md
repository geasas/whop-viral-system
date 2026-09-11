# WORKFLOW.md — السير اليومي التفصيلي

> **هذا الملف هو الـ runbook الفعلي. أي AI agent يقرأ هذا + `MASTER.md` يستطيع تنفيذ اليوم الكامل.**
>
> التزم بالترتيب. لا تخطِ خطوة قبل إكمال السابقة. كل خطوة لها script جاهز.

---

## 1. الصباح (06:00-12:00 UTC) — العقول تستعد

### 06:00 — Sima Yi: State Review

```bash
# اقرأ آخر state
cat state.json | jq '.last_run, .videos_published | length'
# راجع worklog آخر 24 ساعة
tail -200 worklog.md
# راجع MRR trajectory
python scripts/analytics_dashboard.py --last-30-days
```

**قرارات Sima Yi:**
- هل النظام on-track للأهداف؟
- هل في shadowban علامات؟
- هل نوقف اليوم أم نكمل؟

### 07:00 — Cao Cao: Pipeline Health

```bash
# فحص الـ pipeline
python scripts/health_check.py
# فحص API tokens
python scripts/check_tokens.py
# فحص whisper + ffmpeg
ffmpeg -version | head -1
python -c "import faster_whisper; print('whisper OK')"
```

**قرارات Cao Cao:**
- استبدال أي أداة معطلة.
- تحديث الـ requirements إن لزم.

### 08:00 — Guo Jia: Whop Bounties Browse

```bash
# استعراض الحملات المتاحة
python scripts/browse_whop_bounties.py
# أو عبر Whop CLI
whop bounties list --category=all --sort=rate_per_1k
```

**معايير Guo Jia للاختيار (rating >70/100):**

| المعيار | الوزن | الحد الأدنى |
|---------|-------|------------|
| Rate per 1K views | 30 | ≥$1.00 |
| Audience match | 25 | US/Europe |
| Content type | 20 | motivation/business/finance |
| Difficulty | 15 | <= medium |
| KYC required | 10 | yes |

### 09:00 — Liu Bei: Halal Pre-Check

```bash
# تحقق من المصدر
python scripts/check_source_halal.py --url "$CAMPAIGN_URL"
# إن PASSED، استمر
```

**Liu Bei يحذر من:**
- حملات بموسيقى (Lil Baby، Mumford & Sons = تجنب).
- حملات فيها عرض عورة في الـ creatives.
- حملات بمحتوى مخالف (gambling، adult).

### 10:00 — Dong Zhuo: Timing + Niche

```bash
# تحديد أفضل وقت للنشر اليوم
python scripts/optimal_posting_time.py --audience=US --platform=all
# تحقق من niche alignment
python scripts/check_niche_alignment.py --campaign "$CAMPAIGN_URL" --our_niche="motivation/business"
```

**Dong Zhuo يحدد:**
- **Sweet spots للنشر (US audience):**
  - TikTok: Tue-Thu 14:00-18:00 (UTC-5 → 19:00-23:00 UTC)
  - Instagram: Mon-Fri 11:00 + 14:00 EST
  - YouTube: 19:00-22:00 EST

### 11:00 — Lu Bu: Single Big Shot Check

```bash
# هل في حملة bounty كبيرة (≥$5/1K views) اليوم؟
python scripts/find_big_bounty.py --min-rate=5.00
```

**إن وُجدت فرصة 10×:**
- كل الموارد عليها اليوم.
- أنتج 5+ فيديوهات لها بدلاً من المعتاد.

### 12:00 — Yuan Fang: A/B/C Hooks Analysis

```bash
# راجع نتائج الأمس
python scripts/analyze_hook_performance.py --yesterday
# اختبر patterns:
python scripts/generate_hook_variants.py --winning_hook "$(cat state.json | jq -r '.yesterday.winning_hook')"
```

**Yuan Fang يختبر:**
- A: نفس الـ hook الناجح.
- B: variant بصيغة مختلفة.
- C: hook جديد تماماً.

---

## 2. التنفيذ (15:00-18:00 UTC) — Pipeline الكامل

### Step 1: Download Source

```bash
python scripts/download_source.py \
  --url "$CAMPAIGN_URL" \
  --out /tmp/raw_$(date +%Y%m%d_%H).mp4 \
  --format "best[ext=mp4]" \
  --max-duration 7200  # 2 ساعة كحد أقصى
```

### Step 2: Transcribe

```bash
python scripts/transcribe.py \
  --input /tmp/raw_*.mp4 \
  --out /tmp/transcript.json \
  --model small \
  --language en \
  --word-timestamps
```

### Step 3: Auto-Edit (Segment Detection)

```bash
python scripts/auto_edit.py \
  --input /tmp/raw_*.mp4 \
  --transcript /tmp/transcript.json \
  --out /tmp/clips/ \
  --max-clips 5 \
  --min-duration 15 \
  --max-duration 60
```

الناتج: 3-5 segments في `/tmp/clips/clip_01.mp4`، `clip_02.mp4`...

### Step 4: Viral-Edit per Clip (Parallel)

```bash
# شغل 5 فيديوهات بالتوازي
for clip in /tmp/clips/clip_*.mp4; do
  (
    python scripts/viral_edit.py \
      --segment "$clip" \
      --broll assets/broll/ \
      --audio assets/nasheed/track_$(shuf -i 1-10 -n 1).mp3 \
      --hook "$(python scripts/gen_hook.py)" \
      --captions-style hormozi \
      --out /tmp/final_$(basename $clip .mp4).mp4
  ) &
done
wait
```

**ما يطبّقه viral_edit.py:**
- Double Zoom (91% → 100% → 109% كل 4-5 ثواني).
- B-Roll overlay كل 3-5 ثواني (40-60% من الفيديو).
- Beat Sync مع الـ nasheed.
- J-Cut / L-Cut على الانتقالات.
- Captions كارترايدج (Alex Hormozi style).
- Pattern Interrupt كل 3 ثواني.
- Loop closer في آخر 1 ثانية.

### Step 5: Halal Gate

```bash
for video in /tmp/final_*.mp4; do
  python scripts/halal_check.py --video "$video" || rm "$video"
done
```

**الـ 5 بنود في Halal Checklist:**
1. لا موسيقى محرّمة في الخلفية (SFX + nasheed فقط).
2. لا صورة محرّمة في B-roll (لا عورة، لا شخصيات محرّمة).
3. لا غش في الـ hook (الوعد يتحقق في الفيديو).
4. نسبة المصدر واضحة في الفيديو أو caption.
5. AI disclosure (إن لزم على المنصة).

### Step 6: Retention Scorecard

```bash
for video in /tmp/final_*.mp4; do
  SCORE=$(python scripts/retention_scorecard.py --video "$video" --output score)
  if [ "$SCORE" -lt 5 ]; then
    echo "FAIL ($SCORE/6): $video"
    rm "$video"
  else
    echo "PASS ($SCORE/6): $video"
  fi
done
```

**الـ 6 بنود في Retention Scorecard:**
1. Hook قوي في أول 3 ثواني (View Rate >85%).
2. B-Roll 40-60% من الفيديو.
3. Beat Sync مع الـ audio.
4. Captions كاملة + متحركة.
5. Pattern interrupt كل 3 ثواني.
6. Loop closer في آخر 1 ثانية.

### Step 7: Publish to 3 Platforms (Parallel)

```bash
for video in /tmp/final_*.mp4; do
  CAPTION=$(python scripts/gen_caption.py --video "$video")
  HASHTAGS=$(python scripts/gen_hashtags.py --niche="motivation")
  
  # نشر متوازي
  python scripts/publish_tiktok.py \
    --video "$video" \
    --caption "$CAPTION" \
    --hashtags "$HASHTAGS" &
  
  python scripts/publish_instagram.py \
    --video "$video" \
    --caption "$CAPTION" \
    --hashtags "$HASHTAGS" \
    --cover-thumbnail "$(python scripts/gen_thumbnail.py --video $video)" &
  
  python scripts/publish_youtube.py \
    --video "$video" \
    --title "$CAPTION" \
    --description "$CAPTION" \
    --tags "$HASHTAGS" \
    --category 24 &  # Entertainment
  
  wait
  
  # تحديث state.json بالـ post IDs
  python scripts/_common.py update-state --video "$video" --status published
done
```

### Step 8: Submit to Whop Bounty

```bash
for video in /tmp/final_*.mp4; do
  # اجمع الـ URLs من الـ state
  TIKTOK_URL=$(python scripts/_common.py get-state --video $video --field tiktok.url)
  IG_URL=$(python scripts/_common.py get-state --video $video --field instagram.url)
  YT_URL=$(python scripts/_common.py get-state --video $video --field youtube.url)
  
  python scripts/submit_whop_bounty.py \
    --bounty-id "$CAMPAIGN_BOUNTY_ID" \
    --deliverable-type multi_link \
    --links "$TIKTOK_URL,$IG_URL,$YT_URL" \
    --notes "Auto-generated viral clip via Whop Viral System"
done
```

### Step 9: Update State + Worklog

```bash
# تحديث state
python scripts/_common.py update-state --date $(date +%Y-%m-%d) --status complete

# تحديث worklog
cat >> worklog.md << EOF
---
Task ID: $(date +%Y-%m-%d)-pipeline
Agent: All (Multi-Mind Daily Run)
Task: تنفيذ pipeline اليومي الكامل

Work Log:
- اختيار الحملة: $CAMPAIGN_URL (Guo Jia)
- تحميل + transcription + auto-edit
- ${NUM_CLIPS} segments منتجة
- ${NUM_PUBLISHED} فيديوهات نُشرت على 3 منصات
- ${NUM_SUBMITTED} submitted إلى Whop bounty

Stage Summary:
- CPU time: ${ELAPSED}min
- Tokens used: $TIKTOK_TOKEN + $IG_TOKEN + $YT_TOKEN
- Next focus: $NEXT_FOCUS
EOF
```

---

## 3. المساء (22:00 UTC) — Analytics + Reflection

### 22:00 — Analytics Dashboard

```bash
python scripts/analytics_dashboard.py \
  --date $(date +%Y-%m-%d) \
  --output-format json > logs/analytics_$(date +%Y%m%d).json

# عرض الـ summary
cat logs/analytics_$(date +%Y%m%d).json | jq '{
  videos_published,
  total_views,
  avg_view_rate,
  avg_retention_30s,
  share_rate,
  save_rate,
  whop_submissions,
  estimated_revenue_today,
  mrr
}'
```

### 22:30 — Cao Cao: Worklog Update + Lessons

```bash
# راجع الأخطاء
tail -100 logs/errors.log
# أضف lessons learned
cat >> worklog.md << EOF

Lessons:
- ما نجح اليوم: ...
- ما فشل: ...
- ما نجرّب غداً: ...
EOF
```

---

## 4. الأسبوعي (الأحد 10:00 UTC)

### Sunday Review (كل العقول)

```bash
# تقرير أسبوعي
python scripts/weekly_report.py --week $(date +%Y-W%V)

# تحديث:
# - niche إن لزم (Dong Zhuo)
# - hooks الفائزة (Yuan Fang)
# - halal checklist تحديث (Liu Bei)
# - أهداف الأسبوع القادم (Sima Yi)
```

---

## 5. الـ Edge Cases

### 5.1 فشل تحميل الفيديو
```bash
if ! python scripts/download_source.py --url "$CAMPAIGN_URL"; then
  # جرّب URL بديل
  CAMPAIGN_URL=$(python scripts/get_backup_campaign.py)
  python scripts/download_source.py --url "$CAMPAIGN_URL"
fi
```

### 5.2 فشل transcription (لغة غير معروفة)
```bash
python scripts/transcribe.py --input $VIDEO --language en --fallback-model base
# إن فشل، استخدم google-cloud-speech (يدفع)
# أو احذف الفيديو وجرّب فيديو آخر
```

### 5.3 فشل API (rate limit)
```python
# _common.py
def with_retry(fn, max_retries=5, backoff=2.0):
    for attempt in range(max_retries):
        try:
            return fn()
        except RateLimitError:
            sleep(backoff ** attempt)
            continue
```

### 5.4 Shadowban مشتبه
```bash
# 1. توقف 48-72 ساعة
# 2. اطبع الفيديوهات المعلّمة:
python scripts/_common.py list-flagged
# 3. حول كل flagged فيديو إلى "Only Me" (لا تحذف)
python scripts/set_only_me.py --video-id $VID
# 4. انشر 14 يوم original content فقط (no clipping)
# 5. أعد تفعيل النشر بعد 14 يوم
```

### 5.5 Whop bounty مرفوض
```bash
# راجع سبب الرفض
python scripts/whop_bounty_status.py --submission-id $SUB_ID --verbose
# الأسباب الشائعة:
# - فيديو غير مطابق للموضوع
# - نشر مكرر من account تاني
# - botting مشتبه
# - علامة مائية مزعجة
```

---

## 6. الـ Quality Gates — المُلخّص

| الـ Gate | متى | المعيار | السكربت |
|---------|-----|---------|---------|
| Halal Check | قبل النشر | 5/5 | `halal_check.py` |
| Retention Scorecard | قبل النشر | ≥5/6 | `retention_scorecard.py` |
| Hook Test | على الحساب الثانوي | View Rate >70% | `analyze_hook_performance.py` |
| Platform API | قبل النشر | token valid | `check_tokens.py` |
| Whop Bounty | قبل التسليم | campaign active | `browse_whop_bounties.py` |

---

## 7. الـ Daily Targets

| المقياس | الهدف اليومي | الهدف الممتاز |
|---------|--------------|---------------|
| فيديوهات منتجة | 3-5 | 5 |
| فيديوهات منشورة (كل منصة) | 3-5 | 5 |
| Whop bounty submissions | 3-5 | 5 |
| إجمالي مشاهدات (3 منصات) | 1,000+ | 10,000+ |
| Retention @ 30s | >40% | >60% |
| Share Rate | >1.0% | >1.7% |
| Save Rate | >1.5% | >2.0% |

---

## 8. الـ Weekly Targets

| المقياس | الهدف الأسبوعي |
|---------|-----------------|
| فيديوهات منشورة (كل منصة) | 21-35 |
| Whop bounty submissions | 15-25 |
| إجمالي مشاهدات | 10,000+ |
| أول فيروسي (>50K view) | قبل أسبوع 4 |
| أول دولار من Whop | قبل أسبوع 8 |

---

## 9. الـ 90-Day Plan

### الأيام 1-30: Proof of Concept
- حسابات ثانوية فقط.
- 3-5 فيديوهات/يوم.
- Trial Reels على IG.
- Fan Account system على TikTok.
- الهدف: first 10K view video.

### الأيام 31-60: First Revenue
- نقل الناجح للرئيسي.
- أول دولار من Whop Content Rewards.
- 10-30 فيديو فيروسي.
- الهدف: $50-$300 MRR.

### الأيام 61-90: Scaling
- 3-5 فيديوهات/يوم على 3 منصات.
- 100K+ monthly views.
- عضوية Whop الأولى ($15-20/شهر).
- الهدف: $300-$1000 MRR.

---

## 10. الـ 12-Month Plan

### شهور 4-6: $1K → $3K MRR
- 5 حسابات رئيسية على 3 منصات.
- عضوية 30-100 مشترك.
- منتج رقمي أول (template/cheatsheet).

### شهور 7-9: $3K → $5K MRR
- 10K+ متابع عبر الحسابات.
- عضوية 100-200 مشترك.
- منتج رقمي + إطلاق VSL.

### شهور 10-12: $5K → $10K+ MRR
- 5K-10K متابع لكل حساب.
- عضوية 200-500 مشترك.
- 3-5 منتجات رقمية + mastermind ($200/شهر).

---

## 11. متى توقف الـ Pipeline

**توقف فوراً إن:**
1. Shadowban مؤكد → pause 14 يوم.
2. API token مسحوب → rotate قبل الاستئناف.
3. Halal violation اكتُشف → وقف + مراجعة.
4. Retention Scorecard fail rate >50% → وقف + تحسين الـ hooks.
5. Whop bounty reject rate >30% → وقف + راجع الشروط.

---

## 12. الـ Daily Checklist Final

```markdown
## $(date +%Y-%m-%d) Daily Run

### الصباح (06:00-12:00)
- [ ] Sima Yi: state review
- [ ] Cao Cao: pipeline health
- [ ] Guo Jia: bounty selection
- [ ] Liu Bei: halal pre-check
- [ ] Dong Zhuo: timing + niche
- [ ] Lu Bu: big shot check
- [ ] Yuan Fang: A/B/C analysis

### التنفيذ (15:00-18:00)
- [ ] download_source.py
- [ ] transcribe.py
- [ ] auto_edit.py
- [ ] viral_edit.py (3-5 parallel)
- [ ] halal_check.py (5/5)
- [ ] retention_scorecard.py (≥5/6)
- [ ] publish_tiktok.py
- [ ] publish_instagram.py
- [ ] publish_youtube.py
- [ ] submit_whop_bounty.py

### المساء (22:00)
- [ ] analytics_dashboard.py
- [ ] worklog.md update
- [ ] lessons learned
```

احفظ هذا في `logs/$(date +%Y%m%d)_checklist.md` كل يوم.
