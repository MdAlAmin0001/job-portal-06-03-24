# Generated by Django 5.0 on 2024-02-09 05:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_addjob_model_update_at_alter_jobseekerprofile_skills'),
    ]

    operations = [
        migrations.CreateModel(
            name='job_apply_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=11, null=True)),
                ('profile_pic', models.ImageField(null=True, upload_to='media/profile_pic')),
                ('skills', models.CharField(max_length=100, null=True)),
                ('present_address', models.CharField(max_length=100, null=True)),
                ('permanent_address', models.CharField(max_length=100, null=True)),
                ('gender', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')], max_length=50)),
                ('portfolio_link', models.URLField(blank=True, help_text='Portfolio Link', null=True)),
                ('previous_job', models.CharField(blank=True, help_text='Previous Job', max_length=255, null=True)),
                ('job_experience', models.CharField(blank=True, help_text='Job Experience', max_length=255, null=True)),
                ('signature', models.ImageField(blank=True, help_text='Upload Signature (PNG, JPG, JPEG)', null=True, upload_to='signatures/')),
                ('cover_letter', models.TextField(blank=True, help_text='Cover Letter', null=True)),
                ('expected_salary', models.DecimalField(blank=True, decimal_places=2, help_text='Expected Salary', max_digits=10, null=True)),
                ('apply_resume', models.FileField(null=True, upload_to='media/apply_resume')),
                ('applicant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.addjob_model')),
            ],
        ),
    ]
