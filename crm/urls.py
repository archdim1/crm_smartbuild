from django.urls import path
from .views import \
    CompanyDetailView, \
    CompanyCreateView, \
    CompanyDeleteView, \
    CompanyUpdateView, \
    CompanyProjectsDetailView, \
    ProjectDetailView, \
    ProjectDeleteView, \
    ProjectUpdateView, \
    CompanyProjectsNotStartedDetailView, \
    CompanyProjectsInProcessDetailView, \
    CompanyProjectsCompletedDetailView, \
    ProjectInteractionsDetailView, \
    CompanyProjectInteractionsDetailView, \
    CompanyInteractionsPhonesDetailView, \
    CompanyInteractionsEmailDetailView, \
    CompanyInteractionsMessengerDetailView, \
    ProjectInteractionsPhonesDetailView, \
    ProjectInteractionsEmailDetailView, \
    ProjectInteractionsMessengerDetailView


urlpatterns = [
    path('create/', CompanyCreateView.as_view(), name='company_create'),
    path('<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),

    path('<int:pk>/projects/', CompanyProjectsDetailView.as_view(), name='projects'),
    path('<int:pk>/interactions/', CompanyProjectInteractionsDetailView.as_view(), name='company_interactions'),

    path('<int:pk>/interactions_phones', CompanyInteractionsPhonesDetailView.as_view(),
         name='company_interactions_phones'),
    path('<int:pk>/interactions_email', CompanyInteractionsEmailDetailView.as_view(),
         name='company_interactions_email'),
    path('<int:pk>/interactions_messenger', CompanyInteractionsMessengerDetailView.as_view(),
         name='company_interactions_messenger'),

    path('<int:pk>/projects_not_started/', CompanyProjectsNotStartedDetailView.as_view(), name='projects_not_started'),
    path('<int:pk>/projects_in_process/', CompanyProjectsInProcessDetailView.as_view(), name='projects_in_process'),
    path('<int:pk>/completed/', CompanyProjectsCompletedDetailView.as_view(), name='projects_completed'),
    path('<int:pk>/delete/', CompanyDeleteView.as_view(), name='company_delete'),
    path('<int:pk>/update/', CompanyUpdateView.as_view(), name='company_update'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('project/<int:pk>/interactions/', ProjectInteractionsDetailView.as_view(), name='project_interactions'),
    path('project/<int:pk>/interactions_phones/', ProjectInteractionsPhonesDetailView.as_view(),
         name='project_interactions_phones'),
    path('project/<int:pk>/interactions_email/', ProjectInteractionsEmailDetailView.as_view(),
         name='project_interactions_phones'),
    path('project/<int:pk>/interactions_messenger/', ProjectInteractionsMessengerDetailView.as_view(),
         name='project_interactions_phones'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name='project_update'),

]
