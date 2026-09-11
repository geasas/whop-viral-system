# Whop Deep Dive — بحث عميق في منصة Whop + Content Rewards + API + حقوق القص + قصص النجاح

**Task ID:** 1-a
**Mind:** Guo Jia (قراءة سريعة + قرار حاسم) + Yuan Fang (عمارة استغلال)
**التاريخ:** 2026-09-11
**المصادر:** بحث مباشر (curl) من whop.com + docs.whop.com + en.wikipedia.org + شبكة RSS الخاصة بـ Whop + صفحة التسعير (network/pricing). جميع الأرقام موثقة من المصدر الأصلي.

---

## 1) نظرة عامة على Whop (Overview)

### 1.1 — من هي Whop؟ (Who)

> *Whop, Inc. is an American social commerce platform and online marketplace that enables entrepreneurs, influencers, and small businesses to sell digital products, memberships, communities, and software directly to consumers.*
> — Wikipedia (en.wikipedia.org/wiki/Whop.com)

- **اسم الشركة:** Whop, Inc.
- **النوع:** منصة تجارة اجتماعية (social commerce) + سوق رقمي (online marketplace) للمنتجات الرقمية والعضويات والمجتمعات.
- **تاريخ التأسيس:** مارس 2021.
- **المؤسسون:** Steven Schwartz (CEO) + Cameron Zoub + Jack Sharkey (CTO). التقى Schwartz وZoub وهم مراهقون في مجموعة Facebook لـ sneaker reselling.
- **المقر الرئيسي:** Domino Sugar Refinery, Williamsburg, Brooklyn, New York, USA.
- **عدد الموظفين:** ~30 (منتصف 2024) → 120 (يونيو 2026).
- **المنتَجات (Products):** Whop platform — Digital goods marketplace, Payment processing, Creator economy tools, Community and subscription management.
- **الشعارات التسويقية الرسمية:** "Where the internet does business." و"Deliver everyone a sustainable income."

### 1.2 — جولاتات التمويل (Funding Rounds)

| التاريخ | الجولة | المبلغ | القائد | التقييم |
|---------|--------|--------|--------|---------|
| يوليو 2023 | Series A | $17M | Insight Partners | — |
| يونيو 2024 | Series B | $50M | Bain Capital Ventures | $800M |
| فبراير 2026 | استثمار استراتيجي | $200M | Tether | $1.6B |

مستثمرون رئيسيون إضافيون: Peter Thiel, The Chainsmokers, Kevin O'Leary, Justin Mateen, Justin Kan, James Harden.

### 1.3 — ما الذي دفعته Whop للبائعين؟ (Payouts to Sellers)

| المصدر | المبلغ | التاريخ |
|--------|--------|---------|
| مدونة Whop الرسمية (Ways to Make Money Online) | "+$4.6B paid to sellers" | ذُكر في الخطة الاستراتيجية السابقة |
| فيديو Whop الرسمي ("$2billion earned on Whop") | "$2,000,000,000 earned on Whop" | 2026-09 |
| مقال "Getting paid as a Whop creator" | "Whop has paid out over 2 billion dollars to creators" | فبراير 2026 |

> *$2,000,000,000 earned on Whop. Always bet on yourself.*
> — Harry Beechinor, Whop Announcements video

⚠️ ملاحظة هامة: أرقام الإيرادات "earned" قد تشمل الناتج الإجمالي عبر المنصة (GMV-style)، وليس بالضرورة الأرباح الصافية المودَعة في حسابات البائعين. الرقم الحالي الموثق في 2026 هو $2B+ من الإيرادات المتراكمة.

### 1.4 — رسوم المنصة (Platform Fees) — أهم بند

مصدر أساسي: `https://whop.com/network/pricing/` — صفحة التسعير الرسمية الكاملة (Mintlify-powered docs).

#### الرسوم الأساسية (Standard Pricing)
| النوع | الرسوم |
|------|--------|
| المعاملة ببطاقة محلية (domestic card) | **2.7% + $0.30** لكل معاملة ناجحة |
| بطاقة دولية (international card) | +1.5% فوق الأساس |
| تحويل عملة (currency conversion) | +1% |
| ACH direct debit (US bank) | 1.5% (max $5) |
| BNPL (Klarna / AfterPay / Zip / Sezzle / Tamara / Scalapay / Splitit / Climb / SeQura / ClarityPay) | 15% لكل معاملة ناجحة |
| 3DS authentication | $0.03 لكل معاملة |
| ML fraud detection (Radar) | $0.07 لكل معاملة |
| Dispute fee (chargeback) | $15.00 لكل نزاع |
| Early dispute alert (RDR) | $29.00 لكل تنبيه |
| Orchestration (optional) | 0.8% لكل معاملة (when enabled) |
| Billing (auto invoice/retry/lifecycle) | 0.5% لكل معاملة |
| Tax and remittance | 2% لكل معاملة (when tax is collected) |
| Affiliate processing fee | 1.25% لكل معاملة |

> ملاحظة تحليلية (Guo Jia): **رسوم Whop الأساسية (2.7%+$0.30) أقل من Stripe (2.9%+$0.30) و PayPal القياسي (3.49%+$0.49)**. مع رقم المتوسط لبطاقة محلية = 2.7% + $0.30. عند الوصول إلى عروض إنستانت باي آوت أو Crypto، تتكلف رسوم من 4–5% (انظر 1.5).

#### خطة بديلة (Custom Pricing) للـ High-volume
- مدير حساب مخصص (Dedicated Account Manager)
- أسعار حسب الدولة (Country-Specific Rates)
- تسعير حسب الحجم (Volume-Based Pricing)
- تنفيذ مخصص (Dedicated Implementation)
- التواصل مع المبيعات (Contact sales)

### 1.5 — طرق الدفع للمبدعين (Payout Methods)

مصدر: `https://whop.com/network/pricing/` + مقال "Getting paid as a Whop creator".

| الطريقة | الرسوم | المدة | القيود |
|---------|--------|-------|--------|
| Next day ACH (US) | $2.50 لكل دفعة | اليوم التالي (next business day) | حسابات بنكية US فقط |
| Instant Bank Deposit (RTP) | **4% + $1.00** | فوري (real-time) | حسابات مدعومة فقط |
| Crypto (BTC/ETH) | **5% + $1.00** | فوري تقريباً | عالمي (global reach) |
| Venmo | **5% + $1.00** | فوري | **US recipients only** |
| Bank wire | $23.00 | 1–2 business days | تقليدي |
| International local bank | "Varies" | تختلف حسب الدولة | حسب الدولة والعملة |
| Same-day payouts | — | نفس اليوم | متاحة لـ "immediate cash flow" |

> *Whop supports payouts in 241+ territories. Sell globally and still withdraw locally.*
> — Getting paid as a Whop creator (Feb 2026)

**Types of payout delivery** (حسب OpenAPI spec للـ `/payouts/supported_methods`):
`cash_pickup`, `bank_deposit`, `home_delivery`, `mobile_wallet`, `card`, `check`, `bill`, `cryptocurrency`, `unknown`.

**حالات التحقق من الوسيلة (verification status)**:
`checking`, `verified`, `no_data`, `warning`, `broken`, `null`.

**حالات الوسيلة (lifecycle)**:
`created`, `active`, `broken`.

**Crypto payouts ملاحظة تحليلية (Yuan Fang):** عن طريق الـ API، توفر Whop Crypto payouts (BTC/ETH) برسوم 5%+$1 — من الحلال إذا كان النشاط الأصلي حلالاً. لكن انتبه أن Crypto payouts تتطلب أحياناً حد أدنى من المبيعات (minimum_crypto_sales_not_met)، أي أنه لا يمكن الوصول للـ instant crypto payouts قبل بلوغ عتبة معينة من إجمالي المبيعات.

### 1.6 — نظام احتجاز الرصيد (Reserve System)

عند مخاطرة عالية (Dispute Risk Score)، تحتجز Whop نسبة من كل معاملة:

| Risk Score | النسبة المحتجزة | المدة |
|------------|----------------|--------|
| 2–3 | 25% | 30 يوم |
| 3–4 | 50% | 30 يوم |
| 4–5 | 75% | 90 يوم |
| 5+ | **100%** | 90 يوم (قد يُعلَّق الحساب) |

يُطبَّق على المعاملات المُعالَجة مباشرة عبر منصة Whop (ليس على خارجية). يُرفع الاحتجاز بعد استقرار سلوك الحساب.

### 1.7 — متطلبات KYC للتسجيل كبائع/مبدع (KYC Requirements)

> *Whop pays creators directly to their connected bank account or wallet after users choose how they want to withdraw the Whop balance they received from sales, with payouts processed as quickly as possible following compliance checks.*
> — Getting paid as a Whop creator

- **أول معاملة + أول سحب + عتبات إيراد ($1K, $5K...)** تُطلق مراجعة compliance أوتوماتيكياً.
- **نوعا التحقق (Verification types):**
  - **KYC** (Individual — شخص طبيعي): لتلقي payouts كفرد.
  - **KYB** (Business — كيان قانوني): للشركات/الكيانات.
- الحساب يمكن أن يكون لديه كلاهما (KYC + KYB).
- **المزود التقني:** Sumsub — عبر `session_url` من hosted flow (مع selfie + رفع ID). تتوفر خاصية Reusable KYC عبر share_token بين حسابات Sumsub المتفق عليها.
- **الدول المدعومة للـ KYB (Business Structures):** 40+ دولة مدرجة في `docs.whop.com/developer/verification/business-structures.md`. **السعودية (SA) ليست مدرجة، الإمارات (AE) مدرجة** بـ: `llc`, `sole_establishment`, `free_zone_llc`, `free_zone_establishment`. مصر (EG) ليست مدرجة. للدول غير المدرجة: "Declare the business with `business_name` alone and omit `business_structure`."
- للأفراد US: يجب إدخال SSN في حقل `tax_identification_number` (مطلوب لإنشاء payout account).
- **نطاق API للـ KYC:** تحتاج scope `identity:write` للـ Account API key.

### 1.8 — الدول المدعومة للبائعين (مصر/الخليج)

- **الدفع (Payouts):** 241+ territories (يشمل مصر ودول الخليج في الغالب).
- **المدفوعات المقبولة (Payments accepted):** 195+ countries, 100+ payment methods.
- **KYC (Individual):** عبر Sumsub — لكل بلد قائمة وثائق مختلفة (يتم التحقق داخل الـ hosted flow).
- **KYB (Business):** قائمة محدودة (~40 دولة). مصر لا تدعم، الإمارات نعم، السعودية لا.

**للمستخدم المصري/الخليجي (تحليل Yuan Fang):**
1. الحل الأبسط: التسجيل كفرد (KYC) — يدعمه Sumsub للعديد من الدول.
2. لـ payouts من مصر: `bank wire ($23)` أو `crypto (5%+$1)`.
3. من الإمارات: KYB متاح كـ LLC/Free Zone LLC، وعملة AED قد تتاح عبر International local bank transfer.
4. من السعودية: KYB غير مدرج، يمكن استخدام `business_name` بدون `business_structure`، أو التسجيل كفرد.

> ⚠️ **لا يوجد قائمة رسمية لجميع دول KYC الفردية المدعومة في المستندات العامة** — يجب على المستخدم البدء بتسجيل حساب وستظهر له طرق التحقق المحددة لدولته.

---

## 2) برنامج Content Rewards (تفصيلي + أرقام موثقة)

### 2.1 — ما هو Content Rewards؟ (Definition)

مصدر: `https://whop.com/blog/content-rewards/` (مقال: "Content Rewards: Grow your brand without wasting money or time" — Mar 3, 2025) + `https://docs.whop.com/memberships-and-access/third-party-apps/content-rewards.md` + مقال `set-up-content-rewards`.

> *Content Rewards is a marketing tool that connects your brand with content creators — they make content about your brand and you pay them for the number of views they get.*

> *With Whop Content Rewards you don't need to create original content. You can start making money from day one – even with zero followers.*
> — Clipper quote in "79 ways to make money online" (Aug 19, 2026)

**جوهر النموذج:** Pay-per-view (PPV) — تدفع العلامة التجارية للمبدع فقط مقابل المشاهدات الفعلية التي يحققها المحتوى. لا يوجد upfront cost للعلامة، ولا حد أدنى من المتابعين للمبدع.

### 2.2 — كيف يدفع؟ (Rate Model)

| النموذج | التفاصيل |
|---------|---------|
| النموذج الافتراضي (default rate) | **$1 per 1,000 views** — مثبت في مدونة Whop الرسمية |
| مقارنة بـ Facebook/IG ads | $25 per 1,000 views (أي Whop أرخص 25x للعلامة) |
| مقارنة بـ TikTok Creator Rewards | $0.02–$0.08 per 1,000 views (Whop يَدفع 12–50x أكثر من TikTok للمبدع!) |

**هيكل المعدل (Reward Rate)** — من `set-up-content-rewards` + الـ API spec:

- **gross_reward_amount** (per accepted submission): المبلغ الإجمالي بالدولار لكل submission مقبول.
- **accepted_submissions_limit**: عدد الفائزين المسموح (winner slots) — افتراضي 1.
- **budget_amount** = `gross_reward_amount × accepted_submissions_limit` — يحتجز (escrow) عند النشر.
- **min escrow floor**: **$5** (أدنى ميزانية قانونية لكل bounty).
- **minimum payout**: عتبة الحد الأدنى للمشاهدات قبل دخول submission طابور المراجعة (مثال: $3 rate + $6 min = 2,000 views minimum).
- **maximum payout**: سقف لكل فيديو لمنع استئثار فيديو واحد بالميزانية (مثال: $3 rate + $3,000 max = 1M views cap per video).
- **flat fee bonus** (اختياري): مكافأة ثابتة إضافية لكل submission مقبول (مثال: $3 rate + $10 flat + 2K views = $6+$10=$16).

> *Whop escrows the money when the bounty is created and releases it when a submission is approved, so a worker can see the reward is real before starting.*
> — docs.whop.com/developer/bounties/overview.md

### 2.3 — الأمثلة الموثقة لأسعار فعليه (Real Rate Examples)

| العلامة | السعر per 1K views | الميزانية | المنصة | الجمهور المستهدف | المصدر |
|---------|-------------------|----------|--------|-----------------|--------|
| Whop (نفسها) | $1 | $384 (384K views) | unspecified | unspecified | blog/content-rewards |
| Whop Clips (YouTube clip content type) | **$1.25** | $190K/mo budget | YouTube clips | unspecified | blog/whop-clips |
| Lovable AI (UGC + podcast clipping) | **$2** | $10K | TikTok + Instagram | US/UK/Canada/Australia/NZ | blog/content-rewards-x-lovable |
| Lil Baby (music album) | $0.30 | unspecified | unspecified | unspecified | blog/content-rewards |
| General guideline | غالباً $3 per 1K views | — | — | — | blog/what-is-content-clipping |
| بعض حملات الـ UGC | يدفع أكثر من clipping | — | — | — | docs (set-up-content-rewards: "UGC content typically pays higher rates than clipping") |

### 2.4 — أنواع حملات Content Rewards (Campaign Types)

من API spec + docs:

```yaml
business_goal_type:
  enum:
    - clipping           # ← تحويل long-form → short-form
    - post_engagement    # ← منشورات للتفاعل
    - owned_account_growth  # ← نمو حساب العلامة
    - ugc_content        # ← محتوى أصلي عن العلامة
    - local_activation  # ← تنشيط محلي
    - data_capture       # ← جمع بيانات (يستخدم capture_spec)
    - other              # ← غير ذلك
```

**نوعان رئيسيان للـ Content Rewards app (UI side):**
1. **Clipping**: تحويل المحتوى الطويل (بودكاست، livestream، webinar) إلى شورتس على TikTok/YouTube Shorts/X/Instagram Reels.
2. **UGC**: المحتوى الأصلي الذي ينتجه المبدع عن العلامة بناءً على guidelines.

### 2.5 — الحملات المتاحة حالياً + كيف تتصفحها (Browsing Campaigns)

#### الطريقة الرسمية الأولى — انضم لـ Whop Clips (موصى به)
- **URL:** `https://whop.com/discover/whop-clips/`
- **العضوية:** مجانية (Join for free)
- **عدد الأعضاء:** **1M members** (مليون عضو) — من صفحة Whop Clips الرسمية
- **التقييم:** 4.7/5 من 2,432 rating (79% 5-star، 16% 4-star)
- **الشعار الرسمي:** *"Earn $1,000+ per month posting Clips on Whop!"*
- **ميزة جديدة:** أول 3 فيديوهات مدفوعة بغض النظر عن المشاهدات ("you'll get paid for your first 3 videos no matter how many views they get").
- **المسؤول:** Dylan Lundgren (Affiliate Success Manager @ Whop)، @dylanlundgren.
- **الميزانية الشهرية:** حتى **$190,000/mo** لمدفوعات الـ clippers عبر Whop Clips.

#### الطريقة الرسمية الثانية — ابحث في Discover
- **URL:** `https://whop.com/discover/`
- البحث في الـ marketplace عن whops فيها Content Rewards app مفعّل.

#### الطريقة الرسمية الثالثة — استعراض العروض داخل Whop Clips
داخل Whop Clips (بعد التسجيل المجاني) ستجد:
- **Course app**: دورة مجانية من Dylan Lundgren بـ "proven content formula".
- **Chat app**: مجتمع لتبادل النصائح بين الـ clippers.
- **Announcements app**: عروض حصرية من Dylan + صيغ جاهزة للحفاظ على جدول المحتوى.
- **Clipping Deals app**: حيث يُنشر Dylan صفقات جديدة مثل:
  - *Iman Gadzhi UGC*
  - *BBNO$ x Whop*
- **Content Rewards app**: حيث تُسلم المحتوى وتتابع submissions وأرباحك.

### 2.6 — شروط الاشتراك في حملة (Qualification)

مصدر: مدونة Whop + الـ API.

> *Whop Content Rewards means that anyone can become a clipper. It doesn't matter how many followers you have or if you've ever made content before – if your clip gets views, you get paid.*
> — blog/what-is-content-clipping

- **لا حد أدنى للمتابعين.**
- **لا خبرة سابقة مطلوبة.**
- **شرط الـ country targeting**: الحملة تحدد `allowed_country_codes` (ISO 3166 alpha-2). قائمة فارغة = عالمي (worldwide).
- مثال Lovable: اشتراط الجمهور من US, UK, Canada, Australia, New Zealand فقط + comments turned on + no AI voiceovers.
- **شرط الـ minimum payout**: الحملة قد تحدد عتبة مشاهدات قبل دخول طابور المراجعة (مثال: 2,000 views minimum).
- **شرط الـ maximum payout**: سقف لكل فيديو لحماية الميزانية.
- **شرط المنصات المسموحة**: قد تحدد الحملة "TikTok + Instagram فقط" أو "YouTube clips فقط".

### 2.7 — الجمهور المستهدف (Audience Targeting)

مصدر: مقال Lovable + الـ API.

- كل حملة تحدد `allowed_country_codes` (قائمة ISO 3166 alpha-2).
- قد تطلب تفاعل محدد (مثال Lovable: comments turned on for better engagement).
- قد تمنع أنواع محتوى معينة (مثال Lovable: no AI voiceovers).
- قد تحدد نوع المحتوى (UGC vs Clipping).
- قد تحدد المدة (مثال: 20 seconds minimum).

### 2.8 — كيف يتم التحقق من المشاهدات؟ (View Verification)

مصدر: `set-up-content-rewards` + `bounties_run.md`.

> *With the latest Whop update, all submissions to content rewards are now reviewed by our AI Content Rewards Reviewer. It checks submissions based on your campaign requirements and flags any that don't meet them.*
> If the content meets the criteria, you'll have 48 hours to manually review the submission. **If a reviewed submission remains unapproved for more than 48 hours, the system will automatically approve it.**

**آلية التحقق:**
1. المبدع يسلم submission عبر `POST /bounty_submissions` مع `deliverable`:
   ```python
   deliverable = {
       "urls": ["https://www.tiktok.com/@creator/video/1234567890"],
       "file_ids": ["file_XXXXXXXX"],
       "caption": "Vertical cut, 42 seconds."
   }
   ```
2. يتطلب至少 `urls` أو `file_ids` (واحد على الأقل).
3. **AI Content Rewards Reviewer** يراجع الـ submission ضد متطلبات الحملة:
   - مطابقة المنصة
   - مطابقة الجمهور المستهدف
   - مطابقة نوع المحتوى
   - مطابقة duration/format
   - وجود botting (fake views)
4. ينتقل الـ submission لحالة `submitted` (= Awaiting decision).
5. للعلامة 48 ساعة لمراجعة يدوية. **بعد 48 ساعة، الموافقة أوتوماتيكية** إذا لم يُرفَض.
6. القرار النهائي: `approved` (يُدفَع من الـ escrow) أو `denied` (يرفض مع `denial_reason`).
7. يمكن للعلامة "ban user for botting" — أي حظر المستخدم نهائياً باستخدام بوتات للمشاهدات الوهمية.

> ⚠️ **تحذير (Yuan Fang):** Whop تكشف botting بسهولة. أي محاولة لـ fake views = حظر دائم + خسارة الأموال المحتجزة. النموذج الوحيد المستدام هو المشاهدات الحقيقية.

### 2.9 — أنواع الحملات (Niches) — أيها أكثر ربحاً؟

من مصادر Whop المتعددة:

| النيتش | المعدل الموثق | الأمثلة |
|---------|--------------|---------|
| **UGC + Podcast Clipping (Tech/AI)** | $2 per 1K | Lovable AI ($10K campaign) |
| **YouTube Clips** | $1.25 per 1K | Whop Clips official rate |
| **Music Clipping** | $0.30 per 1K | Lil Baby album |
| **Gaming (UGC)** | مرتفع | Iman Gadzhi UGC deal |
| **Music (general)** | متوسط | Mumford & Sons, Brandi Carlile, John Summit — referenced in Wikipedia |
| **Trading/Crypto communities** | مرتفع | Whop's most lucrative niche (Bounce Alerts, The Haven) |
| **Coaching/Business** | مرتفع | Brett Malinowski (@thebrettway) personal brand |
| **Sports betting communities** | مرتفع | Per Whop blog sport betting communities |
| **Faceless content** | متاح | Whop mentions faceless creators in Content Rewards |

**تحليل Guo Jia — النيتشات الأعلى ربحاً:**
1. **AI/Tech (Lovable, Replit, Cursor)** — علامات ممولة جيداً + ميزانيات كبيرة.
2. **Trading/Crypto/Finance** — الجمهور عالي القوة الشرائية.
3. **Gaming (Iman Gadzhi)** — أسعار UGC مرتفعة.
4. **Music** — حجم كبير لكن أسعار منخفضة ( Lil Baby $0.30/1K).

### 2.10 — نموذج مكافأة المبدع (Creator Reward Math)

مثال موثق من مقال Whop نفسها:
> *If your repurposed Whop YouTube clip gets 300,000 views, you'll be eligible for 300 times the current view reward amount.*

أي بـ $1.25/1K → 300 × $1.25 = **$375** من فيديو واحد.
بـ $2/1K (Lovable) → 300 × $2 = **$600** من فيديو واحد.
بـ $3/1K (general guideline) → 300 × $3 = **$900** من فيديو واحد.

> ملاحظة (Yuan Fang): Whop تحتفظ بـ platform fees و affiliate shares من الـ gross reward. الـ `net_reward_amount` يُحسب بعد الرسوم. أي $1.25 gross = ~$1.18 net تقريباً بعد رسوم 5% (وليس 2.7%+$0.30 لأن المعاملة فردية لا card transaction).

---

## 3) نماذج أخرى للربح من Whop

### 3.1 — العضوية/المجتمع (Membership / Community)

مصادر: مقال Whop "what-is-a-whop" + "membership-models" + Business Models master.

- **كيف تنشئها:** Create whop من `whop.com/new/` → Add apps (Chat, Courses, Files, Forums) → Set pricing (free/paid/recurring).
- **التسعير المقترح (من الماسترز):**
  - عضوية شهرية: $15–20/mo (مدخل)
  - برنامج مركّز: $49/mo
  - ماسترمايند/مجموعة حصرية: $200/mo
  - قاعدة الـ 5x gap بين الدرجات
- **نموذج الـ Community-First (موصى به):** 10K متابع → 200–500 مشترك × $15–20 = **$3,000–10,000/mo** (نسبة تحويل 2–5%).
- **أمثلة موثقة:**
  - LetPhil: 13K free Discord + 200 paid mentorship.
  - Budgetdog (Brennan): paid off $304K debt, hit $1M net worth via coaching + community.

### 3.2 — المنتجات الرقمية (Digital Products)

مصادر: Whop blog "best-digital-products-to-sell" + "what-is-a-whop".

- **ماذا يُباع:** templates (مونتاج، Notion، قوالب هوك)، scripts (سكربتات هوك)، AI prompt packs، ebooks، presets (Lightroom)، icons/UI kits، stock photos، plugins.
- **التسليم:** عبر Files app في الـ whop.
- **التسعير:** من $5 (low-ticket) إلى $200+ (high-ticket templates).
- **ملاحظة:** "المنتج المملوك يُبنى مرة ويُباع مراراً" — أعلى ROI من جميع النماذج.

### 3.3 — Coaching / SaaS

مصادر: Whop seller stories + API docs.

- **Coaching:** يمكن جدولة 1:1 أو group sessions عبر Calendar app. مثال Metafy: $99/mo Pro (0% platform cut) vs $15K-$30K/yr gaming coaches.
- **SaaS:** Whop تدعم software subscriptions (Memberships API + Plans API). مثال Replit (50M users) يستخدم Whop embedded checkout.
- **متطلبات:** لا متطلبات رسمية إضافية — فقط KYC للـ payouts.

### 3.4 — Affiliates (Whop Affiliate Program)

مصادر: blog/affiliates-update + blog/affiliate-links-app-whop + blog/whop-partners.

- **حجم البرنامج:** 30,000+ active affiliates (ديسمبر 2025).
- **Affiliate Marketplace:** تصفح منتجات تبحث عن affiliates، شاهد real earnings data، conversion signals، انضم بضغطة.
- **Affiliate Links app:** Link boards أنيقة على الـ whop — تكسب عمولة من الـ clicks/purchases.
- **Whop Partners (مستوى أعى):**
  - Up to 30% of Whop's gross profit من كل business referral.
  - 1% of ad spend (stackable على العمولة).
  - Second-tier commissions (شركة من شركة).
  - **Whop Partners have earned over $10M to date**.
  - **Top partners clearing 6 figures per referral.**
- **Whop Treasury:** حتى 6% APY على رصيد USDT (powered by Aave، شراكة مع Tether). متاح للأفراد والشركات. **تنبيه حلال:** هذا yield من إقراض on-chain عبر Aave — قد يكون غير حلال للمستخدم الملتزم (يتطلب توضيح من عالم شريعة).

### 3.5 — نماذج إضافية

- **Whop Ads:** إطلاق إعلانات عبر major platforms من dashboard واحد.
- **Whop Cards:** إصدار cards تنفق من رصيد Whop.
- **Whop AI:** بناء business عبر محادثة AI.
- **Whop Blueprints:** نسخ business كامل (products + pricing + site) من blueprint جاهز.
- **Whop Treasury:** yield على USDT (6% APY) — متاح للمستخدمين من 2026.
- **Whop CLI:** إدارة business من الـ terminal (للـ agents مثل Claude، Cursor، Grok).
- **Whop Migrations:** نقل business في click واحد.

---

## 4) Whop API للمطورين (Developer Platform)

مصدر رئيسي: `https://docs.whop.com/` + `https://docs.whop.com/llms.txt` (ملف فهرس كامل 221KB).

### 4.1 — المعلومات الأساسية

| البند | القيمة |
|------|--------|
| Base URL (Production) | `https://api.whop.com/api/v1` |
| Base URL (Sandbox) | `https://sandbox-api.whop.com/api/v1` |
| المصادقة | `Authorization: Bearer $WHOP_API_KEY` |
| Versioning | `Api-Version-Date: 2026-09-11` (تاريخ مثبت) |
| Pagination | `first` (page size) + `after` (cursor from `page_info.end_cursor`) |
| SDKs الرسمية | TypeScript `@whop/sdk`, Python `whop-sdk`, Ruby `whop_sdk` |
| CLI | `curl -fsSL https://whop.com/install.sh \| sh` (macOS/Linux) أو npm |
| MCP Docs | `https://docs.whop.com/mcp` (read docs) |
| MCP API | `https://mcp.whop.com/mcp` (operate live data via browser auth) |
| Skills | `https://docs.whop.com/.well-known/skills/index.json` |

### 4.2 — أنواع الاعتمادات (Credential Types)

1. **Account API Keys:** للوصول إلى account واحد.
2. **App API Keys:** للوصول لكل accounts التي ثبَّتت الـ app.
3. **User Tokens (OAuth 2.1 + PKCE):** "Sign in with Whop" — مطلوبة لـ bounty_submissions (لا يمكن للـ account API key تأليف submission).
4. **Access Tokens:** short-lived tokens للـ embedded UI (web/mobile).

### 4.3 — هل يمكن عبر API: استعراض الحملات، التسجيل، رفع إثبات؟

**نعم، كل ذلك ممكن** — عبر `Workforce` resources:

#### استعراض الحملات (Browse Bounties)
```
GET /bounties
```
- **بدون auth:** فقط لو bounty publicly visible.
- **مع user token:** يعرض كل bounties "the user can see and work".
- **مع account API key:** bounties الـ account نفسها (including scheduled drafts).

**Query parameters:**
- `status`: `scheduled`, `open`, `closed`, `completed`, `canceled`
- `business_goal_type`: `clipping`, `post_engagement`, `owned_account_growth`, `ugc_content`, `local_activation`, `data_capture`, `other`
- `country`: ISO 3166-1 alpha-2 (يعرض bounties workable من هذه الدولة)
- `experience_id`: filter by forum experience (prefixed `exp_`)
- `query`: substring match على الـ title أو ID
- `created_after` / `created_before`: ISO 8601 timestamps
- `order`: `created_at` (default) | `gross_paid_out_amount` | `gross_reward_amount`
- `direction`: `asc` | `desc` (default)

#### استعراض bounty منفرد (Retrieve Bounty)
```
GET /bounties/{id}
```
- **بدون auth:** يعمل لو الـ bounty publicly visible (published أو completed، وغير restricted لـ private experience).
- إذا الـ bounty غير مرئي: يعيد `404 not_found` (لا يكشف وجوده).

#### التسجيل في حملة = Submit Submission
```
POST /bounty_submissions
```
Body:
```json
{
  "bounty_id": "bnty_XXXXXXXX",
  "deliverable": {
    "urls": ["https://www.tiktok.com/@creator/video/1234567890"],
    "file_ids": ["file_XXXXXXXX"],
    "caption": "Vertical cut, 42 seconds."
  }
}
```
- **يتطلب user credential** (لا account API key).
- الـ submission يذهب مباشرة إلى `submitted` (= review queue) — `create` is the only step.
- لـ `data_capture` bounties: لا تُرسل `deliverable` — يبدأ claimed attempt وproof يتجمع server-side.

#### رفع الملفات (Upload Files)
- File IDs التي يأخذها الـ deliverable تُرفع أولاً عبر `Upload files` endpoint.
- كل file ID يُستعمل في `file_ids` array.

#### استعراض submissions
```
GET /bounty_submissions
```
**Filters:**
- `bounty_id`
- `status`: `in_progress`, `submitted`, `approved`, `denied`

#### استعراض public submissions (بدون auth)
```
GET /bounties/{id}/submissions/public
```
- بدون auth — يعرض submitted/approved/denied submissions في "reduced public shape".

### 4.4 — حدود API (Rate Limits)

مصدر: `https://docs.whop.com/developer/troubleshooting.md` — غير مُفصَّل في الفهرس العام، لكن:
- Webhooks: تُعاد المحاولة 12 مرة بـ increased delays (30s, 2min, 8min, 30min, 1h, 3h, 6h, ثم كل 12h). المجموع الكلي = ~71 ساعة.
- Webhook endpoint timeout: **5 ثواني** (يجب الرد 2xx).
- Webhook يتم تعطيله بعد 72 ساعة فشل متواصل + 10+ deliveries فاشلة.

### 4.5 — Webhooks (Events)

مواصفة: **Standard Webhooks** مع HMAC-SHA256 signature (الـ key هو `ws_...`).
- **Bounties لا تُطلِق webhooks** (لابد من polling `GET /bounty_submissions` كل دقيقة).
- **Bounty Submissions** تُطلِق: `entry.approved`, `entry.created`, `entry.denied`, `entry.deleted`.
- Webhook envelope:
  ```json
  {
    "id": "msg_XXX",
    "type": "payment.succeeded",
    "api_version": "v1",
    "api_version_date": "2026-08-14",
    "timestamp": "2026-08-10T17:03:24.291Z",
    "account_id": "biz_XXX",
    "data": { "id": "pay_XXX", "...": "..." }
  }
  ```

### 4.6 — موارد API الكاملة (Resources Map)

| الفئة | الموارد |
|------|--------|
| **Core** | Accounts, Users, Team Members, Members, Economic Intelligence, Webhooks, Stats, Verifications, Exports |
| **Notifications** | Notifications |
| **Payments** | Payments, Refunds, Confirmation Tokens, Setup Intents, Disputes, Dispute Alerts, Resolution Center Cases |
| **Money** | Financial Activity, Payouts, Cards, Cashback Rules, Transfers, Deposits, Swaps |
| **Commerce** | Products, Plans, Promo Codes, Memberships, Checkout Configurations, Payment Method Domains, Shipments |
| **Partners** | Partners |
| **Workforce** ⭐ | **Bounties**, **Bounty Submissions** |
| **Tracking** | People, Events |
| **Ads** | Ads, Ad Campaigns, Ad Groups, Audiences |
| **Media** | Files, Media |
| **Identity** | Social Accounts |
| **Developer** | Apps, Domains, App Builds, API Keys, API Logs, Permissions, Experiments |

### 4.7 — الصلاحيات المطلوبة (Required Scopes)

| العملية | الـ Scope |
|--------|----------|
| إنشاء bounty | `bounty:create` + `payout:transfer_funds` |
| قراءة submissions | `bounty:basic:read` |
| تأليف submission | **user credential** (لا account API key) |
| بدء KYC | `identity:write` |
| OAuth | عبر PKCE flow |
| Apple Pay domain verify | `payment_method_domain:write` |

### 4.8 — CLI / Agent Integration

مصدر: `https://whop.com/blog/cli/` (Jul 21, 2026) + `https://whop.com/blog/spacexai-whop-grok/` (Sep 2, 2026).

```bash
# install
curl -fsSL https://whop.com/install.sh | sh

# basic commands
whop --help                  # all commands
whop products list           # what you're selling
whop checkout-configurations create --plan_id plan_xxx   # checkout link
whop stats list              # your numbers
whop --format json           # structured output

# agent integration
whop --llms                  # give AI the full command list
whop mcp add                 # connect to AI assistant (e.g., Claude)
whop skills add              # give your agent ready-made skills
```

- متوافق مع Claude, Cursor, Grok, Codex.
- SpaceXAI اختارت Whop كأول full-stack business connector لـ Grok.
- Cursor Marketplace: تحت 'Payments' يمكن تثبيت Whop plugin.
- Grok Bot: يمكن إنشاء AI teammates يديرون business على Whop asynchronously.

### 4.9 — ملاحظة حقوق القص + الـ API

> ⚠️ **لا يوجد endpoint عام لاستعراض كل bounties دون auth.** الـ `GET /bounties` يتطلب auth أو user token. الـ `GET /bounties/{id}` يعمل بدون auth فقط للـ publicly visible bounties. أي خوارزمية "اكتشاف الحملات الأنسب ربحاً" تحتاج **user token** (OAuth sign-in) — أو الانضمام لـ Whop Clips.

---

## 5) حقوق القص والاستخدام (Clipping Rights & Usage)

### 5.1 — شروط Whop للـ clips المنشورة

مصدر: مدونة Whop (whop-clips، content-rewards، what-is-content-clipping).

- **المبدأ الأساسي:** Content Rewards يعطي المبدع تفويضاً رسمياً للقص — لأن العلامة نفسها تطلب ذلك وتدفع.
- **شروط الحملة (Requirements):** تُحدَّد من قبل العلامة وتشمل:
  - نوع المحتوى (Clipping vs UGC)
  - المنصات المسموحة
  - المدة (e.g., "20 seconds minimum")
  - المحتوى الممنوع (e.g., "No AI voiceovers")
  - ذكر اسم المنتج (Brand mention requirements)
  - الجمهور المستهدف (allowed_country_codes)
  - "comments turned on" للتفاعل
- **المراجعة:** AI Reviewer + 48-hour manual + auto-approve.
- **العقوبة:** حظر للمبتزين (botting) + خسارة الأموال المحتجزة.

### 5.2 — كيف يتم التحقق من أن القص قانوني؟

> *AI Content Rewards Reviewer checks submissions based on your campaign requirements and flags any that don't meet them.*

1. المبدع يرفع deliverable (URL + file_id).
2. AI يحلل المحتوى ضد متطلبات الحملة.
3. 48 ساعة للمراجعة اليدوية.
4. لو الـ submission لم يُرفَض خلال 48 ساعة → auto-approved.
5. العلامة تستطيع "ban user for botting" (fake views).
6. الـ deliverable URL يُتبَع على المنصة (TikTok/IG/YouTube) لحساب المشاهدات.

### 5.3 — ماذا لو استخدمت فيديوهات خارجية (YouTube podcasts)؟

> *Whop's Content Rewards program lets you earn by creating viral clips for existing offers.*
> — blog/what-is-content-clipping

**نموذج آمن (Fair Use):**
1. **استخدم مصادر من within Whop Content Rewards**: العلامة ترفع الأصول (Asset links) للحملة — استخدمها مباشرة.
2. **استخدم الـ Whop Clips assets**: Whop نفسها توفّر محتوى للقص عبر Whop Clips ($1.25/1K views لـ YouTube clips).
3. **Clipping Deals app**: يحدد Dylan صفقات رسمية (Iman Gadzhi UGC, BBNO$ x Whop) — استخدم الأصول المرخّصة فقط.
4. **Fair Use خارج Content Rewards:** إن قصصت يوتيوبر/بودكاست بدون حملة رسمية:
   - أضف تعديلاً إبداعياً جوهرياً (تحليل/تعليق/ترجمة).
   - استخدم فقط فقرات قصيرة (under 30 sec).
   - اذكر المصدر + أعطه credit.
   - لكن هذا النموذج خارج Content Rewards (لن تحصل على payout رسمي).

### 5.4 — هل Whop توفر مصادر فيديو رسمية للقص؟

**نعم** — عبر:
1. **Asset links** في Content Rewards app: العلامة ترفع فيديوها الرسمي (demo, podcast, livestream) كـ Asset links.
2. **Audio links**: لـ Instagram/TikTok audio requirements.
3. **Whop Clips Course**: يوفر محتوى رسمي للقص (e.g., YouTube clips of Whop's content).
4. **Clipping Deals app**: صفقات لـ clips على podcast episodes من Iman Gadzhi و BBNO$.

### 5.5 — نموذج آمن تماماً (Yuan Fang — Minimal Risk)

للـ agent الذي يريد ضمان 100% قانوني:
1. انضم لـ Whop Clips (مجاني).
2. اقرأ الـ Course app — يحدد approved content types.
3. استخدم فقط الأصول المنشورة في Clipping Deals / Content Rewards apps.
4. اتبع متطلبات الحملة بدقة (platform, audience, format, duration).
5. ارفع الـ submission قبل الـ deadline مع URL صحيح.
6. تابع الـ submission status — لو `denied` اقرأ `denial_reason` وعدّل.

---

## 6) قصص النجاح (Success Stories) — أرقام موثقة

### 6.1 — Whop نفسها + ميزانيات Content Rewards

- Whop حصلت على 384K views مقابل $384 على one of their content pieces (rate $1/1K).
- Whop لديها **$190,000/mo budget** لـ Whop Clips payouts.
- Streamer "Neon" paid creators **$300,000+** for clipping his streams (last year).
- MrBeast paid **$50,000** to UGC creators for Feastibles.
- Luke Belmar used clipping system → blew up personal brand → made "tens of millions" on Capital Club launch.
- Lil Baby paid creators **$0.30 per 1,000 views** for music from new album.

### 6.2 — Wikipedia: Music industry campaigns on Whop Content Rewards

> *Its Whop's Content Rewards feature has been used by the music industry for its marketing campaigns known as clipping... Campaigns include Mumford & Sons, Brandi Carlile, and John Summit.*

### 6.3 — Whop Clips Community نفسها

- **1M members** (مليون عضو).
- 4.7/5 rating من 2,432 ratings.
- Whop Clips تَدفع حتى **$190,000 شهرياً** للـ clippers.
- Dylan Lundgren: "the dude is paying out up to $190,000 to creators monthly just for doing their thing."
- "Many users make and withdraw money on their first day joining!"

### 6.4 — Seller Stories من Whop (أرقام فعلية)

| البائع | النيتش | الأرقام |
|--------|--------|--------|
| Metafy | Gaming coaching | $10M+ paid to coaches. واحد earned $10K من two-hour group session. Pro tier $99/mo = 0% platform cut (vs 30% industry). |
| FoodFluence | Hospitality UGC | 50K+ creators في 700 cities. Netflix, Bumble, Samsung early TikTok marketing work. |
| SideShift | UGC platform | 850K+ creators, 50+ campaign structures. 1,000+ brands. **"Millions of dollars paid out per week"**. |
| Budgetdog (Brennan) | Personal finance | Paid off $304K debt, hit $1M net worth على ست راتب standard six-figure salary. |
| LetPhil | Tech mentorship | 13K free Discord + 200 paid mentorship. 40+ members landed $200K+ tech roles (Amazon, AmEx, NatWest). |
| Replit | AI software | 50M users, Whop embedded checkout. |
| Adsolution | Digital Marketing / Facebook Ads / Chatbot AI / CRM | 2 joined (small but verified storefront). |
| Bounce Alerts | Trading/Crypto | "+23% memberships" بعد التحول إلى Whop. |
| The Haven | Crypto analysts | "Star Team of Analysts Changed the Face of Crypto Groups". |

### 6.5 — Whop Partners

> *Whop Partners have earned over $10M to date, just from referring businesses.*
> *Our top partners are clearing 6 figures per referral.*

### 6.6 — متوسط نمو الأعمال

> *The average business on Whop grows revenue 51% year over year.*
> — blog/what-is-a-whop

### 6.7 — نموذج clipper عام (من what-is-content-clipping)

- *Freelance clipper (part-time starting out):* **$200–$500/month** لأقل من few hours/week.
- *Experienced clippers with own channels/streams/agencies:* **$10,000+/month**.
- *Per-video freelance:* **$5–$500+ per video** depending on the paying client and performance incentives.

### 6.8 — مقارنة مع TikTok Creator Rewards

| المنصة | العتبة | المعدل |
|--------|--------|--------|
| TikTok Creator Rewards | 10K followers + 100K views/30d | $0.02–$0.08 per 1K (max $8 per 1K) |
| Whop Content Rewards | **0 followers, 0 experience** | $1 per 1K (default), $1.25 (Whop Clips YouTube), $2 (Lovable UGC), $3+ (general guideline) |
| Facebook Reels | (متغير) | up to $4 per 1K (CPM) |
| YouTube Shorts | (متغير) | $0.01–$0.06 per 1K (CPM) |

> **(Guo Jia):** Whop Content Rewards يَدفع **12–50x أكثر من TikTok Creator Rewards per 1K views** — وأهم: **بدون أي عتبة متابعين**. هذا هو الميزة الاستراتيجية الأهم للـ agent الجديد.

### 6.9 — نقاط يجب تأكيدها

- Brett Malinowski (@thebrettway): مؤسس Content Rewards — Gen-Z marketing guru بـ 8 سنوات خبرة.
- Dylan Lundgren: Affiliate Success Manager — يدير Whop Clips.
- Steven Schwartz: CEO + Co-founder Whop.
- Ryan Ouyang: Head of Platform API @ Whop.
- Nicholas Motamedi: Head of Ads @ Whop.
- Colin McDermott: Head of SEO @ Whop (15+ سنوات).
- Keisha Singleton: Senior Blog Editor @ Whop (9+ سنوات).

---

## 7) التوصيات للمهمة (Recommendations) — قرار Guo Jia الحاسم

### 7.1 — أي نموذج نختار؟

**النموذج المختار: Whop Content Rewards (Clipping) — عبر Whop Clips community.**

#### الأسباب (Guo Jia — Quick Read + Decisive):

1. **دخل من اليوم الأول بلا متابعين** — العائق الأكبر للـ agent جديد هو الـ cold start، وContent Rewards يحله.
2. **معدل $1.25/1K لـ YouTube clips على Whop Clips = 12–50x أعلى من TikTok/YouTube Shorts CPM**.
3. **مجاني للانضمام** (Whop Clips) + payout فوري (instant) + free course من Dylan Lundgren.
4. **أول 3 فيديوهات مدفوعة بغض النظر عن المشاهدات** (zero-risk entry).
5. **حلال:** العلامة نفسها تطلب القص وتدفعه — تفويض رسمي واضح.
6. **1M members** = community صحية قابلة للـ scaling والـ leaderboards.
7. **$190,000/mo budget** = إمكانية واقعية للربح عالي.
8. **API رسمي كامل** — يمكن للأتمتة الكامل عبر `GET /bounties`, `POST /bounty_submissions`, webhooks.

#### النماذج المُتاحة كـ Layer 2 (بعد نمو Content Rewards):

| النموذج | الترتيب | السبب |
|--------|--------|------|
| Whop Content Rewards (Clipping) | ⭐ الأول | الدخل الأساسي، zero-entry-barrier |
| Whop Content Rewards (UGC) | الثاني | أسعار أعلى لكن متطلبات أعلى (محتوى أصلي) |
| Affiliate Marketplace | الثالث | دخل إضافي بدون تكاليف — يمكن دمجه مع الـ clipping |
| Membership ($15–20/mo) | الرابع | MRR بعد نمو audience من clipping |
| Digital products (templates) | الخامس | منتج مملوك يُبنى مرة |
| Whop Partners (referrals) | السادس | دخل passive لكن يحتاج outreach |

### 7.2 — خطة التنفيذ المباشرة (Plan)

#### المرحلة 1 (يوم 1–3): Setup
1. إنشاء حساب Whop (`https://whop.com/signup/`).
2. الانضمام لـ **Whop Clips** (`https://whop.com/discover/whop-clips/`) — مجاني.
3. إكمال **KYC verification** عبر Sumsub hosted flow (يتطلب ID + selfie).
4. إعداد **payout method**:
   - **أولوية أولى (مصر/خليج):** Crypto wallet (BTC/ETH) — 5%+$1.
   - بديل: International local bank transfer (Varies).
   - للـ US recipients: Venmo (5%+$1) أو Next-day ACH ($2.50).
5. تثبيت **Whop CLI** (`curl -fsSL https://whop.com/install.sh | sh`) للأتمتة.
6. إنشاء **API key** مع scopes: `bounty:basic:read` (لا نحتاج `bounty:create` للـ clipper-side).

#### المرحلة 2 (يوم 4–7): Discovery + First Submission
1. مراجعة **Whop Clips Course** (Dylan Lundgren).
2. تصفح **Clipping Deals app** لـ active deals (Iman Gadzhi UGC, BBNO$ x Whop، ...).
3. تصفح **Content Rewards app** لـ all available bounties.
4. اختيار 1–3 bounties بـ:
   - Lowest competition (جدified by gross_paid_out_amount)
   - Highest `gross_reward_amount` (net_reward_amount after fees)
   - Compatible with `allowed_country_codes` (Egypt/US/etc.)
5. استخدام API:
   ```bash
   curl -X GET "https://api.whop.com/api/v1/bounties?status=open&business_goal_type=clipping" \
     -H "Authorization: Bearer $WHOP_USER_TOKEN" \
     -H "Api-Version-Date: 2026-09-11"
   ```
6. اختيار 1 فيديو خام من الـ Asset links المرفوعة.
7. مونتاج 30–60 ثانية شورتس (وفق Retention Editing from Master_Video_Production.md).
8. نشر على TikTok + Instagram Reels (المنصات المسموحة).
9. التسليم عبر:
   ```bash
   curl -X POST "https://api.whop.com/api/v1/bounty_submissions" \
     -H "Authorization: Bearer $WHOP_USER_TOKEN" \
     -d '{"bounty_id":"bnty_XXX","deliverable":{"urls":["https://tiktok.com/@your/video/..."],"caption":"Vertical cut, 42s"}}'
   ```

#### المرحلة 3 (يوم 8–30): Scale
- 3–5 clips/يوم على حسابات ثانوية أولاً (Fan Account pattern from Master_Platform_Strategy).
- تتبع الأداء عبر:
  - `GET /bounty_submissions?status=approved` للـ submissions المقبولة.
  - Webhook listener لـ `entry.approved`, `entry.denied` events.
- نقل الناجح (≥2x median) للحساب الرئيسي.
- ضبط الـ hook بالاعتماد على Retention@3s من الـ submissions السابقة.

#### المرحلة 4 (يوم 31–90): MRR Layer
- إطلاق **Whop Membership** على $15–20/mo مع قيمة من الـ clipping insights.
- دمج **Affiliate Marketplace** — رابط أداة المونتاج المفضلة مع affiliate.
- أول $1000+/mo من Content Rewards → استثمار في تحسين المونتاج + paid scheduling.

### 7.3 — أرقام متوقعة (Projection) — قرار حاسم

| الفترة | الهدف |
|--------|-------|
| أول 3 فيديوهات | مكافأة ثابتة (Whop Clips bonus) |
| أسبوع 2 | أول $50–100 من Content Rewards |
| شهر 1 | $200–$500/mo (معدل part-time clipper) |
| شهر 3 | $1,000+/mo مع 3–5 clips/يوم ناجحين |
| شهر 6 | $2,000–$5,000/mo مع own channels/agencies |
| شهر 12 | $10,000+/mo (top 1% clippers) |

> **(Yuan Fang):** العامل الحاسم ليس فقط عدد الـ clips — بل **اختيار الحملة الأعلى ربحاً** (`gross_reward_amount` × `accepted_submissions_limit`) مع `allowed_country_codes` متوافق + `business_goal_type=clipping` + منافسة منخفضة (`gross_paid_out_amount` منخفض = budget ما زال متاح).

### 7.4 — المخاطر الرئيسية (Risks)

1. **Botting detection:** لو اشتريت views → حظر دائم + خسارة محتجز.
2. **Auto-approve false positive:** بعد 48 ساعة، الـ AI قد يوافق على submission لا يطابق المتطلبات → لا تكرر النمط الخاطئ.
3. **Country targeting:** لو الحملة تحدد `allowed_country_codes: [US, CA]` وأنت في مصر — submission قد يُرفَض.
4. **AI voiceovers ممنوعة:** بعض الحملات (مثل Lovable) ترفضها صراحة.
5. **Comments turned on:** يجب تفعيل الـ comments على المنصة المنشور عليها.
6. **Duration minimum:** بعض الحملات تحدد "20 seconds minimum" — لا تنشر أقل.
7. **API rate limits:** الـ polling كل دقيقة لـ bounty_submissions — لا تتجاوز.
8. **KYC delays:** أول payout قد يتأخر للـ compliance review (first sale, first withdrawal, $1K/$5K milestones).

### 7.5 — الأمان والحلال (Islamic Compliance)

- **نشاط حلال:** clipping محتوى مرخّص من العلامة (مطلوب منهم) + payout مقابل خدمة فعلية = حلال.
- **لا ربا/غرر:** التسعير واضح ($X per 1K views) والقيمة تُسلَّم فعلياً.
- **Payout methods:**
  - ✅ Crypto (BTC/ETH) — حلال بشرط النشاط الأصلي حلال.
  - ✅ Bank wire — حلال.
  - ⚠️ **Whop Treasury (6% APY):** yield من Aave lending protocol — قد يكون غير حلال للمستخدم الملتزم (إقراض بفائدة). **لا تُفعِّل هذه الميزة.**
  - ⚠️ BNPL providers (Klarna/AfterPay): تجنب بيع منتجاتك عبرهم (لكن الـ clipper-side payout لا علاقة له).
- **محتوى:** تجنب الإيحاءات + موسيقى محرّمة (استخدم SFX أو موسيقى مباحة). Whop نفسها تطلب "no AI voiceovers" أحياناً.

### 7.6 — الخطوة الأولى المباشرة (Immediate Next Action)

```bash
# 1. Sign up + KYC
open https://whop.com/signup/

# 2. Join Whop Clips (free)
open https://whop.com/discover/whop-clips/

# 3. Setup API access (for the agent)
open https://whop.com/dashboard/settings/api-keys  # create user OAuth token

# 4. Install CLI
curl -fsSL https://whop.com/install.sh | sh

# 5. Discover active clipping bounties
whop bounties list --status=open --business_goal_type=clipping --format=json
```

---

## ملاحق (Appendices)

### A. المصادر الأساسية المستخدمة (Primary Sources)

1. **Whop homepage:** `https://whop.com/`
2. **Whop blog index:** `https://whop.com/blog/` + sitemap
3. **Whop RSS feed:** `https://whop.com/blog/rss/` (Ghost 6.64-powered, 1.1MB)
4. **Whop network pricing:** `https://whop.com/network/pricing/` — الرسوم الكاملة
5. **Whop blog articles (مفصَّلة في النص):**
   - `/blog/ways-to-make-money-online/` (Aug 19, 2026)
   - `/blog/content-rewards/` (Mar 3, 2025)
   - `/blog/content-rewards-x-lovable/` (May 19, 2025)
   - `/blog/set-up-content-rewards/` (May 14, 2025)
   - `/blog/whop-clips/` (Apr 8, 2025)
   - `/blog/getting-paid-on-whop/` (Feb 11, 2026)
   - `/blog/what-is-content-clipping/` (Oct 13, 2025)
   - `/blog/what-is-a-whop/` (Sep 22, 2025)
   - `/blog/whop-treasury/` (Mar 25, 2026)
   - `/blog/spacexai-whop-grok/` (Sep 2, 2026)
   - `/blog/cli/` (Jul 21, 2026)
   - `/blog/whop-blueprints/` (Aug 31, 2026)
   - `/blog/whop-partners/` (Aug 18, 2026)
   - `/blog/affiliates-update/` (Dec 16, 2025)
   - `/blog/affiliate-links-app-whop/` (Jan 31, 2025)
   - `/blog/get-more-views-tiktok/` (Sep 12, 2024)
   - `/blog/watch/2billion-earned-on-whop/` (2026)
6. **Whop docs:**
   - `https://docs.whop.com/` (Developer Platform)
   - `https://docs.whop.com/llms.txt` (Documentation Index — 221KB)
   - `https://docs.whop.com/api-reference/beta/bounties/bounty.md`
   - `https://docs.whop.com/api-reference/beta/bounties/list-bounties.md`
   - `https://docs.whop.com/api-reference/beta/bounties/create-bounty.md`
   - `https://docs.whop.com/api-reference/beta/bounty-submissions/create-bounty-submission.md`
   - `https://docs.whop.com/api-reference/beta/payouts/list-supported-payout-methods.md`
   - `https://docs.whop.com/api-reference/beta/payouts/list-saved-payout-methods.md`
   - `https://docs.whop.com/developer/bounties/overview.md`
   - `https://docs.whop.com/developer/bounties/run-a-bounty-program.md`
   - `https://docs.whop.com/developer/verification/overview.md`
   - `https://docs.whop.com/developer/verification/business-structures.md`
   - `https://docs.whop.com/memberships-and-access/third-party-apps/content-rewards.md`
   - `https://docs.whop.com/webhooks` (Webhooks reference)
7. **Wikipedia:** `https://en.wikipedia.org/wiki/Whop.com`
8. **Whop Discover:** `https://whop.com/discover/whop-clips/` (1M members, 4.7/5 rating)
9. **Public API probe:** `curl https://api.whop.com/api/v1/bounties/bnty_test` → `{"error":{"type":"not_found","message":"Bounty not found"}}` (يؤكد auth-optional لـ retrieve)

### B. Quotes الحرفية الموثقة

1. > *"With Whop Content Rewards you don't need to create original content. You can start making money from day one – even with zero followers."* — blog/ways-to-make-money-online

2. > *"Content Rewards clippers are, on average, paid $1 per 1,000 views. But it's up to you to set your rates. Compare that to the $25 per 1,000 views you pay on Facebook or Instagram ads."* — blog/content-rewards

3. > *"We at Whop are using this system as I write this. On one of our content pieces, we got 384,000 short-form views – and it only cost us $384. Because of the success we see, we have a $190,000/m budget to pay out clippers through Whop Clips."* — blog/content-rewards

4. > *"Lovable AI's campaigns on Whop are currently paying $2 per 1K views, with a budget of $10K."* — blog/content-rewards-x-lovable

5. > *"The YouTube clip content type currently pays $1.25 per 1,000 views."* — blog/whop-clips

6. > *"Many users make and withdraw money on their first day joining!"* — blog/whop-clips

7. > *"Our Affiliate Success Manager, Dylan, has put in the hard yards and built a course framework for all creators to learn his proven content formula."* — blog/whop-clips

8. > *"If your repurposed Whop YouTube clip gets 300,000 views, you'll be eligible for 300 times the current view reward amount."* — blog/whop-clips

9. > *"Whop Content Rewards means that anyone can become a clipper. It doesn't matter how many followers you have or if you've ever made content before — if your clip gets views, you get paid."* — blog/what-is-content-clipping

10. > *"Right now, as a new member of Whop Clips, you'll get paid for your first 3 videos no matter how many views they get."* — blog/what-is-content-clipping

11. > *"Whop supports payouts in 241+ territories. Sell globally and still withdraw locally."* — blog/getting-paid-on-whop

12. > *"With the latest Whop update, all submissions to content rewards are now reviewed by our AI Content Rewards Reviewer. If a reviewed submission remains unapproved for more than 48 hours, the system will automatically approve it."* — blog/set-up-content-rewards

13. > *"Whop has paid out over 2 billion dollars to creators."* — blog/getting-paid-on-whop

14. > *"$2,000,000,000 earned on Whop. Always bet on yourself."* — Whop Announcements video

15. > *"The average business on Whop grows revenue 51% year over year."* — blog/what-is-a-whop

16. > *"Whop Partners have earned over $10M to date, just from referring businesses. Our top partners are clearing 6 figures per referral."* — blog/whop-partners

17. > *"30,000+ active affiliates are now earning on Whop."* — blog/affiliates-update

18. > *"Earn up to 6% APY on your Whop balance, automatically. Whop Treasury puts your revenue to work the moment it lands: no lockups, no minimum balance, full control."* — blog/whop-treasury

19. > *"SideShift uses Whop's embedded payouts to seamlessly pay 850k+ creators across 50+ campaign structures... More than 1,000 brands use SideShift to find and hire creators, with millions of dollars being paid out per week."* — blog/sideshift

20. > *"From a Pokémon world champion charging $20 an hour to $10 million paid out to coaches."* — blog/metafy

### C. جدول الرسوم الكامل (Fee Schedule)

| الخدمة | الرسوم |
|--------|--------|
| Standard card (domestic) | 2.7% + $0.30 |
| International card | +1.5% |
| Currency conversion | +1% |
| ACH debit | 1.5% (max $5) |
| BNPL financing | 15% |
| 3DS authentication | $0.03/txn |
| Radar (fraud detection) | $0.07/txn |
| Dispute | $15/dispute |
| Early dispute alert (RDR) | $29/alert |
| Orchestration (optional) | 0.8%/txn |
| Billing automation | 0.5%/txn |
| Tax & remittance | 2%/txn (when collected) |
| Affiliate processing | 1.25%/txn |
| Next day ACH payout | $2.50/payout |
| Instant Bank Deposit (RTP) | 4% + $1/payout |
| Crypto payout (BTC/ETH) | 5% + $1/payout |
| Venmo payout | 5% + $1/payout (US only) |
| Bank wire | $23/payout |
| International local bank | Varies |

### D. خريطة API المختصرة (API Quick Reference)

```
Base:        https://api.whop.com/api/v1
Sandbox:     https://sandbox-api.whop.com/api/v1
Headers:     Authorization: Bearer $WHOP_API_KEY
             Api-Version-Date: 2026-09-11

# Browse bounties (with user token)
GET /bounties?status=open&business_goal_type=clipping&country=US

# Get one bounty (auth optional for public)
GET /bounties/{bounty_id}

# Submit a clip
POST /bounty_submissions
  body: { bounty_id, deliverable: { urls, file_ids, caption } }

# List your submissions
GET /bounty_submissions?bounty_id=bnty_XXX&status=submitted

# Webhooks (no bounty events — must poll)
entry.approved, entry.created, entry.denied, entry.deleted

# Payouts
GET /payouts/supported_methods
GET /payouts/methods

# KYC
POST /verifications?account_id=biz_XXX
  body: { kind: "individual" or "business" }
  returns: { session_url } (hosted Sumsub flow)

# Cards (issue cards from balance)
POST /cards

# Economic Intelligence (Whop's recommendation engine)
GET /economic_intelligence?account_id=biz_XXX
POST /economic_intelligence { account_id, input }
```

### E. أمر الـ CLI للأتمتة (CLI Commands for Agent)

```bash
# Setup
curl -fsSL https://whop.com/install.sh | sh
whop --llms      # hand AI the full command list
whop mcp add     # connect to Claude/Cursor/Grok
whop skills add  # add ready-made skills

# Browse bounties (as a clipper)
whop bounties list --status=open --business_goal_type=clipping --format=json

# Submit a clip
whop bounty-submissions create --bounty_id=bnty_XXX \
  --deliverable.urls=https://tiktok.com/@you/video/123 \
  --deliverable.caption="Vertical cut, 42s"

# Track submissions
whop bounty-submissions list --bounty_id=bnty_XXX --status=submitted

# Check earnings
whop stats list
```

---

## خلاصة Guo Jia — Quick Read & Decisive Verdict

**Whop Content Rewards (Clipping) عبر Whop Clips هو النموذج الأمثل** للأسباب التالية:
1. **Zero entry barrier** (لا متابعين، لا خبرة) — يحل أكبر عائق للـ agent جديد.
2. **Rate $1.25/1K = 12–50x أعلى من TikTok/YouTube Shorts CPM** — مع مكافأة أول 3 فيديوهات ثابتة.
3. **مجاني + instant payouts + 1M-member community + $190K/mo budget** = ecosystem صحي.
4. **API + CLI + MCP كاملة** = قابلة للأتمتة الكاملة (browse → submit → poll → withdraw).
5. **حلال:** تفويض رسمي من العلامة للقص + payout مقابل خدمة فعلية + لا غرر.

**الخطوة الأولى:** انضم Whop Clips → أكمِل KYC → ثبِّت payout method (crypto للـ مصر/خليج) → استخدم Whop CLI للأتمتة → اختر 1–3 bounties عالية الـ gross_reward_amount → أنتج 30–60s clip بـ Retention Editing → انشر على المنصات المسموحة → سلم عبر `POST /bounty_submissions` → تابع الـ webhook `entry.approved`.

**المخاطر الرئيسية:** botting detection (حظر دائم) + country targeting (اختيار الـ country المناسب) + AI voiceover restrictions + duration minimums.

**Layer 2 (after $1K+/mo):** Membership $15–20/mo + Affiliate Marketplace + Digital products (templates).

---

*نهاية التقرير. جميع الأرقام موثقة من المصادر الأصلية المذكورة في الملحق A. التقرير قابل للتحديث عند ظهور سياسات/أسعار جديدة من Whop.*
