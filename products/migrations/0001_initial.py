# Generated by Django 3.2 on 2023-08-29 11:15

import accounts.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import products.services


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_all', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('waiter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('price', models.PositiveBigIntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to=products.services.upload_product_image_path, validators=[accounts.validators.validate_image])),
                ('real_price', models.PositiveBigIntegerField()),
                ('count_all', models.PositiveIntegerField()),
                ('count_sold', models.PositiveIntegerField()),
                ('description', models.CharField(blank=True, max_length=70, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='products.category')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveBigIntegerField()),
                ('real_price', models.PositiveBigIntegerField()),
                ('product_count', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='products.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orderitems', to='products.product')),
            ],
        ),
    ]
