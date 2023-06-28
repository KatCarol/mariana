from django.db import models

class Drug(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    manufacturer = models.CharField(max_length=100)
    selling_price = models.PositiveIntegerField()
    # Other fields such as dosage, cost, etc.

    def __str__(self):
        return f'{self.name} by {self.manufacturer}'
    
    def get_quantity(self):
        return sum(batch.quantity for batch in self.batches.all())


class Batch(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='batches')
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE, related_name='batches')
    batch_number = models.CharField(max_length=100, null=True)
    quantity = models.PositiveIntegerField()
    quantity_stocked = models.PositiveIntegerField(null=True)
    expiration_date = models.DateField()
    time_registered = models.DateTimeField(auto_now_add=True)
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.drug.name} - {self.expiration_date}"


class Stock(models.Model):
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Date: {self.date}"


class Invoice(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def total_price(self):
        return sum(item.total_price for item in self.sales_items.all())

    def invoice_number(self):
        return self.id
    
    def total_items(self):
        return sum(item.quantity for item in self.sales_items)
    
    def total_price(self):
        return sum(
            (item.drug.selling_price * item.quantity) for item in self.sales_items
        )
    

class SalesItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='sales_items')
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='sales_items')
    quantity = models.PositiveSmallIntegerField()

    def total_price(self):
        return self.drug.selling_price * self.quantity


class Patient(models.Model):
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    address = models.CharField(max_length=50)


class Diagnosis(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnosis = models.CharField(max_length=50)
    details = models.TextField(null=True, blank=True)
    prescription = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.patient.name
    
    def getDate(self):
        return self.date
    
    def getTime(self):
        return self.date


class ProductCategory(models.Model):
    class Meta:
        verbose_name_plural = "Product categories"
    
    name = models.CharField(max_length=50)
    image = models.ImageField()
    description = models.TextField()

    def __str__(self) -> str:
        return self.name