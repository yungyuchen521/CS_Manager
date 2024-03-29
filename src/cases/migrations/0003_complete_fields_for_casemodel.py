# Generated by Django 4.1.7 on 2023-04-30 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0002_alter_taskmodel_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='casemodel',
            name='issue_details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='casemodel',
            name='location',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='casemodel',
            name='oem_feedback',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='casemodel',
            name='oem_status',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='casemodel',
            name='product_issue',
            field=models.CharField(blank=True, choices=[('PACKAGE_INFO', 'PACKAGE_INFO'), ('PACKAGE_DAMAGED', 'PACKAGE_DAMAGED'), ('SENSUOUS', 'SENSUOUS'), ('FOREIGN_MATTER', 'FOREIGN_MATTER'), ('AMOUNT', 'AMOUNT'), ('OTHERS', 'OTHERS')], max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='casemodel',
            name='product_specs',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='casemodel',
            name='case_id',
            field=models.CharField(max_length=16, unique=True),
        ),
    ]
