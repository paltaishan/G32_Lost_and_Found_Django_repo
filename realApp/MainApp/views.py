from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from .models import Item, ClaimRequest
from .forms import ItemForm, ClaimRequestForm
from users.forms import CustomUserCreationForm
from django.db.models import Q 


# 👮 Admin Dashboard: View all items & claims
@login_required
def admin_dashboard(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    items = Item.objects.all().order_by('-date_reported')
    claims = ClaimRequest.objects.all().order_by('-requested_at')
    return render(request, 'admin_dashboard.html', {
        'items': items,
        'claims': claims,
    })


@login_required
def dashboard(request):
    items = Item.objects.filter(status__in=['found', 'lost'])

    # Search
    search_query = request.GET.get('search')
    if search_query:
        items = items.filter(
            Q(title__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Filter by category
    category = request.GET.get('category')
    if category:
        items = items.filter(category=category)

    # Sorting
    sort_by = request.GET.get('sort')
    if sort_by:
        items = items.order_by(sort_by)
    else:
        items = items.order_by('-date_reported')

    paginator = Paginator(items, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {
        'items': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'category_choices': Item.CATEGORY_CHOICES,
        'status_choices': Item._meta.get_field('status').choices,

    })


# 🧾 Reported Items by Logged-in User
@login_required
def my_reports(request):
    items = Item.objects.filter(reported_by=request.user)
    return render(request, 'my_reports.html', {'items': items})


# 📦 Item Detail
def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, 'item_detail.html', {'item': item})


@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.reported_by = request.user
            item.save()
            messages.success(request, "Item reported successfully!")
            return redirect('dashboard')
    else:
        form = ItemForm()
    return render(request, 'add_item.html', {'form': form})



# 📝 Claim a Found Item
@login_required
def claim_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    if request.method == 'POST':
        form = ClaimRequestForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.item = item
            claim.claimant = request.user
            claim.save()
            messages.success(request, "Your claim has been submitted.")
            return redirect('dashboard')
    else:
        form = ClaimRequestForm()

    return render(request, 'claim_form.html', {'form': form, 'item': item})


# 📜 View User's Claims
@login_required
def my_claims(request):
    claims = ClaimRequest.objects.filter(claimant=request.user).order_by('-requested_at')
    return render(request, 'my_claims.html', {'claims': claims})


# ✅ Admin: Update Claim Status
@require_POST
@login_required
def update_claim_status(request, claim_id):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("Only admins can update claims.")
    
    claim = get_object_or_404(ClaimRequest, pk=claim_id)
    new_status = request.POST.get('status')

    if new_status in dict(ClaimRequest.STATUS_CHOICES):
        claim.status = new_status
        claim.save()
        messages.success(request, f"Claim #{claim.id} updated to {new_status}.")
    else:
        messages.error(request, "Invalid status.")

    return redirect('admin_dashboard')



# 🔍 Category Filter View
def category_filter(request, category_slug):
    filtered_items = Item.objects.filter(category=category_slug, status='found')
    return render(request, 'category_items.html', {
        'items': filtered_items,
        'category_name': dict(Item.CATEGORY_CHOICES).get(category_slug, category_slug),
        'category_choices': Item.CATEGORY_CHOICES,
    })


# 🔐 Registration
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


# 🔐 Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('admin_dashboard' if user.user_type == 'admin' else 'dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')


# 🔓 Logout
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')



def reported_items_view(request):
    items = Item.objects.all().order_by('-date_reported')
    return render(request, 'reported_items.html', {'items': items})