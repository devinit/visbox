from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class Dataset(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    data = models.TextField()
    sep = models.CharField(max_length=1, null=True, blank=True)
    
    class Meta:
        ordering = ['-created']
    
    def __unicode__(self):
        return u'%s' % self.name
    
    def get_absolute_url(self):
        return reverse('core.views.dataset',args=[self.pk])
    
class Visualisation(models.Model):
    chart_type = models.CharField(max_length=255)
    dataset = models.ForeignKey(Dataset)
    creator = models.ForeignKey(User, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField(default=960)
    height = models.IntegerField(default=500)
    padding_top = models.IntegerField(default=20)
    padding_right = models.IntegerField(default=100)
    padding_bottom = models.IntegerField(default=100)
    padding_left = models.IntegerField(default=100)
    x_indicator = models.CharField(null=True,blank=True,max_length=255)
    y_indicator = models.CharField(null=True,blank=True,max_length=255)
    z_indicator = models.CharField(null=True,blank=True,max_length=255)
    c_indicator = models.CharField(null=True,blank=True,max_length=255)
    sort = models.CharField(null=True,blank=True,max_length=255)
    y_maximum = models.CharField(null=True,blank=True,max_length=255)
    y_maximum_value = models.DecimalField(null=True,blank=True,max_digits=99,decimal_places=5)
    colour = models.CharField(null=True,blank=True,max_length=255)
    x_label = models.CharField(null=True,blank=True,max_length=255)
    y_label = models.CharField(null=True,blank=True,max_length=255)
    x_text_rotation = models.IntegerField(default=45)
    
    class Meta:
        ordering = ['-created']

