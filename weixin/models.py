from django.db import models

# Create your models here.
import datetime


class Email(models.Model):
    user_email = models.CharField(max_length=30, blank=True, null=True, verbose_name='user_email')
    user_id = models.CharField(max_length=30, blank=True, null=True, verbose_name='user_id')
    create_time = models.DateTimeField(editable=False,blank=True,null=True)
    def save(self,*args,**kwargs):
        self.create_time = datetime.datetime.now()
        super(Email,self).save(*args,**kwargs)
