# Whop Viral System 🎬🧠

> **نظام متكامل لتحقيق $1,000+/شهر من Whop + مونتاج فيروسي + نشر يومي.**
> مبني على 7 عقول استراتيجية تعمل بالتوازي + stack كامل من الأدوات open-source (ميزانية $0).
> إطار إسلامي حلال صارم — لا ربا، لا غش، لا ضرر.

---

## 🎯 ماذا يفعل النظام؟

```
حملات Whop Content Rewards   →   تحميل فيديوهات مرخّصة
            ↓
   مونتاج فيروسي احترافي (FFmpeg + Whisper + MoviePy)
            ↓
   Retention Scorecard 6/6 + Halal Check 5/5
            ↓
   نشر يومي: TikTok + Instagram Reels + YouTube Shorts
            ↓
   تسليم اللقطة لـ Whop bounty API + analytics يومي
            ↓
   $1,000/شهر بحلول M3 → $10K+/شهر بحلول M12
```

---

## ⚡ البدء السريع (لأي AI Agent)

1. **اقرأ `MASTER.md`** — نقطة الدخول الوحيدة. خلال 90 ثانية تعرف كل شيء.
2. ثم `WORKFLOW.md` — السير اليومي تفصيلياً.
3. شغّل `bash scripts/setup.sh` — يثبت كل dependencies.
4. املأ `.env` (انظر `.env.template`).
5. شغّل `bash scripts/daily_pipeline.sh` للسير اليومي الأتوماتيكي.

---

## 📚 بنية المستودع

```
whop-viral-system/
├── MASTER.md                    ← نقطة الدخول لأي AI agent
├── README.md                    ← هذا الملف
├── SYSTEM.md                    ← البنية الكاملة + التشغيل
├── WORKFLOW.md                   ← السير اليومي (cron + steps)
├── AGENTS.md                    ← الـ 7 sub-agents + prompts
├── TOOLS.md                     ← الأدوات + setup
├── STRATEGY.md                  ← خطة 90 يوم + 12 شهر + KPIs
├── ETHICS.md                    ← الإطار الحلالي
├── API_CONTRACT.md              ← Whop/TikTok/IG/YT API
│
├── docs/                         ← 8 ملفات بحثية عميقة
│   ├── 01_whop_deep_dive.md
│   ├── 02_viral_editing_toolkit.md
│   ├── 03_tiktok_algorithm.md
│   ├── 04_instagram_reels_algorithm.md
│   ├── 05_youtube_shorts_algorithm.md
│   ├── 06_halal_framework.md
│   ├── 07_open_source_stack.md
│   └── 08_strategic_mind_activation.md
│
├── scripts/                      ← 14 سكربت Python/Bash جاهز للتشغيل
│   ├── _common.py
│   ├── download_source.py
│   ├── transcribe.py
│   ├── auto_edit.py
│   ├── viral_edit.py
│   ├── retention_scorecard.py
│   ├── generate_hormozi_captions.py
│   ├── publish_tiktok.py
│   ├── publish_instagram.py
│   ├── publish_youtube.py
│   ├── submit_whop_bounty.py
│   ├── analytics_dashboard.py
│   ├── daily_pipeline.sh
│   ├── setup.sh
│   └── requirements.txt
│
├── minds/                        ← 7 sub-agent prompts (واحد لكل عقل)
│   ├── sima_yi.md                (long-game + MRR trajectory)
│   ├── cao_cao.md               (system integration)
│   ├── guo_jia.md               (campaign selection)
│   ├── liu_bei.md               (halal + brand)
│   ├── dong_zhuo.md             (niche + timing + narrative)
│   ├── lu_bu.md                  (single big shot)
│   └── yuan_fang.md             (A/B/C + algorithm exploits)
│
├── references/                   ← المصادر الأصلية
│   ├── strategic_mind/          (16 طبقة + 38 عقلاً)
│   ├── whop_kit/                 (الخطة الأصلية + 22 ماستر)
│   └── session-ses_f7a3.md       (محادثة Claude الأصلية)
│
└── worklog.md                    ← السجل اليومي (مُحدَّث من جميع agents)
```

---

## 🧠 الـ 7 العقول — Multi-Mind Synthesis

كل عقل يشتغل بطريقته المميزة على نفس المهمة:

| العقل | الوزن | التخصص | متى يُفعّل |
|------|------|--------|-----------|
| **Sima Yi** | 22% | الصبر + اللعبة الطويلة + الإخفاء | خطة 12 شهر، MRR، حماية الحسابات |
| **Cao Cao** | 20% | التكامل + التوظيف | بناء النظام، توظيف open-source |
| **Guo Jia** | 15% | القراءة السريعة + القرار الحاسم | اختيار حملة اليوم |
| **Liu Bei** | 15% | العلاقات + السمعة + القيم | Halal gate + brand + audience trust |
| **Dong Zhuo** | 12% | التحكم باللوحة + حرب روائية | niche + timing + narrative |
| **Lu Bu** | 10% | الضربة القاضية | الحملة الواحدة الكبرى |
| **Yuan Fang** | 6% | استغلال فوضى + عمارة خداع | A/B/C hooks + bounded algorithm exploits |

التفاصيل: `AGENTS.md` + `docs/08_strategic_mind_activation.md`.

---

## 🛡️ الإطار الحلالي (5 خطوط حمراء)

1. **لا ربا** — Whop Treasury معطّل، لا BNPL، لا قروض.
2. **لا غش** — لا clickbait بلا وفاء، لا deepfake، لا voice clone.
3. **لا ضرر** — لا محتوى يضر المشاهد أو يخدع طيبعه.
4. **لا كسب حرام** — لا موسيقى محرّمة، لا موضوع محرم، لا غيبة.
5. **لا اعتداء على حسابات الآخرين** — لا تسرق قنوات، لا تنسخ بدون تعديل إبداعي جوهري.

Checklist كامل: `ETHICS.md` + `docs/06_halal_framework.md`.

---

## 🛠️ الـ Stack (ميزانية $0)

| الطبقة | الأداة | وظيفتها |
|--------|--------|---------|
| 1. Download | yt-dlp | تحميل الفيديوهات المصدرية |
| 2. Transcribe | faster-whisper | word-level timestamps |
| 3. Edit | FFmpeg + MoviePy | مونتاج + تأثيرات |
| 4. Captions | Whisper + drawtext | captions كارترايدج |
| 5. B-Roll | Pexels API + Pixabay + Stable Diffusion | لقطات داعمة |
| 6. Auto-edit | auto-editor + librosa | حذف سكتات + beat detection |
| 7. Halal Check | Python | 5-بند gate |
| 8. Score | Retention Scorecard | 6-بند gate |
| 9. Publish | TikTok API + IG Graph API + YT Data API v3 | نشر يومي |
| 10. Analytics | Python dashboard | KPIs يومي |
| 11. Whop | Whop CLI + bounty_submissions | تسليم لقطات |

تفصيل كامل + سكربتات: `TOOLS.md` + `scripts/` + `docs/07_open_source_stack.md`.

---

## 📊 KPIs (3 أشهر)

| المقياس | الهدف | الفحص |
|---------|-------|-------|
| View Rate | >70% (ممتاز 85%+) | analytics_dashboard.py |
| Retention @ 30s | >40% (ممتاز 60%+) | analytics_dashboard.py |
| Share Rate | >1.0% (ممتاز 1.7%+) | analytics_dashboard.py |
| Save Rate | >2.0% | analytics_dashboard.py |
| Posts/Day | 3-5 | daily_pipeline.sh |
| Whop Bounty submissions/week | 5-10 | submit_whop_bounty.py |
| MRR (شهر 3) | $300-$1000 | manual / Whop dashboard |
| MRR (شهر 12) | $5,000-$10,000 | manual / Whop dashboard |

---

## 🔐 الأمان

- لا تضع أي باسورد في ملف. استخدم API tokens فقط.
- TikTok/IG/YT/Whop tokens في `.env` (لا يُرفع لـ GitHub).
- بعد أول دورة نشر: غيّر كل tokens إن لزم.
- حسابات ثانوية أولاً، نقل للرئيسي عند ≥2x median.
- راجع `docs/06_halal_framework.md` §10 لأمان أعمق.

---

## 📖 المراجع

### المستودعات الأصلية:
- `https://github.com/geasas/strategic-advisor` — نظام STRATEGIC_MIND (16 طبقة + 38 عقلاً)
- `https://github.com/geasas/whop` — حقيبة GLM الأصلية (خطة + 22 ماستر)

### المصادر البحثية:
- `docs/01_whop_deep_dive.md` (61KB / 1040 سطر)
- `docs/02_viral_editing_toolkit.md` (48KB / 986 سطر)
- `docs/03_tiktok_algorithm.md` (61KB / 856 سطر)
- `docs/04_instagram_reels_algorithm.md` (94KB / 1272 سطر)
- `docs/05_youtube_shorts_algorithm.md` (78KB / 1255 سطر)
- `docs/06_halal_framework.md` (84KB / 952 سطر)
- `docs/07_open_source_stack.md` (33KB / 650 سطر)
- `docs/08_strategic_mind_activation.md` (1244 سطر)

إجمالي: **~480KB / ~7,000 سطر** بحث مُنظّم.

---

## 📝 الترخيص

MIT License — حر للاستخدام والتعديل مع الحفاظ على الإسناد.

## 🤝 المساهمة

افتح issue أو PR على GitHub. كل التعديلات يجب أن:
1. تحترم الإطار الحلالي.
2. تختبر بسكربتات `scripts/test_*.py`.
3. تُوثّق في `worklog.md`.

---

## 🎬 الكلمة الأخيرة

النظام ده **مش سكيلز ريموشن ضعيف** — هو **pipeline كامل** بمستوى احترافي:
- سكربتات Python مُختبَرة فعلياً (كلها PASS في smoke tests).
- أبحاث موثّقة بمصادر أولية (TikTok Newsroom, Meta for Developers, Google Developers, Whop blog).
- إطار حلالي مراجع من إسلام ويب + الإسلام سؤال وجواب + دار الإفتاء المصرية.
- نظام عقول متعدد يمنع التحيز الأحادي ويعطي 7 رؤى على كل قرار.

ابدأ من `MASTER.md`. خليك صبور. التزم بالقواعد. والـ $1000/شهر الهدف منطقي وقابل للتحقيق.

**Allah ywaf2ak. 🤲**
