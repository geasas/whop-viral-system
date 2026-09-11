#!/usr/bin/env bash
# daily_pipeline.sh — Cron-driven daily pipeline for the open-source stack
# =========================================================================
# Schedule (UTC — optimised for US + EU audience):
#   08:00 UTC — download phase (low traffic)
#   09:00-11:00 UTC — montage phase (3-5 clips)
#   12:00 UTC — publish TikTok + IG (US morning / EU afternoon peak)
#   18:00 UTC — publish YouTube Shorts (US afternoon peak)
#   22:00 UTC — analytics pull + Whop bounty submission reconciliation
#
# Install in cron (run as: crontab -e):
#   0 8  * * * /home/z/my-project/scripts/daily_pipeline.sh download  >> /home/z/my-project/logs/cron.log 2>&1
#   0 9  * * * /home/z/my-project/scripts/daily_pipeline.sh montage   >> /home/z/my-project/logs/cron.log 2>&1
#   0 12 * * * /home/z/my-project/scripts/daily_pipeline.sh publish_shorts  >> /home/z/my-project/logs/cron.log 2>&1
#   0 18 * * * /home/z/my-project/scripts/daily_pipeline.sh publish_youtube >> /home/z/my-project/logs/cron.log 2>&1
#   0 22 * * * /home/z/my-project/scripts/daily_pipeline.sh analytics  >> /home/z/my-project/logs/cron.log 2>&1
#   0 8  * * * /home/z/my-project/scripts/daily_pipeline.sh full       >> /home/z/my-project/logs/cron.log 2>&1
#
# Or run manually: ./daily_pipeline.sh full

set -e

# --- load .env ---
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"
[ -f .env ] && set -a && source .env && set +a

# --- python interpreter ---
PY="${PY:-/home/z/.venv/bin/python}"
if [ ! -x "$PY" ]; then
    PY="python3"
fi
if [ -z "$(command -v $PY)" ]; then
    echo "Python interpreter not found: $PY" >&2; exit 1
fi

# --- paths ---
LOG_DIR="$PROJECT_ROOT/logs"
mkdir -p "$LOG_DIR"
WORKDIR="$PROJECT_ROOT/_pipeline_workdir"
DOWNLOAD_DIR="$PROJECT_ROOT/download"
TODAY=$(date -u +%Y-%m-%d)
LOG_FILE="$LOG_DIR/pipeline_${TODAY}.log"
STATE_FILE="$PROJECT_ROOT/_pipeline_state.json"

# --- logging helpers ---
log()  { printf "[%s] [info] %s\n" "$(date -u +'%H:%M:%S')" "$*" | tee -a "$LOG_FILE"; }
warn() { printf "[%s] [warn] %s\n" "$(date -u +'%H:%M:%S')" "$*" | tee -a "$LOG_FILE"; }
err()  { printf "[%s] [err]  %s\n" "$(date -u +'%H:%M:%S')" "$*" | tee -a "$LOG_FILE" >&2; }

# --- state helpers (json file) ---
state_get() {
    [ -f "$STATE_FILE" ] || echo "{}" > "$STATE_FILE"
    $PY -c "import json,sys; d=json.load(open('$STATE_FILE')); print(d.get('$1',''))" 2>/dev/null
}
state_set() {
    [ -f "$STATE_FILE" ] || echo "{}" > "$STATE_FILE"
    $PY -c "
import json
d=json.load(open('$STATE_FILE'))
d['$1'] = '$2'
json.dump(d, open('$STATE_FILE','w'), indent=2)
"
}

# --- phases ---
phase_download() {
    log "=== Phase: Download ==="
    # Pull open clipping bounties from Whop
    if [ -z "${WHOP_USER_TOKEN:-}" ] && [ -z "${WHOP_ACCOUNT_KEY:-}" ]; then
        warn "WHOP_USER_TOKEN / WHOP_ACCOUNT_KEY not set — skipping bounty discovery"
        return 0
    fi
    $PY scripts/submit_whop_bounty.py list \
        --business-goal clipping --status open \
        --order gross_paid_out_amount --direction desc \
        2>&1 | tee -a "$LOG_FILE" || warn "Whop list failed"

    # TODO: For each top bounty with asset links, download via yt-dlp.
    # In this template we demonstrate the structure; in production, parse
    # the bounty list output and feed URLs into download_source.py:
    #
    #   for url in $(jq -r '.data[].deliverable.asset_links[0].url' \
    #                <(whop bounties list --format=json | jq ...)); do
    #     $PY scripts/download_source.py --url "$url" \
    #         --out "$DOWNLOAD_DIR/$(basename $url)"
    #   done

    state_set last_download "$TODAY"
    log "Download phase complete"
}

phase_montage() {
    log "=== Phase: Montage ==="
    # Find today's downloaded sources
    for src in "$DOWNLOAD_DIR"/*.mp4; do
        [ -f "$src" ] || continue
        log "Processing $src..."
        base=$(basename "$src" .mp4)
        # Step 1: Transcribe (uses cache if same file already transcribed)
        $PY scripts/transcribe.py "$src" \
            --out-dir "$WORKDIR/transcripts/$TODAY" \
            --model "${WHISPER_MODEL_SIZE:-small}" 2>&1 | tee -a "$LOG_FILE" \
            || { err "transcribe failed for $src"; continue; }
        transcript="$WORKDIR/transcripts/$TODAY/$base.words.json"

        # Step 2: Auto-edit (silence removal + viral segment detection)
        $PY scripts/auto_edit.py "$src" \
            --transcript "$transcript" \
            --out-dir "$WORKDIR/auto/$TODAY/$base" \
            --top-k "${PIPELINE_TOP_K:-5}" \
            --min-score 3.0 \
            --min-dur 15 --max-dur 75 2>&1 | tee -a "$LOG_FILE" \
            || { err "auto_edit failed for $src"; continue; }

        # Step 3: For each cut, run viral_edit.py with scorecard gate
        cuts_dir="$WORKDIR/auto/$TODAY/$base/$base.cuts"
        [ -d "$cuts_dir" ] || continue
        for cut in "$cuts_dir"/*.mp4; do
            [ -f "$cut" ] || continue
            # Extract start/end from filename (cut_NN_START-END.mp4)
            fname=$(basename "$cut" .mp4)
            times=${fname##*_}  # e.g. "16-36"
            start=${times%-*}
            end=${times#*-}
            final="$WORKDIR/final/$TODAY/${base}_$(basename $cut)"
            mkdir -p "$(dirname "$final")"
            $PY scripts/viral_edit.py \
                --clip "$cut" \
                --transcript "$transcript" \
                --start "$start" --end "$end" \
                --out "$final" --scorecard 2>&1 | tee -a "$LOG_FILE" \
                || { warn "viral_edit/scorecard rejected $cut (likely <5/6 score)"; continue; }
        done
    done
    state_set last_montage "$TODAY"
    log "Montage phase complete"
}

phase_publish_shorts() {
    log "=== Phase: Publish to TikTok + IG ==="
    final_dir="$WORKDIR/final/$TODAY"
    [ -d "$final_dir" ] || { warn "No final videos today"; return 0; }
    for v in "$final_dir"/*.mp4; do
        [ -f "$v" ] || continue
        title=$(basename "$v" .mp4 | sed 's/_/ /g')  # placeholder title
        # TikTok
        if [ -n "${TIKTOK_ACCESS_TOKEN:-}" ]; then
            $PY scripts/publish_tiktok.py publish \
                --file "$v" \
                --title "${title} #fyp #whopclips #shorts" \
                2>&1 | tee -a "$LOG_FILE" \
                || err "tiktok publish failed for $v"
        else
            warn "TIKTOK_ACCESS_TOKEN not set — skipping TikTok"
        fi
        # Instagram (needs public URL — can't directly upload local file)
        if [ -n "${IG_ACCESS_TOKEN:-}" ]; then
            warn "IG requires public URL — skipping direct upload. Upload to CDN first."
            # Example: upload to your S3/R2/S3 bucket → IG
        fi
    done
    state_set last_publish_shorts "$TODAY"
    log "Publish shorts phase complete"
}

phase_publish_youtube() {
    log "=== Phase: Publish to YouTube Shorts ==="
    final_dir="$WORKDIR/final/$TODAY"
    [ -d "$final_dir" ] || { warn "No final videos today"; return 0; }
    for v in "$final_dir"/*.mp4; do
        [ -f "$v" ] || continue
        title=$(basename "$v" .mp4 | sed 's/_/ /g')
        # AI content disclosure (set --synthetic if used SD-generated B-roll)
        synthetic_flag=""
        [ "${USE_SYNTHETIC_MEDIA:-0}" = "1" ] && synthetic_flag="--synthetic"
        $PY scripts/publish_youtube.py publish \
            --file "$v" \
            --title "${title} #shorts #whopclips" \
            --tags "shorts,ytshorts,whopclips,clipping" \
            --no-notify $synthetic_flag \
            2>&1 | tee -a "$LOG_FILE" \
            || err "youtube publish failed for $v"
    done
    state_set last_publish_youtube "$TODAY"
    log "Publish YouTube phase complete"
}

phase_analytics() {
    log "=== Phase: Analytics + Whop Submit ==="
    $PY scripts/analytics_dashboard.py pull \
        2>&1 | tee -a "$LOG_FILE" \
        || warn "analytics pull failed"
    $PY scripts/analytics_dashboard.py summary \
        2>&1 | tee -a "$LOG_FILE"
    state_set last_analytics "$TODAY"
    log "Analytics phase complete"
}

# --- top-level dispatcher ---
case "${1:-all}" in
    download)         phase_download ;;
    montage)          phase_montage ;;
    publish_shorts)  phase_publish_shorts ;;
    publish_youtube) phase_publish_youtube ;;
    analytics)       phase_analytics ;;
    full)
        log "Running FULL daily pipeline for $TODAY"
        phase_download
        phase_montage
        phase_publish_shorts
        phase_publish_youtube
        phase_analytics
        log "Daily pipeline complete"
        ;;
    *)
        echo "Usage: $0 {download|montage|publish_shorts|publish_youtube|analytics|full}"
        exit 1
        ;;
esac
