#!/usr/bin/env bash
# ============================================================
# NutriTrack Setup Script
# Run this to initialize the project after installing Django
# ============================================================

set -e  # Exit on any error

echo ""
echo "  🥗 NutriTrack Setup"
echo "  ==================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "🗃️  Running migrations..."
python3 manage.py makemigrations accounts meals calculator
python3 manage.py migrate

echo ""
echo "🌱 Loading food database..."
python3 manage.py loaddata meals/fixtures/foods.json

echo ""
echo "👤 Creating superuser..."
echo "   (You can skip this and create it manually with: python manage.py createsuperuser)"
read -p "   Create superuser now? (y/n): " CREATE_SUPER
if [[ "$CREATE_SUPER" == "y" || "$CREATE_SUPER" == "Y" ]]; then
    python3 manage.py createsuperuser
fi

echo ""
echo "📁 Collecting static files..."
python3 manage.py collectstatic --noinput 2>/dev/null || true

echo ""
echo "  ✅ Setup Complete!"
echo "  ==================="
echo ""
echo "  🚀 Start the server:"
echo "     python3 manage.py runserver"
echo ""
echo "  🌐 Open in browser:"
echo "     http://127.0.0.1:8000/"
echo ""
echo "  🔧 Admin panel:"
echo "     http://127.0.0.1:8000/admin/"
echo ""
