from rest_framework import serializers
from common.models import City, Industry
from user.models import CustomUser, Profile, WorkList, Status, EmployeeRating, ProfileIndustries
from company.models import Company, Vacancy, VacancyIndustries, AppliedVacancies, FavoriteVacancies, CompanyRating, Comments


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'city')


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ('id', 'industry')


class CustomUserDetailsSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = CustomUser.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'is_aspirant', 'is_contact_person')


class ProfileSerializer(serializers.ModelSerializer):
    user = CustomUserDetailsSerializer(read_only=True)
    city = CitySerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'date_of_birth', 'citizenship', 'desired_position', 'working_experience', 'education_degree',
                  'skills', 'institution', 'city', 'avatar')


class ProfileIndustriesSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    industry = IndustrySerializer(read_only=True)

    class Meta:
        model = ProfileIndustries
        fields = ('id', 'profile', 'industry')


class StatusSerializer(serializers.ModelSerializer):
    user = CustomUserDetailsSerializer(read_only=True)

    class Meta:
        model = Status
        fields = ('id', 'status', 'user')


class CompanySerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    contact_person = CustomUserDetailsSerializer(read_only=True)

    class Meta:
        model = Company
        fields = ('id', 'name', 'bin', 'about', 'address', 'website', 'image', 'city', 'contact_person')


class CompanyRatingSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    user = CustomUserDetailsSerializer(read_only=True)

    class Meta:
        model = CompanyRating
        fields = ('id', 'total_rating', 'salary', 'conditions', 'atmosphere', 'interesting_job', 'reputation',
                  'company', 'user')


class CommentsSerializer(serializers.ModelSerializer):    
    user = CustomUserDetailsSerializer(read_only=True)
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Comments
        fields = ('id', 'text', 'date', 'user', 'company')


class VacancySerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Vacancy
        fields = ('id', 'title', 'description', 'salary', 'contract_type', 'required_experience', 'duties',
                  'requirements', 'conditions', 'company')


class VacancyIndustriesSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    industry = IndustrySerializer(read_only=True)

    class Meta:
        model = VacancyIndustries
        fields = ('id', 'vacancy', 'industry')


class AppliedVacanciesSerializer(serializers.ModelSerializer):
    user = CustomUserDetailsSerializer(read_only=True)
    vacancy = VacancySerializer(read_only=True)

    class Meta:
        model = AppliedVacancies
        fields = ('id', 'user', 'vacancy')


class FavoriteVacanciesSerializer(serializers.ModelSerializer):
    user = CustomUserDetailsSerializer(read_only=True)
    vacancy = VacancySerializer(read_only=True)

    class Meta:
        model = FavoriteVacancies
        fields = ('id', 'user', 'vacancy')


class WorkListSerializer(serializers.ModelSerializer):
    user = CustomUserDetailsSerializer(read_only=True)
    company = CompanySerializer(read_only=True)

    class Meta:
        model = WorkList
        fields = ('id', 'work_began', 'work_finished', 'position', 'user', 'company')


class EmployeeRatingSerializer(serializers.ModelSerializer):
    user = CustomUserDetailsSerializer(read_only=True)
    company = CompanySerializer(read_only=True)

    class Meta:
        model = EmployeeRating
        fields = ('id', 'total_rating', 'competence', 'effectiveness', 'responsibility', 'communicability',
                  'hard_work', 'user', 'company')
