from django.db import models


class user(models.Model):
    id = models.CharField(max_length=7)
    name = models.CharField(max_length=25)
    email = models.CharField(max_length=25)
    mobile_number = models.PositiveIntegerField()
    gender = models.CharField(max_length=15)
    password = models.CharField(max_length=15)
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name




