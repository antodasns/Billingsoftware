# Generated by Django 2.2.3 on 2019-07-19 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0007_auto_20190628_1011'),
    ]

    operations = [
        migrations.CreateModel(
            name='create_wholesale_sales_final',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_type', models.CharField(choices=[('retail', 'retail'), ('wholesale', 'wholesale')], max_length=1)),
                ('sales_date', models.DateField(null=True)),
                ('sales_time', models.TimeField(null=True)),
                ('subtotal', models.CharField(max_length=50)),
                ('sale_invoice_ref', models.IntegerField()),
                ('sales_special_discount', models.IntegerField()),
                ('sales_total', models.CharField(max_length=50)),
                ('sales_payment_received', models.IntegerField()),
                ('sales_total_tax_amount', models.CharField(max_length=50)),
                ('sales_total_discount_amount', models.IntegerField()),
                ('sales_round_off', models.IntegerField()),
                ('sales_transaction_mode', models.CharField(choices=[('Cash', 'Cash'), ('Bank', 'Bank')], max_length=5)),
                ('sales_cash_account', models.CharField(choices=[('General', 'General'), ('General', 'General'), ('General', 'General')], max_length=8)),
                ('sales_payment_remainder_date', models.DateField(null=True)),
                ('sales_payment_balance', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='create_wholesale_sales_table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_product_ref_id', models.IntegerField()),
                ('sales_invoice_no', models.IntegerField()),
                ('sales_qty', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='sale_wholesale_totals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_date', models.DateField(null=True)),
                ('sales_totals', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='wholesale_taxes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tax_percent', models.IntegerField()),
                ('sale_date', models.DateField(null=True)),
                ('total_tax_amount', models.CharField(max_length=50)),
                ('price_tax_amount', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='create_sales_final',
            name='sale_type',
            field=models.CharField(choices=[('retail', 'retail'), ('wholesale', 'wholesale')], max_length=1),
        ),
    ]
