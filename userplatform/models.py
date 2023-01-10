from django.db import models


class Platform(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=25)
    url = models.CharField(max_length=3000)
    is_active = models.BooleanField(editable=False, default=True)

    def __str__(self):
        return self.name
