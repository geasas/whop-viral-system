#!/bin/bash
# Quick Start — Whop Viral System
# Run this after cloning the repo for first-time setup.

set -e
cd "$(dirname "$0")/.."

echo "🎬 Whop Viral System — Quick Start"
echo "=================================="

# 1. Check Python
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 not found. Install Python 3.10+."
    exit 1
fi
PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info[0]}.{sys.version_info[1]}")')
echo "✓ Python $PY_VERSION"

# 2. Check FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "✗ FFmpeg not found. Install:"
    echo "  Ubuntu: sudo apt install ffmpeg"
    echo "  macOS: brew install ffmpeg"
    exit 1
fi
echo "✓ FFmpeg $(ffmpeg -version 2>&1 | head -1 | awk '{print $3}')"

# 3. Create venv
if [ ! -d "venv" ]; then
    echo "→ Creating Python virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate

# 4. Install Python deps
echo "→ Installing Python dependencies..."
pip install --upgrade pip -q
pip install -r scripts/requirements.txt -q

# 5. Install yt-dlp
echo "→ Installing yt-dlp..."
pip install -U yt-dlp -q

# 6. Create .env from template
if [ ! -f ".env" ]; then
    echo "→ Creating .env from template..."
    cp scripts/.env.template .env
    echo "✓ Created .env — fill in your tokens before running!"
else
    echo "✓ .env already exists"
fi

# 7. Create directories
mkdir -p logs assets/broll assets/nasheed assets/templates .credentials
echo "✓ Created directories"

# 8. Download Whisper models (optional, saves time later)
echo "→ Downloading Whisper tiny model (75MB)..."
python -c "from faster_whisper import WhisperModel; WhisperModel('tiny', device='cpu')" 2>&1 | tail -1 || true

# 9. Verify installation
echo ""
echo "→ Verifying installation..."
python -c "
import sys
print(f'Python: {sys.version_info[0]}.{sys.version_info[1]}')
try:
    import faster_whisper; print(f'faster-whisper: OK')
except: print('faster-whisper: ✗')
try:
    import yt_dlp; print(f'yt-dlp: OK')
except: print('yt-dlp: ✗')
try:
    import ffmpeg; print(f'ffmpeg-python: OK')
except: print('ffmpeg-python: ✗')
try:
    import moviepy; print(f'moviepy: OK')
except: print('moviepy: ✗')
try:
    import librosa; print(f'librosa: OK')
except: print('librosa: ✗')
"

# 10. Run health check
echo ""
echo "→ Health check..."
if [ -f scripts/health_check.py ]; then
    python scripts/health_check.py 2>&1 || echo "✗ Health check failed — see above"
fi

# 11. Final instructions
echo ""
echo "=================================="
echo "✓ Quick Start complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env and fill in your tokens:"
echo "     nano .env"
echo ""
echo "  2. Activate venv:"
echo "     source venv/bin/activate"
echo ""
echo "  3. Test scripts individually:"
echo "     python scripts/download_source.py --help"
echo "     python scripts/transcribe.py --help"
echo "     python scripts/viral_edit.py --help"
echo ""
echo "  4. Run daily pipeline:"
echo "     bash scripts/daily_pipeline.sh"
echo ""
echo "  5. Set up cron (optional):"
echo "     crontab -e"
echo "     Add: 0 6 * * * cd $(pwd) && bash scripts/daily_pipeline.sh >> logs/cron.log 2>&1"
echo ""
echo "📖 Read MASTER.md for full instructions."
