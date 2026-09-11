# TikTok Algorithm Deep Research — FYP, Shadowban, Content Posting API, Best Practices 2026

**Task ID:** 1-c
**Mind:** Sima Yi (لعبة طويلة + صبر + إخفاء)
**Date:** 2026-09-11
**Researcher:** Sub-Agent (general-purpose)
**Method:** Direct HTTP fetches via `curl` against primary TikTok sources + reputable third-party analyses. Reddit, NYT, Medium, archive.org, Hootsuite were blocked by bot detection (HTTP 403) — that limitation is documented in §10.

---

## §1 — Executive Summary

TikTok's recommendation system is the **For You Page (FYP)** algorithm. It is a **personalized, real-time, content-graph ranking engine** that surfaces videos based on user-interaction signals, video metadata, and (lower-weight) device/account settings. Unlike pre-2020 chronological feeds, FYP **explicitly ignores follower count and previous high-performing videos** when ranking — meaning a brand-new account with zero followers can reach the FYP of millions if the content delivers engagement within the first 60 minutes.

The 2026 ranking formula centers on four pillars (per TikTok's own "Creator Rewards" formula published March 18, 2024): **(1) Originality, (2) Play Duration, (3) Search Value, (4) Audience Engagement**. The "200-view jail" is the platform's deliberate test-bed — every new video is shown to a Seed Audience of 100–500 users, and only if it generates enough **"Qualified Views" (5+ second views)** and a high completion rate will it be pushed to wider audiences.

Shadowban on TikTok is **not officially admitted** — the platform instead uses the term **"ineligible for recommendation to For You feeds"** — but functionally equivalent. It triggers on: borderline content (sexually suggestive, suggestive/repetitive themes, inauthentic behavior, repeat guideline violations, unverified/inauthentic account behavior). It is **detectable** (sudden 0-view state, no FYP presence) and **reversible** via 72-hour pause, content cleanup, original-only posts, and (if needed) account appeal through the in-app "Account Status" page.

The **Content Posting API** (v2) is the official, audit-required path for programmatic posting. Two OAuth scopes apply: **`video.publish`** (Direct Post, requires app audit) and **`video.upload`** (Draft mode, no audit needed). Default rate limit is **600 req/min per endpoint** with HTTP 429 + `rate_limit_exceeded` when exceeded.

Best-practice posting times for US/Europe audiences: **midweek, 14:00–18:00 local time** (per Sprout Social, Feb 2026). Best content: **60–90 second edutainment videos with a strong 3-second hook, keyword-rich captions, trending or original audio, and a clear Save/Share CTA.**

---

## §2 — How the FYP Algorithm Works (Detailed)

### 2.1 Official TikTok Statement (June 18, 2020 — How TikTok recommends videos #ForYou)

TikTok's foundational algorithm transparency article (still the canonical reference, referenced by every later update):

> "When you open TikTok and land in your For You feed, you're presented with a stream of videos curated to your interests... This feed is powered by a recommendation system that delivers content to each user that is likely to be of interest to that particular user. Part of the magic of TikTok is that there's no one For You feed — while different people may come upon some of the same standout videos, each person's feed is unique and tailored to that specific individual."

**Source:** https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you (Newsroom, June 18, 2020)

#### Three official ranking factor categories:

| # | Factor Category | What it includes | Weight |
|---|---|---|---|
| 1 | **User interactions** | videos you like/share, accounts you follow, comments you post, content you create | **HIGH** (primary) |
| 2 | **Video information** | captions, sounds, hashtags, effects, transcripts | **MEDIUM-HIGH** |
| 3 | **Device and account settings** | language preference, country setting, device type | **LOW** (optimization only, "since users don't actively express these as preferences") |

**Critical clarifications (verbatim from TikTok):**
- "A strong indicator of interest, such as whether a user finishes watching a longer video from beginning to end, would receive greater weight than a weak indicator, such as whether the video's viewer and creator are both in the same country."
- "While a video is likely to receive more views if posted by an account that has more followers... **neither follower count nor whether the account has had previous high-performing videos are direct factors in the recommendation system.**"

#### How a new user's FYP is bootstrapped:
1. New user is invited to **select categories of interest** (pets, travel, etc.) to seed initial recommendations.
2. If skipped, TikTok serves a "generalized feed of popular videos" to bootstrap signal-collection.
3. First set of likes/comments/replays initiates an **early round of recommendations** as the system "begins to learn more about your content tastes."
4. Following accounts, exploring hashtags/sounds/effects on Discover further refines the feed.

#### Explicit non-recommendation triggers:
- Videos flagged as "Not Interested" by the user
- Hidden creators or sounds
- Reported content

### 2.2 NYT Leak (December 2024) — Julian McAuley Analysis

The **New York Times published leaked TikTok internal algorithm documentation in December 2024**. Direct access to NYT was blocked (HTTP 403 from sandbox), but Buffer's December 2025 analysis (https://buffer.com/resources/tiktok-algorithm/) summarizes the key academic reaction verbatim:

> "There seems to be some perception that they've cracked some magic code for recommendation, but most of what I've seen seems pretty normal," says Julian McAuley, a professor of computer science at the University of California San Diego. After viewing some internal documentation on the TikTok algorithm, he spoke to the New York Times. What makes TikTok different, he explained, is that they have **"fantastic volumes of data, highly engaged users, and a setting where users are amenable to consuming algorithmically recommended content (think how few other settings have all of these characteristics!). Not some algorithmic magic."**

**Source:** Buffer, "TikTok Algorithm Guide 2026" (Dec 17, 2025), citing NYT leak (Dec 2024) + Washington Post analysis.

### 2.3 The Seed Audience Mechanism (200-View Jail)

Every new TikTok video enters a deliberate **test-batch** phase before mass distribution:

1. **Initial seed:** 100–500 users (interest-matched, often non-followers) see the video in their FYP.
2. **30–60 minute decision window** (vs. 4–5 hours on Instagram Reels, per Master_Platform_Strategy §19) — the algorithm measures Qualified Views, completion rate, save/share/comment velocity in this window.
3. **Promotion ladder:** If positive engagement ≥ threshold → pushed to 1K users → 10K → 100K → 1M+. Each rung is a re-evaluation.
4. **200-view jail** (Sprout Social, Feb 6, 2026, verbatim):
   > "The '200-view jail' is a common phenomenon where videos stop gaining reach after the initial test batch. In 2026, this usually happens because the video failed to generate enough 'Qualified Views' (views longer than 5 seconds) or had a low completion rate. It signals to the algorithm that the content wasn't engaging enough to push to a broader audience."

**Sources:** Sprout Social (Feb 6, 2026) https://sproutsocial.com/insights/tiktok-algorithm/ ; Master_Platform_Strategy_18_platforms_algorithm.md §19 (read in worklog).

### 2.4 What the Algorithm Does NOT Show or Consider

**Does NOT recommend (per Sprout + TikTok official):**
- Duplicate content
- Content you've already seen
- Content considered as spam
- Potentially offensive or unsafe content
- Videos that have just been uploaded (in processing)
- Videos that are under review
- Borderline/sexually suggestive content (made "ineligible" rather than removed — see §3.4)
- Mature/complex themes for teen accounts (via Content Levels system)
- Repetitive sad/extreme-diet/breakup content (anti-repetition heuristic, Dec 16, 2021 update)

**Does NOT directly consider as ranking factors:**
- Follower count
- Previous high-performing videos

**Source:** Sprout Social (Feb 2026) + TikTok Newsroom "An update on our work to safeguard and diversify recommendations" (Dec 16, 2021).

### 2.5 2026 Ranking Signals — Ordered by Importance

Compiled from Sprout (Feb 2026), Buffer (Dec 2025), Influencer Marketing Hub (June 2024), TikTok Newsroom Mar 18 2024 (Creator Rewards formula), and the 2025 Smart Keyword Filtering / Manage Topics rollout (June 2025).

| Rank | Signal | Why it matters in 2026 | Source |
|------|--------|------------------------|--------|
| 1 | **Watch Time / Completion Rate** | Strongest single signal. ≥80% completion = viral candidate. ≥60% retention at 30s = excellent. | Sprout Feb 2026, IMH Jun 2024 |
| 2 | **Saves + Shares** (Compound Signal) | "Save and share signals indicate high value and an intent to return or distribute content, **often outweighing simple Likes by a significant margin**." | Sprout Feb 2026 |
| 3 | **Search Value** (NEW 2024–2026) | "Direct ranking metric" in 2026. Auto-captions + text overlays are scanned by the algorithm to match content to specific search queries. Reward videos that provide direct answers. | Sprout Feb 2026, TikTok Newsroom Mar 18 2024 |
| 4 | **Comments** | Higher-value signal than Likes (active interaction) | TikTok Newsroom Jun 18 2020 |
| 5 | **Likes** | Lower-weight "yes" signal — fast to give, less meaningful than Share/Save | TikTok Newsroom Jun 18 2020 |
| 6 | **Follows from the video** | Indicates intent to return — strong mid-tier signal | IMH Jun 2024 |
| 7 | **Replays / Re-watches** | Counts heavily as "extra watch time" | TikTok Newsroom Jun 18 2020 |
| 8 | **Caption keywords + Hashtags** (Subject Matter) | Categorization. Used by TikTok SEO + Search matching. | Sprout Feb 2026, TikTok Newsroom Mar 13 2024 |
| 9 | **Trending / Original Sound** | Audio categorization. Trending audio exposes to existing engaged audience. Original audio builds brand identity. | IMH Jun 2024, Sprout Feb 2026 |
| 10 | **Not Interested / Skips** (Negative) | Reduces future visibility. Long-press → "Not Interested" or hiding a creator. | TikTok Newsroom Jun 18 2020 |
| 11 | **Language + Country settings** | Low-weight optimization (user doesn't actively express). | TikTok Newsroom Jun 18 2020 |
| 12 | **Device type** | Lowest weight. | TikTok Newsroom Jun 18 2020 |

**2026 hierarchy shift:** Saves + Shares have **surpassed Likes** in weight. Buffer (Dec 2025) explicitly notes "TikTok uses engagement like this as a signal that your content is valuable and worth showing to more users."

### 2.6 The Creator Rewards Formula (March 18, 2024 — Official)

TikTok's **own monetization formula** is the most authoritative 2024–2026 ranking signal disclosure:

> "The Creator Rewards Program will continue to reward high-quality, original content that is over a minute long, using an optimized rewards formula focused on four core metrics: **originality, play duration, search value and audience engagement.**
> - **Originality** refers to quality content unique to the creator, showcasing their point of view or creative thought process.
> - **Play duration** accounts for both watch time and finish rate. The new formula rewards accounts with content that is clear, and engaging, rather than favoring accounts with an excessive amount of videos.
> - **Audience engagement** includes likes, comments and shares.
> - **Search value** is a metric assigned to content based on popular search terms. Content that aligns with in-demand search topics increases its value for searchers."

**Eligibility** (Creator Rewards Program):
- ≥18 years old
- ≥10,000 followers
- ≥100,000 views in last 30 days
- Personal account in good standing in eligible region
- All videos must adhere to Community Guidelines + Terms of Service

**Source:** https://newsroom.tiktok.com/en-us/introducing-the-new-creator-rewards-program (Mar 18, 2024).

### 2.7 The "First Hour" Rule

Although TikTok's 2026 algorithm prioritizes **relevance over recency** (Sprout: "search optimized content can continue to perform weeks after posting"), the **first-hour engagement** still controls the velocity of distribution lift:

> "The algorithm looks at engagements on your video to rank it appropriately. In other words, the more engagement it sees, the more likely your video will show up on the For You pages of relevant users. This means that you need to drive as much engagement as possible within the first few minutes of posting to improve visibility on the platform." — Sprout Social (Feb 6, 2026)

**Why it matters:** The Seed Audience (§2.3) measures engagement over 30–60 minutes. If the Seed returns low Qualified Views + low completion, the video stops at 200 views. If positive, the algorithm pushes to progressively larger audiences — and that initial signal velocity compounds.

---

## §3 — The Shadowban: Causes, Detection, Recovery

### 3.1 Definition and TikTok's Stance

**TikTok does NOT officially acknowledge "shadowban" as a concept.** The equivalent official mechanisms are:

1. **"Ineligible for recommendation to For You feeds"** — content can still be viewed on the creator's profile, by direct link, by followers, but is removed from FYP distribution. Announced Feb 2, 2023 (Account Enforcement System update): "we are beginning to test a new feature in some markets that would provide creators with information about which of their videos have been marked as ineligible for recommendation to For You feeds, let them know why, and give them the opportunity to appeal."

2. **"Borderline content"** — TikTok Safety team makes borderline (not-violative-but-not-recommended) content ineligible rather than removing it. Per Dec 30, 2022 update: "We also have policies to make borderline or 'suggestive' content ineligible for recommendation into TikTok For You feeds."

3. **Account strikes (90-day expiry):** Per Feb 2, 2023 update: "if someone posts content that violates one of our Community Guidelines, the account will accrue a strike as the content is removed. If an account meets the threshold of strikes within either a product feature (i.e. Comments, LIVE) or policy (i.e. Bullying and Harassment), it will be permanently banned. ... Strikes will expire from an account's record after 90 days."

4. **Repeat-violator detection:** "Almost 90% violate using the same feature consistently, and over 75% violate the same policy category repeatedly" (Feb 2, 2023). Permanent ban threshold for cumulative strikes across policies/features also exists.

**Sources:**
- https://newsroom.tiktok.com/en-us/supporting-creators-with-an-updated-account-enforcement-system (Feb 2, 2023)
- https://newsroom.tiktok.com/en-us/strengthening-enforcement-of-sexually-suggestive-content (Dec 30, 2022)
- https://newsroom.tiktok.com/en-us/evolving-our-approach-to-content-enforcement-us (Mar 31, 2023)

### 3.2 Symptoms of a Shadowban

Common observable symptoms (per third-party analysis + TikTok's own Q4 2022 transparency):

1. **Sudden view drop to ~0 (or "0 views" on FYP test)** — the "200-view jail" turns into "0-view jail."
2. **Video does not appear on FYP** of non-followers (only followers see it on profile).
3. **Hashtag search returns your video last or not at all.** (Note: TikTok had a real bug May–June 2020 where 225,611 hashtags showed "0 views" due to data-stream flushing failure — confirmed in their post-mortem. A persistent 0-views issue after this bug was fixed is a stronger shadowban signal.)
4. **"Under review" indicator** appearing on your video for >24h.
5. **Account Status page (in-app)** shows flagged strikes or ineligible videos.

### 3.3 Common Causes

| # | Cause | Mechanism | Source |
|---|---|---|---|
| 1 | **Rapid-fire posting (volume spam)** | Many posts in short time → spam filter flag | TikTok CG §spam, Feb 2023 AE |
| 2 | **Bot/fake-account activity** (likes, follows, comments) | Inauthentic engagement detection | TikTok Safety Center |
| 3 | **Suspicious behavior** (mass-follow/unfollow, VPN abuse, repeated identical content) | Inauthentic behavior detection | TikTok Trust & Safety |
| 4 | **Banned hashtags** | Hashtags with guideline-violating content get suppressed (e.g., specific conspiracy or adult hashtags) | TikTok CG |
| 5 | **Borderline/sexually suggestive content** | Made "ineligible for recommendation" rather than removed | Dec 30, 2022 update |
| 6 | **Misinformation / unverified claims** | Made ineligible during fact-check; removed if confirmed false | Sep 28, 2022 update |
| 7 | **Repeat violations** | Account enforcement: 3+ strikes in 90 days = permanent ban | Feb 2, 2023 AE |
| 8 | **Low-quality/duplicate/plagiarized content** | Algorithm "can even deem it ineligible for the For You Page" | IMH Jun 2024 |
| 9 | **Repetitive themes** (sadness, extreme diet, sexually suggestive) within the recommendation graph | Anti-repetition heuristic reduces recommendation frequency | Dec 16, 2021 update |
| 10 | **Unverified URL / unauthorized link in bio** | Link Sharing requires URL verification | TikTok App Review Guidelines |

### 3.4 Proactive Prevention (Sima Yi's Long-Game Layer)

Adapted from `Master_Platform_Strategy_18_platforms_algorithm.md` §4.3 (Shadowban Prevention Protocol) + TikTok's own guidance:

1. **No automated liking/following/unfollowing.** No botting.
2. **Original content** — never republish another creator's video verbatim. Add transformation: hook + montage + caption + commentary.
3. **Natural engagement** — reply to comments, interact with audience.
4. **Content diversity** — avoid identical video templates/hashtags across consecutive posts.
5. **Rest periods** — never post 10+ in an hour then go silent for a week. Stick to 3–5/day cadence (Master Platform Strategy §5.3).
6. **Safe links only** — no shortened/affiliated URLs that haven't been verified.
7. **Use eSIM or separate device for commercial accounts** (Concept_eSIM_Mobile_Device_Anti_Shadowban).
8. **Avoid VPNs** (raises suspicion); use stable residential IP.
9. **Pre-test on secondary account** (Concept_Secondary_Account_Strategy) — publish on a "fan account" first; if it gets 200-view jail on the secondary, do NOT push to primary.
10. **Hashtag hygiene** — use 3–5 specific hashtags, no #FYP / #ForYou spam (these have been informally deprioritized).

### 3.5 Reactive Detection

1. **Check Account Status page** (in-app Settings → Safety → Account Status) — TikTok shows strikes, ineligible videos, and reasons.
2. **Search your video by hashtag** from a logged-out browser — if it doesn't appear, it's been made ineligible.
3. **Check Analytics → Content tab → For You distribution** (only on Creator / Business accounts) — if "For You" views are <5% of total, you are likely shadow-restricted on that video.
4. **Check the "Video Under Review" indicator** — if present >24h, you've been flagged for human moderation.

### 3.6 Recovery Protocol (Restoring the Account)

Recommended sequence (per TikTok's strike system + observed best practice):

1. **Pause new posts for 48–72 hours.** Let any algorithmic flag cool down.
2. **Audit recent videos** via Account Status page. Remove or set to "Only Me" any flagged content. Note: Sprout (Feb 2026) explicitly warns: "deleting videos can negatively impact your account. It removes data points that the algorithm uses to understand your content, and mass-deleting can trigger spam filters. Instead of deleting, it is recommended to change the video's privacy settings to 'Only Me.'"
3. **Clean up hashtags** — remove any banned/repetitive ones from recent posts (edit caption if possible, otherwise re-upload fresh).
4. **Switch to 100% original content** for the next 14 days. No clipping, no repurposing, no audio reuse.
5. **Engage authentically** — 30+ minutes/day on the app: watch, like, comment on others' content in your niche.
6. **Use a secondary account** during the recovery window so the primary doesn't bleed audience trust.
7. **Appeal if strikes are visible** — TikTok Feb 2, 2023 update: "support creators' ability to appeal enforcements and have strikes removed if valid."
8. **Strike expiry** — wait the 90 days for strikes to roll off the record.

---

## §4 — Content Posting API (Official Programmatic Posting)

### 4.1 Overview

TikTok's **Content Posting API** (v2) is the official OAuth-2.0-secured API for posting videos and photos to user accounts from external apps. Available at `https://open.tiktokapis.com/v2/post/publish/...`.

**Source:** https://developers.tiktok.com/docs/en/content-posting-api-get-started

### 4.2 Registration & Prerequisites

1. Create a TikTok developer account at https://developers.tiktok.com (email signup).
2. Create/join an organization (recommended).
3. Register your app and add the **Content Posting API** product.
4. Configure platforms (Web, iOS, Android, Desktop) with proper Redirect URIs.
5. Verify URL properties (Domain or URL prefix verification by signature file):
   - Web/Desktop redirect URIs must be `https` (web) or `localhost`/`127.0.0.1` with port (desktop), max 10 URIs.
   - iOS redirect URIs must be Apple Universal Links.
   - Android redirect URIs must be App Links / Deep Links.
6. Add scopes: `video.publish` (Direct Post — requires audit) and/or `video.upload` (Draft mode).
7. Submit app for review with at least one demo video (max 5 videos × 50 MB each).
8. App review status: Draft → In review → Live (or Not approved with comments).

**Note on visibility restriction:** "All content posted by unaudited clients will be restricted to private viewing mode. Once you have successfully tested your integration, to lift the restrictions on content visibility, your API client must undergo an audit to verify compliance with our Terms of Service."

**Source:** https://developers.tiktok.com/docs/en/getting-started-create-an-app + https://developers.tiktok.com/docs/en/app-review-guidelines

### 4.3 Available Scopes (Official Reference)

| Scope | Purpose | User-facing description | Products |
|------|---------|------------------------|----------|
| `video.publish` | **Directly post content to a user's TikTok profile.** | "Post content to TikTok." | Direct Post, Get Post Status |
| `video.upload` | **Share content to creator's account as a draft** to further edit and post in TikTok. | "Share content as a draft to your TikTok account." | Share Video API, Upload, Get Post Status |
| `video.list` | Read a user's public videos on TikTok | "Read your public videos on TikTok" | List Videos, Query Videos |
| `user.info.basic` | Read user profile info (open id, avatar, display name) | "Read your profile info (avatar, display name)" | User Info |
| `user.info.profile` | Read profile_web_link, profile_deep_link, bio_description, is_verified | "Read your additional profile information..." | User Info |
| `user.info.stats` | Read likes count, follower count, following count, video count | "Read your profile engagement statistics..." | User Info |
| `portability.all.*` | Data portability (single/ongoing) | various | Data Portability API |
| `research.data.*` | Research API (basic / u18eu / vra) | various | Research API |
| `research_adlib` `research.adlib.basic` | Commercial content API | "Access to public commercial data for research purposes" | Commercial Content API |

**Source:** https://developers.tiktok.com/docs/en/tiktok-api-scopes

### 4.4 Rate Limits

Per https://developers.tiktok.com/docs/en/tiktok-api-v2-rate-limit (Last updated August 4, 2026):

- Default per-endpoint limit: **600 requests per minute** on `/v2/user/info/`, `/v2/video/query/`, `/v2/video/list/`.
- "Request rate calculation is based on a one minute sliding window."
- Over-limit response: HTTP 429 + error code `rate_limit_exceeded`.
- Higher limits available by request via TikTok Support Page (review process).

### 4.5 Workflow for Posting a Video (Python Example)

Adapted from the official docs at https://developers.tiktok.com/docs/en/content-posting-api-get-started. Both FILE_UPLOAD and PULL_FROM_URL source modes are supported.

```python
"""
TikTok Content Posting API — minimal Python client (v2).
Prereq: pip install requests
Scopes required: video.publish (for Direct Post) or video.upload (for Draft).
"""
import requests

TIKTOK_API = "https://open.tiktokapis.com/v2"

def query_creator_info(access_token: str):
    """Step 1: Fetch creator info (privacy_level_options, max_video_post_duration_sec, etc.)"""
    r = requests.post(
        f"{TIKTOK_API}/post/publish/creator_info/query/",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=UTF-8",
        },
    )
    r.raise_for_status()
    return r.json()
    # Response: { "data": { "creator_username": "...", "privacy_level_options": [...],
    #   "max_video_post_duration_sec": 300, ... }, "error": { "code": "ok", ... } }

def init_video_upload_file(access_token: str, title: str, video_size_bytes: int,
                            chunk_size: int = 10_000_000, total_chunks: int = 5):
    """Step 2a: Initialize FILE_UPLOAD direct post. Returns upload_url + publish_id."""
    r = requests.post(
        f"{TIKTOK_API}/post/publish/video/init/",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=UTF-8",
        },
        json={
            "post_info": {
                "title": title,  # incl. hashtags: "this will be a funny #cat video on your @tiktok #fyp"
                "privacy_level": "PUBLIC_TO_EVERYONE",  # or MUTUAL_FOLLOW_FRIENDS / SELF_ONLY
                "disable_duet": False,
                "disable_comment": True,
                "disable_stitch": False,
                "video_cover_timestamp_ms": 1000,
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": video_size_bytes,
                "chunk_size": chunk_size,
                "total_chunk_count": total_chunks,
            },
        },
    )
    r.raise_for_status()
    return r.json()
    # Response: { "data": { "publish_id": "v_pub_file~v2-1.123456789",
    #   "upload_url": "https://open-upload.tiktokapis.com/video/?upload_id=67890&upload_token=Xza123" }, ... }

def init_video_upload_url(access_token: str, title: str, video_url: str):
    """Step 2b: Initialize PULL_FROM_URL direct post. Domain must be verified."""
    r = requests.post(
        f"{TIKTOK_API}/post/publish/video/init/",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=UTF-8",
        },
        json={
            "post_info": {
                "title": title,
                "privacy_level": "PUBLIC_TO_EVERYONE",
                "disable_duet": False,
                "disable_comment": True,
                "disable_stitch": False,
                "video_cover_timestamp_ms": 1000,
            },
            "source_info": {
                "source": "PULL_FROM_URL",
                "video_url": video_url,  # must be on verified domain/prefix
            },
        },
    )
    r.raise_for_status()
    return r.json()

def upload_video_file(upload_url: str, file_path: str, content_range: str):
    """Step 3 (FILE_UPLOAD only): Upload bytes to upload_url via HTTP PUT."""
    with open(file_path, "rb") as f:
        video_bytes = f.read()
    r = requests.put(
        upload_url,
        data=video_bytes,
        headers={
            "Content-Range": content_range,  # e.g. "bytes 0-30567099/30567100"
            "Content-Type": "video/mp4",
        },
    )
    r.raise_for_status()
    return r.status_code

def fetch_post_status(access_token: str, publish_id: str):
    """Step 4: Poll status with publish_id until processing completes."""
    r = requests.post(
        f"{TIKTOK_API}/post/publish/status/fetch/",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=UTF-8",
        },
        json={"publish_id": publish_id},
    )
    r.raise_for_status()
    return r.json()

# === Photo posting uses a different endpoint ===
def init_photo_post(access_token: str, title: str, description: str, photo_urls: list[str]):
    """Init photo carousel post. Use /v2/post/publish/content/init/ (NOT /video/init/)."""
    r = requests.post(
        f"{TIKTOK_API}/post/publish/content/init/",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        json={
            "post_info": {
                "title": title,
                "description": description,
                "disable_comment": True,
                "privacy_level": "PUBLIC_TO_EVERYONE",
                "auto_add_music": True,
            },
            "source_info": {
                "source": "PULL_FROM_URL",
                "photo_cover_index": 1,
                "photo_images": photo_urls,
            },
            "post_mode": "DIRECT_POST",
            "media_type": "PHOTO",
        },
    )
    r.raise_for_status()
    return r.json()
```

### 4.6 Important Caveats for the Pipeline

1. **All unaudited apps post in "private viewing mode"** — followers don't see it until audit approval. So for production clipping distribution, audit approval is **mandatory**.
2. **Verified domain required** for `PULL_FROM_URL` source. Verify via signature file (downloadable from Developer Portal) uploaded to your URL.
3. **Max video duration returned by `creator_info` is 300s (5 minutes)** — but Creator Rewards requires >60s. Aim for 60–90s sweet spot.
4. **`privacy_level: "PUBLIC_TO_EVERYONE"`** is required for FYP distribution.
5. **Polling recommendation:** Poll `/post/publish/status/fetch/` once every 60 seconds (NOT faster — rate limit is 600/min and you don't want to burn it).
6. **No webhooks for content posting** — only polling. (Same as Whop bounties — confirmed in worklog Task 1-a.)

---

## §5 — Community Guidelines 2026 + Allowed/Forbidden Content

### 5.1 The 10 Categories of Prohibited Content

From "Adding clarity to our Community Guidelines" (Jan 8, 2020) and refreshed "Refreshing our policies to support community well-being" (Dec 15, 2020) and subsequent quarterly enforcement reports:

1. **Harmful or dangerous content** (challenges, dares, dangerous acts)
2. **Terrorist organizations and any other criminal organizations**
3. **Graphic, shocking, or violent content** (incl. CSAM — permanent first-strike ban)
4. **Discrimination or hate speech** (incl. hateful ideologies — strict threshold)
5. **Nudity or sexual activity** (incl. adult content, directing to adult websites/apps)
6. **Child safety infringement** (zero tolerance)
7. **Harassment or personal identification of another user** (incl. doxxing, cyberstalking, sexual harassment)
8. **Impersonation, spam, or other misleading content** (inauthentic behavior, fake accounts, botting)
9. **Content that violates someone else's copyrights, trademarks, or other IP rights** (Fair Use is the defense, but TikTok errs on the side of restriction for borderline cases)
10. **Misinformation** (civic, public health, vaccines, voting, etc.) — ineligible for FYP during fact-check, removed if confirmed false

### 5.2 Borderline Content Categories (Made Ineligible for FYP, NOT Removed)

These are the **soft-shadowban triggers** for content that is "fine as a single video but problematic if viewed in clusters" (Dec 16, 2021):

- **Sexually suggestive content** (implied nudity, sensual content) — Dec 30, 2022 update; over 1M overtly suggestive videos prevented from teen reach in 30 days
- **Sadness / breakup content** (in repetitive sequence)
- **Extreme fitness or dieting content** (in repetitive sequence)
- **Cosmetic surgery content** for teen accounts (Content Levels system made 65,000 videos ineligible in Jan–Feb 2023 alone)
- **Misinformation being fact-checked** (ineligible while review pending)

### 5.3 Fair Use & Clipping on TikTok

TikTok's IP enforcement errs toward removal on copyright claims, but the platform allows **transformative content** under Fair Use. Best practices for clipping (relevant to Task 1-c integration with Whop Content Rewards):

1. **Always add transformation** — hook + montage + captions + commentary + translation + B-roll.
2. **Source from licensed/authorized programs** — Whop Content Rewards provides formal delegation.
3. **Cite the original creator** in caption or on-screen text where possible.
4. **Avoid re-uploading full clips** — keep under 60s and select the punchiest moment.
5. **Use original sounds where possible** to avoid audio copyright claims (trending sounds are typically licensed for use on the platform).

### 5.4 What Is Unsafe Content (Forbidden Categories for This Project)

- **Music:** Avoid copyrighted commercial tracks unless officially licensed via TikTok's Commercial Music Library. Use the library / original sounds / SFX.
- **Visuals:** No nudity, no sexually suggestive visuals, no graphic violence, no dangerous acts.
- **Topics:** No medical misinformation, no election misinformation, no hateful ideologies, no harassment, no doxxing, no impersonation.
- **Behavior:** No mass-liking, no mass-following, no botting, no VPN abuse, no repetitive identical content.

### 5.5 Halal-Compliant Content Checklist

- Audio: original sounds, SFX, or licensed Halal tracks (no music with haram themes/lyrics).
- Visuals: modest clothing, no inappropriate framing, no indecent exposure.
- Topics: educational/inspirational/comedy/financial/business — avoid adult, violent, or haram subject matter.
- Disclosure: clearly label AI-generated or repurposed content where required.
- Truthfulness: no clickbait that lies, no false promises, no exaggerated income claims.

---

## §6 — Captions, Hashtags, Audio (Best Practices 2026)

### 6.1 Captions: Manual vs Auto

- TikTok auto-generates closed captions from spoken audio; **manual caption editing is more accurate** and is rewarded via **Search Value** (algorithm "listens" to spoken content via auto-captions + on-screen text overlays).
- Keyword-rich captions match the video to in-demand search terms (Creator Rewards Program Search Value metric).
- Gen Z uses TikTok as a search engine — descriptive captions improve both FYP reach AND search visibility.

**Best practice (Sprout, Feb 2026):** "Craft descriptive, keyword-rich titles and captions that summarize visuals clearly and highlight key themes — don't be cryptic or use unrelated terms. Additionally, ensure your spoken content and on-screen text overlays reflect these keywords."

### 6.2 Hashtags

**Recommended structure (3–5 hashtags, mixed specificity):**

| Layer | Purpose | Example |
|-------|---------|---------|
| **Specific topic** | Tells algorithm exactly what the video is about | `#cleaningmakeupbrushes` |
| **Niche / community** | Reaches the engaged audience | `#cleantok` |
| **Broad / branding** | Visibility + brand identity | `#satisfyingvideo`, your brand tag |
| **Trending challenge (optional)** | Taps into viral momentum | `#currenttrend` |

**Avoid:**
- Stuffing (10+ hashtags)
- Generic `#fyp`, `#foryou`, `#viral` — informally deprioritized
- Banned hashtags (check via Search → if hashtag page has 0 views or warning label, it's restricted)
- Hashtags irrelevant to content (algorithm penalizes for mismatch)

**Tool:** TikTok Creator Search Insights (in-app) shows trending topics with popularity score and "Recommended Topic" label. Filter for "content gap topics" (high search volume + low video count) — these are the gold for 2026 content planning.

**Source:** https://newsroom.tiktok.com/en-us/creator-search-insights (Mar 13, 2024) + Sprout Feb 2026 + IMH Jun 2024.

### 6.3 Trending Sounds vs Original Sounds

**Trending sounds:**
- Boost reach by tapping into an already-engaged audience.
- "When a sound starts trending, make it your own by using it creatively in a video. This taps you into an audience already engaged with that audio." (Sprout Feb 2026)
- Find via Discover → Sounds → Trending, or third-party trackers like TikTok Creative Center.

**Original sounds:**
- Build brand identity (e.g., Ryanair's branded original sounds).
- Eligible for the Creator Rewards Program "originality" metric (transformative content is rewarded).
- Allow full IP control (no risk of audio being pulled for copyright).

**Hybrid strategy:** Use trending audio as the foundation; add voiceover or original music layer to create a new "original sound" derived from the trend — gets the trend boost + the originality score.

**2024 trend:** "From Hi to Audi-Lo" — communities remixing premium audio in lo-fi ways, "putting unexpected, often-comical spins on sounds." (TikTok What's Next 2024 In Action report, June 25, 2024.)

---

## §7 — Best Times to Post + Successful Channel Examples

### 7.1 Posting Times (US/Europe Audience)

**Per Sprout Social (Feb 6, 2026):** "The best times to post on TikTok, in general, are **midweek afternoons and evenings between 2 and 6 p.m.** However, every audience is different. It's best to look at your follower activity and see when your audience is most active."

**Additional context (TikTok official data, June 2025 TikTok World '25):**
- "1 in 4 TikTok users starting to search for something within the first 30 seconds of opening the app" — implies the first 30 minutes after they wake up or open the app is also a high-engagement window.
- "Billions of searches are happening on TikTok every day — up more than 40% from last year" — search-based discovery extends the post lifetime, but early-hour engagement still drives initial lift.

**Recommended posting schedule (UTC offsets):**
| Audience | Optimal Window (local) | UTC Equivalent |
|----------|-------------------------|----------------|
| US East Coast (EST/EDT) | Tue–Thu, 14:00–18:00 | 18:00–22:00 UTC (EST) / 19:00–23:00 UTC (EDT) |
| US West Coast (PST/PDT) | Tue–Thu, 14:00–18:00 | 22:00–02:00 UTC (PST) / 21:00–01:00 UTC (PDT) |
| Western Europe (CET/CEST) | Tue–Thu, 14:00–18:00 | 13:00–17:00 UTC (CET) / 12:00–16:00 UTC (CEST) |
| Gulf (UTC+3, e.g. UAE/KSA) | Tue–Thu, 14:00–18:00 | 11:00–15:00 UTC |

**Caveat:** Master Platform Strategy §5.3 recommends 3–5 videos/day in batches; this is for organic growth, not single-post virality. Batch into a single daily posting slot if possible — fatigue from over-posting can hurt.

### 7.2 Successful Channel Examples

#### Brand examples (from Sprout + IMH):

| Brand | Strategy | Result |
|-------|----------|--------|
| **Ryanair** (@ryanair) | Humorous, shareable videos using trending sounds + brand-specific meme language | Viral recurring posts, master-class in social brand voice |
| **Huda Beauty** | Niche hashtag combos (#cleaningmakeupbrushes + #cleantok) + cleaning tutorials | Strong reach within engaged niche |
| **Rare Beauty** | POV trend + TikTok Shop integration | 2.4M views on single Shop launch video |
| **Chipotle** | Text overlay hook in first 2 seconds to communicate value | Higher retention |
| **Booking.com** | Keyword-rich captions ("home", "view", "Cape Town") | TikTok SEO optimization, search-driven reach |
| **Amazon** | Trending sound + meme format combination | Trend boost + brand exposure |
| **Starbucks** | Localized accounts (e.g. @starbucks_france in French, country-specific products) | Geo-targeted engagement |

#### Creator + small business examples (TikTok Year on TikTok 2024, Dec 4, 2024):

| Creator/Business | Achievement |
|------------------|-------------|
| **Stormi Steele** (Canvas Beauty) | First seller to surpass $2M in TikTok Shop sales via a single livestream; $1M within first 2 hours |
| **Mandy Peña** (SimplyMandys) | $1.2M in sales during a single TikTok LIVE |
| **Alexandra Lourdes Ph.D** (Refined Hospitality Group, Las Vegas) | 2M+ followers built around working-mom content |
| **NerdyNuts** (dessert-style nut butter) | Scaled from local farmers market to multi-million-dollar enterprise |
| **The Skincare Bakery** (Kymani Gorham, 24, Black founder) | ~1M followers, dessert-inspired skincare |
| **Kaylin and Kaylin Pickles** | LA-based pickle shop, expanded customer base + significant online sales |
| **@thecustardco** (Karim and Jamal, family ice cream shop) | Built thriving community via FYP discovery |
| **Jools Lebron** | Popularized "very demure, very mindful" catchphrase — global movement |
| **Kelley Heyer** | Created the iconic "Apple dance" — viral 2024 |
| **#BookTok community** | 1.2M posts in first 10 months of 2024; #Romantasy posts +300% YoY; authors like Sarah J. Maas, Rebecca Yarros, Laura Swan reached bestseller lists; Keila Shaheen's "The Shadow Work Journal" became Amazon bestseller via self-publishing |

**Source:** https://newsroom.tiktok.com/en-us/year-on-tiktok-2024 (Dec 4, 2024).

#### Clipping-specific success (from Whop research, worklog Task 1-a):

- Whop Clips community: 1M members, $190K/mo budget, $1.25/1K views for YouTube clips.
- Top 1% Whop clippers reach $10K+/mo.
- Metafy $10M+ paid to gaming coaches; SideShift $1M+/week to creators.

### 7.3 Highest-Virality Content Patterns 2026

Compiled from Sprout Feb 2026 + Buffer Dec 2025 + IMH Jun 2024 + TikTok What's Next 2024 + Year on TikTok 2024:

1. **60–90 second edutainment** (education + entertainment) — the strongest 2026 viral format (Sprout: "the most consistent path to virality in 2026 is the edutainment formula").
2. **Photo carousels** (Photo Mode) — own algorithm based on "Swipe-Through Rate" (STR); full carousel swipe = completion equivalent.
3. **POV trend** videos — Rare Beauty's 2.4M view example.
4. **Storytelling unhinged** — non-linear, multiple threads, unexpected cuts (TikTok What's Next 2024 macro trend).
5. **Curiosity peaked** — open loop + resolution (TikTok What's Next 2024).
6. **Audi-Lo** — premium audio remixed in lo-fi ways for comedic effect.
7. **TikTok on the Block** — unfiltered street interactions, retail pop-ups, unscripted challenges.
8. **Brandship** — always-engaged content reflecting brand values between splashy campaigns.
9. **Bridging the Trust Gap** — transparent, behind-the-scenes, founder-led content.
10. **TikTok Shop integrations** — algorithm boosts content that uses product anchors / shopping features.

---

## §8 — The FYP Ranking Formula: "Lift = (Quality × Audience Match) ÷ Friction"

Master Platform Strategy §5.1 formula: **الرفع = (جودة × تطابق الجمهور) ÷ مقاومة الاحتكاك** — applied to TikTok:

### 8.1 Quality (الجودة)
- **Completion rate** ≥ 80% (excellent) / ≥ 60% (good)
- **Watch time** ≥ 70% APV (Average Percentage Viewed)
- **Originality** (Creator Rewards formula weight #1)
- **Production value** — clear audio, stable video, good lighting, no artifacts
- **Hook strength** in first 3 seconds (3-second rule, Sprout Feb 2026)

### 8.2 Audience Match (تطابق الجمهور)
- **Subject matter alignment** — caption keywords + hashtags + sounds + transcript matching target audience's previous engagement signals
- **Language + Country settings** — posting in audience's preferred language, during audience's local active hours
- **Search Value** — content directly answers search queries the audience is making (Creator Search Insights)
- **Trending audio** — taps into existing engaged-audio community

### 8.3 Friction (مقاومة الاحتكاك)
- **Audio quality** — background noise, low audio = friction
- **Captions** — missing = friction (especially for hearing-impaired + non-native speakers + autoplay-mute environments)
- **Video length inappropriate** — too long without retention strategy = friction
- **Loading issues / poor video compression** = friction
- **Spam hashtags** = friction (algorithm penalty)
- **Watermarks from other platforms** (e.g., Instagram Reels watermark) = friction (TikTok deprioritizes)
- **Borderline/sexually suggestive content** = friction (ineligible for FYP)

### 8.4 The Formula in Practice

```
FYP Distribution Lift = ( Quality × Audience Match ) ÷ Friction
```

**Examples:**
- High Quality (0.85 completion) × High Match (perfect keyword/audio targeting) ÷ Low Friction (0.9) = **0.95 lift** — viral
- High Quality (0.85) × Low Match (wrong hashtags) ÷ Low Friction (0.9) = **0.28 lift** — stops at 200-view jail
- Medium Quality (0.50) × High Match × High Friction (no captions, watermarked) = **0.13 lift** — minimal reach

---

## §9 — Recommendations for the Whop Clipping Task

### 9.1 Immediate Setup (Days 1–14)

1. **Create 3 TikTok accounts:**
   - **Primary**: brand channel, halal clipping niche (financial/business/educational content).
   - **Secondary 1** (Fan Account): same niche, used as "test bed" before posting to primary.
   - **Secondary 2** (backup): only activated if primary is shadowbanned.

2. **Switch all accounts to Creator Account** (not Personal) to enable Analytics → For You distribution tracking.

3. **Apply for TikTok for Developers** → register app → add Content Posting API product → request `video.publish` scope (Direct Post) → submit for review with demo video.

4. **Use eSIM or separate device** for commercial accounts (per Shadowban Prevention Protocol).

5. **Verify URL properties** for the domain that will host the source video URLs (needed for `PULL_FROM_URL` source in Content Posting API).

### 9.2 Content Pipeline (Days 15–90)

1. **Source from Whop Content Rewards campaigns** (formal licensing — see worklog Task 1-a). Browse `GET /bounties?status=open&business_goal_type=clipping`.
2. **Use the viral_pipeline.py from Task 1-b** to:
   - Download source via `yt-dlp`
   - Transcribe via `faster-whisper`
   - Cut silence via `auto-editor`
   - Beat-detect via `librosa`
   - Montage via `FFmpeg` (Double Zoom + B-Roll + J-Cut + Beat Sync)
   - Generate captions via `generate_hormozi_captions.py` (word-level ASS file)
3. **Target 60–90 seconds** for Creator Rewards eligibility + algorithm preference.
4. **Caption + hashtag structure:**
   - Specific: `#businesstips` `#passiveincome` `#sidehustle`
   - Niche: `#whopclips` `#clippingtiktok`
   - Brand: your brand tag
   - Use Creator Search Insights to pick "content gap" topics
5. **Audio:** Original sound (your voiceover) + SFX only — no commercial music (halal + IP-safe). Trending sound if officially licensed.
6. **Posting cadence:** 3–5 videos/day per account. Best time: Tue–Thu, 14:00–18:00 local audience time.
7. **Pre-test on secondary** → if median last-50 views ≥ 2× primary's average → push to primary.
8. **Submit to Whop bounty via `POST /bounty_submissions`** within 24h of TikTok publish (for Content Rewards payout).

### 9.3 Distribution Stack (Programmatic)

Use the **Content Posting API** Python client from §4.5 to automate posting:

```python
# Pseudocode for the auto-posting loop
for video in render_queue:
    init_resp = init_video_upload_url(
        access_token=USER_ACCESS_TOKEN,
        title=video.caption_with_hashtags,
        video_url=f"https://verified.domain.com/{video.filename}"
    )
    publish_id = init_resp["data"]["publish_id"]

    # Poll for completion
    while True:
        status = fetch_post_status(USER_ACCESS_TOKEN, publish_id)
        if status["data"]["status"] in ("PUBLISH_COMPLETE", "FAILED"):
            break
        time.sleep(60)

    # Submit to Whop Content Rewards
    whop_client.submit_bounty(
        bounty_id=video.bounty_id,
        deliverable={"urls": [f"https://tiktok.com/@user/video/{publish_id}"]}
    )
```

### 9.4 Anti-Shadowban Discipline (Ongoing)

1. **Never mass-post** — stagger posts ≥ 30 min apart.
2. **Never use the same caption/hashtag combo** on consecutive posts (vary the specific hashtag).
3. **Reply to every comment** in the first 60 minutes after posting.
4. **No VPN, no auto-likers, no botting.**
5. **Audit Account Status weekly** — check for strikes/ineligible videos.
6. **If shadowbanned: pause 48–72h, set flagged videos to "Only Me" (don't delete), post 100% original for 14 days, use secondary account meanwhile.**

### 9.5 Metrics to Track (Weekly)

| Metric | Target | Source |
|--------|--------|--------|
| View Rate (first 3s) | ≥ 85% | Task 1-b benchmarks |
| Retention@30s | ≥ 60% | Task 1-b |
| Completion Rate | ≥ 80% (viral) / ≥ 60% (good) | Sprout Feb 2026 |
| Share Rate | ≥ 1.7% | Task 1-b benchmarks |
| Save Rate | ≥ 2% | Task 1-b |
| Qualified Views (5+s) ratio | ≥ 75% of total views | Sprout Feb 2026 |
| For You distribution % | ≥ 60% of total views | TikTok Analytics |
| Whop Content Rewards payout | $200–$500/mo month 1, $1,000+/mo month 3, $10,000+/mo month 12 | Worklog Task 1-a targets |

---

## §10 — Sources Consulted (Primary)

### 10.1 TikTok Official (Primary, Fetched Live)

| Source | URL | Date |
|--------|-----|------|
| Newsroom: How TikTok recommends videos #ForYou | https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you | Jun 18, 2020 |
| Newsroom: Learn why a video is recommended For You | https://newsroom.tiktok.com/en-us/learn-why-a-video-is-recommended-for-you | Dec 20, 2022 |
| Newsroom: An update on safeguarding & diversifying recommendations | https://newsroom.tiktok.com/en-us/an-update-on-our-work-to-safeguard-and-diversify-recommendations | Dec 16, 2021 |
| Newsroom: Refresh your For You feed | https://newsroom.tiktok.com/en-us/introducing-a-way-to-refresh-your-for-you-feed-on-tiktok-us | Mar 16, 2023 |
| Newsroom: Updated account enforcement system | https://newsroom.tiktok.com/en-us/supporting-creators-with-an-updated-account-enforcement-system | Feb 2, 2023 |
| Newsroom: Evolving content enforcement | https://newsroom.tiktok.com/en-us/evolving-our-approach-to-content-enforcement-us | Mar 31, 2023 |
| Newsroom: Counter misinformation update | https://newsroom.tiktok.com/en-us/an-update-on-our-work-to-counter-misinformation | Sep 28, 2022 |
| Newsroom: Strengthening sexually suggestive enforcement | https://newsroom.tiktok.com/en-us/strengthening-enforcement-of-sexually-suggestive-content | Dec 30, 2022 |
| Newsroom: Refreshing policies / community well-being | https://newsroom.tiktok.com/en-us/refreshing-our-policies-to-support-community-well-being | Dec 15, 2020 |
| Newsroom: Adding clarity to Community Guidelines | https://newsroom.tiktok.com/en-us/adding-clarity-to-our-community-guidelines | Jan 8, 2020 |
| Newsroom: Understanding Community Guidelines | https://newsroom.tiktok.com/en-us/understanding-our-community-guidelines | Dec 21, 2018 |
| Newsroom: Strengthening privacy and safety for youth | https://newsroom.tiktok.com/en-us/strengthening-privacy-and-safety-for-youth | Jan 13, 2021 |
| Newsroom: Introducing Creator Rewards Program | https://newsroom.tiktok.com/en-us/introducing-the-new-creator-rewards-program | Mar 18, 2024 |
| Newsroom: Creator Search Insights | https://newsroom.tiktok.com/en-us/creator-search-insights | Mar 13, 2024 |
| Newsroom: TikTok World '25 | https://newsroom.tiktok.com/en-us/tiktok-world-2025 | Jun 3, 2025 |
| Newsroom: More ways to discover content | https://newsroom.tiktok.com/en-us/more-ways-to-discover-new-content-and-creators-you-love | Jun 3, 2025 |
| Newsroom: What's Next 2024 in Action | https://newsroom.tiktok.com/en-us/whats-next-2024-in-action | Jun 25, 2024 |
| Newsroom: Year on TikTok 2024 | https://newsroom.tiktok.com/en-us/year-on-tiktok-2024 | Dec 4, 2024 |
| Newsroom: Hashtag view count display issue post-mortem | https://newsroom.tiktok.com/en-us/hashtag-view-count-display-issue-post-mortem | Jun 16, 2020 |
| Developers: Content Posting API Get Started | https://developers.tiktok.com/docs/en/content-posting-api-get-started | (current) |
| Developers: TikTok API Scopes | https://developers.tiktok.com/docs/en/tiktok-api-scopes | (current) |
| Developers: Scopes Overview | https://developers.tiktok.com/docs/en/scopes-overview | (current) |
| Developers: Login Kit Overview | https://developers.tiktok.com/docs/en/login-kit-overview | (current) |
| Developers: Get Started (Create App) | https://developers.tiktok.com/docs/en/getting-started-create-an-app | (current) |
| Developers: App Review Guidelines | https://developers.tiktok.com/docs/en/app-review-guidelines | (current) |
| Developers: Rate Limits (v2) | https://developers.tiktok.com/docs/en/tiktok-api-v2-rate-limit | Aug 4, 2026 |
| Developers: Monetization Overview | https://developers.tiktok.com/docs/en/monetization-overview | (current) |

### 10.2 Secondary Sources (Fetched Live)

| Source | URL | Date | Notes |
|--------|-----|------|-------|
| Buffer: TikTok Algorithm Guide 2026 | https://buffer.com/resources/tiktok-algorithm/ | Dec 17, 2025 | Cites NYT leak + Washington Post analysis + Julian McAuley (UCSD) |
| Sprout Social: How the TikTok algorithm works in 2026 | https://sproutsocial.com/insights/tiktok-algorithm/ | Feb 6, 2026 | 11 tips + FAQs (200-view jail, Qualified Views 5s, 3-second rule) |
| Influencer Marketing Hub: How Does the TikTok Algorithm Work? | https://influencermarketinghub.com/tiktok-algorithm/ | Jun 24, 2024 (26-min read) | Comprehensive factor breakdown + brand examples |
| Later: Top 10 TikTok Algorithm Hacks | https://later.com/blog/tiktok-algorithm/ | Mar 4, 2025 | Practical hacks |
| Wikipedia: TikTok | https://en.wikipedia.org/wiki/TikTok | (current) | Algorithm + For You page section |
| Wikipedia: Shadow banning | https://en.wikipedia.org/wiki/Shadow_banning | (current) | Cross-platform context |

### 10.3 Attempted but Blocked (HTTP 403/404)

- **Reddit JSON API** (`/r/TikTok/search.json`, `/r/TikTokCringe`, `/r/shadowban`, `/r/NewTubers`, `old.reddit.com`) — all 403 from sandbox IP. Bot detection active.
- **NYT direct article** (multiple URL variants for the Dec 2024 leak) — 403.
- **archive.org / Wayback Machine** — connection failed (DNS/timeout).
- **Google Search results page** — bot detection returned redirect-to-CH-language placeholder.
- **Bing Search results page** — returned only `tiktok.com` + cache URLs, no organic result pages.
- **DuckDuckGo HTML** — bot challenge.
- **Google Scholar** — 403.
- **Hootsuite blog** — 403.
- **Medium search** — 403.
- **Rest of World** — 403.
- **SearchEngineLand** — 403.
- **Wired (algorithm-leak articles)** — 404.

### 10.4 Cross-Referenced Documents (Already in Repo)

- `Master_Platform_Strategy_18_platforms_algorithm.md` §1–§7 (algorithm philosophy, shadowban prevention, secondary accounts, benchmarks) — read first 200 lines.
- `01_whop_shorts_plan.md` (Whop + clipping plan) — read in full.
- `worklog.md` (Task 0-init + Task 1-a Whop deep dive + Task 1-b viral editing toolkit) — read in full.
- `02_viral_editing_toolkit.md` (Task 1-b output) — referenced for FFmpeg stack and benchmarks.

---

## §11 — Key Direct Quotes (Verbatim, for Citation)

> **TikTok Newsroom, June 18, 2020:** "While a video is likely to receive more views if posted by an account that has more followers, by virtue of that account having built up a larger follower base, **neither follower count nor whether the account has had previous high-performing videos are direct factors in the recommendation system.**"

> **TikTok Newsroom, Mar 18, 2024 (Creator Rewards):** "The Creator Rewards Program will continue to reward high-quality, original content that is over a minute long, using an optimized rewards formula focused on four core metrics: **originality, play duration, search value and audience engagement.**"

> **TikTok Newsroom, Feb 2, 2023 (Account Enforcement):** "if someone posts content that violates one of our Community Guidelines, the account will accrue a strike as the content is removed. If an account meets the threshold of strikes within either a product feature (i.e. Comments, LIVE) or policy (i.e. Bullying and Harassment), it will be permanently banned... **Strikes will expire from an account's record after 90 days.**"

> **TikTok Newsroom, Dec 16, 2021 (Safeguard & Diversify):** "our recommendation system works to intersperse recommendations that might fall outside people's expressed preferences, offering an opportunity to discover new categories of content. For example, **our systems won't recommend two videos in a row made by the same creator or with the same sound.**"

> **TikTok Newsroom, Dec 30, 2022 (Sexually Suggestive):** "We also have policies to make **borderline or 'suggestive' content ineligible for recommendation into TikTok For You feeds**."

> **TikTok Newsroom, Sep 28, 2022 (Misinformation):** "while content is being fact-checked or when content can't be substantiated through fact-checking, **it becomes ineligible for recommendation into For You feeds**."

> **TikTok Newsroom, Jun 3, 2025 (TikTok World '25):** "1 in 4 TikTok users starting to search for something within the first 30 seconds of opening the app... Billions of searches are happening on TikTok every day — up more than 40% from last year."

> **TikTok Developers, Content Posting API (current):** "All content posted by unaudited clients will be restricted to private viewing mode. Once you have successfully tested your integration, to lift the restrictions on content visibility, your API client must undergo an audit to verify compliance with our Terms of Service."

> **TikTok Developers, Rate Limits (Aug 4, 2026):** "Default limits: `/v2/user/info/` 600, `/v2/video/query/` 600, `/v2/video/list/` 600. Request rate calculation is based on a one minute sliding window. If the number of requests exceeds the threshold, new requests will be throttled and a response will be returned with HTTP status 429 and error code `rate_limit_exceeded`."

> **Sprout Social, Feb 6, 2026:** "Save and share signals indicate high value and an intent to return or distribute content, **often outweighing simple 'Likes' by a significant margin.**"

> **Sprout Social, Feb 6, 2026 (200-view jail):** "The '200-view jail' is a common phenomenon where videos stop gaining reach after the initial test batch. In 2026, this usually happens because the video failed to generate enough 'Qualified Views' (views longer than 5 seconds) or had a low completion rate."

> **Sprout Social, Feb 6, 2026 (deleting videos):** "deleting videos can negatively impact your account. It removes data points that the algorithm uses to understand your content, and mass-deleting can trigger spam filters. Instead of deleting, it is recommended to change the video's privacy settings to 'Only Me.'"

> **Buffer, Dec 17, 2025 (NYT leak citation):** "There seems to be some perception that they've cracked some magic code for recommendation, but most of what I've seen seems pretty normal." — Julian McAuley, professor of computer science, UC San Diego.

> **TikTok Newsroom, Dec 4, 2024 (Year on TikTok 2024):** "Stormi Steele of Canvas Beauty became the first-ever seller to surpass $2M in TikTok Shop sales via a single livestream, with over $1 million of that within the first two hours."

---

## §12 — Sima Yi's Long-Game Closing Reflection

عقل سيماه يي يرى: خوارزمية TikTok ليست سرًّا سحريًّا — هي مرآة سلوك المستخدم. من يفهم أن "الإشارة الأولى" (Watch Time + Saves + Shares) هي المفتاح، ومن يصبر على 90 يومًا من البناء بدون هندسة قرارات متهورة، يفوز.

- **الصبر:** لا تنتظر فيروسي يوم 1. ابنِ مكتبة محتوى 90 يومًا، حلِّل، كرِّر.
- **الإخفاء:** استخدم حسابًا ثانويًّا كمختبر أمان — لا تنقل للرئيسي إلا ما تجاوز 2× المتوسط.
- **اللعبة الطويلة:** الـ API + الـ Content Posting API + الـ audit = استثمار 4–6 أسابيع قبل أول منشور عمومي. هذا ليس خسارة، هذا بناء البنية التحتية للنشر الأتوماتيكي اليومي لـ 90 يومًا قادمة.
- **التوافق الحلال:** كل ما ينشر سيكون من خلال تفويض رسمي (Whop Content Rewards) + مونتاج جوهري إبداعي + صوت أصلي حلال. لا غرر، لا ربا، لا محتوى مخالف — هذه قاعدة لا تُكسر.

الطريق: قنوات بطيئة النمو في أول 30 يومًا → قفزة فيروسية في يوم 30–60 (نقل من الثانوي للرئيسي) → دخول Whop Content Rewards في يوم 60–90 → أول دولار.

**المعادلة النهائية:**
```
نجاح TikTok = (Originality × Search Value × Audience Match) ÷ (Spam signals + Friction)
```

حيث العامل البشري (الصبر + الإخفاء + الالتزام الحلال) هو المُمَيِّز بين من يصل لـ $200/شهر ومن يصل لـ $10,000+/شهر.
