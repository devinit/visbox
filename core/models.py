from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


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
    group_by = models.CharField(null=True,blank=True,max_length=255)
    sort = models.CharField(null=True,blank=True,max_length=255)
    y_maximum = models.CharField(null=True,blank=True,max_length=255,default="auto")
    y_maximum_value = models.DecimalField(null=True,blank=True,max_digits=99,decimal_places=5)
    x_maximum = models.CharField(null=True,blank=True,max_length=255,default="auto")
    x_maximum_value = models.DecimalField(null=True,blank=True,max_digits=99,decimal_places=5)
    colour = models.CharField(null=True,blank=True,max_length=255,default="#e84439")
    x_label = models.CharField(null=True,blank=True,max_length=255)
    y_label = models.CharField(null=True,blank=True,max_length=255)
    x_text_rotation = models.IntegerField(default=45)
    save_as_template = models.BooleanField(default=False)
    labels_on_chart = models.BooleanField(default=False)
    label_font_size = models.IntegerField(default=10)
    label_format = models.CharField(default=",.2f",max_length=255)
    unit_divisor = models.IntegerField(default=1)
    
    def __unicode__(self):
        return u'%s' % self.title
    
    class Meta:
        ordering = ['-created']
        
    def get_absolute_url(self):
        return reverse('core.views.viewVis',args=[self.pk])
    
    def save(self, *args, **kwargs):
        super(Visualisation, self).save(*args, **kwargs)
        if self.title is None or self.title == "":
            self.title = self.chart_type + " " + str(self.pk)
        super(Visualisation, self).save(*args, **kwargs)

