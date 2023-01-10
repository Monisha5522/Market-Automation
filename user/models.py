from django.db import models
from role.models import Role


class User(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=25, null=True)
    email = models.EmailField(max_length=30, unique=True)
    phone = models.BigIntegerField(null=True, unique=True)
    gender = models.CharField(max_length=15)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user', null=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(editable=False, default=True)

    def __str__(self):
        return self.name
