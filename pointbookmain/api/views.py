from rest_framework.generics import ListAPIView, CreateAPIView

from django.http import HttpResponse

from pointbookmain.models import PB_Service, Partner, Service_Bridge, PB_Booking
from .serializers import ServiceSerializer, PartnerByServiceIdSerializer, CreateBookingSerializer, GetBookingSerializer

def index(request):
    html = "<html><body>API FROM POINTBOOK</body></html>"
    return HttpResponse(html)

class ServiceListAPIView(ListAPIView):
    queryset = PB_Service.objects.all()
    serializer_class = ServiceSerializer

class PartnerListByServiceIdAPIView(ListAPIView):
    serializer_class = PartnerByServiceIdSerializer

    def get_queryset(self):
        service_id = self.kwargs['service_id']
        # return Partner.objects.filter(service_bridge__service=service_id)
        return Service_Bridge.objects.filter(service=service_id)

class CreateBookingAPICreate(CreateAPIView):
    queryset = PB_Booking.objects.all()
    serializer_class = CreateBookingSerializer
    lookup_field = 'user_name'

class BookingListByUserKeyAPIView(ListAPIView):
    serializer_class = GetBookingSerializer

    def get_queryset(self):
        user_key = self.kwargs['user_key']
        return PB_Booking.objects.filter(user_name=user_key)