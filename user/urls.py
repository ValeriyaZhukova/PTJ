from user import views
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from allauth.account.views import confirm_email
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    # User
    path('admin/', admin.site.urls),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.UserRegisterView.as_view()),
    path('user/', views.UserGetAllView.as_view()),
    path('user/<int:pk>', views.UserGetView.as_view()),
    path('update/user/<int:pk>', views.UserUpdateView.as_view()),
    path('delete/user/<int:pk>', views.UserDeleteView.as_view()),
    # User status
    path('add/user/status/', views.StatusAddView.as_view()),
    path('user/status/<int:pk>', views.StatusGetByUserView.as_view()),
    # Employee rating
    path('add/user/rating/', views.EmployeeRatingAddView.as_view()),
    path('user/rating/<int:pk>', views.EmployeeRatingGetByEmployeeView.as_view()),
    # WorkList
    path('add/worklist/', views.WorkListAddView.as_view()),
    path('user/worklist/<int:pk>', views.WorkListGetView.as_view()),
    # Profile
    path('add/profile/', views.ProfileAddView.as_view()),
    path('profile/', views.ProfileGetAllView.as_view()),
    path('profile/<int:pk>', views.ProfileGetView.as_view()),
    path('update/profile/<int:pk>', views.ProfileUpdateView.as_view()),
    path('delete/profile/<int:pk>', views.ProfileDeleteView.as_view()),
    # Profile industries
    path('add/profile/industries/', views.ProfileIndustriesAddView.as_view()),
    path('profile/industries/<int:profile_id>', views.ProfileIndustriesGetByProfileView.as_view()),
    path('industry/vacancies/<int:industry_id>', views.ProfileIndustriesGetByIndustryView.as_view()),
    
    
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]