from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Festival, Interpret, Reservation, Show, Stage
from .forms import (FestivalForm, InterpretForm, CreateUserForm, ReservationForm,
                    ReservationEditForm, ChangePasswordAdminForm, UserEditAdminForm,
                    UserEditForm, UserPasswordForm, ShowForm, AddUserForm)
from vanilla import ListView, DetailView, CreateView, TemplateView, UpdateView
from django.views.generic.edit import DeleteView 
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from .decorators import unauthenticated_user, allowed_users
from django.utils.decorators import method_decorator
# Create your views here.

def home(request):
    return render(request, "home.html", {})

class FestivalList(ListView):
    model = Festival

@method_decorator(allowed_users(allowed_roles=['admin', 'organizer']), name='dispatch')
class FestivalCreate(CreateView):
    model = Festival
    def get(self, request, *args, **kwargs):
        # GET method
        form = FestivalForm()
        context = {"form": form}
        return render(request, "FestivalReservations/festival_form.html", context)

    def post(self, request, *args, **kwargs):
        # POST method
        form = FestivalForm(request.POST)

        FestivalID = form.save()
        FestivalID = FestivalID.pk

        number_of_stages = request.POST['NumberOfStages']

        number_of_stages = int(number_of_stages)
        print(number_of_stages)

        if form.is_valid():
            i = 1
            while i <= number_of_stages:
                new_stage = Stage(Label=i, Festival=Festival.objects.filter(id=FestivalID).first())
                new_stage.save()
                i += 1

            form.save()

        context = {"form": form}
        return render(request, "FestivalReservations/festival_form.html", context)


@method_decorator(allowed_users(allowed_roles=['admin', 'organizer']), name='dispatch')
class FestivalDelete(DeleteView):
    template_name = 'FestivalReservations/festival_delete.html'
    model = Festival
    success_url = "/fest/"

    def post(self, request, pk=None, *args, **kwargs):
        # POST method
        context = {}
        obj = Festival.objects.get(pk=pk)
        if obj is not None:
            obj.delete()
            context['object'] = None
            return redirect('../FestivalList/FestivalBrand')
        return render(request, "FestivalReservations/", context)


class Data():
    def __init__(self, Interpret, Datum, Start, End):
        self.Interpret = Interpret
        self.Datum = Datum
        self.Start = Start
        self.End = End

    Interpret = ""
    Datum = ""
    Start = ""
    End = ""


class FestivalDetail(DetailView):
    model = Festival
    template_name='FestivalReservations/festival_detail.html'

    def get(self, request, *args, **kwargs):
        FestivalID = kwargs.pop("pk")
        festival = Festival.objects.filter(id = FestivalID).first()
        stages = Stage.objects.filter(Festival=FestivalID)

        shows_list = []
        interprets = []
        dates = []
        start_end = {}


        stage_view = dict()
        for stage in stages:
            shows = Show.objects.filter(Stage=stage)            
            if shows:
                stage_view[stage.Label] = list()
                for show in shows:
                    interpret = Interpret.objects.get(show=show)    
                    date = show.Date
                    start = show.Start
                    end = show.End
                    stage_view[stage.Label].append(Data(Interpret = interpret.Name, Datum = date, Start = start, End = end))

        context = {
            "FestivalID" : FestivalID,
            "Stages" : stages,
            "Interprets" : interprets,
            "Dates" : dates,
            "Start_End" : start_end,
            "festival" : festival,
            "stage_view" : stage_view

        }

        return render(request, "FestivalReservations/festival_detail.html", context)


@method_decorator(allowed_users(allowed_roles=['admin', 'organizer']), name='dispatch')
class AddShow(CreateView):
    model = Show
    template_name = 'FestivalReservations/add_show.html'
    success_url = "/fest/"

    def get(self, request, *args, **kwargs):
        # GET method
        FestivalID = kwargs.pop("pk")
        form = ShowForm(FestivalID)

        
        context = {
            "form": form,
            "FestivalID" : FestivalID
            }
        return render(request, "FestivalReservations/add_show.html", context)

    def post(self, request, *args, **kwargs):
        # POST method
        FestivalID = kwargs.pop("pk")

        form = ShowForm(FestivalID, request.POST)

        if form.is_valid():
            stages = Stage.objects.filter(Festival=FestivalID)
            for s in stages:
                if s.id == form.cleaned_data["Stage"].id:
                    stage = s
            show = Show(Start=form.cleaned_data['Start'], End=form.cleaned_data['End'], Date=form.cleaned_data['Date'],
                    Interpret=form.cleaned_data['Interpret'], Stage=stage)
            show.save()

            form = ShowForm(FestivalID)

        context = {
            "form": form,
            "FestivalID" : FestivalID
            }
        return render(request, "FestivalReservations/add_show.html", context)




@method_decorator(allowed_users(allowed_roles=['admin', 'organizer']), name='dispatch')
class FestivalUpdate(UpdateView):
    model = Festival
    fields = ["FestivalBrand", "Place", "Genre", "Start", "End", "PriceForTicket", "Capacity",]
    template_name = 'FestivalReservations/festival_update.html'
    success_url = "/fest/FestivalList"


class InterpretList(ListView):
    model = Interpret

@method_decorator(allowed_users(allowed_roles=['admin', 'organizer']), name='dispatch')
class InterpretCreate(CreateView):
    model = Interpret
    def get(self, request, *args, **kwargs):
        # GET method
        form = InterpretForm()
        context = {"form": form}
        return render(request, "FestivalReservations/interpret_form.html", context)

    def post(self, request, *args, **kwargs):
        # POST method
        form = InterpretForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = InterpretForm()
        context = {"form": form}
        return render(request, "FestivalReservations/interpret_form.html", context)

@method_decorator(allowed_users(allowed_roles=['admin', 'organizer']), name='dispatch')
class InterpretDelete(DeleteView):
    template_name = 'FestivalReservations/interpret_delete.html'
    model = Interpret
    success_url = "/fest/InterpretList"

    def post(self, request, pk=None, *args, **kwargs):
        # POST method
        context = {}
        obj = Interpret.objects.get(pk=pk)
        if obj is not None:
            obj.delete()
            context['object'] = None
            return redirect('../InterpretList')
        return render(request, "FestivalReservations/", context)

@method_decorator(allowed_users(allowed_roles=['admin', 'organizer']), name='dispatch')
class InterpretUpdate(UpdateView):
    model = Interpret
   #form_class = FestivalForm
    fields = ["Name", "Members", "photoLogo", "Rating", "Genre"]
    template_name = 'FestivalReservations/interpret_update.html'
    success_url = "/fest/InterpretList"



class InterpretDetail(DetailView):
    model = Interpret



@unauthenticated_user
def registerPage(request, *args, **kwargs):
    if 'email' in kwargs:
        form = CreateUserForm(kwargs.pop('email'))
    else:
        form = CreateUserForm(None)
    if request.method == 'POST':
        form = CreateUserForm(None, request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            login(request, user)
            return redirect('FestivalReservations:user-page')
        

    context = {'form':form}
    return render(request, 'FestivalReservations/register.html', context)


    # if request.method == 'POST':
    #     form = CreateUserForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    # context = {'form':form}
    # return render(request, 'FestivalReservations/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('FestivalReservations:home')
        else:
            messages.info(request, 'Login nebo heslo je chybné')

    context = {}
    return render(request, 'FestivalReservations/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('FestivalReservations:login')

def userPage(request):
    name = str(request.user)
    email = str(request.user.email)
    reservations = request.user.reservations.all()
    if not reservations:
        reservations = None
    context = {"Reservations": reservations, "Name": name, "Email": email}
    return render(request, 'FestivalReservations/user.html', context)



class ReservationCreate(CreateView):
    model = Reservation
    def get(self, request, *args, **kwargs):
        # GET method
        festival_id = kwargs.pop('pk')
        chosen_festival = Festival.objects.filter(id=festival_id).first()
        capacity = self.countCapacity(festival_id)
        avaiable = capacity > 0
        form = ReservationForm(festival_id, capacity, request)
        success = 1
        context = {"form": form,
                   "fest": festival_id,
                   "capacity": avaiable,
                   "festival":chosen_festival,
                   "success":success}
        return render(request, "FestivalReservations/reservation_form.html", context)

    def post(self, request, *args, **kwargs):
        # POST method
        form = ReservationForm(None, None, request, request.POST)
        festival_id = kwargs.pop('pk')
        chosen_festival = Festival.objects.filter(id=festival_id).first()
        if form.is_valid():
            success = 0
            new_reservation = form.save()
            if 'reserve_and_register' in request.POST:
                return redirect('../register/' + form.cleaned_data['Email'])
            else:
                if form.cleaned_data['User'] is not None:
                    user = form.cleaned_data['User']
                else:
                
                    user = User.objects.get(username = request.user)
                    new_reservation.User = user
                    new_reservation.save()

        capacity = self.countCapacity(festival_id)
        form = ReservationForm(festival_id, capacity, request)

        capacity = self.countCapacity(festival_id)
        avaiable = capacity > 0
        
        context = {"form": form, "fest": festival_id, "capacity": avaiable,
                   "festival":chosen_festival, "success":success}
        return render(request, "FestivalReservations/reservation_form.html", context)

    def countCapacity(self, festival_id):
        chosen_festival = Festival.objects.filter(id=festival_id).first()
        reservations_for_festival = Reservation.objects.filter(Festival=festival_id)
        sold = 0
        for r in reservations_for_festival:
            sold += r.Tickets
        capacity = chosen_festival.Capacity - sold
        return capacity

def MyReservations(request, *args, **kwargs):
    my_reservations = Reservation.objects.filter(User=request.user.id)
    if not my_reservations:
        empty = True
    else:
        empty = False

    context = {"my_reservations": my_reservations, "empty":empty}
    if request.method == 'GET':
        return render(request, "FestivalReservations/my_reservations.html", context)
    elif request.method == 'POST':
        return render(request, "FestivalReservations/my_reservations.html", context)


@allowed_users(allowed_roles=['admin', 'cashier', 'organizer'])
def ReservationsAdmin(request, *args, **kwargs):

    delete = False
    if 'pk' in kwargs:
        reservation_id = kwargs.pop('pk')
        Reservation.objects.filter(id=reservation_id).delete()
        delete = True

    all_reservations = Reservation.objects.all()
    context = {"all_reservations": all_reservations, "delete":delete}

    if request.method == 'GET':
        return render(request, "FestivalReservations/ReservationsAdmin.html", context)
    elif request.method == 'POST':
        return render(request, "FestivalReservations/ReservationsAdmin.html", context)    


def countCapacityEditReservation(reservation_id):
        reservation = Reservation.objects.filter(id=reservation_id).first()
        festival = Festival.objects.filter(id=reservation.Festival_id).first()
        reservations_for_festival = Reservation.objects.filter(Festival=festival.id)
        sold = 0
        for r in reservations_for_festival:
            sold += r.Tickets
        capacity = festival.Capacity - sold + reservation.Tickets
        return capacity


def ReservationEdit(request, *args, **kwargs):

    reservation_id = kwargs.pop('pk')
    reservation = Reservation.objects.filter(id=reservation_id).first()
    festival = Festival.objects.filter(id=reservation.Festival_id).first()
    if request.method == 'POST':
        capacity = countCapacityEditReservation(reservation_id)
        form = ReservationEditForm(capacity, None, None, request.POST)
        success = 0
        if form.is_valid():
            tickets = request.POST['Tickets']
            if  'Paid' in request.POST:
                paid = True
            else:
                paid = False
            Reservation.objects.filter(id=reservation_id).update(Tickets=tickets, Paid=paid)

        context = {"form": form, "res": reservation_id, "success":success, "festival":festival}        
        return render(request, "FestivalReservations/ReservationEdit.html", context)    

    elif request.method == 'GET':
        capacity = countCapacityEditReservation(reservation_id)
        form = ReservationEditForm(capacity, reservation.Tickets, reservation.Paid)
        success = 1
        context = {"form": form, "res": reservation_id, "success":success, "festival":festival }
        return render(request, "FestivalReservations/ReservationEdit.html", context)


@allowed_users(allowed_roles=['admin'])
def UserAdmin(request, *args, **kwargs):

    delete = False
    if 'pk' in kwargs:
        user_id = kwargs.pop('pk')
        User.objects.filter(id=user_id).delete()
        delete = True

    all_users = User.objects.all()
    context = {"all_users": all_users, "delete":delete}

    if request.method == 'GET':
        return render(request, "FestivalReservations/UserAdmin.html", context)
    elif request.method == 'POST':
        return render(request, "FestivalReservations/UserAdmin.html", context)    


def UserEditAdmin(request, *args, **kwargs):

    if 'pk' in kwargs:
        user_id = kwargs.pop('pk')
        user = User.objects.get(id=user_id)
    
    if request.method == 'GET':
        success = 1
        form = UserEditAdminForm(user_id)
        context = {"form":form, "user_id": user_id, "success" : success, "user":user}
        return render(request, "FestivalReservations/UserEditAdmin.html", context)
    elif request.method == 'POST':
        form = UserEditAdminForm(user_id, request.POST)
        success = -3
        if form.is_valid():
            new_username = form.cleaned_data['Username']
            new_email = form.cleaned_data['Email']
            new_group = form.cleaned_data['Groups']
            found = User.objects.filter(username=new_username)
            for f in found:
                if f.id != user_id:
                    success = -1

            if success != -1:
                user = User.objects.get(id=user_id)
                user.username = new_username
                user.email = new_email
                current_group = user.groups.all().first()
                if current_group != new_group:
                    user.groups.remove(current_group)
                    user.groups.add(new_group) 
                user.save()
                success = 0

        context = {"form":form, "user_id": user_id, "success":success, "user":user}
        return render(request, "FestivalReservations/UserEditAdmin.html", context)    


def ChangePasswordAdmin(request, *args, **kwargs):
    if 'pk' in kwargs:
        user_id = kwargs.pop('pk')
        user = User.objects.get(id = user_id)
    if request.method == 'GET':
        form = ChangePasswordAdminForm()
        context = {"form":form,"pk": user_id, "success": 1, "user":user}
        return render(request, "FestivalReservations/ChangePasswordAdmin.html", context)
    elif request.method == 'POST':
        form = ChangePasswordAdminForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data["Password1"]
            password2 = form.cleaned_data["Password2"]
            if password1 == password2:
                user = User.objects.get(id = user_id)
                user.set_password(password1)
                user.save()
                success = 0
            else:
                success = -1
        context = {"form":form,"pk": user_id, "success": success, "user":user}
        return render(request, "FestivalReservations/ChangePasswordAdmin.html", context)    


def ChangePassword(request, *args, **kwargs):
    
    if request.method == 'GET':
        form = UserPasswordForm()
        success = 1
        context = {"form": form, "success":success}
        return render(request, "FestivalReservations/ChangePassword.html", context)
    elif request.method == 'POST':
        form = UserPasswordForm(request.POST)
        success = -2
        if form.is_valid():
            password1 = form.cleaned_data["Password1"]
            password2 = form.cleaned_data["Password2"]
            if password1 == password2:
                user = User.objects.get(id = request.user.id)
                user.set_password(password1)
                user.save()
                success = 0
            else:
                success = -1
        context = {"form": form, "success":success}
        return render(request, "FestivalReservations/ChangePassword.html", context)

def UserEdit(request, *args, **kwargs):
    
    if request.method == 'GET':
        form = UserEditForm(request.user.id)
        success = 1
        context = {"form":form, "success":success}
        return render(request, "FestivalReservations/UserEdit.html", context)
    elif request.method == 'POST':
        form = UserEditForm(None, request.POST)
        success = -1
        if form.is_valid():
            user = User.objects.get(id = request.user.id)
            user.email = form.cleaned_data["email"]
            user.save()
            success = 0

        context = {"form":form, "success":success}
        return render(request, "FestivalReservations/UserEdit.html", context)


def AddUser(request, *args, **kwargs):
    
    if request.method == 'GET':
        form = AddUserForm()
        success = 1
        context = {"form":form, "success":success}
        return render(request, "FestivalReservations/AddUser.html", context)
    elif request.method == 'POST':
        form = AddUserForm(request.POST)
        success = -1
        if form.is_valid():
            new_username = form.cleaned_data["Username"]
            user = User(username=new_username, email=form.cleaned_data['Email'])
            password1 = form.cleaned_data["Password1"]
            password2 = form.cleaned_data["Password2"]
            if password1 == password2:
                user.set_password(password1)
                found = User.objects.filter(username=new_username)
                if not found:
                    user.save()
                    user.groups.add(form.cleaned_data["Group"]) 
                    success = 0
                else:
                    success = -3
            else:
                success = -2

        context = {"form":form, "success":success}
        return render(request, "FestivalReservations/AddUser.html", context)