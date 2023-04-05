# Generated by Django 4.1.7 on 2023-03-27 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CaseModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='')),
            ],
            options={
                'db_table': 'case_model',
            },
        ),
        migrations.CreateModel(
            name='CaseResultModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(choices=[('bugs', 'bugs'), ('scorch', 'scorch')], default='bugs', max_length=32)),
                ('result', models.TextField()),
                ('case', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='case_result', to='cases.casemodel')),
            ],
            options={
                'db_table': 'case_result_model',
            },
        ),
    ]
