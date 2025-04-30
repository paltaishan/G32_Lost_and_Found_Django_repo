from django.urls import path
from . import views

urlpatterns = [
    # General Access
    path('', views.dashboard, name='dashboard'),  # Default: found item gallery
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('reported-items/', views.reported_items_view, name='reported_items'),

    # Items
    path('items/', views.my_reports, name='my_reports'),  # Items reported by user
    path('add-item/', views.add_item, name='add_item'),  # Report new lost/found item
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),  # Item detail view
    path('category/<slug:category_slug>/', views.category_filter, name='category_filter'),  # Filter by category

    # Claims
    path('item/<int:item_id>/claim/', views.claim_item, name='claim_item'),  # Submit claim
    path('claims/', views.my_claims, name='my_claims'),  # View user's claims
    path('claim/<int:claim_id>/update-status/', views.update_claim_status, name='update_claim_status'),  # Admin: update claim status

    # Authentication
    path('claim/<int:claim_id>/update/', views.update_claim_status, name='update_claim_status'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
