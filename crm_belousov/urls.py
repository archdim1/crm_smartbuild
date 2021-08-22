"""crm_belousov URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django_filters.views import FilterView


from crm.views import ProjectCreateView, \
    CompanyListView, InteractionListView, \
    InteractionDetailView, \
    InteractionCreateView, \
    ProjectListView, \
    InteractionUpdateView, \
    InteractionDeleteView, \
    ManagerCRMDetailView, \
    ManagerCRMListView, \
    CustomerListView, \
    CustomerDetailView, \
    UserDetailView, \
    UpdatePassword, \
    UserUpdateView, \
    UserManagerCRMUpdateView, \
    UserCustomerUpdateView, \
    InteractionManagerCRMListView, \
    AboutPageDetailView, \
    ProjectCustomerListView


urlpatterns = [
    path('admin/', admin.site.urls, ),
]

urlpatterns += [
    path('companies/', CompanyListView.as_view(), name='companies'),
    path('about/', AboutPageDetailView.as_view(), name='about'),
    path('company/', include('crm.urls')),

    path('projects/', ProjectListView.as_view(), name='projects'),
    path('project/create/', ProjectCreateView.as_view(), name='project_create'),


    path('manager_crm_list/', ManagerCRMListView.as_view(), name='manager_crm_list'),
    path('manager_crm/<int:pk>/', ManagerCRMDetailView.as_view(), name='manager_crm_detail'),

    path('user/profile/', UserDetailView.as_view(), name='user_profile'),
    path('user/update/', UserUpdateView.as_view(), name='user_update'),
    path('user_managercrm/update/', UserManagerCRMUpdateView.as_view(), name='user_managercrm_update'),
    path('user_customer/update/', UserCustomerUpdateView.as_view(), name='user_customer_update'),
    path('user/change-password/', UpdatePassword.as_view(), name="update_password"),


    path('customer_list/', CustomerListView.as_view(), name='customer_list'),
    path('customer/<int:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
    path('customer/project_list/', ProjectCustomerListView.as_view(), name='customer_project_list'),

    path('interactions/', InteractionListView.as_view(), name='interactions'),
    path('interaction/<int:pk>/', InteractionDetailView.as_view(), name='interaction-detail'),
    path('interaction/create/', InteractionCreateView.as_view(), name='interaction_create'),
    path('interaction/<int:pk>/update/', InteractionUpdateView.as_view(), name='interaction_update'),
    path('interaction/<int:pk>/delete/', InteractionDeleteView.as_view(), name='interaction_delete'),
    path('user/interactions/', InteractionManagerCRMListView.as_view(), name='interaction_manager_crm'),

]

urlpatterns += [
    path('', RedirectView.as_view(url='/crm/', permanent=True)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
