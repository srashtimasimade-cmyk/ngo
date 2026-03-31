"""
Views for NGO Better Tomorrow application.
Implements CRUD operations with class-based views.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.db.models import Q, Sum, Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Organization, Member, Project, Donation, Impact
from .forms import OrganizationForm, MemberForm, ProjectForm, DonationForm


# ==================== Dashboard Views ====================

def dashboard(request):
    """Redirect root URL to donation list for a single-entrypoint UX."""
    return redirect('ngo_app:donation-list')


def register(request):
    """User registration view."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('ngo_app:project-list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# ==================== Organization Views ====================

class OrganizationListView(ListView):
    """List all organizations."""
    model = Organization
    template_name = 'ngo_app/organization_list.html'
    context_object_name = 'organizations'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Organization.objects.filter(status=Organization.Status.ACTIVE)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        return queryset.order_by('-created_at')


class OrganizationDetailView(DetailView):
    """View organization details with statistics."""
    model = Organization
    template_name = 'ngo_app/organization_detail.html'
    context_object_name = 'organization'
    slug_field = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        org = self.get_object()
        
        context['projects_count'] = org.projects.count()
        context['members_count'] = org.members.count()
        context['total_donations'] = org.donations.filter(
            status=Donation.Status.RECEIVED
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        context['recent_projects'] = org.projects.all()[:5]
        context['team_members'] = org.members.filter(status=Member.Status.ACTIVE)[:8]
        
        return context


class OrganizationCreateView(CreateView):
    """Create new organization."""
    model = Organization
    form_class = OrganizationForm
    template_name = 'ngo_app/organization_form.html'
    success_url = reverse_lazy('ngo_app:organization-list')


class OrganizationUpdateView(UpdateView):
    """Update organization information."""
    model = Organization
    form_class = OrganizationForm
    template_name = 'ngo_app/organization_form.html'
    slug_field = 'slug'
    
    def get_success_url(self):
        return reverse_lazy('ngo_app:organization-detail', kwargs={'slug': self.object.slug})


# ==================== Project Views ====================

class ProjectFilter(django_filters.FilterSet):
    """Filter for projects."""
    title = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.ChoiceFilter(choices=Project.Category.choices)
    status = django_filters.ChoiceFilter(choices=Project.Status.choices)
    
    class Meta:
        model = Project
        fields = ['category', 'status']


class ProjectListView(ListView):
    """List all projects with filtering."""
    model = Project
    template_name = 'ngo_app/project_list.html'
    context_object_name = 'projects'
    paginate_by = 12
    filterset_class = ProjectFilter
    
    def get_queryset(self):
        queryset = Project.objects.select_related('organization', 'lead_member')
        
        # Category filter
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Status filter
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Search filter
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        
        return queryset.order_by('-start_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Project.Category.choices
        context['statuses'] = Project.Status.choices
        return context


class ProjectDetailView(DetailView):
    """View project details with impact information."""
    model = Project
    template_name = 'ngo_app/project_detail.html'
    context_object_name = 'project'
    slug_field = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        
        # Impact metrics
        try:
            context['impact'] = project.impact
        except Impact.DoesNotExist:
            context['impact'] = None
        
        # Donations for this project
        context['project_donations'] = project.donations.filter(
            status=Donation.Status.RECEIVED
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        context['donation_count'] = project.donations.count()
        
        return context


class ProjectCreateView(CreateView):
    """Create new project."""
    model = Project
    form_class = ProjectForm
    template_name = 'ngo_app/project_form.html'
    success_url = reverse_lazy('ngo_app:project-list')
    
    def form_valid(self, form):
        # Assign organization if needed (assumes single org for demo)
        if not form.instance.organization_id:
            form.instance.organization = Organization.objects.first()
        return super().form_valid(form)


class ProjectUpdateView(UpdateView):
    """Update project information."""
    model = Project
    form_class = ProjectForm
    template_name = 'ngo_app/project_form.html'
    slug_field = 'slug'
    
    def get_success_url(self):
        return reverse_lazy('ngo_app:project-detail', kwargs={'slug': self.object.slug})


class ProjectDeleteView(DeleteView):
    """Delete project."""
    model = Project
    template_name = 'ngo_app/project_confirm_delete.html'
    success_url = reverse_lazy('ngo_app:project-list')
    slug_field = 'slug'


# ==================== Member Views ====================

class MemberListView(ListView):
    """List organization members."""
    model = Member
    template_name = 'ngo_app/member_list.html'
    context_object_name = 'members'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Member.objects.select_related('organization').filter(
            status=Member.Status.ACTIVE
        )
        
        role = self.request.GET.get('role')
        if role:
            queryset = queryset.filter(role=role)
        
        return queryset.order_by('-joined_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roles'] = Member.Role.choices
        return context


class MemberDetailView(DetailView):
    """View member profile."""
    model = Member
    template_name = 'ngo_app/member_detail.html'
    context_object_name = 'member'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = self.get_object()
        context['led_projects'] = member.led_projects.all()
        return context


class MemberCreateView(CreateView):
    """Add new team member."""
    model = Member
    form_class = MemberForm
    template_name = 'ngo_app/member_form.html'
    success_url = reverse_lazy('ngo_app:member-list')
    
    def form_valid(self, form):
        if not form.instance.organization_id:
            form.instance.organization = Organization.objects.first()
        return super().form_valid(form)


class MemberUpdateView(UpdateView):
    """Update member information."""
    model = Member
    form_class = MemberForm
    template_name = 'ngo_app/member_form.html'
    pk_url_kwarg = 'pk'
    
    def get_success_url(self):
        return reverse_lazy('ngo_app:member-detail', kwargs={'pk': self.object.pk})


# ==================== Donation Views ====================

class DonationListView(ListView):
    """List all donations."""
    model = Donation
    template_name = 'ngo_app/donation_list.html'
    context_object_name = 'donations'
    paginate_by = 15
    
    def get_queryset(self):
        queryset = Donation.objects.select_related('project', 'organization')
        
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        donation_type = self.request.GET.get('type')
        if donation_type:
            queryset = queryset.filter(donation_type=donation_type)
        
        return queryset.order_by('-donation_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_donations'] = Donation.objects.filter(
            status=Donation.Status.RECEIVED,
            donation_type=Donation.DonationType.MONETARY
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        context['statuses'] = Donation.Status.choices
        context['types'] = Donation.DonationType.choices
        return context


class DonationDetailView(DetailView):
    """View donation details."""
    model = Donation
    template_name = 'ngo_app/donation_detail.html'
    context_object_name = 'donation'
    pk_url_kwarg = 'pk'


class DonationCreateView(CreateView):
    """Record new donation."""
    model = Donation
    form_class = DonationForm
    template_name = 'ngo_app/donation_form.html'
    success_url = reverse_lazy('ngo_app:donation-list')


def donation_accept(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    donation.status = Donation.Status.RECEIVED
    donation.save()
    return redirect('ngo_app:donation-list')


def donation_cancel(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    donation.status = Donation.Status.CANCELLED
    donation.save()
    return redirect('ngo_app:donation-list')


class DonationUpdateView(UpdateView):
    """Update donation status."""
    model = Donation
    form_class = DonationForm
    template_name = 'ngo_app/donation_form.html'
    pk_url_kwarg = 'pk'
    
    def get_success_url(self):
        return reverse_lazy('ngo_app:donation-detail', kwargs={'pk': self.object.pk})
