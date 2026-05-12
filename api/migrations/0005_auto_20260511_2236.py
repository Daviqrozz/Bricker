from django.db import migrations

categories = [
  'Celulares e smartphones', 'Notebooks e computadores', 'Periféricos', 'TVs',
  'Áudio e vídeo', 'Videogames', 'Câmeras e fotografia', 'Eletrodomésticos',
  'Móveis', 'Bicicletas', 'Esporte e lazer', 'Autopeças e acessórios',
  'Infantil e bebê', 'Moda e acessórios', 'Outros',
]

def create_default_categories(apps, schema_editor):
  Category = apps.get_model('api', 'Category')

  for name in categories:
    Category.objects.get_or_create(name=name)

def remove_default_categories(apps, schema_editor):
  Category = apps.get_model('api', 'Category')
  Category.objects.filter(name__in=categories).delete()

class Migration(migrations.Migration):
  dependencies = [('api', '0004_auto_20260508_1922')]
  operations = [migrations.RunPython(create_default_categories, remove_default_categories)]
