# Generated by Django 3.1.1 on 2020-09-21 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0002_auto_20200921_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='post_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='social_network.post'),
        ),
    ]
