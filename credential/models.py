from django.db import models
from user.models import User
from userplatform.models import Platform


class Credential(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credential', null=False, default=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=15)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name='platform', null=False, default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.OneToOneField('self', on_delete=models.CASCADE, editable=False,
                                      blank=True, null=True, related_name='create_user')
    updated_by = models.OneToOneField('self', on_delete=models.CASCADE, editable=False,
                                      blank=True, null=True, related_name='update_user')
    is_active = models.BooleanField(editable=False, default=True)

    def __str__(self):
        return self.name
