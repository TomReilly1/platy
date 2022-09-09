from django.db import models
from django.contrib.auth.models import User
# from django.contrib.postgres import search

# Create your models here.
class DirectMessages(models.Model):
    msg_sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='msg_sender_user')
    msg_receiver = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='msg_receiver_user')
    text_content = models.TextField(max_length=2000)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        text = self.text_content if len(self.text_content) < 23 else self.text_content[:20] + '...'
        return f'Sender: {self.msg_sender}, Receiver: {self.msg_receiver}, Text: {text}'

class Friends(models.Model):
    req_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='req_sender_user')
    req_receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='req_receiver_user')
    is_accepted = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        flag = ' '
        if not self.is_accepted:
            flag = ' not '

        return f'{self.req_sender} has sent a request to {self.req_receiver}. It has{flag}been accepted.'


"""
class Option(Model):
    name = CharField()

class Thing(TimeStampedModel):
    options = ManyToManyField("Option", through="ThingOption")    

class ThingOption(Model):
    thing = ForeignKey(Thing)
    option = ForeignKey(Option)
    value = CharField()

    class Meta:
        unique_together = ('thing', 'option')
"""