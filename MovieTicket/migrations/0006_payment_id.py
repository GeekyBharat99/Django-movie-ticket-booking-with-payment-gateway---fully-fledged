# Generated by Django 3.0.1 on 2020-02-11 19:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MovieTicket', '0005_sheets_usr'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment_Id',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PayId', models.CharField(blank=True, max_length=120, null=True)),
                ('Usr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]