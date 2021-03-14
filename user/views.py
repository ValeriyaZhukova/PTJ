from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from common.models import City, Industry
from company.models import Company
from user.models import CustomUser, Profile, Status, WorkList, EmployeeRating, ProfileIndustries
from common import serializers


# Create your views here.


# User CRUD
class UserRegisterView(CreateAPIView):
    model = CustomUser
    queryset = CustomUser.objects.all()
    serializer_class = serializers.CustomUserDetailsSerializer
    permission_classes = (AllowAny,)


class UserGetAllView(APIView):
    serializers_class = serializers.CustomUserDetailsSerializer

    def get(self, request, format=None):
        users = CustomUser.objects.all()
        serializer = self.serializers_class(users, many=True)
        return Response(serializer.data)


class UserGetView(APIView):
    serializers_class = serializers.CustomUserDetailsSerializer

    def get_queryset(self, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return False
        return user

    def get(self, request, pk, format=None):
        user = self.get_queryset(pk)
        if not user:
            content = \
                {
                    'status': 'Not Found'
                }
            return Response(content, status.HTTP_400_BAD_REQUEST)
        serializer = self.serializers_class(user)
        return Response(serializer.data)


class UserUpdateView(APIView):
    serializers_class = serializers.CustomUserDetailsSerializer
    permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.all()

    def get_queryset(self, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return False
        return user

    def put(self, request, pk, format=None):
        user = self.get_queryset(pk)
        if not user:
            content = \
                {
                    'status': 'Not Found'
                }
            return Response(content, status.HTTP_400_BAD_REQUEST)
        serializer = self.serializers_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(APIView):
    serializers_class = serializers.CustomUserDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return False
        return user

    def delete(self, request, pk, format=None):
        user = self.get_queryset(pk)
        if not user:
            content = \
                {
                    'status': 'Not Found'
                }
            return Response(content, status.HTTP_400_BAD_REQUEST)
        user.delete()
        return Response({'msg': 'Successfully deleted'}, status=status.HTTP_200_OK)


# Employee Rating
class EmployeeRatingAddView(APIView):
    permission_classes = (IsAuthenticated,)
    serializers_class = serializers.EmployeeRatingSerializer

    def post(self, request, format=None):
        serializer = self.serializers_class(data=request.data)
        if serializer.is_valid():
            try:
                employee_rating = EmployeeRating.objects.get(company=serializer.validated_data.get('company'),
                                                             user=request.user)
                employee_rating.save()
                return Response(self.serializers_class(employee_rating).data)
            except EmployeeRating.DoesNotExist:
                serializer.save(company=Company.objects.get(pk=request.data["company"]), user=request.user)
                return Response(serializer.data)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeRatingGetByEmployeeView(APIView):
    serializers_class = serializers.EmployeeRatingSerializer

    def get(self, request, employee_id, format=None):
        employee_rating = EmployeeRating.objects.select_related('user').filter(user=employee_id)
        serializer = self.serializers_class(employee_rating, many=True)
        return Response(serializer.data)


# User Status
class StatusAddView(APIView):
    permission_classes = (IsAuthenticated,)
    serializers_class = serializers.StatusSerializer

    def post(self, request, format=None):
        serializer = self.serializers_class(data=request.data)
        if serializer.is_valid():
            try:
                user_status = Status.objects.get(user=request.user)
                user_status.save()
                return Response(self.serializers_class(user_status).data)
            except Status.DoesNotExist:
                serializer.save(user=request.user)
                return Response(serializer.data)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class StatusGetByUserView(APIView):
    serializers_class = serializers.StatusSerializer

    def get_queryset(self, pk):
        try:
            user_status = Status.objects.select_related('user').get(pk=pk)
        except Status.DoesNotExist:
            return False
        return user_status

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


class StatusUpdateView(APIView):
    permission_classes = (IsAuthenticated,)
    serializers_class = serializers.StatusSerializer

    def get_queryset(self, pk):
        try:
            user_status = Status.objects.get(pk=pk)
        except Status.DoesNotExist:
            return False
        return user_status

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


# Profile CRUD
class ProfileAddView(APIView):
    permission_classes = (IsAuthenticated,)
    serializers_class = serializers.ProfileSerializer

    def post(self, request, format=None):
        serializer = self.serializers_class(data=request.data)
        if serializer.is_valid():
            try:
                profile = Profile.objects.get(city=serializer.validated_data.get('city'),
                                              user=request.user)
                profile.save()
                return Response(self.serializers_class(profile).data)
            except Profile.DoesNotExist:
                serializer.save(user=request.user, city=City.objects.get(pk=request.data["city"]))
                return Response(serializer.data)
        else:
            Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProfileGetAllView(APIView):
    serializers_class = serializers.ProfileSerializer

    def get(self, request, format=None):
        profile = Profile.objects.select_related('user').all()
        serializer = self.serializers_class(profile, many=True)
        return Response(serializer.data)


class ProfileGetView(APIView):
    serializers_class = serializers.ProfileSerializer

    def get_queryset(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return False
        return profile

    def get(self, request, pk, format=None):
        profile = self.get_queryset(pk)
        if not profile:
            content = \
                {
                    'status': 'Not Found'
                }
            return Response(content, status.HTTP_400_BAD_REQUEST)
        serializer = self.serializers_class(profile)
        return Response(serializer.data)


class ProfileUpdateView(APIView):
    serializers_class = serializers.ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return False
        return profile

    def put(self, request, pk, format=None):
        profile = self.get_queryset(pk)
        if not profile:
            content = \
                {
                    'status': 'Not Found'
                }
            return Response(content, status.HTTP_400_BAD_REQUEST)
        serializer = self.serializers_class(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProfileDeleteView(APIView):
    serializers_class = serializers.ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return False
        return profile

    def delete(self, request, pk, format=None):
        profile = self.get_queryset(pk)
        if not profile:
            content = \
                {
                    'status': 'Not Found'
                }
            return Response(content, status.HTTP_400_BAD_REQUEST)
        profile.delete()
        return Response({'msg': 'Successfully deleted'}, status=status.HTTP_200_OK)


# Profile Industries
class ProfileIndustriesAddView(APIView):
    permission_classes = (IsAuthenticated,)
    serializers_class = serializers.ProfileIndustriesSerializer

    def post(self, request, format=None):
        serializer = self.serializers_class(data=request.data)
        if serializer.is_valid():
            try:
                profile_industries = ProfileIndustries.objects.get(profile=serializer.validated_data.get('profile'),
                                                                   industry=serializer.validated_data.get('industry'))
                profile_industries.save()
                return Response(self.serializers_class(profile_industries).data)
            except ProfileIndustries.DoesNotExist:
                serializer.save(profile=Profile.objects.get(pk=request.data["profile"]),
                                industry=Industry.objects.get(pk=request.data["industry"]))
                return Response(serializer.data)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProfileIndustriesGetByProfileView(APIView):
    serializers_class = serializers.ProfileIndustriesSerializer

    def get(self, request, profile_id, format=None):
        profile_industries = ProfileIndustries.objects.select_related('profile', 'industry').filter(profile=profile_id)
        serializer = self.serializers_class(profile_industries, many=True)
        return Response(serializer.data)


class ProfileIndustriesGetByIndustryView(APIView):
    serializers_class = serializers.ProfileIndustriesSerializer

    def get(self, request, industry_id, format=None):
        profile_industries = ProfileIndustries.objects.select_related('industry', 'profile').filter(
            industry=industry_id)
        serializer = self.serializers_class(profile_industries, many=True)
        return Response(serializer.data)


# WorkList
class WorkListAddView(APIView):
    serializers_class = serializers.WorkListSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = self.serializers_class(data=request.data)
        if serializer.is_valid():
            try:
                work_list = WorkList.objects.get(user=request.user,
                                                 company=serializer.validated_data.get('company'))
                serializer.save()
                return Response(self.serializers_class(work_list).data)
            except WorkList.DoesNotExist:
                serializer.save(user=request.user, company=Company.objects.get(pk=request.data["company"]))
                return Response(serializer.data)
        else:
            Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class WorkListGetView(APIView):
    serializers_class = serializers.WorkListSerializer

    def get(self, request, user_id, format=None):
        work_list = WorkList.objects.select_related('user').filter(user=user_id)
        serializer = self.serializers_class(work_list, many=True)
        return Response(serializer.data)
