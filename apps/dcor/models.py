# HiPerCic Project / St. Olaf College / Computer Science Dept.
###################################################################################
# apps/dcor/models.py
# Created INSERT_DATE
# Holds "models", which are Django classes that are synced to the database.
###################################################################################
from django.db import models

### Create your models here. ###
### Each model is a class, extending models.Model
### For help with models, check out https://docs.djangoproject.com/en/dev/topics/db/models/
### Once you have set up your models, be sure to run 'hipercic-local/manage syncdb --database=DB_NAME' in your hipercic top directory.  This will configure the database for you.
### Note that models cannot be linked to models in other databases using ForeignKey relationships.  You'll have to do that lookup manually.
class Asset(models.Model):
	name = models.CharField("asset name", max_length=100)

class Record(models.Model):
	asset        = models.ForeignKey(Asset, on_delete=models.PROTECT)
	date         = models.DateField("record date")
	closed_price = models.DecimalField(max_digits=10, decimal_places=2)
	updated_at   = models.DateTimeField("last update", auto_now=True)
	created_at   = models.DateTimeField("creation date", auto_now_add=True)
