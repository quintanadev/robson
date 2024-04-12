# Generated by Django 5.0.4 on 2024-04-12 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('intervalo', models.CharField(max_length=8)),
                ('volume', models.DecimalField(decimal_places=13, max_digits=20)),
                ('tmo', models.DecimalField(decimal_places=13, max_digits=20)),
                ('abandono', models.DecimalField(decimal_places=13, max_digits=20)),
                ('agentesSemIndisp', models.DecimalField(decimal_places=13, max_digits=20)),
                ('agentesComIndisp', models.DecimalField(decimal_places=13, max_digits=20)),
                ('nivelServico', models.DecimalField(decimal_places=13, max_digits=20)),
                ('trafego', models.DecimalField(decimal_places=13, max_digits=20)),
                ('atendidasNivelServico', models.DecimalField(decimal_places=13, max_digits=20)),
            ],
        ),
        migrations.CreateModel(
            name='NiceDisposition',
            fields=[
                ('dispositionId', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('dispositionName', models.CharField(max_length=100)),
                ('notes', models.CharField(max_length=100)),
                ('lastUpdated', models.CharField(max_length=100)),
                ('classificationId', models.CharField(max_length=100)),
                ('systemOutcome', models.CharField(max_length=100)),
                ('isPreviewDisposition', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='NiceSkill',
            fields=[
                ('skillId', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('skillName', models.CharField(max_length=100)),
                ('campaignId', models.CharField(max_length=100)),
                ('campaignName', models.CharField(max_length=100)),
                ('notes', models.CharField(max_length=100)),
                ('scriptName', models.CharField(max_length=100)),
                ('callSuppressionScriptId', models.CharField(max_length=100)),
                ('agentless', models.CharField(max_length=100)),
            ],
        ),
    ]