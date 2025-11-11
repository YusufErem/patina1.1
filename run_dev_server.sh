#!/bin/bash

# Development server runner script
# Bypasses system HTTPS enforcement

echo "🚀 Starting Patina Cappadocia Development Server"
echo "=================================================="
echo ""
echo "✓ DEBUG mode enabled"
echo "✓ HTTPS redirects disabled"
echo "✓ Security headers disabled for development"
echo ""
echo "Access at: http://127.0.0.1:8000"
echo "Admin at:  http://127.0.0.1:8000/admin"
echo ""
echo "Press CTRL+C to stop"
echo "=================================================="
echo ""

# Export environment variables
export DEBUG=True
export PYTHONUNBUFFERED=1

# Run Django development server
python manage.py runserver 127.0.0.1:8000 --nothreading --noreload
