# Generated by Django 4.2.7 on 2023-11-01 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddedProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('total', models.FloatField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cart.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.product')),
            ],
        ),
        migrations.RemoveField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(through='cart.AddedProducts', to='product.product'),
        ),
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(through='cart.AddedProducts', to='product.product'),
        )
    ]
