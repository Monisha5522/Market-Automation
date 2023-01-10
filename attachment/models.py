from django.db import models
from post.models import Post


class Attachment(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='attachment', null=True)
    type = models.CharField(max_length=50)
    url = models.CharField(max_length=3000)
    is_active = models.BooleanField(editable=False, default=True)

    def __str__(self):
        return self.type

