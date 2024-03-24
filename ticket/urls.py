from django.urls import path
from .import views

app_name = "ticket"

urlpatterns = [
    path('', views.home, name="home"),
    path('create-ticket/', views.createProject, name="create-ticket"),
    path('update-ticket/<int:id>/', views.updateProject, name="update-ticket"),
    path('accept-ticket/<int:id>/', views.accept_ticket, name="accept-ticket"),   
    path('close-ticket/<int:id>/', views.close_ticket, name="close-ticket"),   
    path('workspace/', views.workspace, name="workspace"),   
    path('resolved tickets/', views.all_closed_tickets, name="all-closed"),   
    path('ticket-detail/<int:id>/', views.ticket_detail, name="ticket-detail"),   
    path('company-details/<int:id>/', views.company_details, name="company-details"),   
    path('all-closed-tickets', views.all_closed_tickets, name="all-closed-tickets"),   
]