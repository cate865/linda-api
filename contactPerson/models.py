from django.db import models
from linda import settings

# Create your models here.
class ContactPerson(models.Model):
    email = models.TextField(null=False)
    name = models.TextField(null=False)
    phone = models.CharField(max_length=50, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)


# class Contact(models.Model):
#     contact_id = models.IntegerField(null=False)
    # user_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=False)
#     person_id = models.ForeignKey(ContactPerson, on_delete=models.CASCADE, null=False)
