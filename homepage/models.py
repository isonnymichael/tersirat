from django.db import models
from datetime import datetime  
import datetime

# Create your models here.
class Counter(models.Model):
    id =  models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    creation_time = models.DateField(default=datetime.date.today, blank=True)
    update_time = models.DateField(default=datetime.date.today, blank=True)
    count = models.IntegerField(default=1)
