
from django.contrib import admin
from django.urls import path
from MovieTicket.views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", Home, name = "home"),
    path("login/", Login, name = "login"),
    path("add_cat/", Admin_Add_Cat, name = "add_cat"),
    path("add_movie/", Admin_Add_Movie, name = "add_movie"),
   #path("create_sheets/", Create_Sheets, name = "sheets"),
    path("payMentMake", MakePayment, name = "payment"),
    path("add_show_time", Admin_Add_ShowTime, name = "add_show_time"),
    path("booking/<int:m_id>/", Movie_Confirmation, name = "confirmation"),
    path("signup/", SignUP, name = "signup"),
    path('delete/<int:m_id>/',Delete_Album,name="delete"),
    path('logout/', Logout, name="logout"),
    path("contact/",Contact,name='contact'),
    path("about/",About, name= 'about'),
    path("all_movies/",All_Movies, name= 'all_movies'),
    path("movie_details/<int:m_id>/", Movie_Details_Page, name="movie_detail"),
    path("seat_booking/<int:m_id>/", SeatBookingPage, name="seatbooking"),
    path("PayCheck/<str:Usr>/", PayChack, name = "paycheck"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
