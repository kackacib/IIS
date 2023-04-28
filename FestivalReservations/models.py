from django.db import models
from jsonfield import JSONField
from django.conf import settings
# Create your models here.
class Festival(models.Model):

	FestivalBrand = models.CharField(max_length=30, verbose_name= ("Jméno"))
	Place = models.CharField(max_length=400, verbose_name= ("Místo"))
	Genre = models.CharField(max_length=30, verbose_name= ("Žánr"))
	Start = models.DateField(default="2020-01-01", verbose_name= ("Začátek"))
	End = models.DateField(default="2020-02-01", verbose_name= ("Konec"))
	PriceForTicket = models.IntegerField(verbose_name= ("Cena za lístek"))
	Capacity = models.IntegerField(verbose_name= ("Kapacita"))
	photoLogo = models.ImageField(upload_to="./FestivalReservations/static/images/festival", null=True, blank=True, verbose_name= ("Fotografie"))

	def __str__(self):
		return f'{self.FestivalBrand}'


class Interpret(models.Model):
	Name = models.CharField(max_length=30)
	Members = models.CharField(max_length=100)
	photoLogo = models.ImageField(upload_to="./FestivalReservations/static/images/interpret", null=True, blank=True)
	Rating = models.IntegerField()
	Genre = models.CharField(max_length=30)

	def __str__(self):
		return f'{self.Name}   ({self.Genre})'
	
	
class Reservation(models.Model):
	User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name = 'Uživatel',related_name='reservations', null=True) 
	Festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
	Tickets = models.IntegerField()
	Paid = models.BooleanField(default=False, null=True)


class Stage(models.Model):
	Label = models.IntegerField()
	Festival = models.ForeignKey(Festival, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.Label}'


class Show(models.Model):
	Interpret = models.ForeignKey(Interpret, on_delete=models.CASCADE)
	Stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
	Date = models.DateField()
	Start = models.TimeField()
	End = models.TimeField()

