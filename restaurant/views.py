import json
from datetime import date
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_http_methods
from django.core.exceptions import ValidationError
from .models import Booking
def home(request): return render(request,"restaurant/index.html")
def book(request): return render(request,"restaurant/book.html",{"today":timezone.localdate().isoformat()})
def reservations_page(request): return render(request,"restaurant/reservations.html",{"today":timezone.localdate().isoformat()})
def serialize(b): return {"id":b.pk,"first_name":b.first_name,"reservation_date":b.reservation_date.isoformat(),"reservation_slot":b.reservation_slot,"reservation_time":f"{b.reservation_slot//60:02d}:00"}
@require_GET
def bookings_for_date_api(request,booking_date=None):
 value=booking_date or request.GET.get("date")
 qs=Booking.objects.all()
 if value:
  try: parsed=date.fromisoformat(value)
  except ValueError: return JsonResponse({"error":"Date must use YYYY-MM-DD format."},status=400)
  qs=qs.filter(reservation_date=parsed)
 return JsonResponse([serialize(b) for b in qs],safe=False)
@require_http_methods(["GET","POST"])
def booking_api(request):
 if request.method=="GET": return bookings_for_date_api(request)
 try:
  data=json.loads(request.body or "{}")
  name=str(data.get("first_name","")).strip(); day=date.fromisoformat(str(data.get("reservation_date",""))); slot=int(data.get("reservation_slot"))
 except (json.JSONDecodeError,TypeError,ValueError): return JsonResponse({"error":"Please provide a name, date, and valid reservation slot."},status=400)
 if not name: return JsonResponse({"error":"First name is required."},status=400)
 if day<timezone.localdate(): return JsonResponse({"error":"Reservations cannot be made in the past."},status=400)
 if slot not in range(600,1320,60): return JsonResponse({"error":"Choose a valid reservation time."},status=400)
 try:
  with transaction.atomic():
   booking=Booking(first_name=name,reservation_date=day,reservation_slot=slot); booking.full_clean(); booking.save()
 except IntegrityError: return JsonResponse({"error":"That time is already booked. Choose another slot."},status=409)
 except ValidationError as exc: return JsonResponse({"error":"; ".join(exc.messages)},status=400)
 return JsonResponse(serialize(booking),status=201)
