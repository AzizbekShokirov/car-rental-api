from django.core.management.base import BaseCommand
from car_rental.models import RentPrice, CarType


class Command(BaseCommand):
    help = 'Initialize rental prices for different car types'

    def handle(self, *args, **kwargs):
        rent_prices = {
            CarType.SEDAN: 50,
            CarType.COUPE: 80,
            CarType.WAGON: 60,
            CarType.CABRIO: 100,
            CarType.SUV: 150,
        }

        for car_type, price in rent_prices.items():
            RentPrice.objects.get_or_create(
                car_type=car_type,
                defaults={'daily_rate': price}
            )
            
        self.stdout.write(self.style.SUCCESS('Successfully initialized rental prices'))
