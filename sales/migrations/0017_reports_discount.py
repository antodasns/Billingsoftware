# Generated by Django 2.2.3 on 2019-10-22 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0016_auto_20191021_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='reports',
            name='discount',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
