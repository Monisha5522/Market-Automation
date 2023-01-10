# Generated by Django 4.2 on 2023-01-09 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=75)),
                ('caption', models.CharField(max_length=1000)),
                ('is_active', models.BooleanField(default=True, editable=False)),
            ],
        ),
    ]
