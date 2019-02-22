from django.db import models
from apps.log_reg.models import User

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=45)
    user_owning_item = models.ForeignKey(User, related_name="owned_items", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)