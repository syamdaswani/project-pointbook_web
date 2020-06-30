from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^getServiceList/$', views.ServiceListAPIView.as_view(), name='service_list'),

    url(r'^getPartnersByServiceId/(?P<service_id>[0-9]+)/$', views.PartnerListByServiceIdAPIView.as_view(), name='partners_by_service_id'),

    url(r'^createBookingRequest/$', views.CreateBookingAPICreate.as_view(), name='create_booking'),

    url(r'^getBookingByUserKey/(?P<user_key>[\w{}.-]{1,40})/$', views.BookingListByUserKeyAPIView.as_view(), name='bookings_by_user_key')

]
