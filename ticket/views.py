from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from account.models import *
from django.contrib import messages
from django.db.models import Q
import datetime

# Create your views here.

def staff_view(request):
    q = request.GET.get('q') if request.GET.get('q') != None else''
    tickets = Ticket.objects.filter(Q(company__name__icontains=q) | Q(title__icontains=q) | Q(description__icontains=q), ticket_status='Pending')
    context = {'tickets':tickets}
    return render(request, 'home.html', context)

def customer_view(request):
    q = request.GET.get('q') if request.GET.get('q') != None else''
    tickets = Ticket.objects.filter(Q(company__name__icontains=q) | Q(title__icontains=q) | Q(description__icontains=q),created_by=request.user)
    context = {'tickets':tickets}
    return render(request, 'home.html', context)    

@login_required
def home(request):
  if request.user.is_staff:
      return staff_view(request)
  else:
      return customer_view(request)

# def createProject(request):
#     if request.method == 'POST':
#         form = CreateTicketForm(request.POST)
#         if form.is_valid():
#             var = form.save(commit=False)
#             var.ticket_status = 'Pending'
#             var.save()
#             messages.info(request, 'Your ticket has been successfully submitted')
#             return redirect('account:dashboard')
#         else:
#             messages.warning(request,'Something went wrong')
#             return redirect('ticket:home')
#     else:
#         form = CreateTicketForm()
#         context = {'form':form}
#         return render(request, 'tickets/clients/ticket_form.html',context)

def createProject(request):
    form = CreateTicketForm
    companies = Company.objects.all()
    if request.method == 'POST':
        company_name = request.POST.get('company')
        company,created = Company.objects.get_or_create(name=company_name)
        
        Ticket.objects.create(
            company=company,
            created_by = request.user,
            title = request.POST.get('title'),
            description = request.POST.get('description'),
            ticket_status = 'Pending'
        )
        return redirect('ticket:home')


    context={'form':form,'companies':companies}
    return render(request, 'tickets/clients/ticket_form.html', context)
    
#ticket detaisl
def ticket_detail(request,id):
    ticket = Ticket.objects.get(id=id)
    project_messages = ticket.message_set.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            ticket=ticket,
            body=request.POST.get('body')
        )   
       # room.participants.add(request.user.name)
        return redirect('ticket:ticket-detail', id=ticket.id)
    t = UserBase.objects.get(user_name = ticket.created_by )
    tickets_per_user = t.created_by.all()
    context = {'ticket':ticket, 'tickets_per_user':tickets_per_user,'project_messages':project_messages}
    return render(request, 'tickets/clients/ticket_detail.html', context)

def updateProject(request,id):
    ticket = Ticket.objects.get(id=id)
    form = UpdateTicketForm(instance=ticket)
    
    if request.method =='POST':
        ticket.title = request.POST.get('title')
        ticket.description = request.POST.get('description')
        ticket.save()
        return redirect('ticket:home')

    context = {'form':form, 'ticket':ticket}
    return render(request, 'tickets/clients/update_ticket_form.html', context)

def company_details(request,id):
    ticket = Ticket.objects.get(id=id)
    user = UserBase.objects.get(id=id)
    context = {'user':user,'ticket':ticket}
    return render(request, 'tickets/clients/company-details.html',context)

""" For Engineers """

#view ticket queue
# def ticket_queue(request):
#     tickets = Ticket.objects.filter(ticket_status='Pending')
#     context = {'tickets':tickets}
#     return render(request, 'tickets/staff/ticket_queue.html', context)

#accept a ticket from the queue
def accept_ticket(request,id):
    ticket = Ticket.objects.get(id=id)
    ticket.assigned_to = request.user
    ticket.ticket_status = 'Active'
    ticket.accepted_date = datetime.datetime.now()
    ticket.save()
    messages.info(request, 'Ticket has been accepted.Please resolve as soon as possible')
    return redirect('ticket:workspace')

#close a ticket
def close_ticket(request,id):
    ticket = Ticket.objects.get(id=id)
    ticket.ticket_status = 'Completed'
    ticket.is_resolved = True
    ticket.closed_date = datetime.datetime.now()
    ticket.save()
    messages.info(request, 'Ticket has been closed.')
    return redirect('ticket:home')
    
#tickets engineer is working on
def workspace(request):
    tickets = Ticket.objects.filter(assigned_to=request.user,is_resolved=False)
    company = Company.objects.all()
    context = {'tickets':tickets}
    return render(request, 'tickets/staff/workspace.html', context)

#all closed/resolved tickets
def all_closed_tickets(request):
    tickets = Ticket.objects.filter(assigned_to=request.user,is_resolved=True)
    tickets.closed_date = datetime.datetime.now()
    context = {'tickets':tickets}
    return render(request, 'tickets/staff/all_closed_tickets.html', context)
            