# Generated by Django 4.2.5 on 2023-09-27 14:33

import colorfield.fields
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Избранный рецепт',
                'verbose_name_plural': 'Избранные рецепты',
                'ordering': ('user__username',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('image', models.ImageField(upload_to='recipes/images/', verbose_name='Ссылка на картинку на сайте')),
                ('text', models.TextField(verbose_name='Описание')),
                ('cooking_time', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(720)], verbose_name='Время приготовления (в минутах)')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000)], verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'Рецепт-Инредиент',
                'verbose_name_plural': 'Рецепты-Инредиенты',
                'ordering': ('recipe__name', 'ingredient__name'),
            },
        ),
        migrations.CreateModel(
            name='RecipeTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Рецепт-Тег',
                'verbose_name_plural': 'Рецепты-Теги',
                'ordering': ('recipe__name', 'tag__name'),
            },
        ),
        migrations.CreateModel(
            name='ShoppingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Блюдо в корзине',
                'verbose_name_plural': 'Блюда в корзине',
                'ordering': ('recipe__name',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('color', colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=25, samples=None, verbose_name='Цвет в HEX')),
                ('slug', models.CharField(max_length=200, unique=True, validators=[django.core.validators.RegexValidator('^[-a-zA-Z0-9_]+$')], verbose_name='Уникальный слаг')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ('name',),
            },
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(fields=('name', 'slug'), name='unique_tag'),
        ),
        migrations.AddField(
            model_name='shoppinglist',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='recipes.recipe', verbose_name='Рецепт'),
        ),
    ]
