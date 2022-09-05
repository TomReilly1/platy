from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class DirectMessages(models.Model):
    msg_sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='sender_user')
    msg_receiver = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='reciever_user')
    text_content = models.TextField(max_length=2000)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        text = self.text_content if len(self.text_content) < 23 else self.text_content[:20] + '...'
        return f'Sender: {self.sender}, Receiver: {self.receiver}, Text: {text}'
