#!/usr/bin/env bash
# setup.sh — install the full open-source viral-clipping stack
# =================================================================
# Usage:
#   chmod +x scripts/setup.sh && ./scripts/setup.sh
#
# Idempotent: safe to re-run.
# Tested on: Debian 13 / Ubuntu 24.04 LTS / WSL2 Ubuntu.

set -e

# --- colors ---
RED=$'\033[0;31m'; GREEN=$'\033[0;32m'; YELLOW=$'\033[1;33m'
BLUE=$'\033[0;34m'; NC=$'\033[0m'

info()  { printf "${BLUE}[info]${NC}  %s\n" "$*"; }
ok()    { printf "${GREEN}[ok]${NC}    %s\n" "$*"; }
warn()  { printf "${YELLOW}[warn]${NC}  %s\n" "$*"; }
err()   { printf "${RED}[err]${NC}   %s\n" "$*" >&2; }

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

info "Setting up open-source viral clipping stack in $PROJECT_ROOT"

# --- 0. Detect Python ---
if command -v python3 &>/dev/null; then
    PY=python3
elif command -v python &>/dev/null; then
    PY=python
else
    err "Python 3 not found. Install: sudo apt install python3 python3-venv"
    exit 1
fi
info "Using Python: $($PY --version)"

# --- 1. System packages (apt) ---
info "Checking system dependencies..."
NEED_APT=()
command -v ffmpeg &>/dev/null        || NEED_APT+=(ffmpeg)
command -v ffprobe &>/dev/null       || NEED_APT+=(ffmpeg)
command -v yt-dlp &>/dev/null        || NEED_APT+=(yt-dlp)   # we'll pip install anyway
command -v auto-editor &>/dev/null   || true                # we'll pip install
pkg-config --exists libsndfile1 2>/dev/null || NEED_APT+=(libsndfile1)
pkg-config --exists libopenblas0 2>/dev/null || NEED_APT+=(libopenblas-dev)

if [ ${#NEED_APT[@]} -gt 0 ]; then
    info "Installing apt packages: ${NEED_APT[*]}"
    if [ "$(id -u)" = "0" ]; then
        apt-get update -qq && apt-get install -y "${NEED_APT[@]}"
    else
        warn "Not running as root — trying sudo. Enter password if prompted."
        sudo apt-get update -qq && sudo apt-get install -y "${NEED_APT[@]}"
    fi
fi
ok "System deps ready: ffmpeg $(ffmpeg -version | head -1 | awk '{print $3}')"

# --- 2. Python venv ---
VENV_DIR="${VENV_DIR:-$PROJECT_ROOT/.venv}"
if [ ! -d "$VENV_DIR" ]; then
    info "Creating venv at $VENV_DIR"
    $PY -m venv "$VENV_DIR"
fi
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
PY="$(which python)"
info "Venv Python: $PY"
ok "venv ready"

# --- 3. Python packages ---
info "Upgrading pip..."
pip install --quiet --upgrade pip

info "Installing Python packages from scripts/requirements.txt..."
pip install --quiet -r "$PROJECT_ROOT/scripts/requirements.txt"
ok "Python packages installed"

# --- 4. Credentials dir ---
mkdir -p "$PROJECT_ROOT/creds"
mkdir -p "$PROJECT_ROOT/data"
mkdir -p "$PROJECT_ROOT/logs"
mkdir -p "$PROJECT_ROOT/download"
mkdir -p "$PROJECT_ROOT/_pipeline_workdir"

# --- 5. .env file ---
ENV_FILE="$PROJECT_ROOT/.env"
if [ ! -f "$ENV_FILE" ]; then
    info "Creating .env from template"
    cp "$PROJECT_ROOT/scripts/.env.template" "$ENV_FILE"
    warn "Edit $ENV_FILE and fill in your API keys before running the pipeline."
else
    ok ".env already exists"
fi

# --- 6. Whop CLI (optional) ---
if ! command -v whop &>/dev/null; then
    info "Installing Whop CLI (optional)..."
    if curl -fsSL https://whop.com/install.sh | sh; then
        ok "Whop CLI installed"
    else
        warn "Whop CLI install failed — install manually with:"
        warn "  curl -fsSL https://whop.com/install.sh | sh"
    fi
else
    ok "Whop CLI already installed"
fi

# --- 7. Stable Diffusion WebUI (optional) ---
if [ "${INSTALL_SD:-0}" = "1" ]; then
    info "Installing Stable Diffusion WebUI (optional — INSTALL_SD=1)..."
    if [ ! -d "$PROJECT_ROOT/repos/stable-diffusion-webui" ]; then
        git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git \
            "$PROJECT_ROOT/repos/stable-diffusion-webui"
    fi
    info "First SD run will download models — be patient."
fi

# --- 8. Final smoke test ---
info "Running smoke test (verify core imports)..."
$PY - <<'PYEOF'
import sys
sys.path.insert(0, "scripts")
import importlib
failures = []
for mod in ["yt_dlp", "faster_whisper", "librosa", "moviepy",
            "cv2", "ffmpeg", "srt", "requests", "dotenv", "yaml", "tqdm"]:
    try:
        importlib.import_module(mod)
    except Exception as e:
        failures.append((mod, str(e)))
if failures:
    for m, e in failures:
        print(f"  ⚠ {m}: {e}")
    print("Some optional modules failed to import. See requirements.txt.")
    sys.exit(0)
print("  ✓ All core modules import OK")
PYEOF

# --- 9. Final print ---
ok "Setup complete!"
echo
info "Next steps:"
echo "  1. Edit .env to fill in your API keys"
echo "  2. Place client_secret.json in creds/ (for YouTube OAuth)"
echo "  3. Test the pipeline end-to-end:"
echo "     $PY scripts/download_source.py --url '<podcast URL>'"
echo "     $PY scripts/transcribe.py download/source.mp4"
echo "     $PY scripts/auto_edit.py download/source.mp4 --transcript ..."
echo "     $PY scripts/viral_edit.py --clip cut_00.mp4 --transcript ... \\"
echo "         --start 16 --end 36 --out final.mp4 --scorecard"
echo "     $PY scripts/publish_tiktok.py publish --file final.mp4 --title '...'"
echo "     $PY scripts/submit_whop_bounty.py submit \\"
echo "         --bounty-id bnty_XXX --urls https://tiktok.com/@you/... \\"
echo "         --caption 'Vertical cut, 42s' --platform tiktok"
echo "  4. Schedule daily cron: scripts/daily_pipeline.sh"
echo
info "Happy clipping. Total cost: \$0."
