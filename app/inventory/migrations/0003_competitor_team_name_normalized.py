# Generated for 25_normalize-competitor-team-names-on-import.md

from django.db import migrations, models


def backfill_name_normalized(apps, schema_editor):
    from inventory.domain.normalize_name import normalize_name

    Competitor = apps.get_model("inventory", "Competitor")
    Team = apps.get_model("inventory", "Team")

    for competitor in Competitor.objects.all():
        competitor.name_normalized = normalize_name(competitor.name)
        competitor.save(update_fields=["name_normalized"])

    for team in Team.objects.all():
        team.name_normalized = normalize_name(team.name)
        team.save(update_fields=["name_normalized"])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_car_created_at_competitor_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitor',
            name='name_normalized',
            field=models.CharField(db_index=True, default='', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='name_normalized',
            field=models.CharField(db_index=True, default='', max_length=50),
            preserve_default=False,
        ),
        migrations.RunPython(backfill_name_normalized, noop_reverse),
    ]
