from django.db import models

class Feedback(models.Model):
    name = models.CharField(max_length=90)
    mobile_no = models.CharField(max_length=20)
    email = models.EmailField(null= False,blank=False)
    district = models.CharField(max_length=100)
    massage = models.TextField(max_length=400)

    def __str__(self):
        return f'{self.name} - {self.mobile_no}'