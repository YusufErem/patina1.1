from django.apps import AppConfig
import os


class MainappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainapp'
    
    def ready(self):
        """Django uygulaması hazır olduğunda scheduled task'ları başlat"""
        # Sadece production'da veya environment variable ile aktif edildiğinde çalıştır
        if os.environ.get('ENABLE_SCHEDULER', 'false').lower() in ('true', '1', 'yes'):
            self.start_scheduler()
    
    def start_scheduler(self):
        """APScheduler ile günlük Google yorumlarını çek"""
        try:
            from apscheduler.schedulers.background import BackgroundScheduler
            from apscheduler.triggers.cron import CronTrigger
            import atexit
            
            scheduler = BackgroundScheduler()
            
            # Her gün saat 02:00'de Google yorumlarını çek
            scheduler.add_job(
                self.fetch_google_reviews,
                trigger=CronTrigger(hour=2, minute=0),  # Her gün saat 02:00
                id='fetch_google_reviews_daily',
                name='Günlük Google Yorumlarını Çek',
                replace_existing=True,
            )
            
            scheduler.start()
            print("✓ Scheduled task başlatıldı: Google yorumları her gün saat 02:00'de çekilecek")
            
            # Uygulama kapanırken scheduler'ı durdur
            atexit.register(lambda: scheduler.shutdown())
            
        except ImportError:
            print("⚠️ APScheduler bulunamadı. Lütfen 'pip install APScheduler' komutunu çalıştırın")
            print("💡 Alternatif: Cron job veya scheduled task kullanabilirsiniz (fetch_reviews_daily.sh)")
        except Exception as e:
            print(f"⚠️ Scheduler başlatılamadı: {e}")
            print("💡 Alternatif: Cron job veya scheduled task kullanabilirsiniz (fetch_reviews_daily.sh)")
    
    def fetch_google_reviews(self):
        """Google yorumlarını çek (management command'ı çağır)"""
        import subprocess
        import sys
        
        try:
            # Django management command'ını çalıştır
            result = subprocess.run(
                [sys.executable, 'manage.py', 'fetch_google_reviews'],
                cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                capture_output=True,
                text=True,
                timeout=300  # 5 dakika timeout
            )
            
            if result.returncode == 0:
                print("✓ Google yorumları başarıyla çekildi")
            else:
                print(f"⚠️ Google yorumları çekilirken hata: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Google yorumları çekilirken hata: {e}")
