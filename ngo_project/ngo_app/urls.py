"""
URL Configuration for NGO app.
"""

from django.urls import path
from . import views

app_name = 'ngo_app'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Auth
    path('register/', views.register, name='register'),
    
    # Organization URLs
    path('organizations/', views.OrganizationListView.as_view(), name='organization-list'),
    path('organizations/create/', views.OrganizationCreateView.as_view(), name='organization-create'),
    path('organizations/<slug:slug>/', views.OrganizationDetailView.as_view(), name='organization-detail'),
    path('organizations/<slug:slug>/edit/', views.OrganizationUpdateView.as_view(), name='organization-update'),
    
    
    # Member URLs
    path('members/', views.MemberListView.as_view(), name='member-list'),
    path('members/<int:pk>/', views.MemberDetailView.as_view(), name='member-detail'),
    path('members/create/', views.MemberCreateView.as_view(), name='member-create'),
    path('members/<int:pk>/edit/', views.MemberUpdateView.as_view(), name='member-update'),
    
    # Project URLs
    path('projects/', views.ProjectListView.as_view(), name='project-list'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='project-create'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('projects/<slug:slug>/edit/', views.ProjectUpdateView.as_view(), name='project-update'),
    path('projects/<slug:slug>/delete/', views.ProjectDeleteView.as_view(), name='project-delete'),

    # Donation URLs
    path('donations/', views.DonationListView.as_view(), name='donation-list'),
    path('donations/<int:pk>/', views.DonationDetailView.as_view(), name='donation-detail'),
    path('donations/create/', views.DonationCreateView.as_view(), name='donation-create'),
    path('donations/<int:pk>/edit/', views.DonationUpdateView.as_view(), name='donation-update'),
    path('donations/<int:pk>/accept/', views.donation_accept, name='donation-accept'),
    path('donations/<int:pk>/cancel/', views.donation_cancel, name='donation-cancel'),
]
