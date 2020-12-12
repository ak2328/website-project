# Generated by Django 3.1.1 on 2020-09-17 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Analytics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_name', models.CharField(max_length=50)),
                ('company_name', models.CharField(max_length=200)),
                ('stall_name', models.CharField(max_length=200)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('random_string', models.CharField(max_length=50)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='another_poll_answers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_id', models.IntegerField(default=0)),
                ('user_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='call_schedules',
            fields=[
                ('schedule_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('mobile', models.CharField(max_length=30)),
                ('selected_date', models.CharField(blank=True, max_length=50, null=True)),
                ('selected_time', models.CharField(blank=True, max_length=50, null=True)),
                ('stall_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.stalls')),

            ],
        ),
        migrations.CreateModel(
            name='ChannelOnlineCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_reciever_string', models.CharField(max_length=50)),
                ('count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('seen_status', models.BooleanField(default=False)),
                ('author_reciever_string', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_reciever_string', models.CharField(max_length=20)),
                ('count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='partners_tab',
            fields=[
                ('image', models.ImageField(upload_to='')),
                ('partner_id', models.AutoField(primary_key=True, serialize=False)),
                ('partner_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Permanent_Poll_Answers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_id', models.IntegerField(default=0)),
                ('question', models.TextField()),
                ('option_one_count', models.IntegerField(default=0)),
                ('option_two_count', models.IntegerField(default=0)),
                ('option_three_count', models.IntegerField(default=0)),
                ('option_four_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='poll',
            fields=[
                ('question_id', models.AutoField(primary_key=True, serialize=False)),
                ('question', models.TextField()),
                ('option_one', models.CharField(max_length=30, null=True)),
                ('option_two', models.CharField(max_length=30, null=True)),
                ('option_three', models.CharField(max_length=30, null=True)),
                ('option_four', models.CharField(max_length=30, null=True)),
                ('option_one_count', models.IntegerField(default=0)),
                ('option_two_count', models.IntegerField(default=0)),
                ('option_three_count', models.IntegerField(default=0)),
                ('option_four_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=200, null=True)),
                ('question', models.TextField()),
            ],
        ),
    ]
