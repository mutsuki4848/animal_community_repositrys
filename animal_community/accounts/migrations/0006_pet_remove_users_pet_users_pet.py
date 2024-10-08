# Generated by Django 4.1 on 2024-08-12 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_users_pet_delete_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='users',
            name='pet',
        ),
        migrations.AddField(
            model_name='users',
            name='pet',
            field=models.ManyToManyField(blank=True, related_name='users', to='accounts.pet'),
        ),
    ]
