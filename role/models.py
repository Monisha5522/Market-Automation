from django.db import models


class Role(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(editable=False, default=True)

    def __str__(self):
        return self.name
