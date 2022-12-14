# Generated by Django 4.0.6 on 2022-07-14 17:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_language_alter_bookinstance_id_book_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(help_text="13 Character <a href='https://www.isbn-international.org/content/what-isbn>ISBN number'</a>", max_length=13, verbose_name='ISBN'),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.UUID('c335dd0a-a395-413b-a6d9-49fafe203673'), help_text='ID único para este libro', primary_key=True, serialize=False),
        ),
    ]
