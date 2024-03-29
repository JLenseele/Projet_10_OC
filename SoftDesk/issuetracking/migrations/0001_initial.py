# Generated by Django 4.1.7 on 2023-03-10 17:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.CharField(choices=[('RD', 'READ'), ('WR', 'WRITE'), ('AD', 'ADMIN')], default='READ', max_length=2)),
                ('role', models.CharField(choices=[('AU', 'AUTHOR'), ('CO', 'COLLAB')], max_length=2)),
                ('contributor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('desc', models.CharField(blank=True, max_length=500)),
                ('type', models.CharField(choices=[('PJ', 'PROJET'), ('PR', 'PRODUIT'), ('AP', 'APPLICATION')], max_length=2)),
                ('status', models.CharField(choices=[('DV', 'DEVELOPMENT'), ('PR', 'PRODUCTION')], max_length=2)),
                ('contributors', models.ManyToManyField(related_name='contributions', through='issuetracking.Contributor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('desc', models.CharField(max_length=500)),
                ('tag', models.CharField(max_length=255)),
                ('priority', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('assign', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assign', to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='issuetracking.project')),
            ],
        ),
        migrations.AddField(
            model_name='contributor',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='issuetracking.project'),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=500)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='issuetracking.issue')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='contributor',
            unique_together={('project', 'contributor')},
        ),
    ]
