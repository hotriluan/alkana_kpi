from django.db import models

# Create your models here.

class HangHoa(models.Model):
    Name = models.CharField(max_length=100)
    qty = models.IntegerField()
    unitprice = models.IntegerField()
    totalamount = models.IntegerField(editable=False, default=0)
    
    class Meta:
        verbose_name = 'Hàng hóa'
        verbose_name_plural = 'Hàng hóa'
        ordering = ['Name']

    def save(self, *args, **kwargs):
        """
        Overrides the save method to automatically calculate and set the total amount
        based on the quantity (qty) and unit price (unitprice) before saving the instance.

        Args:
            *args: Variable length argument list passed to the parent save method.
            **kwargs: Arbitrary keyword arguments passed to the parent save method.
        """
        self.totalamount = self.qty * self.unitprice
        super().save(*args, **kwargs) # Call the parent class's save method to ensure the instance is saved correctly.

    @property
    def total(self):
        return self.qty * self.unitprice

    def __str__(self):
        return self.Name
