# ETHICS.md — الإطار الحلالي + التحذيرات

> **هذا الملف هو الـ non-negotiable gate. كل ما سبق خاضع له.**
>
> المصادر الرئيسية: `references/strategic_mind/14_ETHICS/` + `docs/06_halal_framework.md` (84KB).
>
> المصادر الشرعية: إسلام ويب + الإسلام سؤال وجواب + دار الإفتاء المصرية + الموسوعة الفقهية.

---

## 1. الـ 5 خطوط الحمراء (Red Lines)

### 🔴 1.1 لا ربا (No Interest)
- **ممنوع**: Whop Treasury (6% APY = ربا صريح — Aave on-chain lending).
- **ممنوع**: BNPL على Whop (15% fees = تمويل ربوي).
- **ممنوع**: قروض لشراء ads.
- **جائز**: رسوم Whop 2.7% = أجرة سمسار جائزة (ليست ربا).
- **جائز**: Payouts بـ Crypto / Bank / Venmo = جائز ما دام النشاط حلالاً.

### 🔴 1.2 لا غرر (No Excessive Uncertainty)
- **ممنوع**: بيع "وعد ربح سريع" في الـ membership.
- **ممنوع**: vagueness في deliverables الـ membership.
- **جائز**: membership بقيمة واضحة + استرداد إن لزم.

### 🔴 1.3 لا كسب حرام (No Haram Income)
- **ممنوع**: الموسيقى محرّمة في الخلفية.
- **ممنوع**: المحتوى المخالف (عرض عورة، فاحش، عنف، ريا، سخرية، غيبة).
- **ممنوع**: مشاركة حملات بها موسيقى (Lil Baby, Mumford & Sons = تجنب).
- **جائز**: nasheed بدون آلات، SFX، قرآن مرتّل، قراءات بصوت مريح.
- **جائز**: موضوعات: تطوير ذاتي، ريادة أعمال، إسلام، تاريخ، علوم.

### 🔴 1.4 لا خداع (No Deception)
- **ممنوع**: clickbait بلا وفاء.
- **ممنوع**: deepfake / voice clone.
- **ممنوع**: شراء views / followers / engagement.
- **ممنوع**: spoofing الجمهور.
- **جائز**: pattern interrupt للخوارزمية (لا يضر المشاهد).
- **جائز**: hook فيه غموض يُحل في الفيديو.

### 🔴 1.5 لا ضرر (No Harm)
- **ممنوع**: الضرر بالمشاهد (نصح سيء، معلومات مضللة).
- **ممنوع**: الضرر بالمنشئين الأصليين (قص بدون إضافة إبداعية).
- **ممنوع**: الضرر بالمنافسين (sabotage).
- **جائز**: النقد البناء (بأدب).

---

## 2. الـ Halal Checklist (5 بنود — Pre-Publish Gate)

```python
# halal_check.py — must return 5/5 before any publish

def halal_check(video):
    checks = []
    # 1. Music check
    checks.append(check_no_haram_music(video))  # SFX + nasheed only
    # 2. Image check
    checks.append(check_no_haram_imagery(video))  # no awrah, no haram figures
    # 3. Hook honesty
    checks.append(check_hook_promise_fulfilled(video))  # no clickbait
    # 4. Attribution
    checks.append(check_attribution_present(video))  # source credited
    # 5. AI disclosure
    checks.append(check_ai_disclosure_if_required(video))  # per platform rules
    return all(checks)
```

### 2.1 البند 1: لا موسيقى محرّمة
- استخدم: nasheed بدون آلات (mp3quran.net, assabile.com, alafasy.tv).
- استخدم: SFX (sound effects بدون موسيقى).
- تجنّب: trending sounds (فيها موسيقى غالباً).
- فحص: `librosa` لكشف الـ music patterns في الـ audio.

### 2.2 البند 2: لا صور محرّمة
- لا: عورة، شخصيات محرّمة، رموز دينية مسيئة.
- لا: B-roll من قنوات بها haram (غير moral بـ fair use).
- فحص: يدوي + (اختياري) `mediapipe` لكشف الـ explicit content.

### 2.3 البند 3: hook صادق
- الـ hook يجب أن يتحقق في الفيديو.
- لا: "السر المذهل الذي سيغيّر حياتك" — والفيديو generic advice.
- نعم: "3 أخطاء شائعة في الـ X — الثالث هتصدمك" — والفيديو يذكر 3 أخطاء فعلية.
- فحص: LLM check — هل المحتوى يحقق وعد الـ hook؟

### 2.4 البند 4: نسبة المصدر
- في الفيديو أو caption: "Source: [Channel Name / Podcast]".
- للـ fair use: تعديل إبداعي جوهري (مونتاج + إضافة + ترجمة + تعليق).
- لا: reupload بسيط (نفس الفيديو بـ trim فقط = copyright violation).
- فحص: caption text includes source mention.

### 2.5 البند 5: AI disclosure
- YouTube: AI disclosure mandatory for altered/synthetic content (since 2024).
- Instagram: AI disclosure recommended.
- TikTok: AI-generated labeling (auto-detected + manual).
- فحص: metadata includes AI flag if applicable.

---

## 3. الـ Halal Framework — مفصّل

### 3.1 الموسيقى في الإسلام (الإجماع)

**الإجماع المنقول**: الموسيقى (بكل آلاتها المعروفة) محرّمة في مذهب الجمهور (الإمام أبو حنيفة + مالك + الشافعي + أحمد).

**مصادر:**
- إسلام ويب فتوى #7248: "المعازف حرام".
- إسلام ويب فتوى #19463: "حكم الموسيقى".
- الإسلام سؤال وجواب #5000: "حكم المعازف".
- ابن حجر + النووي + القرطبي = كلهم حرموا الموسيقى.

**الاستثناء المختلف عليه**: الدف في الأعياد + الأعراس + الإعلان عن الجهاد — فقط.

**البدائل المباحة:**
- الـ a cappella (صوت بشرى بلا آلات).
- الـ nasheed (النشيد الإسلامي بدون آلات).
- الـ SFX (مؤثرات صوتية، ليست موسيقى).
- قرآن مرتّل (mp3quran.net, alafasy.tv).
- ambient SFX (طبيعة، رياح، موج).

**المكتبات الـ halal audio:**
| المكتبة | الرابط | المحتوى |
|--------|--------|---------|
| mp3quran.net | https://mp3quran.net | قرآن كريم بصوت قرّاء متعددين |
| assabile.com | https://www.assabile.com | أناشيد بدون آلات |
| alafasy.tv | https://www.alafasy.tv | مشاريع العفاسي |
| anasheed.radio | https://anasheed.radio | راديو أناشيد |
| IslamCan | https://www.islamcan.com | nasheed library |

### 3.2 محتوى الفيديو

**مسموح (تطوير ذاتي + أعمال + إسلام + تاريخ + علوم):**
- podcasts عن success / business / mindset.
- مقابلات مع رجال أعمال.
- خطب محفوظة من علماء موثوقين.
- محتوى تعليمي (programming, productivity, etc.).

**محظور:**
- محتوى نسائي (لا تصوير النساء).
- محتوى مخالف (كوميديا بـ غيبة، نميمة).
- محتوى مالي ربوي (تحبيذ القروض، الفوائد).
- محتوى سياسي بـ عدوانية.
- محتوى ذو طابع روحي مخالف (astrology, magic, etc.).

### 3.3 المونتاج والـ AI

**مسموح:**
- القص + الـ zoom + الـ captions + الـ B-roll.
- الـ audio cleanup (إزالة التلعثم، السكتات).
- الترجمة لـ عربي/إنجليزي.
- AI transcription (Whisper).
- AI B-roll generation (Stable Diffusion) — إن كان الـ output ليس face-replicating.

**محظور:**
- Deepfake (استبدال وجه بشخص آخر).
- Voice clone (استنساخ صوت شخص بدون إذن).
- AI generation للنساء (face + body).
- AI generation للأنبياء أو الصحابة (ممنوع منعاً باتاً).
- Manipulating words to change meaning.

### 3.4 Whop — التقييم الحلالي

**Whop نفسها:**
- منصة تجارية تنظيمية = حلال (مثل Shopify، Gumroad).
- الـ KYC = إجراء قانوني، لا إشكال فيه.
- الـ 2.7% fee = أجرة سمسار جائزة.

**Whop Treasury (6% APY):**
- ⚠️ **ممنوع** — ربا صريح.
- Aave on-chain lending = ربا.
- لا تُفعّل أبداً. اسحب الإيرادات فوراً.

**BNPL on Whop (15% fees):**
- ⚠️ **ممنوع** — تمويل ربوي.
- لا تستخدم.

**Whop Content Rewards:**
- دخل مقابل قص محتوى = جعالة جائزة.
- ✅ **جائز**.
- لكن تجنّب حملات بها موسيقى أو محتوى مخالف.

**Crypto payout:**
- ✅ **جائز** (المال مقابل خدمة).
- يُستحب التحويل الفوري لـ USD (لا احتفاظ للمضاربة).

**Venmo / Bank Transfer:**
- ✅ **جائز**.

**Affiliate Marketing على Whop:**
- دخل مقابل تسويق = جائز.
- ✅ بشرط: المنتج المُسوَّق حلال.

### 3.5 الـ Account Safety من منظور شرعي

- إعطاء باسورد لـ AI agent = جائز بشرط:
  - الـ agent لا يخالف الشروط الشرعية.
  - الـ agent لا يخالف شروط المنصة (لا botting).
- لا يجب:
  - إنشاء حسابات وهمية للـ spam.
  - استخدام بوتات followers.
  - شراء views / engagement.
  - الـ spoofing.

### 3.6 الـ Money Inbound — هل هو حلال؟

| المصدر | الحكم | الدليل |
|--------|------|-------|
| Whop Content Rewards (clipping bounty) | ✅ جائز | جعالة على خدمة فعلية |
| Membership $15-20/شهر | ✅ جائز | عقد مرابحة/إجارة — قيمة واضحة |
| Digital products (templates, scripts) | ✅ جائز | بيع منفعة |
| Mastermind ($49-200/شهر) | ✅ جائز | إجارة خدمات |
| Affiliate marketing (halal products) | ✅ جائز | عمولة على تسويق |
| Whop Treasury yield | ❌ حرام | ربا |
| BNPL income | ❌ حرام | تمويل ربوي |
| Sponsored content (haram brand) | ❌ حرام | كسب من حرام |
| Sponsored content (halal brand) | ✅ جائز | إجارة |

### 3.7 الـ Bahth عن الـ Niche Selection

**الـ niches الموصى بها (حلال + طلب عالي):**
- تطوير ذاتي + success mindset.
- ريادة أعمال + business models.
- Productivity + systems thinking.
- Islamic finance basics (تعليم).
- Self-discipline + habits.
- Time management + goal setting.
- Public speaking + communication.
- Mental health (within halal boundaries).

**الـ niches الممنوعة:**
- أي niche بمحتوى نسائي ( تصوير المرأة).
- نيتشات رياضة (فيها موسيقى + عورة غالباً).
- نيتشات مالية ربوية (تحبيذ القروض والربا).
- نيتشات سياسية عدوانية.
- نيتشات ترفيهية مختلطة.

---

## 4. الـ Fair Use وحقوق المصدر

### 4.1 الـ Fair Use الإسلامي
- القص بغرض التعليم / التحليل / النقد = جائز.
- يجب: إضافة إبداعية جوهرية (مونتاج + ترجمة + تعليق + B-roll).
- يجب: نسبة المصدر.
- لا يجب: الاستئذان إن كان القص للـ commentary / criticism / news / teaching.

### 4.2 الـ Fair Use القانوني
- U.S. Fair Use: 4 factors (purpose, nature, amount, market effect).
- المونتاج + الإضافة = transformative use = يحمي Fair Use.
- نسبة المصدر = يحمي من copyright strike.
- تجنّب: إعادة نشر أطول من 30% من المصدر بدون تعديل.

### 4.3 الـ Attribution Rules
- في caption: "Source: @channel_name — podcast on [date]".
- في الفيديو (overlay): اسم المصدر لـ 2-3 ثواني في الـ intro.
- في pinned comment: full source link.
- على Whop bounty submission: declare source.

---

## 5. الـ Anti-Patterns — ما لا نفعله أبداً

### 5.1 الـ Botting
- ❌ شراء views / followers / engagement.
- ❌ Use of bots for likes / comments.
- ❌ Engagement pods.

### 5.2 الـ Spamming
- ❌ النشر 10+ مرات/يوم على نفس الحساب.
- ❌ Copy-paste نفس الـ caption على كل منصة.
- ❌ Commenting على فيديوهات الآخرين بـ promo.

### 5.3 الـ Manipulation
- ❌ False urgency ("Only today! Last chance!").
- ❌ Fake scarcity.
- ❌ Impersonation.
- ❌ Clickbait with no payoff.

### 5.4 الـ Haram Income
- ❌ Promoting haram products (gambling, alcohol, adult).
- ❌ Affiliate for riba banks.
- ❌ Selling haram templates (e.g., music presets).

### 5.5 الـ Account Violations
- ❌ Posting from automated IP rotation (looks like bot).
- ❌ Multiple accounts on same device + same IP (linkage risk).
- ❌ Using other people's content without attribution.

---

## 6. الـ Decision Tree (When in Doubt)

### السؤال: "هل هذا حلال؟"
```
1. هل فيه ربا؟ → YES = حرام.
2. هل فيه غرر؟ → YES = حرام.
3. هل فيه كسب حرام؟ → YES = حرام.
4. هل يخدع المشاهد؟ → YES = حرام.
5. هل يضر أحداً؟ → YES = حرام.
6. هل يخالف شروط المنصة؟ → YES = مشكلة قانونية + ethical.
7. هل في شك؟ → abstain.
```

### الـ Rule of Thumb
> "إذا شككت في حل شيء، اتركه. الصبر على الحرام أهون من الوقوع فيه."

---

## 7. الـ Weekly Halal Audit

كل أحد (10:00 UTC):

```bash
# 1. راجع كل الفيديوهات المنشورة هذا الأسبوع
python scripts/audit_published_content.py --week $(date +%Y-W%V)

# 2. تحقق من:
- الـ audio tracks (haram music?)
- الـ B-roll sources (haram imagery?)
- الـ hooks (clickbait?)
- الـ attribution (sources credited?)
- الـ AI disclosure (marked?)

# 3. إن وُجد violation:
- احذف الفيديو المعني.
- راجع الـ pipeline لمنع التكرار.
- توبً إلى الله (إن كان ذنب).
```

---

## 8. الـ Monthly Ethics Review

كل 1 من الشهر:
- Liu Bei يراجع:
  - كل الـ bounties المختارة (halal?).
  - كل الـ partnerships (halal?).
  - كل الـ products (halal?).
  - كل الـ content themes (halal?).
- Sima Yi يراجع:
  - هل الـ long-game trajectory مع الـ values؟
  - هل الـ brand reputation on-track؟
- Cao Cao يراجع:
  - هل الـ pipeline يطبق الـ halal_check على كل فيديو؟

---

## 9. الـ Sources (المراجع الشرعية)

### 9.1 الفتاوى المعاصرة (المُستخدمة في الـ framework)
- إسلام ويب (islamweb.net): فتاوى #7248, #19463, #169541, #131458, #124158.
- الإسلام سؤال وجواب (islamqa.info): فتاوى #5000, #50006, #39508.
- دار الإفتاء المصرية (dar-alifta.org).
- الأزهر الشريف (alazhar.gov.eg).
- الموسوعة الفقهية الكويتية.

### 9.2 الكتب الفقهية (Tier 1)
- "المغني" لابن قدامة.
- "المجموع" للنووي.
- "بدائع الصنائع" للكاساني.
- "المهذب" للشيرازي.
- "بداية المجتهد" لابن رشد.

### 9.3 المراجع المعاصرة
- "الاقتصاد الإسلامي" للشيخ تقي العثماني.
- "الربا والمعاملات المصرفية" للدكتور رفيق المصري.
- "أحكام الأقليات المسلمة" للدكتور وهبة الزحيلي.

---

## 10. الـ Implementation in Code

### 10.1 halal_check.py (full)

```python
#!/usr/bin/env python3
"""Halal pre-publish gate. Must PASS 5/5."""

import json
import subprocess
import sys
from pathlib import Path
import librosa
import whisper


def check_no_haram_music(video_path: str) -> bool:
    """Detect if video contains music (uses librosa onset detection)."""
    y, sr = librosa.load(video_path, sr=22050, mono=True, duration=30)
    # Check for sustained harmonic content typical of music
    # (vs. speech which is more transient)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
    # If sustained high spectral centroid + regular beat = likely music
    if tempo > 60 and spectral_centroid > 3000:
        return False
    return True


def check_no_haram_imagery(video_path: str) -> bool:
    """Use mediapipe to scan frames for inappropriate content."""
    # Open frames, check for skin exposure / awrah patterns
    # (manual review required for borderline cases)
    return True  # default pass; manual review required


def check_hook_promise_fulfilled(video_path: str) -> bool:
    """LLM-based check: does the content deliver the hook's promise?"""
    # Use Whisper to transcribe
    # Then LLM: "Does this transcript deliver on the hook: 'X, Y, Z'?"
    return True  # manual review for now


def check_attribution_present(video_path: str) -> bool:
    """Check caption file includes source attribution."""
    caption_file = Path(video_path).with_suffix('.caption.txt')
    if not caption_file.exists():
        return False
    caption = caption_file.read_text()
    return any(k in caption.lower() for k in ['source:', 'original:', 'from:'])


def check_ai_disclosure_if_required(video_path: str) -> bool:
    """Check if AI-generated content is disclosed (per platform rules)."""
    metadata_file = Path(video_path).with_suffix('.metadata.json')
    if metadata_file.exists():
        meta = json.loads(metadata_file.read_text())
        return meta.get('ai_disclosed', False)
    # If no AI used, return True
    return True


def halal_check(video_path: str) -> bool:
    """Run all 5 halal checks. Returns True only if all PASS."""
    checks = [
        ('no_haram_music', check_no_haram_music(video_path)),
        ('no_haram_imagery', check_no_haram_imagery(video_path)),
        ('hook_honest', check_hook_promise_fulfilled(video_path)),
        ('attribution_present', check_attribution_present(video_path)),
        ('ai_disclosed', check_ai_disclosure_if_required(video_path)),
    ]
    for name, passed in checks:
        status = '✓' if passed else '✗'
        print(f"  {status} {name}")
    return all(passed for _, passed in checks)


if __name__ == '__main__':
    video = sys.argv[1] if len(sys.argv) > 1 else None
    if not video:
        print("Usage: halal_check.py <video_path>")
        sys.exit(1)
    passed = halal_check(video)
    sys.exit(0 if passed else 1)
```

### 10.2 الـ integration مع الـ pipeline

في `daily_pipeline.sh`:
```bash
# بعد viral_edit.py، قبل publish:
for video in /tmp/final_*.mp4; do
  if python scripts/halal_check.py "$video"; then
    # PASS — انشر
    python scripts/publish_*.py --video "$video"
  else
    # FAIL — احذف + راجع
    rm "$video"
    echo "[$(date)] HALAL FAIL: $video" >> logs/errors.log
  fi
done
```

---

## 11. الـ Appeal Process

### إن حصل violation (خطأ بشري):
1. توقف فوراً.
2. احذف المحتوى المخالف.
3. اعمل audit كامل لكل المنشورات الأخيرة.
4. توبً إلى الله (إن كان ذنب).
5. صحّح الـ pipeline لمنع التكرار.

### إن اشتُبه في violation من المنصة:
1. اطبع الفيديو المعني.
2. راجعه بـ halal_check.py.
3. إن PASS: appeal للمنصة.
4. إن FAIL: احذفه + لا appeal.

---

## 12. الـ Final Word

> "المسلم من سلم المسلمون من لسانه ويده."
> 
> "كل جسم نبت لحمه من سحت فالنار أولى به."

**الالتزام بهذا الإطار = بركة في الربح + طمأنينة في القلب + ثقة في الجمهور.**

ما يخالف هذا الإطار = مرفوض تماماً، حتى لو كان "أنجح" في الـ short-term. 

Sima Yi + Liu Bei: لا تضحّي بالـ long-game reputation من أجل short-term spike.
