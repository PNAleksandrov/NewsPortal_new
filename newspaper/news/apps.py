from django.apps import AppConfig
import redis


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        import news.signals


red = redis.Redis(
    host='redis-15186.c299.asia-northeast1-1.gce.cloud.redislabs.com',
    port=15186,
    password='VEoyK2o8f95jrIPyYJ5zy1ushU2v9EjG',
)


# red = redis.Redis(host='localhost', port=6379, db=0)
