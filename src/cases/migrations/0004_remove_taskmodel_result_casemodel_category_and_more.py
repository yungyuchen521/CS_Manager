# Generated by Django 4.1.7 on 2023-06-02 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0003_complete_fields_for_casemodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskmodel',
            name='result',
        ),
        migrations.AddField(
            model_name='casemodel',
            name='category',
            field=models.CharField(blank=True, choices=[('FIBER', 'FIBER'), ('SCORCH', 'SCORCH'), ('CAKING', 'CAKING'), ('OTHERS', 'OTHERS')], max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='casemodel',
            name='report',
            field=models.TextField(blank=True, null=True),
        ),
    ]
