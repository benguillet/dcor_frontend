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

## An example model
## TODO: remove and write your own models!
class ExampleModel(models.Model):

    # some example fields -- will be stored in the database
    exampleField1 = models.CharField(max_length=20) # makes a character field (string) with a maximum size of 20
    exampleField2 = models.FloatField() # makes a floating point number field
