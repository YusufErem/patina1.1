# Development & Deployment Guide

## Development Server Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Database Migrations
```bash
python manage.py migrate
```

### 3. Load Sample Data (Optional - for testing)
```bash
# Load sample Google reviews
python manage.py load_sample_reviews

# Load sample homepage images and about sections
python manage.py load_sample_content
```

### 4. Create Admin User (First Time Only)
```bash
python manage.py createsuperuser
```

### 5. Run Development Server
```bash
python manage.py runserver 0.0.0.0:8000
```

Then visit: `http://127.0.0.1:8000`

---

## Admin Panel Access

After creating a superuser:
1. Go to: `http://127.0.0.1:8000/admin`
2. Login with your credentials
3. Manage:
   - **Google Reviews** - Mark as featured, control display order
   - **HomePage Images** - Upload slider images, manage sections
   - **About Sections** - Edit multi-language content and images
   - **Rooms** - Manage room categories, images, and features

---

## Google Reviews Integration

### Option 1: Using Real Google Reviews

#### Get API Key:
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable "Places API"
4. Create "Service Account" credentials
5. Copy the API key

#### Fetch Reviews:
```bash
export GOOGLE_PLACES_API_KEY='your-api-key-here'
python manage.py fetch_google_reviews
```

Or with command-line argument:
```bash
python manage.py fetch_google_reviews --api-key 'your-key' --place-id 'ChIJIxzgoXFpKhURSRlfATWSfBs'
```

### Option 2: Using Sample Reviews (No API Key)
```bash
python manage.py load_sample_reviews
```

---

## Settings Configuration

### Development Mode (default)
- DEBUG = True
- SECURE_SSL_REDIRECT = False
- Allows HTTP connections
- Full error pages and debug info

### Production Mode
Set environment variables:
```bash
export DEBUG='False'
export SECRET_KEY='your-secure-random-key-here'
export ALLOWED_HOSTS='example.com www.example.com'
```

Then:
- DEBUG = False
- SECURE_SSL_REDIRECT = True
- Requires HTTPS
- Uses environment variables for security

---

## Scheduling Daily Review Fetch (Production)

### Option 1: Cron Job
```bash
# Edit crontab
crontab -e

# Add this line to run daily at midnight:
0 0 * * * cd /path/to/project && export GOOGLE_PLACES_API_KEY='your-key' && python manage.py fetch_google_reviews
```

### Option 2: Celery Beat (Recommended for scale)
```python
# settings.py
CELERY_BEAT_SCHEDULE = {
    'fetch-google-reviews-daily': {
        'task': 'mainapp.tasks.fetch_google_reviews',
        'schedule': crontab(hour=0, minute=0),
    },
}
```

---

## Common Issues

### Issue: "You're accessing over HTTPS but server only supports HTTP"
**Solution:** The dev server runs on HTTP. This is normal.
- Use `http://127.0.0.1:8000` (not https)
- In production, configure proper SSL/TLS

### Issue: HTTPS redirect errors in development
**Solution:** Set DEBUG=True (already configured)
- DEBUG mode disables SECURE_SSL_REDIRECT
- Development server only supports HTTP

### Issue: "Google Places API key not found"
**Solution:** Set the environment variable:
```bash
export GOOGLE_PLACES_API_KEY='your-key'
python manage.py fetch_google_reviews
```

### Issue: Database locked
**Solution:** Close other connections to db.sqlite3
```bash
# Remove lock files
rm -f db.sqlite3-shm db.sqlite3-wal
# Run again
python manage.py migrate
```

---

## Project Structure

```
patina_cappadocia/
├── patina_cappadocia/
│   ├── settings.py          # Django configuration
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI config
├── mainapp/
│   ├── models.py            # Database models (RoomCategory, GoogleReview, etc.)
│   ├── views.py             # View functions
│   ├── admin.py             # Admin panel configuration
│   ├── management/
│   │   └── commands/        # Custom management commands
│   │       ├── fetch_google_reviews.py
│   │       ├── load_sample_reviews.py
│   │       └── load_sample_content.py
│   ├── templates/
│   │   ├── index.html       # Homepage
│   │   ├── about.html       # About page
│   │   ├── rooms.html       # Rooms page
│   │   ├── contact.html     # Contact page
│   │   └── partials/        # Reusable template components
│   │       ├── _reviews.html
│   │       ├── _sliderHome.html
│   │       └── _aboutHome.html
│   ├── migrations/          # Database migrations
│   └── static/              # CSS, JS, images (collected)
├── static/                  # Development static files
├── media/                   # User-uploaded files (images)
├── db.sqlite3              # SQLite database
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```

---

## Useful Commands

```bash
# Check system configuration
python manage.py check

# Run tests (if available)
python manage.py test

# Create a backup of database
cp db.sqlite3 db.sqlite3.backup

# Reset database (WARNING: deletes all data)
rm db.sqlite3
python manage.py migrate

# Collect static files (production)
python manage.py collectstatic --noinput

# Create admin user
python manage.py createsuperuser

# Run management command
python manage.py [command_name]

# Show all migrations
python manage.py showmigrations

# Revert to previous migration
python manage.py migrate mainapp 0005
```

---

## Features Summary

### ✅ Google Reviews
- Cache reviews in database
- One-time daily API fetch
- Featured review management
- Multi-language support

### ✅ HomePage Images
- Section-based organization (slider, about, etc.)
- Dynamic slider with database images
- Fallback to static images
- Admin image management

### ✅ About Section
- Multi-language content (7 languages)
- Image management with position control
- Multiple sections support
- Dynamic rendering with admin control

### ✅ Room Management
- Dynamic room categories
- Room images and features
- Multi-language descriptions
- Admin panel control

### ✅ Security
- HTTPS enforcement (production)
- Content Security Policy (CSP)
- XFrame options configured
- HSTS headers enabled
- Secure cookies
- CSRF protection

---

## Performance Optimization

### Current Setup
- Database: SQLite (suitable for small-medium sites)
- Caching: WhiteNoise for static files
- Database queries: Using prefetch_related for efficiency
- Reviews: Cached daily (not real-time API calls)

### For High Traffic
1. Upgrade to PostgreSQL database
2. Add Redis caching layer
3. Use CDN for static files
4. Implement page caching
5. Use production WSGI server (Gunicorn, uWSGI)

---

## Deployment Checklist

- [ ] Set DEBUG = False
- [ ] Generate secure SECRET_KEY
- [ ] Configure ALLOWED_HOSTS with domain names
- [ ] Set up HTTPS/SSL certificate
- [ ] Configure database (PostgreSQL recommended)
- [ ] Set up email backend for notifications
- [ ] Configure static files serving
- [ ] Set up media files storage (S3, etc.)
- [ ] Configure Google Places API key
- [ ] Set up cron job for daily review fetch
- [ ] Enable security headers
- [ ] Set up monitoring and logging
- [ ] Configure backups
- [ ] Test admin panel access
- [ ] Run security checks: `python manage.py check --deploy`

---

## Support

For issues or questions:
1. Check `django.log` for error messages
2. Run `python manage.py check` to diagnose
3. Review Django documentation: https://docs.djangoproject.com
4. Check specific app documentation in IMPLEMENTATION_SUMMARY.md
