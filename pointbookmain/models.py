from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

# Create your models here.
SERVICE_STATUS_CHOICE = [
	('AV', 'Available'),
	('PV', 'Pending Verification'),
	('FA', 'For Approval')
]

IS_PARTNER_CHOICES = [
	('Yes', 'Yes'),
	('No', 'No')
]

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    last_login_date = models.DateTimeField('last login', null=True)
    last_failed_login_attempt = models.DateTimeField('last failed login', null=True)
    is_partner = models.CharField(max_length=3, choices=IS_PARTNER_CHOICES, null=True)

    def __str__(self):
        return str(self.user.username)

class PB_Category(models.Model):
	name = models.CharField(max_length=60)
	description = models.TextField;

	created_by = models.CharField(max_length=30)
	created_on = models.DateTimeField('created on', null=True)
	modified_by = models.CharField(max_length=30)
	modified_on = models.DateTimeField('modified on', null=True, blank=True)

	def save(self, *args, **kwargs):
		if not self.id:
			self.created_on = timezone.now()
		self.modified_on = timezone.now()
		return super(PB_Category, self).save(*args, **kwargs)

	def __str__(self):
		return self.id.__str__()

class PB_Professional(models.Model):
	first_name = models.CharField(max_length=60)
	middle_name = models.CharField(max_length=60)
	last_name = models.CharField(max_length=60)

	created_by = models.CharField(max_length=30)
	created_on = models.DateTimeField('created on', null=True)
	modified_by = models.CharField(max_length=30)
	modified_on = models.DateTimeField('modified on', null=True, blank=True)

	def save(self, *args, **kwargs):
		if not self.id:
			self.created_on = timezone.now()
		self.modified_on = timezone.now()
		return super(PB_Professional, self).save(*args, **kwargs)

	def __str__(self):
		return self.id.__str__()

class PB_Service(models.Model):
	name = models.CharField(max_length=60)
	description = models.CharField(max_length=255)
	long_description = models.TextField(blank=True)

	created_by = models.CharField(max_length=30)
	created_on = models.DateTimeField('created on', null=True)
	modified_by = models.CharField(max_length=30)
	modified_on = models.DateTimeField('modified on', null=True, blank=True)

	def save(self, *args, **kwargs):
		if not self.id:
			self.created_on = timezone.now()
		self.modified_on = timezone.now()
		return super(PB_Service, self).save(*args, **kwargs)

	def __str__(self):
		return self.id.__str__()

class Partner(models.Model):
	ON_PROMO_CHOICES = (
		('Y', 'Y'),
		('N', 'N'),
	)

	user_key = models.ForeignKey(Account, on_delete=models.CASCADE)

	name = models.CharField(max_length=50)
	on_promo = models.CharField(max_length=1, choices=ON_PROMO_CHOICES)
	category_key = models.ForeignKey(PB_Category, on_delete=models.PROTECT)
	address_line_1 = models.CharField(max_length=120)
	city = models.CharField(max_length=40)
	contact_person = models.CharField(max_length=80)
	primary_email = models.EmailField(max_length=50)
	primary_mobile = models.CharField(max_length=15, validators=[RegexValidator(r'^\d{1,10}$')])
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
								 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	primary_mobile = models.CharField(validators=[phone_regex], max_length=17)  # validators should be a list
	rating_lifetime = models.DecimalField(max_digits=2, decimal_places=1);

	services = models.ManyToManyField(PB_Service, through='Service_Bridge')
	professionals = models.ManyToManyField(PB_Professional)

	created_by = models.CharField(max_length=30)
	created_on = models.DateTimeField('created on', null=True)
	modified_by = models.CharField(max_length=30)
	modified_on = models.DateTimeField('modified on', null=True, blank=True)

	def save(self, *args, **kwargs):
		if not self.id:
			self.created_on = timezone.now()
		self.modified_on = timezone.now()
		return super(Partner, self).save(*args, **kwargs)

	def __str__(self):
		return self.id.__str__()

class Service_Bridge(models.Model):
	price = models.DecimalField(max_digits=6, decimal_places=2)
	partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
	service = models.ForeignKey(PB_Service, on_delete=models.CASCADE)

class PB_Booking(models.Model):
	BOOKING_STATUS = (
		('Pending', 'Pending'),
		('Negotiating', 'Negotiating'),
		('Partner_Declined', 'Partner_Declined'),
		('User_Declined', 'User_Declined'),
	)

	user_name = models.CharField(max_length=50)
	partner_key = models.ForeignKey(Partner, on_delete=models.CASCADE)
	client_address = models.CharField(max_length=120)
	req_datetime_begin = models.DateTimeField('begin', null=True)
	req_datetime_end = models.DateTimeField('end', null=True)
	req_service_professional_id = models.ForeignKey(PB_Professional)
	req_service_price = models.DecimalField(max_digits=10, decimal_places=2)
	req_service_id = models.ForeignKey(PB_Service)
	req_service_duration = models.DecimalField(max_digits=2, decimal_places=1)
	req_user_notes = models.TextField(null=True)
	booking_status = models.CharField(max_length=30, choices=BOOKING_STATUS)
	reward_points_used = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])
	amount_total = models.DecimalField(max_digits=10, decimal_places=2)
	amount_due = models.DecimalField(max_digits=10, decimal_places=2)
	promo_code = models.CharField(max_length=20, null=True)

	created_by = models.CharField(max_length=30, default='POINTBOOK')
	created_on = models.DateTimeField('created on', null=True, auto_now=True)
	modified_by = models.CharField(max_length=30, default='POINTBOOK')
	modified_on = models.DateTimeField('modified on', null=True, blank=True, auto_now=True)

	def save(self, *args, **kwargs):
		if not self.id:
			self.created_on = timezone.now()
		self.modified_on = timezone.now()
		return super(PB_Booking, self).save(*args, **kwargs)

	def __str__(self):
		return self.id.__str__()


