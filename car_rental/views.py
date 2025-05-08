from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Car, Rental, RentPrice
from .serializers import (
    CarSerializer,
    RentalCreateSerializer,
    RentalDetailSerializer,
    RentalUpdateSerializer,
    RentPriceSerializer,
)


class CarListCreateView(ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    @extend_schema(
        summary="List all cars",
        description="Returns a list of all cars in the system",
        responses={200: CarSerializer(many=True)},
        tags=["Cars"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new car",
        description="Create a new car with all required fields. VIN number must be unique.",
        request=CarSerializer,
        responses={201: CarSerializer},
        tags=["Cars"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CarDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    @extend_schema(
        summary="Retrieve a specific car",
        description="Get details for a specific car by its ID",
        responses={200: CarSerializer, 404: "Car not found"},
        tags=["Cars"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update a car",
        description="Update a car's details by its ID",
        request=CarSerializer,
        responses={200: CarSerializer, 404: "Car not found"},
        tags=["Cars"],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update a car",
        description="Update specific fields of a car by its ID",
        request=CarSerializer,
        responses={200: CarSerializer, 404: "Car not found"},
        tags=["Cars"],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a car",
        description="Delete a car from the system by its ID",
        responses={204: "No content", 404: "Car not found"},
        tags=["Cars"],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class CarByVinView(APIView):
    @extend_schema(
        summary="Get car by VIN number",
        description="Retrieve car details using its VIN number",
        parameters=[
            OpenApiParameter(
                name="vin_number",
                description="The VIN number of the car",
                required=True,
                type=str,
            )
        ],
        responses={200: CarSerializer, 404: "Car not found"},
        tags=["Cars"],
    )
    def get(self, request):
        vin_number = request.query_params.get("vin_number")
        if not vin_number:
            return Response(
                {"error": "VIN number is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        car = get_object_or_404(Car, vin_number=vin_number)
        serializer = CarSerializer(car)
        return Response(serializer.data)


class RentalListCreateView(APIView):
    @extend_schema(
        summary="List all rentals",
        description="Returns a list of all rentals with detailed information",
        responses={200: RentalDetailSerializer(many=True)},
        tags=["Rentals"],
    )
    def get(self, request):
        rentals = Rental.objects.all()
        serializer = RentalDetailSerializer(rentals, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create a new rental",
        description="Create a new rental by providing car registration number and rental duration",
        request=RentalCreateSerializer,
        responses={201: RentalDetailSerializer},
        tags=["Rentals"],
    )
    def post(self, request):
        serializer = RentalCreateSerializer(data=request.data)
        if serializer.is_valid():
            rental = serializer.save()
            response_serializer = RentalDetailSerializer(rental)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RentalDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Rental, pk=pk)

    @extend_schema(
        summary="Retrieve a specific rental",
        description="Get details for a specific rental by its ID with calculated price and fine",
        responses={200: RentalDetailSerializer, 404: "Rental not found"},
        tags=["Rentals"],
    )
    def get(self, request, pk):
        rental = self.get_object(pk)
        serializer = RentalDetailSerializer(rental)
        return Response(serializer.data)

    @extend_schema(
        summary="Update a rental",
        description="Update a rental's completion status",
        request=RentalUpdateSerializer,
        responses={200: RentalDetailSerializer, 404: "Rental not found"},
        tags=["Rentals"],
    )
    def put(self, request, pk):
        rental = self.get_object(pk)
        serializer = RentalUpdateSerializer(rental, data=request.data)
        if serializer.is_valid():
            rental = serializer.save()
            response_serializer = RentalDetailSerializer(rental)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Partially update a rental",
        description="Update specific fields of a rental (mainly rent_complete)",
        request=RentalUpdateSerializer,
        responses={200: RentalDetailSerializer, 404: "Rental not found"},
        tags=["Rentals"],
    )
    def patch(self, request, pk):
        rental = self.get_object(pk)
        serializer = RentalUpdateSerializer(rental, data=request.data, partial=True)
        if serializer.is_valid():
            rental = serializer.save()
            response_serializer = RentalDetailSerializer(rental)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete a rental",
        description="Delete a rental from the system",
        responses={204: "No content", 404: "Rental not found"},
        tags=["Rentals"],
    )
    def delete(self, request, pk):
        rental = self.get_object(pk)
        rental.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RentalOverdueView(ListAPIView):
    serializer_class = RentalDetailSerializer

    def get_queryset(self):
        today = timezone.now().date()

        # Get all incomplete rentals
        rentals = Rental.objects.filter(rent_complete=False)

        # Build a list of PKs for overdue rentals
        overdue_pks = []
        for rental in rentals:
            end_date = rental.rent_start_date + timezone.timedelta(
                days=rental.rent_duration
            )
            if end_date < today:
                overdue_pks.append(rental.pk)

        # Return rentals with overdue PKs
        return Rental.objects.filter(pk__in=overdue_pks)

    @extend_schema(
        summary="List overdue rentals",
        description="Get all rentals that are overdue (past end date and not completed)",
        responses={200: RentalDetailSerializer(many=True)},
        tags=["Rentals"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class RentPriceListView(ListAPIView):
    queryset = RentPrice.objects.all()
    serializer_class = RentPriceSerializer

    @extend_schema(
        summary="List all rent prices",
        description="Get daily rental rates for each car type",
        responses={200: RentPriceSerializer(many=True)},
        tags=["Pricing"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
