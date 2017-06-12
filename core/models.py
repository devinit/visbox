from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
import json


class Dataset(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    data = models.TextField()
    sep = models.CharField(max_length=1,default="\t")
    
    class Meta:
        ordering = ['-created']
    
    def __unicode__(self):
        return u'%s' % self.name
    
    def get_absolute_url(self):
        return reverse('core.views.dataset',args=[self.pk])
    
class Visualisation(models.Model):
    title = models.CharField(null=True,blank=True,max_length=255)
    chart_type = models.CharField(max_length=255)
    dataset = models.ForeignKey(Dataset)
    creator = models.ForeignKey(User, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    configuration_flat = JSONField(blank=True,null=True)
    configuration = JSONField(blank=True,null=True)
    save_as_template = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u'%s' % self.title
    
    class Meta:
        ordering = ['-created']
        
    def get_absolute_url(self):
        return reverse('core.views.viewVis',args=[self.pk])
    
    def get_flat_config(self):
        return json.dumps(self.configuration_flat)
    
    def get_config(self):
        return json.dumps(self.configuration)
    
    def save(self, *args, **kwargs):
        super(Visualisation, self).save(*args, **kwargs)
        if self.title is None or self.title == "":
            self.title = str(self.pk)
        super(Visualisation, self).save(*args, **kwargs)

