# Generated by Django 5.1.4 on 2025-04-10 08:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hotel', '0001_initial'),
        ('sunil', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer_cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('total_amount', models.FloatField(default=0)),
                ('qty', models.IntegerField()),
                ('note', models.CharField(max_length=100, null=True)),
                ('accepted_status', models.CharField(default='Pendding', max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('customer_session_id', models.CharField(max_length=500, null=True)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='hotel.item')),
                ('table', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='hotel.table')),
            ],
        ),
        migrations.CreateModel(
            name='Rattings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.IntegerField()),
                ('customer_session_id', models.CharField(max_length=500, null=True)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.item')),
            ],
        ),
        migrations.CreateModel(
            name='Table_qr_count',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('hotel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='sunil.hotel')),
            ],
        ),
        migrations.CreateModel(
            name='Table_QrCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=100)),
                ('active_status', models.IntegerField(default=1)),
                ('watch_and_order_status', models.IntegerField(default=1)),
                ('table', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='hotel.table')),
            ],
        ),
    ]
