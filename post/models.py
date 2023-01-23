from django.db import models
from role.models import Role
from user.models import User


class Attachment(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    type = models.CharField(max_length=50)
    url = models.CharField(max_length=3000)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Role, on_delete=models.CASCADE, editable=False,
                                   blank=True, null=True, related_name='create_user')
    updated_by = models.OneToOneField('self', on_delete=models.CASCADE, editable=False,
                                      blank=True, null=True, related_name='update_user')
    is_active = models.BooleanField(editable=False, default=True)

    def __str__(self):
        return self.type


class Post(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    subject = models.CharField(max_length=75)
    caption = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post', null=False, default=True)
    status = models.BooleanField(editable=True, default=False)
    attachment = models.ManyToOneRel(to=Attachment, on_delete=models.CASCADE, related_name='attachment', field_name='post', field='id')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.OneToOneField('self', on_delete=models.CASCADE, editable=False,
                                      blank=True, null=True, related_name='create_user')
    updated_by = models.OneToOneField('self', on_delete=models.CASCADE, editable=False,
                                      blank=True, null=True, related_name='update_user')
    is_active = models.BooleanField(editable=False, default=True)

    # def __str__(self):
    #     return self.subject

