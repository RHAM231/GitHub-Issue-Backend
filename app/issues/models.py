from django.db import models


class Issue(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    body = models.CharField(max_length=100)
    # created_at = 
    # updated_at = 
    # closded_at = 
    # number = 
    

    def __str__(self):
        return self.name
