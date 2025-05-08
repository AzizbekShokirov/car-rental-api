from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
import datetime


class CarType(models.TextChoices):
    SEDAN = "SEDAN", "Sedan"
    COUPE = "COUPE", "Coupe"
    WAGON = "WAGON", "Wagon"
    CABRIO = "CABRIO", "Cabrio"
    SUV = "SUV", "SUV"


class FuelType(models.TextChoices):
    PETROL = "PETROL", "Petrol"
    DIESEL = "DIESEL", "Diesel"
    ELECTRIC = "ELECTRIC", "Electric"
    HYBRID = "HYBRID", "Hybrid"


class Car(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    car_type = models.CharField(max_length=20, choices=CarType.choices)
    color = models.CharField(max_length=50)
    engine_size = models.DecimalField(max_digits=3, decimal_places=1)
    fuel_type = models.CharField(max_length=20, choices=FuelType.choices)
    odometer = models.IntegerField()
    year_of_production = models.IntegerField()
    vin_number = models.CharField(max_length=17, unique=True)
    registration_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.registration_number})"


class RentPrice(models.Model):
    car_type = models.CharField(max_length=20, choices=CarType.choices, unique=True)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.car_type} - ${self.daily_rate}/day"


class Rental(models.Model):
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        to_field="registration_number",
        related_name="rentals",
    )
    rent_start_date = models.DateField(default=timezone.now)
    rent_duration = models.IntegerField(validators=[MinValueValidator(1)])
    rent_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"Rental for {self.car} - {self.rent_start_date}"

    @property
    def rent_end_date(self):
        return self.rent_start_date + datetime.timedelta(days=self.rent_duration)

    @property
    def is_overdue(self):
        return not self.rent_complete and timezone.now().date() > self.rent_end_date

    @property
    def price(self):
        try:
            car_type = self.car.car_type
            rent_price = RentPrice.objects.get(car_type=car_type)
            return rent_price.daily_rate * self.rent_duration
        except (RentPrice.DoesNotExist, AttributeError):
            return 0

    @property
    def fine(self):
        if self.is_overdue:
            return self.price * 0.20
        return 0
