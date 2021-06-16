# Generated by Django 3.1.5 on 2021-05-02 23:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('aemter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kandidatur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('vorname', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('wahldatum', models.DateField(null=True)),
                ('beschlussnummer', models.CharField(max_length=50, null=True)),
                ('funktion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aemter.funktion')),
            ],
            options={
                'verbose_name': 'Kandidatur',
                'verbose_name_plural': 'Kandidaturen',
            },
        ),
    ]
