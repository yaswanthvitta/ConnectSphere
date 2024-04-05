# Generated by Django 4.1.5 on 2023-07-17 08:24

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_post_no_of_likes_alter_post_id_alter_post_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Postpic',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('image', models.ImageField(upload_to='post_images')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.CharField(max_length=100)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('no_of_likes', models.IntegerField(default=0)),
            ],
        ),
    ]