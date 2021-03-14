from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from common import serializers
from common.models import City, Industry
from company.models import Company, CompanyRating, Comments, Vacancy, VacancyIndustries, AppliedVacancies, \
    FavoriteVacancies


# Create your views here.


# Company CRUD
class CompanyAddView(APIView):
    permission_classes = (IsAuthenticated,)
    serializers_class = serializers.CompanySerializer

    def post(self, request, format=None):
        serializer = self.serializers_class(data=request.data)
        if serializer.is_valid():
            try:
                company = Company.objects.get(city=serializer.validated_data.get('city'),
                                              contact_person=request.user)
                company.save()
                return Response(self.serializers_class(company).data)
            except Company.DoesNotExist:
                serializer.save(contact_person=request.user, city=City.objects.get(pk=request.data["city"]))
                return Response(serializer.data)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CompanyGetAllView(APIView):
    serializers_class = serializers.CompanySerializer

    def get(self, request, format=None):
        company = Company.objects.all()
        serializer = self.serializers_class(company, many=True)
        return Response(serializer.data)


class CompanyGetView(APIView):
    serializers_class = serializers.CompanySerializer

    def get_queryset(self, pk):
        try:
            company = Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            return False
        return company

    def get(self, request, pk, format=None):
        company = self.get_queryset(pk)
        if not company:
            content = \
                {
                    'status': 'Not Found'
                }
            return Response(content, status.HTTP_400_BAD_REQUEST)
        serializer = self.serializers_class(company)
        return Response(serializer.data)


class CompanyUpdateView(APIView):
    permission_classes = (IsAuthenticated,)
    serializers_class = serializers.CompanySerializer

    def get_queryset(self, pk):
        try:
            company = Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            return False
        return company

    def put(self, request, pk, format=None):
        company = self.get_queryset(pk)
        if not company:
            content = \
                {
                    "status": "Not Found"
                }
            return Response(content, status.HTTP_404_NOT_FOUND)
        serializer = self.serializers_class(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CompanyDeleteView(APIView):
    permission_classes = (IsAuthenticated,)
    serializers_class = serializers.CompanySerializer

    def get_queryset(self, pk):
        try:
            company = Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            return False
        return company

    def delete(self, reqest, pk, format=None):
        company = self.get_queryset(pk)
        if not company:
            content = \
                {
                    "status": "Not found"
                }
            return Response(content, status.HTTP_404_NOT_FOUND)
        company.delete()
        return Response({"msg": "No Content"}, status=status.HTTP_204_NO_CONTENT)


class CompanySearchView(APIView):
    serializers_class = serializers.CompanySerializer

    def get(self, request, key, format=None):
        companies = Company.objects.filter(Q(name__contains=key))
        serializer = self.serializers_class(companies, many=True)
        return Response(serializer.data)


# Company Rating 
class CompanyRatingAddView(APIView):
    permission_classes = (IsAuthenticated,)
    serializers_class = serializers.CompanyRatingSerializer

    def post(self, request, format=None):
        serializer = self.serializers_class(data=request.data)
        if serializer.is_valid():
            try:
                company_rating = CompanyRating.objects.get(company=serializer.validated_data.get('company'),
                                                           user=request.user)
                company_rating.save()
                return Response(self.serializers_class(company_rating).data)
            except CompanyRating.DoesNotExist:
                serializer.save(company=Company.objects.get(pk=request.data["company"]), user=request.user)
                return Response(serializer.data)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CompanyRatingGetByCompanyView(APIView):
    serializers_class = serializers.CompanyRatingSerializer

    def get(self, request, company_id, format=None):
        company_rating = CompanyRating.objects.select_related('company').filter(company=company_id)
        serializer = self.serializers_class(company_rating, many=True)
        return Response(serializer.data)


# Vacancy CRUD
class VacancyAddView(APIView):
    permission_classes = (IsAuthenticated,)
    serializers_class = serializers.VacancySerializer

    def post(self, request, format=None):
        serializer = self.serializers_class(data=request.data)
        if serializer.is_valid():
            try:
                vacancy = Vacancy.objects.get(company=serializer.validated_data.get('company'))
                vacancy.save()
                return Response(self.serializers_class(vacancy).data)
            except Vacancy.DoesNotExist:
                serializer.save(company=Company.objects.get(pk=request.data["company"]))
                return Response(serializer.data)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class VacancyGetAllView(APIView):
    serializers_class = serializers.VacancySerializer

    def get(self, request, format=None):
        vacancy = Vacancy.objects.all()
        serializer = self.serializers_class(vacancy, many=True)
        return Response(serializer.data)


class VacancyGetView(APIView):
    serializers_class = serializers.VacancySerializer

    def get_queryset(self, pk):
        try:
            vacancy = Vacancy.objects.get(pk=pk)
        except Vacancy.DoesNotExist:
            return False
        return vacancy

    def get(self, request, pk, format=None):
        vacancy = self.get_queryset(pk)
        if not vacancy:
            content = \
                {
                    'status': 'Not Found'
                }
            return Response(content, status.HTTP_400_BAD_REQUEST)
        serializer = self.serializers_class(vacancy)
        return Response(serializer.data)


class VacancyUpdateView(APIView):
    permission_classes = (IsAuthenticated,)
    serializers_class = serializers.VacancySerializer

    def get_queryset(self, pk):
        try:
            vacancy = Vacancy.objects.get(pk=pk)
        except Vacancy.DoesNotExist:
            return False
        return vacancy

    def put(self, request, pk, format=None):
        vacancy = self.get_queryset(pk)
        if not vacancy:
            content = \
                {
                    "status": "Not Found"
                }
            return Response(content, status.HTTP_404_NOT_FOUND)
        serializer = self.serializers_class(vacancy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class VacancyDeleteView(APIView):
    permission_classes = (IsAuthenticated,)
    serializers_class = serializers.VacancySerializer

    def get_queryset(self, pk):
        try:
            vacancy = Vacancy.objects.get(pk=pk)
        except Vacancy.DoesNotExist:
            return False
        return vacancy

    def delete(self, request, pk, format=None):
        vacancy = self.get_queryset(pk)
        if not vacancy:
            content = \
                {
                    "status": "Not found"
                }
            return Response(content, status.HTTP_404_NOT_FOUND)
        vacancy.delete()
        return Response({"msg": "No Content"}, status=status.HTTP_200_OK)


class VacancySearchView(APIView):
    serializers_class = serializers.VacancySerializer

    def get(self, request, key, format=None):
        vacancies = Vacancy.objects.filter(Q(title__contains=key))
        serializer = self.serializers_class(vacancies, many=True)
        return Response(serializer.data)


# Vacancy Industries
class VacancyIndustriesAddView(APIView):
    permission_classes = (IsAuthenticated,)
    serializers_class = serializers.VacancyIndustriesSerializer

    def post(self, request, format=None):
        serializer = self.serializers_class(data=request.data)
        if serializer.is_valid():
            try:
                vacancy_industries = VacancyIndustries.objects.get(vacancy=serializer.validated_data.get('vacancy'),
                                                                   industry=serializer.validated_data.get('industry'))
                vacancy_industries.save()
                return Response(self.serializers_class(vacancy_industries).data)
            except VacancyIndustries.DoesNotExist:
                serializer.save(vacancy=Vacancy.objects.get(pk=request.data["vacancy"]),
                                industry=Industry.objects.get(pk=request.data["industry"]))
                return Response(serializer.data)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class VacancyIndustriesGetByVacancyView(APIView):
    serializers_class = serializers.VacancyIndustriesSerializer

    def get(self, request, vacancy_id, format=None):
        vacancy_industries = VacancyIndustries.objects.select_related('vacancy').filter(vacancy=vacancy_id)
        serializer = self.serializers_class(vacancy_industries, many=True)
        return Response(serializer.data)


class VacancyIndustriesGetByIndustryView(APIView):
    serializers_class = serializers.VacancyIndustriesSerializer

    def get(self, request, industry_id, format=None):
        vacancy_industries = VacancyIndustries.objects.select_related('industry').filter(industry=industry_id)
        serializer = self.serializers_class(vacancy_industries, many=True)
        return Response(serializer.data)


# Applied Vacancies
class AppliedVacanciesAddView(APIView):
    serializers_class = serializers.AppliedVacanciesSerializer

    def post(self, request, format=None):
        serializer = self.serializers_class(data=request.data)
        if serializer.is_valid():
            try:
                applied_vacancy = AppliedVacancies.objects.get(user=request.user,
                                                               vacancy=serializer.validated_data.get('vacancy'))
                applied_vacancy.save()
                return Response(self.serializers_class(applied_vacancy).data)
            except AppliedVacancies.DoesNotExist:
                serializer.save(user=request.user, vacancy=Vacancy.objects.get(pk=request.data["vacancy"]))
                return Response(serializer.data)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AppliedVacanciesGetByVacancyView(APIView):
    serializers_class = serializers.AppliedVacanciesSerializer

    def get(self, request, vacancy_id, format=None):
        applied_vacancy = AppliedVacancies.objects.select_related('vacancy').filter(vacancy=vacancy_id)
        serializer = self.serializers_class(applied_vacancy, many=True)
        return Response(serializer.data)


class AppliedVacanciesGetByUserView(APIView):
    serializers_class = serializers.AppliedVacanciesSerializer

    def get(self, request, user_id, format=None):
        applied_vacancy = AppliedVacancies.objects.select_related('user').filter(user=user_id)
        serializer = self.serializers_class(applied_vacancy, many=True)
        return Response(serializer.data)


# Favorite Vacancies
class FavoriteVacanciesAddView(APIView):
    serializers_class = serializers.FavoriteVacanciesSerializer

    def post(self, request, format=None):
        serializer = self.serializers_class(data=request.data)
        if serializer.is_valid():
            try:
                favorite_vacancy = FavoriteVacancies.objects.get(user=request.user,
                                                                 vacancy=serializer.validated_data.get('vacancy'))
                favorite_vacancy.save()
                return Response(self.serializers_class(favorite_vacancy).data)
            except FavoriteVacancies.DoesNotExist:
                serializer.save(user=request.user, vacancy=Vacancy.objects.get(pk=request.data["vacancy"]))
                return Response(serializer.data)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class FavoriteVacanciesGetByUserView(APIView):
    serializers_class = serializers.FavoriteVacanciesSerializer

    def get(self, request, user_id, format=None):
        favorite_vacancy = FavoriteVacancies.objects.select_related('user').filter(user=user_id)
        serializer = self.serializers_class(favorite_vacancy, many=True)
        return Response(serializer.data)


# class FavoriteVacanciesDeleteView(APIView):
#     permission_classes = (IsAuthenticated,)
#     serializers_class = serializers.FavoriteVacanciesSerializer
#
#     def get_queryset(self, pk):
#         try:
#             fav = FavoriteVacancies.objects.get()
#         except FavoriteVacancies.DoesNotExist:
#             return False
#         return fav
#
#     def delete(self, request, pk, format=None):
#         vacancy = self.get_queryset(pk)
#         if not vacancy:
#             content = \
#                 {
#                     "status": "Not found"
#                 }
#             return Response(content, status.HTTP_404_NOT_FOUND)
#         vacancy.delete()
#         return Response({"msg": "No Content"}, status=status.HTTP_200_OK)


# Comments
class CommentsAddView(APIView):
    serializers_class = serializers.CommentsSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = self.serializers_class(data=request.data)
        if serializer.is_valid():
            try:
                comment = Comments.objects.get(user=request.user,
                                               company=serializer.validated_data.get('company'))
                serializer.save()
                return Response(self.serializers_class(comment).data)
            except Comments.DoesNotExist:
                serializer.save(user=request.user, company=Company.objects.get(pk=request.data["company"]))
                return Response(serializer.data)
        else:
            Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CommentsGetView(APIView):
    serializers_class = serializers.CommentsSerializer

    def get(self, request, company_id, format=None):
        comments = Comments.objects.select_related('user').filter(company=company_id)
        serializer = self.serializers_class(comments, many=True)
        return Response(serializer.data)
