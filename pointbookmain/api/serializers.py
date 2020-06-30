from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField

from pointbookmain.models import PB_Service, Partner, PB_Professional, Service_Bridge, PB_Booking

class ServiceSerializer(ModelSerializer):
    class Meta:
        model = PB_Service
        fields = [
            'id',
            'name',
            'description',
            'long_description',
        ]

class ProfessionalSerializer(ModelSerializer):
    class Meta:
        model = PB_Professional
        fields = [
            'id',
            'first_name',
            'middle_name',
            'last_name'
        ]

class PartnerSerializer(ModelSerializer):
    partner_professionals = ProfessionalSerializer(source='professionals', many=True)
    partner_services = ServiceSerializer(source='services', many=True)
    # partner_services = ServicePriceSerializer(source='service_bridge_set', data=Service_Bridge.objects.all(),many=True)
    class Meta:
        model = Partner
        fields = [
            'id',
            'name',
            'partner_services',
            'partner_professionals',
            'city',
            'on_promo',
            'rating_lifetime',
        ]

class PartnerByServiceIdSerializer(ModelSerializer):
    # service_details = ServiceSerializer(source='service', data=PB_Service.objects.all())
    # id = CharField(source='service.id')
    partner = PartnerSerializer(data=Partner.objects.all)

    class Meta:
        model = Service_Bridge
        fields = [
            'partner',
            'price'
        ]

class DynamicCreateBookingSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super (DynamicCreateBookingSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class CreateBookingSerializer(DynamicCreateBookingSerializer):
    class Meta:
        model = PB_Booking
        fields = [
            'user_name',
            'partner_key',
            'client_address',
            'req_datetime_begin',
            'req_datetime_end',
            'req_service_professional_id',
            'req_service_price',
            'req_service_id',
            'req_service_duration',
            'req_user_notes',
            'booking_status',
            'reward_points_used',
            'amount_total',
            'amount_due',
            'promo_code',
        ]

class GetBookingSerializer(ModelSerializer):
    partner_name = CharField(source='partner_key.name')
    service_name = CharField(source='req_service_id.description')
    professional_full_name = SerializerMethodField()
    def get_professional_full_name(self, obj):
        return '{} {} {}'.format(obj.req_service_professional_id.first_name,
                              obj.req_service_professional_id.middle_name,
                              obj.req_service_professional_id.last_name)
    class Meta:
        model = PB_Booking
        fields = [
            'id',
            'user_name',
            'partner_name',
            'client_address',
            'req_datetime_begin',
            'req_datetime_end',
            'professional_full_name',
            'req_service_price',
            'service_name',
            'req_service_duration',
            'req_user_notes',
            'booking_status',
            'reward_points_used',
            'amount_total',
            'amount_due',
            'promo_code',
        ]