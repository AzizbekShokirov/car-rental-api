from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Car, Rental, RentPrice


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = [
            "id",
            "brand",
            "model",
            "car_type",
            "color",
            "engine_size",
            "fuel_type",
            "odometer",
            "year_of_production",
            "vin_number",
            "registration_number",
        ]


class RentPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentPrice
        fields = ["id", "car_type", "daily_rate"]


class RentalCreateSerializer(serializers.ModelSerializer):
    registration_number = serializers.CharField(
        source="car.registration_number", write_only=True
    )

    class Meta:
        model = Rental
        fields = ["id", "registration_number", "rent_start_date", "rent_duration"]

    def create(self, validated_data):
        car_data = validated_data.pop("car")
        registration_number = car_data.get("registration_number")

        car = get_object_or_404(Car, registration_number=registration_number)
        rental = Rental.objects.create(car=car, **validated_data)
        return rental


class RentalDetailSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source="car.brand", read_only=True)
    model = serializers.CharField(source="car.model", read_only=True)
    color = serializers.CharField(source="car.color", read_only=True)
    car_type = serializers.CharField(source="car.car_type", read_only=True)
    registration_number = serializers.CharField(
        source="car.registration_number", read_only=True
    )
    rent_end_date = serializers.DateField(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    fine = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Rental
        fields = [
            "id",
            "brand",
            "model",
            "color",
            "car_type",
            "registration_number",
            "rent_start_date",
            "rent_duration",
            "rent_end_date",
            "rent_complete",
            "price",
            "fine",
        ]


class RentalUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ["rent_complete"]
