from django.db import models


class User(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=25)
    email = models.CharField(max_length=25)
    mobile_number = models.IntegerField()
    gender = models.CharField(max_length=15)
    created_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(editable=False, default=False)

    def __str__(self) -> str:
        return self.name


class Credential(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credential', null=True)
    name = models.CharField(max_length=25)
    email = models.CharField(max_length=25)
    mobile_number = models.IntegerField()
    password = models.CharField(max_length=15)
    created_on = models.DateTimeField(auto_now=True)
    platform_type_id = models.PositiveIntegerField()
    urls = models.CharField(max_length=50)
    is_active = models.BooleanField(editable=False, default=False)

    def __str__(self) -> str:
        return self.name


class PlatformType(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=25)


