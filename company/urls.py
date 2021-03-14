from company import views
from django.urls import path, include

urlpatterns = [
    # Company
    path('add/company/', views.CompanyAddView.as_view()),
    path('company/', views.CompanyGetAllView.as_view()),
    path('company/<int:pk>', views.CompanyGetView.as_view()),
    path('update/company/<int:pk>', views.CompanyUpdateView.as_view()),
    path('delete/company/<int:pk>', views.CompanyDeleteView.as_view()),
    path('search/company/<str:key>', views.CompanySearchView.as_view()),
    # Company rating
    path('add/company/rating/', views.CompanyRatingAddView.as_view()),
    path('company/rating/<int:company_id>', views.CompanyRatingGetByCompanyView.as_view()),
    # Vacancy
    path('add/vacancy/', views.VacancyAddView.as_view()),
    path('vacancy/', views.VacancyGetAllView.as_view()),
    path('vacancy/<int:pk>', views.VacancyGetView.as_view()),
    path('update/vacancy/<int:pk>', views.VacancyUpdateView.as_view()),
    path('delete/vacancy/<int:pk>', views.VacancyDeleteView.as_view()),
    path('search/vacancy/<str:key>', views.VacancySearchView.as_view()),
    # Vacancy industries
    path('add/vacancy/industries/', views.VacancyIndustriesAddView.as_view()),
    path('vacancy/industries/<int:vacancy_id>', views.VacancyIndustriesGetByVacancyView.as_view()),
    path('industry/vacancies/<int:industry_id>', views.VacancyIndustriesGetByIndustryView.as_view()),
    # Applied vacancies
    path('add/applied-vacancies/', views.AppliedVacanciesAddView.as_view()),
    path('user/vacancies/<int:user_id>', views.AppliedVacanciesGetByUserView.as_view()),
    path('vacancy/users/<int:vacancy_id>', views.AppliedVacanciesGetByVacancyView.as_view()),
    # Favorite vacancies
    path('add/favorite-vacancies/', views.FavoriteVacanciesAddView.as_view()),
    path('user/favorites/<int:user_id>', views.FavoriteVacanciesGetByUserView.as_view()),
    #Comments
    path('add/comments/', views.CommentsAddView.as_view()),
    path('comments/<int:company_id>', views.CommentsGetView.as_view()),
]