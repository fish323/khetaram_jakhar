from django.db import models

class Workmodels(models.Model):
    client_name = models.CharField(max_length=200)
    type_of_work = models.CharField(max_length=300)
    site = models.CharField(max_length=300)
    
    # CHANGED: Use IntegerField for Year instead of DateField
    start_from = models.IntegerField(help_text="Enter Start Year (e.g. 2020)")
    end_at = models.IntegerField(help_text="Enter End Year (e.g. 2022)")
    
   # Keep storing the full amount in Rupees here
    value = models.BigIntegerField()
    
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
         return f"{self.client_name}"

   # --- MAKE SURE THIS IS HERE AND INDENTED CORRECTLY ---
    @property
    def value_in_crores(self):
        if self.value:
            # 1 Crore = 10,000,000
            # Dividing value by 1 Cr to get the decimal
            return f"{self.value / 10000000:.2f}"
        return "0.00"
    
# ... (Keep Strengthmodel and Equipmentmodel as they are)


class Strengthmodel(models.Model):
    description = models.CharField(max_length=200)
    quantity = models.IntegerField()
    # Field to store the custom order
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.description}"

class Equipmentmodel(models.Model):
    description = models.CharField(max_length=200)
    quantity = models.IntegerField()
    # Field to store the custom order
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.description}"