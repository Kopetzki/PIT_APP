# Generated by Django 3.0.6 on 2020-06-10 21:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Age',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField(choices=[(0, 'Under 18'), (1, '18 - 24'), (2, '25+'), (99, 'Not Sure')], default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ethnicity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ethnicity', models.IntegerField(choices=[(1, 'Hispanic'), (2, 'Non-Hispanic'), (99, "Doesn't Know")], default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.IntegerField(choices=[(0, 'Male'), (1, 'Female'), (99, 'Not Sure')], default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Homeless',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_homeless', models.IntegerField(choices=[(0, 'Definetly'), (1, 'Possibly'), (99, 'Not Sure')], default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('race', models.IntegerField(choices=[(0, 'American Indian or Alaska Native'), (1, 'Asian'), (2, 'Black or African American'), (3, 'Native Hawaiian or Other Pacific Islander'), (4, 'White'), (5, 'Other'), (99, 'Not Sure')], default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Observation_Individual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_location', models.CharField(help_text='Location where observed', max_length=200)),
                ('client_information', models.CharField(help_text='Other information or identifying characteristics', max_length=200)),
                ('client_age', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Age')),
                ('client_ethnicity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Ethnicity')),
                ('client_gender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Gender')),
                ('client_homeless', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Homeless')),
                ('client_race', models.ManyToManyField(to='survey.Race')),
            ],
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obs_reason', models.IntegerField(choices=[(0, 'You are unable to enter a site'), (1, 'You cannot conduct a PIT count survey (person refused, language, or other problems'), (2, 'You do not wish to disturb people sleeping')], default=1, null=True)),
                ('obs_adults', models.IntegerField(default=0, null=True)),
                ('obs_children', models.IntegerField(default=0, null=True)),
                ('obs_unsure', models.IntegerField(default=0, null=True)),
                ('obs_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('obs_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Observation_Individual')),
                ('obs_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]