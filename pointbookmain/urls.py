from django.conf.urls import url, include
from . import views


urlpatterns = [
	url(r'^$',views.index, name='index'),

	url(r'^signup/$', views.sign_up, name='signup'),

	url(r'^login/$', views.log_in, name='login'),

	url(r'^logout/$', views.log_out, name='logout'),

	url(r'^partnerprofile/(?P<partner_id>[0-9]+)/$', views.partner_profile, name='partner_profile'),

	url(r'^partnerprofile/(?P<partner_id>[0-9]+)/edit$', views.partner_profile_edit, name='partner_profile_edit'),

	url(r'^partnerprofile/(?P<partner_id>[0-9]+)/delete$', views.partner_profile_delete, name='partner_profile_delete'),

	url(r'^partnerlist/$', views.partner_list, name='partner_list'),

	url(r'^api/', include('pointbookmain.api.urls')),

	# url(r'^partnerprofileform/$', views.partner_profile_form, name='partner_profile_form'),

]