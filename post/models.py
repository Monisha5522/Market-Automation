from django.db import models


class Post(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    subject = models.CharField(max_length=75)
    caption = models.CharField(max_length=1000)
    is_active = models.BooleanField(editable=False, default=True)

    def __str__(self):
        return self.subject
