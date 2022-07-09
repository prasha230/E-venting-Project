# Generated by Django 4.0.4 on 2022-06-29 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('events', '0010_delete_person_person_alter_event_attendees'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Person',
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
            ],
            options={
                'ordering': ('first_name',),
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.user',),
        ),
    ]