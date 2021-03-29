# Generated by Django 3.1.7 on 2021-03-28 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0005_auto_20210328_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='budget_for',
            field=models.CharField(choices=[('1', 'DAY'), ('7', 'WEEK'), ('30', 'MONTH')], max_length=50, verbose_name='Budget For'),
        ),
    ]
