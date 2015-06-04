from django.conf.urls import patterns, include, url
from views.views import HomePageView, SignUp1View, LogInView, PizzaPreferencesView, AddressPreferencesView


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # User Registration URLs
    url(r'^$', HomePageView.as_view(), name='index'),
    url(r'^signup1/', SignUp1View.as_view(), name='signup1'),
    url(r'^login/', LogInView.as_view(), name='login'),
    url(r'^signup2/', 'views.views.sign_up_2_view', name='signup2'),
    url(r'^signup3/', 'views.views.sign_up_3_view', name='signup3'),
    url(r'^signup4/', 'views.views.sign_up_4_view', name='signup4'),
    url(r'^settings/', 'views.views.settings_view', name='settings'),
    url(r'^pizza-preferences/', PizzaPreferencesView.as_view(), name='pizza-preferences'),
    url(r'^address-preferences/', AddressPreferencesView.as_view(), name='address-preferences'),
    url(r'^payment-preferences/', 'views.views.payment_preferences_view', name='payment-preferences'),
    url(r'^contact/', 'views.views.contact_us_view', name='contact'),
    url(r'^contact-form-handler/', 'views.views.contact_form_handler_view'),
    url(r'^forgot-password/', 'views.views.forgot_password_view', name='forgot-password'),
    url(r'^email-body/', 'views.views.email_body_view', name='email-body'),
    url(r'^forgot-password-email/', 'views.views.forgot_password_email_view', name='forgot-password-email'),
    url(r'^send-forgot-password-email/', 'views.views.send_forgot_password_email_view'),
    url(r'^user-registration-confirmation-email/', 'views.views.user_registration_confirmation_email_view', name='user-registration-confirmation-email'),
    url(r'^unsubscribe/', 'views.views.unsubscribe_view', name="unsubscribe"),
    url(r'^unsubscribe2/', 'views.views.unsubscribe_view_2'),
    url(r'^create-new-password/', 'views.views.create_new_password_view', name="create-new-password"),
    url(r'^create-new-password-2/', 'views.views.create_new_password_view_2'),
    url(r'^register-via-email-direct/', 'views.views.register_via_email_direct_view', name="register-via-email-direct"),
    url(r'^confirm-registration-final/', 'views.views.confirm_registration_final_view', name="confirm-registration-final"),
    url(r'^confirm-registration-final-2/', 'views.views.confirm_registration_final_view_2'),
    url(r'^home/', 'views.views.home_view', name="home"),
    # Merchant Interface URLs
    url(r'^merchant-login/', 'views.views.merchant_login_view', name="merchant-login"),
    url(r'^merchant-home/', 'views.views.merchant_home_view', name="merchant-home"),
    url(r'^new-driver-submit/', 'views.views.new_driver_submit_view'),
    url(r'^enter-delivery-address-submit/', 'views.views.enter_delivery_address_submit_view'),
    url(r'^enter-confirmed-delivery-address-submit/', 'views.views.enter_confirmed_delivery_address_submit_view'),
    url(r'^submit-initial-delivery-order-description/', 'views.views.submit_initial_delivery_order_description_view'),
    url(r'^google-distance-matrix-api/', 'views.views.google_distance_matrix_api_view'),
    url(r'^drivers-list/', 'views.views.drivers_list_view'),
    url(r'^send-text-message-to-driver/', 'views.views.send_text_message_to_driver_view'),
    url(r'^delete-driver/', 'views.views.delete_driver_view'),
    url(r'^submit-spec-pizza-transaction/', 'views.views.submit_spec_pizza_transaction_view'),
    url(r'^cancel-order/', 'views.views.cancel_order_view'),
    # Driver Interface URLs
    url(r'^driver-interface-login/', 'views.views.driver_interface_login_view'),
    url(r'^driver-interface/', 'views.views.driver_interface_view'),
    url(r'^send-text-to-users/', 'views.views.send_text_to_users_view'),
    url(r'^driver-user-intermediary/', 'views.views.driver_user_intermediary_view'),
    url(r'^notifications-to-driver/', 'views.views.notifications_to_driver_view'),
    url(r'^add-spec-pizza-delivery-time-stamp/', 'views.views.add_spec_pizza_delivery_time_stamp_view'),
    # User Speculation Pizza View URLs
    url(r'^find-status-of-spec-pizza-if-any/', 'views.views.find_status_of_spec_pizza_if_any'),
    url(r'^get-speculation-pizza-info/', 'views.views.get_speculation_pizza_info_view'),
    url(r'^not-interested/', 'views.views.not_interested_view'),
    url(r'^confirm-spec-pizza-purchase/', 'views.views.confirm_spec_pizza_purchase_view'),
    url(r'^winner/', 'views.views.winner_view'),
    url(r'^sorry/', 'views.views.sorry_view'),
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^myproject/', include('myproject.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
