from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
class Booking(models.Model):
 first_name=models.CharField(max_length=100)
 reservation_date=models.DateField()
 reservation_slot=models.PositiveSmallIntegerField()
 created_at=models.DateTimeField(auto_now_add=True)
 class Meta:
  ordering=["reservation_date","reservation_slot"]
  constraints=[models.UniqueConstraint(fields=["reservation_date","reservation_slot"],name="unique_booking_date_slot")]
 def clean(self):
  if self.reservation_date and self.reservation_date < timezone.localdate(): raise ValidationError({"reservation_date":"Reservations cannot be made in the past."})
  if self.reservation_slot not in range(600,1320,60): raise ValidationError({"reservation_slot":"Choose a valid reservation time."})
 def __str__(self): return f"{self.first_name} - {self.reservation_date} {self.reservation_slot//60:02d}:00"
