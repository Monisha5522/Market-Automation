from django.db import models
from user.models import User
from userplatform.models import Platform


class Credential(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credential', null=True)
    name = models.CharField(max_length=25)
    password = models.CharField(max_length=15)
    created_on = models.DateTimeField(auto_now=True)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name='platform', null=True)
    is_active = models.BooleanField(editable=False, default=True)

    def __str__(self):
        return self.name
