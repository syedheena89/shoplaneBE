# Generated by Django 4.1.10 on 2023-08-24 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('email', models.CharField(max_length=60)),
                ('mobile_number', models.CharField(max_length=12)),
                ('password', models.CharField(max_length=16)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BillingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('discount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField()),
                ('order_number', models.CharField(max_length=20)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('product', models.IntegerField()),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('image', models.TextField(blank=True, null=True)),
                ('brand', models.CharField(max_length=100)),
                ('shipping', models.TextField()),
                ('description', models.TextField()),
                ('price', models.FloatField(default=0.0)),
                ('category', models.CharField(max_length=100)),
                ('featured', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField()),
                ('product', models.IntegerField()),
                ('rate', models.PositiveIntegerField()),
                ('review', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['name'], name='name-index'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['category', 'brand'], name='category-brand-index'),
        ),
        migrations.AddField(
            model_name='order',
            name='order_item',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_detail', to='shoplane_api.orderitem'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='orders',
            field=models.ManyToManyField(related_name='order', to='shoplane_api.order'),
        ),
    ]