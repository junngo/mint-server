# Generated by Django 4.2.7 on 2024-01-01 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_financialstate_ratios_incomestatement_balancesheet'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockprice',
            name='eps',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='stockprice',
            name='pbr',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='stockprice',
            name='per',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='stockprice',
            name='share_count',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='financialstate',
            name='report',
            field=models.CharField(choices=[('11011', '1 YEAR'), ('11012', 'Q2'), ('11014', 'Q3'), ('11013', 'Q1')], max_length=5),
        ),
    ]