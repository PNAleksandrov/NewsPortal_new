from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

# from newspaper import settings
# from news.model import PostCategory
# from news.model import settings
from .models import PostCategory


def send_email_notif(preview, pk, title, subscribers_email):
    #берет за основу шаблон и создает текст письма
    html_mail = render_to_string(
        'post_add_email.html',
        {
            'text': preview,
            'link': f'http://127.0.0.1:8000/news/{pk}',
        }
    )

    message = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email='windmilll@yandex.ru',
        to=subscribers_email
    )

    message.attach_alternative(html_mail, 'text/html')
    message.send()


@receiver(m2m_changed, sender=PostCategory)
def new_post_added(sender, instance, **kwargs):
    # событие - добавление статьи
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        # наполняем список подписчиков категорий добавленной статьи
        subscribers = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers_email_list = []
        for subscr in subscribers:
            subscribers_email_list.append(subscr.email)

        send_email_notif(instance.preview(), instance.pk, instance.title, subscribers_email_list)
