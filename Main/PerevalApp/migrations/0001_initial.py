# Generated by Django 4.2.11 on 2024-04-25 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(max_length=20)),
                ('longitude', models.FloatField(max_length=20)),
                ('height', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Levels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spring', models.CharField(blank=True, choices=[('1', ''), ('2', '1A')], max_length=1, null=True)),
                ('summer', models.CharField(blank=True, choices=[('1', ''), ('2', '1A')], max_length=1, null=True)),
                ('autumn', models.CharField(blank=True, choices=[('1', ''), ('2', '1A')], max_length=1, null=True)),
                ('winter', models.CharField(blank=True, choices=[('1', ''), ('2', '1A')], max_length=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100)),
                ('fam', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('otc', models.CharField(max_length=100, verbose_name='Отчество')),
                ('phone', models.IntegerField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Pereval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('beauty_title', models.CharField(max_length=255)),
                ('other_title', models.CharField(max_length=255)),
                ('connect', models.TextField(blank=True, null=True)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('coords', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='PerevalApp.coords')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PerevalApp.levels')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PerevalApp.users')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('data', models.ImageField(blank=True, null=True, upload_to='images')),
                ('pereval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='PerevalApp.pereval')),
            ],
        ),
    ]
