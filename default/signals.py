from django.db.models.signals import post_save
from django.dispatch import receiver
from base_user.models import MyUser
from default import tasks
from default.models import TokenModel


@receiver(post_save,sender = MyUser)
def create_token(sender,instance,created,**kwargs):
    if created:
        TokenModel.objects.create(
            user=instance
        )
        print('USER CREATE')
@receiver(post_save,sender=TokenModel)
def start_task(sender,instance,created,**kwargs):
    if created:
        link = f'http://localhost:8000/verify/{instance.token}/{instance.user.id}/'
        tasks.send_mail_task(instance.user.email,link)
        print('TASK RUNNED')


#test
#asdasdasdasdasdgit