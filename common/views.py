from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, AllowAny, SAFE_METHODS
from common import serializers
from common.models import City, Industry

# Create your views here.


class IsAdminUserOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super(
            IsAdminUserOrReadOnly,
            self).has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin


# City CRUD
class CityAddView(APIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializers_class = serializers.CitySerializer

    def post(self, request, format=None):
        serializer = self.serializers_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CityGetAllView(APIView):
    serializers_class = serializers.CitySerializer

    def get(self, request, format=None):
        city = City.objects.all()
        serializer = self.serializers_class(city, many=True)
        return Response(serializer.data)


class CityGetView(APIView):
    serializers_class = serializers.CitySerializer

    def get_queryset(self, pk):
        try:
            city = City.objects.get(pk=pk)
        except City.DoesNotExist:
            return False
        return city

    def get(self, request, pk, format=None):
        city = self.get_queryset(pk)
        if not city:
            content = \
                {
                    'status': 'Not Found'
                }
            return Response(content, status.HTTP_400_BAD_REQUEST)
        serializer = self.serializers_class(city)
        return Response(serializer.data)


class CityUpdateView(APIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializers_class = serializers.CitySerializer

    def get_queryset(self, pk):
        try:
            city = City.objects.get(pk=pk)
        except City.DoesNotExist:
            return False
        return city

    def put(self, request, pk, format=None):
        city = self.get_queryset(pk)
        if not city:
            content = \
                {
                    "status": "Not Found"
                }
            return Response(content, status.HTTP_404_NOT_FOUND)
        serializer = self.serializers_class(city, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CityDeleteView(APIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializers_class = serializers.CitySerializer

    def get_queryset(self, pk):
        try:
            city = City.objects.get(pk=pk)
        except City.DoesNotExist:
            return False
        return city

    def delete(self, reqest, pk, format=None):
        city = self.get_queryset(pk)
        if not city:
            content = \
                {
                    "status": "Not found"
                }
            return Response(content, status.HTTP_404_NOT_FOUND)
        city.delete()
        return Response({"msg": "No Content"}, status=status.HTTP_204_NO_CONTENT)


# Industry CRUD
class IndustryAddView(APIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializers_class = serializers.IndustrySerializer

    def post(self, request, format=None):
        serializer = self.serializers_class(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class IndustryGetAllView(APIView):
    serializers_class = serializers.IndustrySerializer

    def get(self, request, format=None):
        industry = Industry.objects.all()
        serializer = self.serializers_class(industry, many=True)
        return Response(serializer.data)


class IndustryGetView(APIView):
    serializers_class = serializers.IndustrySerializer

    def get_queryset(self, pk):
        try:
            industry = Industry.objects.get(pk=pk)
        except Industry.DoesNotExist:
            return False
        return industry

    def get(self, request, pk, format=None):
        industry = self.get_queryset(pk)

        if not industry:
            content = \
                {
                    'status': 'Not Found'
                }
            return Response(content, status.HTTP_400_BAD_REQUEST)

        serializer = self.serializers_class(industry)
        return Response(serializer.data)


class IndustryUpdateView(APIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializers_class = serializers.IndustrySerializer

    def get_queryset(self, pk):
        try:
            industry = Industry.objects.get(pk=pk)
        except Industry.DoesNotExist:
            return False
        return industry

    def put(self, request, pk, format=None):
        industry = self.get_queryset(pk)
        if not industry:
            content = \
                {
                    "status": "Not Found"
                }
            return Response(content, status.HTTP_404_NOT_FOUND)
        serializer = self.serializers_class(industry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class IndustryDeleteView(APIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializers_class = serializers.IndustrySerializer

    def get_queryset(self, pk):
        try:
            industry = Industry.objects.get(pk=pk)
        except Industry.DoesNotExist:
            return False
        return industry

    def delete(self, reqest, pk, format=None):
        industry = self.get_queryset(pk)
        if not industry:
            content = \
                {
                    "status": "Not found"
                }
            return Response(content, status.HTTP_404_NOT_FOUND)
        industry.delete()
        return Response({"msg": "No Content"}, status=status.HTTP_204_NO_CONTENT)
