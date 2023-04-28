from django.urls import path
from .views import (ReservationCreate, userPage, registerPage, loginPage, logoutUser, FestivalList,
                   InterpretList, FestivalDelete, InterpretCreate, InterpretDelete,
                   InterpretUpdate, FestivalDetail, InterpretDetail, FestivalCreate,
                   FestivalUpdate, MyReservations, ReservationsAdmin, ReservationEdit, AddShow,
                   UserAdmin, UserEditAdmin, ChangePasswordAdmin, ChangePassword, UserEdit, AddUser)
from .views import home
from django.conf import settings
from django.conf.urls.static import static

app_name='FestivalReservations'

urlpatterns=[
	path('FestivalList/', FestivalList.as_view(), name='FestivalList'),
	path('FestivalList/<slug:slug>', FestivalList.as_view(), name='FestivalList'),
	path('FestivalCreate/', FestivalCreate.as_view(), name='FestivalCreate'),
	path('FestivalDetail/<int:pk>', FestivalDetail.as_view(), name='FestivalDetail' ),
    path('FestivalDelete/<int:pk>', FestivalDelete.as_view(), name='FestivalDelete'),
    path('FestivalUpdate/<int:pk>', FestivalUpdate.as_view(), name='FestivalUpdate'),
	path('InterpretList/', InterpretList.as_view(), name='InterpretList'),
    path('InterpretCreate/', InterpretCreate.as_view(), name='InterpretCreate'),
	path('InterpretDetail/<int:pk>', InterpretDetail.as_view(), name='InterpretDetail'),
    path('InterpretDelete/<int:pk>', InterpretDelete.as_view(), name='InterpretDelete'),
    path('InterpretUpdate/<int:pk>', InterpretUpdate.as_view(), name='InterpretUpdate'),
    path('register/<email>/', registerPage, name="register"),
    path('register/', registerPage, name="register"),
    path('login/', loginPage, name="login"),
    path('logout/', logoutUser, name="logout"),
    path('user/', userPage, name="user-page"),
    path('reservation/<int:pk>', ReservationCreate.as_view(), name="reservation-page"),
    path('MyReservations/', MyReservations, name="MyReservations"),
    path('ReservationsAdmin/', ReservationsAdmin, name="ReservationsAdmin"),
    path('ReservationsAdmin/<int:pk>', ReservationsAdmin, name="ReservationsAdmin"),
    path('ReservationEdit/<int:pk>', ReservationEdit, name="ReservationEdit"),
    path('AddShow/<int:pk>', AddShow.as_view(), name='AddShow'),
    path('UserAdmin/', UserAdmin, name='UserAdmin'),
    path('UserAdmin/<int:pk>', UserAdmin, name='UserAdmin'),
    path('UserEditAdmin/<int:pk>', UserEditAdmin, name='UserEditAdmin'),
    path('ChangePasswordAdmin/<int:pk>', ChangePasswordAdmin, name='ChangePasswordAdmin'),
    path('ChangePassword/', ChangePassword, name='ChangePassword'),
    path('UserEdit/', UserEdit, name='UserEdit'),
    path('AddUser/', AddUser, name='AddUser'),
    path('', home, name="home")
]
urlpatterns  +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)