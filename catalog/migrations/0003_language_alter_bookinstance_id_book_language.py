# Generated by Django 4.0.6 on 2022-07-14 17:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_author_book_bookinstance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Ingrese el nombre de un lenguaje.', max_length=50, verbose_name='Nombre')),
            ],
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.UUID('3bae414a-ab44-4e8f-914c-8846e9c570a9'), help_text='ID único para este libro', primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.language'),
        ),
    ]
