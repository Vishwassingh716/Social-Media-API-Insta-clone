# Generated by Django 4.1.7 on 2024-03-14 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0005_commentonpost'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='commentonpost',
            unique_together={('user', 'post', 'time')},
        ),
    ]
