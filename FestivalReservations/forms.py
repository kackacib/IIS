from django import forms
from django.forms import ModelChoiceField

from .models import Festival, Interpret, Show, Reservation, Stage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

class FestivalForm(forms.ModelForm):
    FestivalBrand = forms.CharField(label='Název')
                    
    Place = forms.CharField(required=True, label = "Místo")
    Genre = forms.CharField(max_length=30)
    Start = forms.DateField(widget=forms.DateInput)
    End = forms.DateField(widget=forms.DateInput)
    PriceForTicket       = forms.IntegerField(initial=199)
    Capacity       = forms.IntegerField(initial=6)
    photoLogo = forms.ImageField(required = False)
    
    class Meta:
        model = Festival
        fields = [
            'FestivalBrand',
            'Place',
            'Genre',
            'Start',
            'End',
            'PriceForTicket',
            'Capacity',
            'photoLogo'
        ]


class InterpretForm(forms.ModelForm):
    Name    = forms.CharField(label='Jméno interpreta')
                    
    Members = forms.CharField(label="Popis",  widget=forms.TextInput(attrs={"placeholder": "např. členové, zajímavosti..."}))
    photoLogo = forms.ImageField(required = False, label='Fotografie')
    Rating = forms.IntegerField(label='Hodnocení', max_value=100, min_value=0)
    Genre       = forms.CharField(max_length=50, label="Žánr")
    
    class Meta:
        model = Interpret
        fields = [
            'Name',
            'Members',
            'photoLogo',
            'Rating',
            'Genre'
        ]

class CreateUserForm(UserCreationForm):
    def __init__(self, email, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        if email is not None:
            self.fields['email'] = forms.CharField(initial=email)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ReservationForm(forms.ModelForm):
    def __init__(self, festival_id, capacity, request, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        if festival_id is not None:
            chosen_festival = Festival.objects.filter(id=festival_id).first()
            self.fields['Tickets']=forms.IntegerField(max_value=capacity, min_value=0, label="Počet lístků")
            self.fields['Festival'] = forms.CharField(widget=forms.HiddenInput(), initial=chosen_festival.id)
        if request.user.is_authenticated:
            user_group_name = request.user.groups.all().first().name
            if user_group_name == "customer":
                self.fields['User'] = forms.ModelChoiceField(queryset = None, widget = forms.HiddenInput(), required = False, label="Uživatel")
                self.fields['Paid'] = forms.BooleanField(widget = forms.HiddenInput(),required = False, initial = False, label="Zaplaceno")
            elif user_group_name == "cashier" or user_group_name == "organizer" or user_group_name == "admin":
                self.fields['User'] == forms.ModelChoiceField(queryset=User.objects.all(), required = True, label="Uživatel")
                self.fields['Paid'] = forms.BooleanField(required = False, label="Zaplaceno")
        else:
            self.fields['User'] = forms.ModelChoiceField(queryset = None, widget = forms.HiddenInput(), required = False, label="Uživatel")
            self.fields['Email'] = forms.CharField()
            self.fields['Paid'] = forms.BooleanField(widget = forms.HiddenInput(), required=False, label="Zaplaceno")
        
    User = forms.ModelChoiceField(queryset=User.objects.all(), required = False)

    class Meta:
        model = Reservation
        fields = [
            'Tickets',
            'Paid',
            'Festival'
        ]

class ReservationEditForm(forms.ModelForm):
    def __init__(self, capacity, tickets, paid, *args, **kwargs):
        super(ReservationEditForm, self).__init__(*args, **kwargs)
        if tickets is not None:
            self.fields['Tickets']=forms.IntegerField(max_value=capacity, min_value=0, initial=tickets, label="Počet lístků")
            self.fields['Paid']=forms.BooleanField(initial=paid, required=False, label="Zaplaceno")
        else:
            if 'Paid' in args[0]:
                paid = True
            else:
                paid = False
            self.fields['Paid']=forms.BooleanField(initial=paid, required=False, label="Zaplaceno")

    class Meta:
        model = Reservation
        fields = [
            'Tickets',
            'Paid',
        ]    


class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "Stage #%i" % obj.id

def getlabels(festival_id):
    choices = []
    labels = []
    for label in Stage.objects.values('Label'):
        labels.append(label)
        for choice in labels.filter(Festival=festival_id):
            choices.append(choice)

    return choices


class ShowForm(forms.ModelForm):
    def __init__(self, festival_id, *args, **kwargs):
        super(ShowForm, self).__init__(*args, **kwargs)

        if festival_id is not None:
            #FestId = Festival.objects.get(id=festival_id)
            self.fields['Stage'] = forms.ModelChoiceField(queryset = Stage.objects.filter(Festival=festival_id))

    Interpret = forms.ModelChoiceField(queryset=Interpret.objects.all())
    Date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))
    Start = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    End = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    Stage = forms.ModelChoiceField(queryset=None)

    def check_date():
        if not (FestivalForm.Start <= Date <= FestivalForm.End):
            raise ValidationError

    

    class Meta:
        model = Show
        fields = [
            'Interpret',
            'Date',
            'Start',
            'End'
        ]


class ChangePasswordAdminForm(forms.ModelForm):
    Password1 = forms.CharField(min_length=8, label="Nové heslo", widget=forms.PasswordInput)        
    Password2 = forms.CharField(min_length=8, label="Heslo znovu", widget=forms.PasswordInput)        


    class Meta:
        model = User
        fields = []

class UserEditAdminForm(forms.ModelForm):
    def __init__(self, user_id, *args, **kwargs):
        super(UserEditAdminForm, self).__init__(*args, **kwargs)
        user = User.objects.get(id=user_id)
        self.fields['Username'] = forms.CharField(initial = user.username, label="Login")
        self.fields['Email'] = forms.CharField(initial = user.email)
        self.fields['Groups'] = forms.ModelChoiceField(queryset=Group.objects.all(), initial = user.groups.all().first, label="Uživatelská skupina")

    Groups = forms.ModelChoiceField(queryset=Group.objects.all())
    Username = forms.CharField()
    Email = forms.CharField()

    class Meta:
        model = User
        fields = [
        ]

class UserEditForm(forms.ModelForm):
    def __init__(self, user_id, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        if user_id is not None:
            user = User.objects.get(id = user_id)
            self.fields['email'] = forms.CharField(initial = user.email)

    class Meta:
        model = User
        fields = [
            'email'
        ]    


class UserPasswordForm(forms.ModelForm):
    Password1 = forms.CharField(min_length=8, label="Nové heslo", widget=forms.PasswordInput)        
    Password2 = forms.CharField(min_length=8, label="Heslo znovu", widget=forms.PasswordInput)        


    class Meta:
        model = User
        fields = []


class AddUserForm(forms.ModelForm):
    Username = forms.CharField(label="Login")
    Email = forms.CharField()
    Group = forms.ModelChoiceField(queryset=Group.objects.all(), label="Uživatelská skupina")
    Password1 = forms.CharField(min_length=8, label="Heslo", widget=forms.PasswordInput)        
    Password2 = forms.CharField(min_length=8, label="Heslo znovu", widget=forms.PasswordInput)                


    class Meta:
        model = User
        fields = [
            
        ]  