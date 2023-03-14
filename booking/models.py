from django.db import models
from application.models import HotelNumber
from django.db.models import Q
from django.core.exceptions import ValidationError


class Booking(models.Model):
    date_started = models.DateField('Дата начала', null=True, blank=True)
    date_end = models.DateField('Дата окончания', null=True, blank=True)
    date_len = models.PositiveIntegerField('Сколько ночей', blank=True, null=True)
    number = models.ForeignKey('Номер отеля', HotelNumber, on_delete=models.CASCADE)

    def create(self, *args, **kwargs):
        bookings = Booking.objects.filter(
            Q(date_started__gte=self.date_started) & Q(date_end__lte=self.date_end)
        )
        if len(bookings):
            raise ValidationError(f'На такие даты уже есть номера {", ".join(bookings)}')
        super(Booking, self).save(*args, **kwargs)
