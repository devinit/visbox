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
    
    # def get_absolute_url(self):
    #     return reverse('core.views.data',args=[self.pk])

