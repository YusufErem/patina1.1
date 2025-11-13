#!/bin/bash
# Günlük Google yorumlarını çekmek için cron script
# Kullanım: Bu script'i crontab'a ekleyin veya scheduled task olarak çalıştırın
# Örnek crontab: 0 2 * * * /path/to/fetch_reviews_daily.sh

# Script'in bulunduğu dizini al
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Python virtual environment aktif et (eğer varsa)
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Django management command'ını çalıştır
python manage.py fetch_google_reviews

# Çıkış kodu kontrolü
if [ $? -eq 0 ]; then
    echo "$(date): Google yorumları başarıyla çekildi"
else
    echo "$(date): Google yorumları çekilirken hata oluştu" >&2
    exit 1
fi

