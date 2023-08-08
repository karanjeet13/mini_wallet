# Generated by Django 4.2.4 on 2023-08-08 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mywallet", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="transactions",
            name="reference_id",
        ),
        migrations.AlterField(
            model_name="transactions",
            name="wallet",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="mywallet.wallet"
            ),
        ),
    ]
