from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    # pro_pic = models.FileField(blank=True, null=True,upload_to='pro_pictures')

    def __str__(self):
        return self.name

class Bill(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    gst_number = models.CharField(max_length=20, blank=True, null=True)
    hsn_code = models.CharField(max_length=20, blank=True, null=True)
    customer_details = models.TextField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    include_tax = models.BooleanField(default=False, null=True,blank=True)

    def __str__(self):
        return f'Bill {self.id} - {self.date}'

class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    gross_weight = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    stone_weight = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    net_weight = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    ornament_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    value_addition = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stone_charge = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    huid = models.CharField(max_length=10,null=True, blank=True,)

    def get_total_value(self):
        return (self.ornament_value + self.value_addition + self.stone_charge) * self.quantity * self.product.price