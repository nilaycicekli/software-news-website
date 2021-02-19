# Generated by Django 3.1.3 on 2021-01-07 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, unique=True)),
                ('count', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['count'],
            },
        ),
        migrations.RemoveField(
            model_name='article',
            name='labels',
        ),
        migrations.DeleteModel(
            name='Label',
        ),
    ]
