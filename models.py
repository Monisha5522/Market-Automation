from django.db import models


class Auth_user(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=25)
    email = models.CharField(max_length=25)
    mobile_number = models.PositiveIntegerField()
    gender = models.CharField(max_length=15)
    password = models.CharField(max_length=15)
    created_on = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'auth_user'
