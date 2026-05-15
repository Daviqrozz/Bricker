from django.db import migrations

def create_default_plan(apps, schema_editor):
  Plan = apps.get_model('bricker_app', 'Plan')
  Plan.objects.get_or_create(
    name='Plano Free',
    defaults={
      'price': 0.00,
      'max_products': 50,
      'description': 'Plano padrão inicial'
    }
  )

def remove_default_plan(apps, schema_editor):
  Plan = apps.get_model('bricker_app', 'Plan')
  Plan.objects.filter(name='Plano Free').delete()

class Migration(migrations.Migration):
  dependencies = [('bricker_app', '0003_alter_userprofile_plan')]
  operations = [migrations.RunPython(create_default_plan, remove_default_plan)]
