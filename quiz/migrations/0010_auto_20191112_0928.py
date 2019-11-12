# Generated by Django 2.2.6 on 2019-11-12 03:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20191110_2004'),
        ('quiz', '0009_variable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='correct_answer',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)], default=1),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feed_back', models.TextField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Student')),
            ],
        ),
    ]
