from django.contrib import admin
from django.urls import path
from restaurant import views
urlpatterns=[path("admin/",admin.site.urls),path("",views.home,name="home"),path("book/",views.book,name="book"),path("reservations/",views.reservations_page,name="reservations"),path("api/bookings/",views.booking_api,name="bookings-api"),path("api/bookings/<str:booking_date>/",views.bookings_for_date_api,name="bookings-for-date-api")]
