from django.db import models
from django.core.exceptions import ValidationError


class App(models.Model):
    # user = models.ManyToManyField(User,blank=True, null=True)
    status = models.BooleanField(default=False)
    status_serveur = models.BooleanField(default=False)
    application = models.CharField(max_length=100,blank=True)
    urls = models.CharField(max_length=100,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Date création')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Date modification')
    is_activate=models.BooleanField(default=False)  

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.application

class setting(models.Model):
    intervale_check = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "Parametrage"

    def save(self, *args, **kwargs):
        if not self.pk and setting.objects.exists():
            raise ValidationError('There is can be only one setting instance')
        return super(setting, self).save(*args, **kwargs)

