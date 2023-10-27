# Generated by Django 4.2.6 on 2023-10-27 00:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CertTracApp', '0007_rename_number_basic_courses_tutor_number_basic_courses_completed_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='InPersonTrainingSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=40)),
                ('training_time', models.DecimalField(decimal_places=2, max_digits=5)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CertTracApp.course')),
            ],
        ),
        migrations.CreateModel(
            name='TotalTrainingSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=40)),
                ('training_time', models.DecimalField(decimal_places=2, max_digits=5)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CertTracApp.course')),
            ],
        ),
        migrations.RenameField(
            model_name='tutor',
            old_name='number_basic_courses_completed',
            new_name='number_basic_courses_completed_level_1',
        ),
        migrations.RenameField(
            model_name='tutor',
            old_name='number_communication_courses_completed',
            new_name='number_basic_courses_completed_level_2',
        ),
        migrations.RenameField(
            model_name='tutor',
            old_name='number_elective_courses_completed',
            new_name='number_communication_courses_completed_level_1',
        ),
        migrations.RenameField(
            model_name='tutor',
            old_name='number_ethicsequality_courses_completed',
            new_name='number_communication_courses_completed_level_2',
        ),
        migrations.RenameField(
            model_name='tutor',
            old_name='number_learningstudytechinque_courses_completed',
            new_name='number_elective_courses_completed_level_1',
        ),
        migrations.AddField(
            model_name='tutor',
            name='number_elective_courses_completed_level_2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tutor',
            name='number_ethicsequality_courses_completed_level_1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tutor',
            name='number_ethicsequality_courses_completed_level_2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tutor',
            name='number_learningstudytechinque_courses_completed_level_1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tutor',
            name='number_learningstudytechinque_courses_completed_level_2',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='date_hired',
            field=models.CharField(max_length=10),
        ),
        migrations.DeleteModel(
            name='TrainingSession',
        ),
    ]