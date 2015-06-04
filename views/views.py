from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView, ListView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from users.sign_up_2_form import SignUp2Form
from users.models import Users
from authorizenet.cim import add_profile, get_profile, update_payment_profile, process_transaction
from authorizenet.models import CIMResponse, Response
from datetime import date
from topping_preferences.models import ToppingPreferences
from topping_preferences.topping_preference_form import ToppingPreferencesForm, ToppingPreferencesAdjustForm
from time_preferences.models import TimePreferences
from time_preferences.time_preference_form import TimePreferencesForm, TimePreferencesAdjustForm
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.template import Context
from django.template.loader import render_to_string, get_template
from twilio.rest import TwilioRestClient
import hashlib
from email_identifiers.models import EmailIdentifiers
from pizza_merchants.models import PizzaMerchants
from drivers.models import Drivers
from drivers.new_driver_form import NewDriverForm
from pygeocoder import Geocoder
from pizza_orders.models import PizzaOrders
from pizza_types.models import PizzaTypes
from datetime import datetime
from google_distance_matrix.core import DM
import decimal
from spec_pizza_candidate_records.models import SpecPizzaCandidateRecords
from spec_pizza_sales.models import SpecPizzaSales
import json
from driver_pizza_orders.models import DriverPizzaOrders


class HomePageView(TemplateView):
    template_name = "index.html"

class SignUp1View(TemplateView):
    template_name = "signup1.html"

class LogInView(TemplateView):
    template_name = "login.html"

def sign_up_2_view(request):
    if request.method == 'POST':
        request.session['first_name'] = request.POST['first_name']
        request.session['last_name'] = request.POST['last_name']        
        if(EmailIdentifiers.objects.filter(email_address=request.POST['email']).exists()):
            return HttpResponseRedirect("/login/?response=It+looks+like+you+already+have+an+account+with+us.+Please+sign+in.&pizza_order_id=0")
        else:
            request.session['email'] = request.POST['email']
            request.session['password'] = request.POST['password']
            return render(request, "signup2.html")
    elif((settings.ALLOWED_HOSTS[0]+"/signup2/" in request.META['HTTP_REFERER'])and(request.method=="GET")):
        return render(request, 'signup2.html')
    else:
        return HttpResponse("You are not allowed to view this page")

def sign_up_3_view(request):
    if request.method == 'POST':
        request.session['address'] = request.POST['address']
        request.session['address2'] = request.POST['address2']
        request.session['city'] = request.POST['city']
        request.session['state'] = request.POST['state']
        request.session['zip'] = request.POST['zip']
        request.session['phone'] = request.POST['phone']
        f = SignUp2Form(request.POST)
        sign_up_2_save = f.save()
        if sign_up_2_save:
            get_session_id = Users.objects.filter(email = request.session['email'], password = request.session['password'])
            get_session_id_2 = Users.objects.get(email = request.session['email'], password = request.session['password'])
            get_session_id.update(registration_confirmed="no")
            request.session['id'] = get_session_id_2.id
            return render(request, "signup3.html")
        else:
            return HttpResponseRedirect("/signup2/?response=There+was+a+problem+saving+your+account+info.")
    elif((settings.ALLOWED_HOSTS[0]+"/signup3/" in request.META['HTTP_REFERER'])and(request.method=="GET")):
        return render(request, 'signup3.html')           
    else:
        return HttpResponse("You are not allowed to view this page")

def sign_up_4_view(request):
    if ((settings.ALLOWED_HOSTS[0]+"/signup3/" in request.META['HTTP_REFERER']) and (request.method == 'POST')):
        get_current_customer = Users.objects.get(email = request.session['email'], password = request.session['password'])
        customer_id = get_current_customer.id
        company = ""
        country = ""
        fax_number = ""
        cc_number = int(str(request.POST['ccnumber1'])+str(request.POST['ccnumber2'])+str(request.POST['ccnumber3'])+str(request.POST['ccnumber4']))
        expiration_date = date(int(request.POST['year']), int(request.POST['month']), 1)
        billing_fields = {'firstName':request.session['first_name'], 'lastName': request.session['last_name'], 'company': company, 'address':request.session['address'], 'city':request.session['city'], 'state':request.session['state'], 'zip':request.session['zip'], 'country':country, 'phoneNumber':request.session['phone'], 'faxNumber':fax_number}
        credit_card_fields = {'cardNumber':cc_number, 'expirationDate':expiration_date, 'cardCode':request.POST['seccode']}
        add_customer_profile = add_profile(customer_id, credit_card_fields, billing_fields, shipping_form_data=None, customer_email=None, customer_description=None)        
        save_profile_id_authnet = Users.objects.filter(id = request.session['id'], email = request.session['email'], password = request.session['password'])
        save_profile_id_authnet.update(profile_id_authnet = add_customer_profile['profile_id'])
        if(save_profile_id_authnet[0].profile_id_authnet):
            return render(request, 'signup4.html')
        else:
            save_profile_id_authnet.delete()
            EmailIdentifiers.objects.filter(email_address=request.session['email']).delete()
            return HttpResponseRedirect(settings.ALLOWED_HOSTS[0]+"/?response=There+was+an+issue+with+your+credit+card+information.+Please+try+your+registration+again.")
    else:
        return HttpResponse("You are not allowed to view this page")


def settings_view(request):
    if(settings.ALLOWED_HOSTS[0]+'/home/' in request.META['HTTP_REFERER']) and (request.method == 'GET'):
        request.session['pizza_order_id']=request.GET['pizza_order_id']
        return render(request, "settings.html")
    elif(settings.ALLOWED_HOSTS[0]+'/pizza-preferences/' in request.META['HTTP_REFERER']) and (request.method == 'GET'):
        return render(request, "settings.html")
    elif(settings.ALLOWED_HOSTS[0]+'/address-preferences/' in request.META['HTTP_REFERER']) and (request.method == 'GET'):
        return render(request, "settings.html")
    elif(settings.ALLOWED_HOSTS[0]+'/payment-preferences/' in request.META['HTTP_REFERER']) and (request.method == 'GET'):
        return render(request, "settings.html")
    elif(settings.ALLOWED_HOSTS[0]+'/contact/' in request.META['HTTP_REFERER']) and (request.method == 'GET'):
        return render(request, "settings.html")
    elif(settings.ALLOWED_HOSTS[0]+'/confirm-spec-pizza-purchase/' in request.META['HTTP_REFERER']) and (request.method == 'GET'):
        return render(request, "settings.html")
    elif(settings.ALLOWED_HOSTS[0]+'/pizza-preferences/' in request.META['HTTP_REFERER']) and (request.method == 'POST'):
        session_id = int(request.session['id'])
        for entry in ToppingPreferences.objects.filter(user_id=session_id):
            entry.delete()
        for entry in TimePreferences.objects.filter(user_id=session_id):
            entry.delete()
        for topping in request.POST.getlist('topping_preference'):
            f = ToppingPreferencesAdjustForm(request.POST)
            topping_preference_save = f.save(commit=False)
            topping_preference_save.topping_preference = topping
            topping_preference_save.user_id = session_id
            topping_preference_save.save(force_insert=True)
        for time in request.POST.getlist('time_preference'):
            f = TimePreferencesAdjustForm(request.POST)
            time_preference_save = f.save(commit=False)
            time_preference_save.time_preference = time
            time_preference_save.user_id = session_id
            time_preference_save.save(force_insert=True)
        return render(request, "settings.html")
    elif(settings.ALLOWED_HOSTS[0]+'/address-preferences/' in request.META['HTTP_REFERER']) and (request.method == 'POST'):
        session_id = int(request.session['id'])
        Users.objects.filter(id=session_id).update(address=request.POST['address'],address2=request.POST['address2'],city=request.POST['city'],state=request.POST['state'],zip=request.POST['zip'],phone=request.POST['phone'])   
        return render(request, "settings.html")
    elif(settings.ALLOWED_HOSTS[0]+'/payment-preferences/' in request.META['HTTP_REFERER']) and (request.method == 'POST'):
        cc_number = int(str(request.POST['ccnumber1'])+str(request.POST['ccnumber2'])+str(request.POST['ccnumber3'])+str(request.POST['ccnumber4']))
        expiration_date = date(int(request.POST['year']), int(request.POST['month']), 1)
        company = ''
        country = ''
        fax_number = ''
        session_id = int(request.session['id'])
        profile_id_user = Users.objects.get(id=session_id, email = request.session['email'], password = request.session['password'])
        profile_id = profile_id_user.profile_id_authnet
        payment_profile_id_user = Users.objects.get(id=session_id, email = request.session['email'], password = request.session['password'])
        payment_profile_id = payment_profile_id_user.payment_profile_id_authnet
        billing_fields = {'firstName':request.session['first_name'], 'lastName': request.session['last_name'], 'company': company, 'address':request.session['address'], 'city':request.session['city'], 'state':request.session['state'], 'zip':request.session['zip'], 'country':country, 'phoneNumber':request.session['phone'], 'faxNumber':fax_number}
        credit_card_fields = {'cardNumber':cc_number, 'expirationDate':expiration_date, 'cardCode':request.POST['seccode']}
        if(update_payment_profile(profile_id, payment_profile_id, credit_card_fields, billing_fields)):
            return render(request, "settings.html")
        else:
            return HttpResponse("There was an issue with the credit card information you entered.")
    else:
        return HttpResponse("You are not allowed to access this page.")
    
    return render(request, 'settings.html', {'form': f})
     
              
class PizzaPreferencesView(ListView):
    model = ToppingPreferences
    template_name = "pizza-preferences.html"
    context_object_name = "topping_preference_list"

    def get_context_data(self, **kwargs):
        context = super(PizzaPreferencesView, self).get_context_data(**kwargs)
        context['time_preference_list'] = TimePreferences.objects.all()
        return context

                         
class AddressPreferencesView(ListView):
    model = Users
    template_name = "address-preferences.html"
    context_object_name = "address_preference_list"

def payment_preferences_view(request):
    if((settings.ALLOWED_HOSTS[0]+"/settings/" in request.META['HTTP_REFERER']) and (request.method == "GET")):
        get_user_single = Users.objects.get(id = request.session['id'], email = request.session['email'], password = request.session['password'])
        get_user = Users.objects.filter(id = request.session['id'], email = request.session['email'], password = request.session['password'])
        get_customer_cc_info = get_profile(get_user_single.profile_id_authnet)
        get_user.update(payment_profile_id_authnet = get_customer_cc_info['payment_profiles'][0]['payment_profile_id'])
        return render(request,'payment-preferences.html',{'first_name':get_customer_cc_info['payment_profiles'][0]['billing']['first_name'],
                'last_name':get_customer_cc_info['payment_profiles'][0]['billing']['last_name'],
                'credit_card_number':get_customer_cc_info['payment_profiles'][0]['credit_card']['card_number'],
                'expiration_date':get_customer_cc_info['payment_profiles'][0]['credit_card']['expiration_date']})
    else:
        return HttpResponse("You are not allowed to access this page.")

def contact_us_view(request):
    if((settings.ALLOWED_HOSTS[0]+"/settings/" in request.META['HTTP_REFERER']) and (request.method == "GET")):
        return render(request, "contact.html", {'first_name':request.session['first_name'], 'last_name':request.session['last_name'], 'email':request.session['email']})
    else:
        return HttpResponse("You are not allowed to access this page.")

def contact_form_handler_view(request):
    if((settings.ALLOWED_HOSTS[0]+"/contact/" in request.META['HTTP_REFERER']) and (request.method == "POST")):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        email_recipient = [settings.EMAIL_RECIPIENT_CONTACT_FORM]
        contact_body = request.POST['contact_body']
        subject = "Inquiry from User"
        send_email = send_mail(subject, contact_body, email, email_recipient)
        if(send_email):
            return HttpResponse("email sent")
        else:
            return HttpResponse("email not sent")
    else:
        return HttpResponse("You are not allowed to view this page.")

def forgot_password_view(request):
    return render(request, "forgot-password.html")

def email_body_view(request):
    if(request.method == "GET"):
        return render(request, "email-body.html")

def forgot_password_email_view(request):
    if(request.method == "GET"):
        first_name = "Mickey"       
        password = "password12345"
        email_address = "mickey.mouse@disneyland.com"
        password_reset_link = settings.ALLOWED_HOSTS[0]+"/create-new-password/"+hashlib.md5(email_address+password).hexdigest()
        host = settings.ALLOWED_HOSTS[0]
        message_body = "<span style='font-weight:bold;'>Hi "+first_name+",</span><br />"
        message_body += "<br />"
        message_body += "<span style='font-weight:bold;'>Please reset your password at the following link:</span><br />"
        message_body += "<br />"
        message_body += "<span style='font-weight:bold;'><span style='color:#993333;'>"+password_reset_link+"</span></span><br />"
        signature = settings.OUTER_EMAIL_SIGNATURE
        company_official_name = settings.COMPANY_OFFICIAL_NAME
        physical_address_1 = settings.PHYSICAL_ADDRESS_1
        physical_address_2 = settings.PHYSICAL_ADDRESS_2
        unsubscribe_link = settings.ALLOWED_HOSTS[0]+"/unsubscribe/"+hashlib.md5(email_address+password).hexdigest()
        return render(request, "forgot-password-email.html", {'main_message':message_body, 'outer_email_signature':signature, 'email_address':email_address, 'host':host, 'company_official_name':company_official_name, 'physical_address_1':physical_address_1, 'physical_address_2':physical_address_2, 'unsubscribe_link':unsubscribe_link, 'password_reset_link':password_reset_link})

def send_forgot_password_email_view(request):
    if(request.method == 'POST'):
        subject = "Login Info Reminder"
        to = [request.POST['email']]
        from_email = settings.EMAIL_HOST_USER
        if(Users.objects.filter(email=request.POST['email']).exists()):
            identify_user = Users.objects.get(email=request.POST['email'])
            first_name = identify_user.first_name
            password = identify_user.password
            email_address = identify_user.email
            password_reset_link = settings.ALLOWED_HOSTS[0]+"/create-new-password/"+hashlib.md5(email_address+password).hexdigest()
            host = settings.ALLOWED_HOSTS[0]
            message_body = "<span style='font-weight:bold;'>Hi "+first_name+",</span><br />"
            message_body += "<br />"
            message_body += "<span style='font-weight:bold;'>Please reset your password at the following link:</span><br />"
            message_body += "<br />"
            message_body += "<span style='font-weight:bold;'><span style='color:#993333;'>"+password_reset_link+"</span></span><br />"
            signature = settings.OUTER_EMAIL_SIGNATURE
            company_official_name = settings.COMPANY_OFFICIAL_NAME
            physical_address_1 = settings.PHYSICAL_ADDRESS_1
            physical_address_2 = settings.PHYSICAL_ADDRESS_2
            static_url = settings.ALLOWED_HOSTS[0]+"/"+settings.STATIC_URL
            email_identifier_new = hashlib.md5(email_address+password).hexdigest()
            unsubscribe_link = settings.ALLOWED_HOSTS[0]+"/unsubscribe/"+email_identifier_new
            ctx = {'main_message':message_body, 'outer_email_signature':signature, 'email_address':email_address, 'host':host, 'company_official_name':company_official_name, 'physical_address_1':physical_address_1, 'physical_address_2':physical_address_2, 'STATIC_URL':static_url, 'unsubscribe_link':unsubscribe_link, 'password_reset_link':password_reset_link}
            message = get_template('forgot-password-email.html').render(Context(ctx))
            msg = EmailMessage(subject, message, to=to, from_email=from_email)
            msg.content_subtype = 'html'
            msg.send()
            return HttpResponse("Email was sent.")
        else:
            return HttpResponse("Email address provided not identified in our records. Maybe you have registered with us using another email address?")
    else:
        return HttpResponse("Email was not sent. There may be an issue with the email address we have on file for you.")

def user_registration_confirmation_email_view(request):
    if(request.method=="GET"):
        email_address = "mickey.mouse@disneyland.com"
        password = "password12345"
        first_name = "Mickey"
        message_body = "<span style='font-weight:bold;'>Hi "+first_name+",</span><br />"
        message_body += "<br />"
        message_body += "<span style='font-weight:bold;'>Thank you for registering an account with Pizza Impulse!</span><br />"
        message_body += "<br />"
        message_body += "<span style='font-weight:bold;'>We look forward to letting you know when your neighbors have put in "
        message_body += "a pizza order so that you can get in on the action too!</span><br />"
        message_body += "<br />"
        message_body += "<span style='font-weight:bold;'>Stay tuned!</span>"
        host = settings.ALLOWED_HOSTS[0]
        signature = settings.OUTER_EMAIL_SIGNATURE
        company_official_name = settings.COMPANY_OFFICIAL_NAME
        physical_address_1 = settings.PHYSICAL_ADDRESS_1
        physical_address_2 = settings.PHYSICAL_ADDRESS_2
        static_url = settings.ALLOWED_HOSTS[0]+"/"+settings.STATIC_URL
        email_identifier_new = hashlib.md5(email_address+password).hexdigest()
        unsubscribe_link = settings.ALLOWED_HOSTS[0]+"/unsubscribe/"+email_identifier_new
        return render(request, "user-registration-confirmation-email.html", {'main_message':message_body, 'outer_email_signature':signature, 'email_address':email_address, 'host':host, 'company_official_name':company_official_name, 'physical_address_1':physical_address_1, 'physical_address_2':physical_address_2, 'STATIC_URL':static_url, 'unsubscribe_link':unsubscribe_link})        

def unsubscribe_view(request):
    if(EmailIdentifiers.objects.filter(email_identifier=request.META['PATH_INFO'][13:]).exists()):
        return render(request, 'unsubscribe.html', {'show_page':'yes'})
    else:
        return render(request, 'unsubscribe.html', {'show_page':'no'})


def unsubscribe_view_2(request):
    if(request.method == "POST"):
        get_user = Users.objects.filter(email=request.POST['email'])
        email_identifier = EmailIdentifiers.objects.filter(email_address=request.POST['email'])
        if(get_user):
            get_user.delete()
            email_identifier.delete()
            return HttpResponse("Your account with Pizza Impulse<br />has been deleted. Sorry<br />to see you go!")
        else:
            return HttpResponse("Please enter the email address<br />you used to set up your<br />Pizza Impulse account.<br />(You may have already unsubscribed as well)")
    else:
        return HttpResponse("Sorry, you are not allowed to access this page.")

def create_new_password_view(request):
     if(EmailIdentifiers.objects.filter(email_identifier=request.META['PATH_INFO'][21:]).exists()):
        return render(request, 'create-new-password.html', {'show_page':'yes'})
     else:
        return render(request, 'create-new-password.html', {'show_page':'no'})

def create_new_password_view_2(request):
    if(request.method == "POST"):
        del request.session['id']
        del request.session['email']
        del request.session['password']
        del request.session['first_name']
        del request.session['last_name']
        del request.session['address']
        del request.session['address2']
        del request.session['city']
        del request.session['state']
        del request.session['zip']
        del request.session['phone']
        get_user = Users.objects.filter(email=request.POST['email'])
        get_email_identifier = EmailIdentifiers.objects.filter(email_address=request.POST['email'])
        if(get_user):
            get_user.update(password=request.POST['new_password'])
            new_email_identifier = hashlib.md5(request.POST['email']+request.POST['new_password']).hexdigest()
            get_email_identifier.update(email_identifier=new_email_identifier)
            return HttpResponse("Your password has been successfully reset! Please <a href='/login/' style='color:#FFCC66;'>LOGIN</a>.")
        else:
            return HttpResponse("There was a problem resetting your password.<br />Please make sure your email address<br />is the one you used to register.")
    else:
        return HttpResponse("Sorry, you are not allowed to access this page.")

def home_view(request):
    if(request.META['HTTP_REFERER'] == settings.ALLOWED_HOSTS[0]+'/signup4/') and (request.method == "POST"):
        session_id = int(request.session['id'])
        for topping in request.POST.getlist('topping_preference'):
            f = ToppingPreferencesForm(request.POST)
            topping_preference_save = f.save(commit=False)
            topping_preference_save.topping_preference = topping
            topping_preference_save.user_id = session_id
            topping_preference_save.save(force_insert=True)
        """
        for time in request.POST.getlist('time_preference'):
            f = TimePreferencesForm(request.POST)
            time_preference_save = f.save(commit=False)
            time_preference_save.time_preference = time
            time_preference_save.user_id = session_id
            time_preference_save.save(force_insert=True)
        """
        subject = "One More Step - User Registration Confirmation"
        to = [request.session['email']]
        from_email = settings.EMAIL_HOST_USER
        first_name = request.session['first_name']
        email_address = request.session['email']
        password = request.session['password']
        host = settings.ALLOWED_HOSTS[0]
        email_identifier_new = hashlib.md5(email_address+password).hexdigest()
        registration_confirmation_link = settings.ALLOWED_HOSTS[0]+"/confirm-registration-final/"+email_identifier_new
        message_body = "<span style='font-weight:bold;'>Hi "+first_name+",</span><br />"
        message_body += "<br />"
        message_body += "<span style='font-weight:bold;'>Thank you for registering an account with Pizza Impulse!</span><br />"
        message_body += "<br />"
        message_body += "<span style='font-weight:bold;'>We look forward to letting you know when your neighbors have put in "
        message_body += "a pizza order so that you can get in on the action too!</span><br />"
        message_body += "<br />"
        message_body += "Please confirm your registration through this link: <span style='font-weight:bold;'><a href='"+registration_confirmation_link+"' style='color:#993333;'>"+registration_confirmation_link+"</a></span>"
        message_body += "<br />"
        message_body += "<span style='font-weight:bold;'>Stay tuned!</span>"
        signature = settings.OUTER_EMAIL_SIGNATURE
        company_official_name = settings.COMPANY_OFFICIAL_NAME
        physical_address_1 = settings.PHYSICAL_ADDRESS_1
        physical_address_2 = settings.PHYSICAL_ADDRESS_2
        static_url = settings.ALLOWED_HOSTS[0]+"/"+settings.STATIC_URL
        register_again_link = "<a href='"+settings.ALLOWED_HOSTS[0]+"' style='color:#FFCC66;'>HERE</a>"
        ei = EmailIdentifiers(email_address=email_address, email_identifier=email_identifier_new)
        ei.save()
        unsubscribe_link = settings.ALLOWED_HOSTS[0]+"/unsubscribe/"+email_identifier_new
        ctx = {'main_message':message_body, 'outer_email_signature':signature, 'email_address':email_address,'host':host, 'company_official_name':company_official_name, 'physical_address_1':physical_address_1,'physical_address_2':physical_address_2, 'STATIC_URL':static_url, 'unsubscribe_link':unsubscribe_link}
        message = get_template('user-registration-confirmation-email.html').render(Context(ctx))
        msg = EmailMessage(subject, message, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        message_successfully_sent = msg.send()
        if(message_successfully_sent):
            return HttpResponseRedirect("/register-via-email-direct/?response=Thank+you+!+We+have+sent+you+an+email.+Please+use+the+link+provided+to+confirm+your+registration+with+Pizza+Impulse.")
        else:
            return HttpResponseRedirect("/register-via-email-direct/?response=There+appears+to+be+an+issue+with+your+registration+confirmation.+Please+try+registering+again"+register_again_link)
    elif((settings.ALLOWED_HOSTS[0]+"/login/" in request.META['HTTP_REFERER']) and (request.method == "POST")):
        if(Users.objects.filter(email=request.POST['email'], password=request.POST['password']).exists()):
            get_user = Users.objects.get(email=request.POST['email'], password=request.POST['password'])
            if(get_user.registration_confirmed=="yes"):
                request.session['id']=get_user.id
                request.session['email']=get_user.email
                request.session['password']=get_user.password
                request.session['first_name']=get_user.first_name
                request.session['last_name']=get_user.last_name
                request.session['address']=get_user.address
                request.session['address2']=get_user.address2
                request.session['city']=get_user.city
                request.session['state']=get_user.state
                request.session['zip']=get_user.zip
                request.session['phone']=get_user.phone
                return HttpResponse("user found")
            elif(get_user.registration_confirmed=="no"):
                subject = "One More Step - User Registration Confirmation"
                to = [get_user.email]
                from_email = settings.EMAIL_HOST_USER
                first_name = get_user.first_name
                email_address = get_user.email
                password = get_user.password
                host = settings.ALLOWED_HOSTS[0]
                email_identifier_new = hashlib.md5(email_address+password).hexdigest()
                registration_confirmation_link = settings.ALLOWED_HOSTS[0]+"/confirm-registration-final/"+email_identifier_new
                message_body = "<span style='font-weight:bold;'>Hi "+first_name+",</span><br />"
                message_body += "<br />"
                message_body += "<span style='font-weight:bold;'>Thank you for registering an account with Pizza Impulse!</span><br />"
                message_body += "<br />"
                message_body += "<span style='font-weight:bold;'>We look forward to letting you know when your neighbors have put in "
                message_body += "a pizza order so that you can get in on the action too!</span><br />"
                message_body += "<br />"
                message_body += "Please confirm your registration through this link: <span style='font-weight:bold;'><a href='"+registration_confirmation_link+"' style='color:#993333;'>"+registration_confirmation_link+"</a></span>"
                message_body += "<br />"
                message_body += "<span style='font-weight:bold;'>Stay tuned!</span>"
                signature = settings.OUTER_EMAIL_SIGNATURE
                company_official_name = settings.COMPANY_OFFICIAL_NAME
                physical_address_1 = settings.PHYSICAL_ADDRESS_1
                physical_address_2 = settings.PHYSICAL_ADDRESS_2
                static_url = settings.ALLOWED_HOSTS[0]+"/"+settings.STATIC_URL
                ei = EmailIdentifiers(email_address=email_address, email_identifier=email_identifier_new)
                ei.save()
                unsubscribe_link = settings.ALLOWED_HOSTS[0]+"/unsubscribe/"+email_identifier_new
                ctx = {'main_message':message_body, 'outer_email_signature':signature, 'email_address':email_address,'host':host, 'company_official_name':company_official_name, 'physical_address_1':physical_address_1,'physical_address_2':physical_address_2, 'STATIC_URL':static_url, 'unsubscribe_link':unsubscribe_link}
                message = get_template('user-registration-confirmation-email.html').render(Context(ctx))
                msg = EmailMessage(subject, message, to=to, from_email=from_email)
                msg.content_subtype = 'html'
                message_successfully_sent = msg.send()
                if(message_successfully_sent):
                    return HttpResponse("We found your record, but we need to confirm your registration. You should receive an email shortly. Please follow the link in the email to complete your registration.")
                else:
                    return HttpResponse("There appears to be an issue with your registration confirmation. Please try registering again here: <a href='"+settings.ALLOWED_HOSTS[0]+"' style='color:#FFCC66;'>REGISTER</a>")        
        else:
            return HttpResponse("user not found")
    elif((settings.ALLOWED_HOSTS[0]+"/login/" in request.META['HTTP_REFERER']) and (request.method == "GET")):
        return render(request, "home.html")
    elif((settings.ALLOWED_HOSTS[0]+"/settings/" in request.META['HTTP_REFERER']) and (request.method == "GET")):
        return render(request, "home.html")
    else:
        return HttpResponse("You are not allowed to access this page.")

    return render(request, 'home.html', {'form': f})
    
def register_via_email_direct_view(request):
    if((settings.ALLOWED_HOSTS[0]+"/signup4/" in request.META['HTTP_REFERER']) and (request.method == "GET")):
        return render(request, "register-via-email-direct.html")
    else:
        return HttpResponse("Sorry, you are not allowed to access this page.")

def confirm_registration_final_view(request):
    if(EmailIdentifiers.objects.filter(email_identifier=request.META['PATH_INFO'][28:])):
        return render(request, "confirm-registration-final.html", {'show_page':'yes'})
    else:
        return render(request, "confirm-registration-final.html", {'show_page':'no'})

def confirm_registration_final_view_2(request):
    if(request.method=="POST"):
        length_of_host_and_path = len(settings.ALLOWED_HOSTS[0])+28
        if(EmailIdentifiers.objects.filter(email_identifier=request.META['HTTP_REFERER'][length_of_host_and_path:], email_address=request.POST['email']).exists()):
            get_user = Users.objects.filter(email=request.POST['email'])
            get_user.update(registration_confirmed="yes")
            return HttpResponseRedirect("/login/?response=Thank+you+for+registering!+Please+log+in+to+proceed+to++the+site!&pizza_order_id=0")
        else:
            get_user = Users.objects.filter(email=request.POST['email'])
            get_user.update(registration_confirmed="no")
            return HttpResponseRedirect("/confirm-registration-final/?response=Sorry,+we+could+not+locate+your+registration+info.+Please+try+your+registration+again+here:+<a href='"+settings.ALLOWED_HOSTS[0]+"' style='color:#FFCC66;'>BEGIN REGISTRATION</a>.")
    else:
        return HttpResponse("Sorry, you are not allowed to access this page")
        
def merchant_login_view(request):
    if(request.method=="GET"):
        return render(request, "merchant-login.html", {"title":"Pizza Impulse - Merchant Login","jumbotron_small_title":"Merchant Login"})
    elif((settings.ALLOWED_HOSTS[0]+"/merchant-home/" in request.META['HTTP_REFERER']) and (request.method=="GET")):
        request.session.flush()
        return render(request, "merchant-login.html", {"title":"Pizza Impulse - Merchant Login","jumbotron_small_title":"Merchant Login"})   

def merchant_home_view(request):
    if((settings.ALLOWED_HOSTS[0]+"/merchant-login/" in request.META['HTTP_REFERER']) and (request.method=="POST")):
        if(PizzaMerchants.objects.filter(user_name=request.POST['user_name'], password=request.POST['password']).exists()):
            get_merchant = PizzaMerchants.objects.get(user_name=request.POST['user_name'], password=request.POST['password'])
            request.session['merchant_name'] = get_merchant.merchant_name
            return render(request, "merchant-home.html", {"title":"Pizza Impulse - Merchant Home","jumbotron_small_title":"Merchant Home","spec_pizza_market_radius_max":settings.SPECULATION_PIZZA_MARKET_RADIUS_MAX})
        else:
            return HttpResponseRedirect("/merchant-login/?response=We+were+not+able+to+find+your+login+info+in+our+system.+Please+try+again&title=Pizza+Impulse+-+Merchant+Login&jumbotron_big_title=PIZZA+IMPULSE&jumbotron_small_title=Merchant+Login")
    elif((settings.ALLOWED_HOSTS[0]+"/merchant-home/" in request.META['HTTP_REFERER']) and (request.method=="POST")):
        return render(request, "merchant-home.html", {"title":"Pizza Impulse - Merchant Home","jumbotron_small_title":"Merchant Home","spec_pizza_market_radius_max":settings.SPECULATION_PIZZA_MARKET_RADIUS_MAX})
    else:
        return HttpResponse("Sorry, you are not allowed to access this page.")

def new_driver_submit_view(request):
    if(request.method=="POST"):
        if(Drivers.objects.filter(driver_first_name=request.POST['driver_first_name'],driver_last_name=request.POST['driver_last_name'],driver_cell_phone=request.POST['driver_cell_phone'],merchant_name=request.POST['merchant_name']).exists()):
            return HttpResponse("This driver already exists in your driver list.")
        else:
            f = NewDriverForm(request.POST)
            new_driver_form_save = f.save()
            if(new_driver_form_save):
                return HttpResponse("New driver added!")
            else:
                return HttpResponse("There was a problem adding the new driver. Please check the contact info entered")
    else:
        return HttpResponse("Sorry, you are not allowed to access this page.")

def enter_delivery_address_submit_view(request):
    if(request.method=="POST"):
        street_address_1 = request.POST['street_address_1']
        street_address_2 = request.POST['street_address_2']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip_code']
        result = Geocoder.geocode(street_address_1+", "+city+", "+state+" "+zip_code)
        if(result.valid_address == True):
            list_of_addresses = []
            for entry in range(0,len(result)):
                list_of_addresses.append("<p onclick='submitValidatedAddress(this.innerHTML)' class='validate_delivery_address_content text-center text-primary lead border_bottom_dotted cursor_pointer'>")
                list_of_addresses.append(result[entry])
                list_of_addresses.append("</p>")
            list_of_addresses.append("<p class='validate_delivery_address_apartment_number text-center lead'>")
            list_of_addresses.append(street_address_2)
            list_of_addresses.append("</p>")
            return HttpResponse(list_of_addresses)
        else:        
            return HttpResponse("The address you have provided could not be validated. Please enter a valid address.");
    else:
        return HttpResponse("Sorry, you are not allowed to access this page.")

def enter_confirmed_delivery_address_submit_view(request):
    if(request.method=="POST"):
        confirmed_address = request.POST['confirmed_address']
        confirmed_street_address_2 = request.POST['confirmed_street_address_2']
        date_now_user_time_zone = int(request.POST['date_now_user_time_zone'])
        result = Geocoder.geocode(confirmed_address)
        if(result.valid_address == True):
            new_delivery_address = PizzaOrders(delivery_addr1=result[0].street_number+" "+result[0].route, delivery_addr2=confirmed_street_address_2, delivery_city = result[0].sublocality_level_1, delivery_state = result[0].administrative_area_level_1, delivery_zip_code = result[0].postal_code, merchant_name = request.session['merchant_name'], order_placed_time_stamp_user_time_zone = date_now_user_time_zone)
            new_delivery_address.save()
            return HttpResponse(new_delivery_address.id)
        else:
            return HttpResponse("Confirmed Delivery Address Not Successfully Saved.")    
    else:
        return HttpResponse("Sorry, you are not allowed to access this page.")

def submit_initial_delivery_order_description_view(request):
    if(request.method=="POST"):
        initial_delivery_order_description = request.POST['initial_delivery_order_description']
        initial_delivery_id = int(request.POST['initial_delivery_id'])
        new_primary_delivery_order_description = PizzaTypes(pizza_order_description = initial_delivery_order_description, pizza_order_id = initial_delivery_id)
        new_primary_delivery_order_description_save = new_primary_delivery_order_description.save()
        return HttpResponse("Primary delivery order description successfully saved.")
    else:
        return HttpResponse("Sorry, you are not allowed to access this page.")        

def google_distance_matrix_api_view(request):
    if(request.method=="POST"):
        initial_delivery_id = request.POST['initial_delivery_id']
        num_of_miles = int(int(request.POST['num_of_miles'])*1609.34)
        if(PizzaOrders.objects.filter(id=initial_delivery_id).exists()):
            get_initial_delivery = PizzaOrders.objects.filter(id=initial_delivery_id).update(spec_pizza_radius=request.POST['num_of_miles']+" miles")
            get_initial_delivery = PizzaOrders.objects.get(id=initial_delivery_id)
            get_initial_delivery_address = get_initial_delivery.delivery_addr1+", "+get_initial_delivery.delivery_city+", "+get_initial_delivery.delivery_state+" "+get_initial_delivery.delivery_zip_code
        list_of_destination_addresses = []
        for entry in Users.objects.filter(registration_confirmed="yes"):
            get_address = entry.address+", "+entry.city+", "+entry.state+" "+entry.zip
            list_of_destination_addresses.append(get_address)
        a = DM()
        a.make_request([get_initial_delivery_address], list_of_destination_addresses)
        list_of_final_results = []
        list_of_top_topping_prefs = []
        if(a.get_closest_points(max_distance = num_of_miles)):
            for entry in a.get_closest_points(max_distance = num_of_miles):
                for entry2 in Users.objects.filter(registration_confirmed="yes"):
                     if(entry[0]==entry2.address+", "+entry2.city+", "+entry2.state+" "+entry2.zip):
                         list_of_final_results.append(entry2.first_name+" "+entry2.last_name+", "+entry2.address+", "+entry2.city+", "+entry2.state+" "+entry2.zip+" "+entry2.phone+"<br />")
                         if(ToppingPreferences.objects.filter(user_id=entry2.id).exists()):
                             user_top_topping_prefs = ToppingPreferences.objects.filter(user_id=entry2.id)
                             for entry3 in user_top_topping_prefs:
                                 list_of_top_topping_prefs.append(entry3.topping_preference)
            pepperoni_count = list_of_top_topping_prefs.count("pepperoni")     
            cheese_count = list_of_top_topping_prefs.count("cheese")
            veggie_count = list_of_top_topping_prefs.count("veggie")
            supreme_count = list_of_top_topping_prefs.count("supreme")
            most_preferred_topping_count = max(pepperoni_count,cheese_count,veggie_count,supreme_count)
            most_preferred_topping = "<p class='lead text-center width_75_percent center-block'>The Speculation Pizza Is:</p>"
            if(most_preferred_topping_count == pepperoni_count):
                most_preferred_topping += "<p class='lead text-success text-center width_75_percent center-block'>Pepperoni</p>"            
            elif(most_preferred_topping_count == cheese_count):
                most_preferred_topping += "<p class='lead text-success text-center width_75_percent center-block'>Cheese</p>"            
            elif(most_preferred_topping_count == supreme_count):
                most_preferred_topping += "<p class='lead text-success text-center width_75_percent center-block'>Supreme</p>"
            elif(most_preferred_topping_count == veggie_count):
                most_preferred_topping += "<p class='lead text-success text-center width_75_percent center-block'>Veggie</p>"     
            most_preferred_topping_strip_html_1 = most_preferred_topping.replace("<p class='lead text-center width_75_percent center-block'>The Speculation Pizza Is:</p>","")
            most_preferred_topping_strip_html_2 = most_preferred_topping_strip_html_1.replace("<p class='lead text-success text-center width_75_percent center-block'>","")
            most_preferred_topping_strip_html_3 = most_preferred_topping_strip_html_2.replace("</p>","")
            PizzaOrders.objects.filter(id=initial_delivery_id).update(spec_pizza_type=most_preferred_topping_strip_html_3)
            return HttpResponse(most_preferred_topping)
        else:
            return HttpResponse("<p class='lead text-success text-center width_75_percent center-block'>Please widen your search above - there were no Pizza Impulse users found in the distance radius you provided.</p>")
       
def drivers_list_view(request):
    if(request.method=="POST"):
        if(Drivers.objects.filter(merchant_name=request.session['merchant_name']).exists()):
            drivers_options_tags = ["<option value='none_selected'>Select A Driver</option>"]
            for entry in Drivers.objects.filter(merchant_name=request.session['merchant_name']):        
                drivers_options_tags.append("<option value=")
                drivers_options_tags.append(entry.id)
                drivers_options_tags.append("> Driver: ")
                drivers_options_tags.append(entry.driver_first_name)
                drivers_options_tags.append(" ")
                drivers_options_tags.append(entry.driver_last_name)
                drivers_options_tags.append(" - ")
                drivers_options_tags.append(entry.driver_cell_phone)
                drivers_options_tags.append("</option>")
            return HttpResponse(drivers_options_tags)
        else:
            return HttpResponse("There are no drivers listed yet.<br />Please add at least one driver.")
    else:
        return HttpResponse("Sorry, you are not allowed to access this page.")

def send_text_message_to_driver_view(request): 
    if(request.method == "POST"):
        if(Drivers.objects.filter(id=request.POST['selected_driver_number']).exists()):                  
            selected_driver = Drivers.objects.get(id=request.POST['selected_driver_number'])
            pizza_order = PizzaOrders.objects.get(id=request.POST['initial_delivery_id'])
            pizza_type = PizzaTypes.objects.get(pizza_order_id=request.POST['initial_delivery_id'])
            add_driver_id_to_pizza_order = DriverPizzaOrders(driver_id=int(request.POST['selected_driver_number']),pizza_order_id=request.POST['initial_delivery_id'])
            add_driver_id_to_pizza_order.save()
            body_message = "Hello "+selected_driver.driver_first_name+","
            body_message += "\n\n"
            body_message += "Please click on the following link once you have delivered the order of "+pizza_type.pizza_order_description+" to:\n\n"
            body_message += pizza_order.delivery_addr1+"\n"
            if(len(pizza_order.delivery_addr2)>0):
                body_message += pizza_order.delivery_addr2+"\n"
            body_message += pizza_order.delivery_city+", "+pizza_order.delivery_state+" "+pizza_order.delivery_zip_code
            body_message += "\n\n"
            body_message += settings.ALLOWED_HOSTS[0]+"/driver-interface-login/?pizza_order_id="+str(pizza_order.id)+"&driver_id="+str(selected_driver.id)
            body_message += "\n"
            from_number = settings.TWILIO_FROM_NUMBER
            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN
            client = TwilioRestClient(account_sid, auth_token)
            message = client.messages.create(body=body_message,
                to=selected_driver.driver_cell_phone,
                from_=from_number)
            message_identifier = message.sid
            if(len(message_identifier)>0):
                return HttpResponse("Text message sent successfully!");
            else:
                return HttpResponse("This driver was not found and may have been<br />deleted by another member of your team,<br />or his number may not be valid.");

def delete_driver_view(request):
    if(request.method == "POST"):
        if(Drivers.objects.filter(id=request.POST['select_driver_to_delete'],merchant_name=request.POST['merchant_name']).exists()):
            Drivers.objects.filter(id=request.POST['select_driver_to_delete'],merchant_name=request.POST['merchant_name']).delete()
            return HttpResponse("This driver has been deleted.")
    else:
        return HttpResponse("Sorry, you are not allowed to access this page.")

def submit_spec_pizza_transaction_view(request):
    if(request.method == "POST"):
        integer_1 = request.POST['integer_1']
        integer_2 = request.POST['integer_2']
        integer_3 = request.POST['integer_3']
        integer_4 = request.POST['integer_4']
        decimal.getcontext().prec = 4
        price = integer_1+integer_2+"."+integer_3+integer_4
        price_spec_pizza = decimal.Decimal(price)/decimal.Decimal(1)
        initial_delivery_id = request.POST['initial_delivery_id']
        if(PizzaOrders.objects.filter(id=initial_delivery_id).exists()):
            PizzaOrders.objects.filter(id=initial_delivery_id).update(spec_pizza_price=price_spec_pizza)
            submitted_price = PizzaOrders.objects.get(id=initial_delivery_id)
            submitted_price_final = submitted_price.spec_pizza_price
            response_to_user = []
            response_to_user.append("The speculation pizza price for this order is $")
            response_to_user.append(submitted_price_final)
            return HttpResponse(response_to_user)
    else:
        return HttpResponse("Sorry, you are not allowed to access this page.")

def cancel_order_view(request):
    if(request.method=="POST"):    
        initial_delivery_id = request.POST['initial_delivery_id']    
        PizzaOrders.objects.filter(id=initial_delivery_id).delete()
        PizzaTypes.objects.filter(pizza_order_id=initial_delivery_id).delete()
        return HttpResponse("This order has been cancelled.")
    else:
        return HttpResponse("Sorry, you are not allowed to access this page.")

def driver_interface_login_view(request):
    if(request.method=="GET"):
        return render(request, "driver-interface-login.html", {"title":"Pizza Impulse - Driver Interface Login","jumbotron_small_title":"Driver Interface Login"})

def driver_interface_view(request):
    if((request.method=="POST") and (("?pizza_order_id" in request.META['HTTP_REFERER']) or ("&pizza_order_id" in request.META['HTTP_REFERER']))):
        cell_portion_1 = request.POST['cell_portion_1']
        cell_portion_2 = request.POST['cell_portion_2']
        cell_portion_3 = request.POST['cell_portion_3']
        pizza_order_id = request.POST['pizza_order_id']
        driver_id = request.POST['driver_id']
        cell_number = cell_portion_1+cell_portion_2+cell_portion_3
        get_pizza_type = PizzaOrders.objects.get(id=pizza_order_id).spec_pizza_type
        get_driver = Drivers.objects.get(id=driver_id)
        get_driver_cell_phone = get_driver.driver_cell_phone
        get_driver_cell_phone = get_driver_cell_phone.replace("-","")
        get_driver_cell_phone = get_driver_cell_phone.replace("(","")
        get_driver_cell_phone = get_driver_cell_phone.replace(")","")
        get_driver_cell_phone = get_driver_cell_phone.replace(".","")
        get_driver_cell_phone = get_driver_cell_phone.replace(" ","")
        if(PizzaOrders.objects.get(id=pizza_order_id).spec_pizza_vetting_begin > PizzaOrders.objects.get(id=pizza_order_id).order_placed_time_stamp_user_time_zone):
            text_sent_or_not = "yes"
        else:
            text_sent_or_not = "no"
        if(get_driver_cell_phone == cell_number):        
            return render(request, "driver-interface.html", {"title":"Pizza Impulse - Driver Interface","jumbotron_small_title":"Driver Interface","spec_pizza_market_radius_max":settings.SPECULATION_PIZZA_MARKET_RADIUS_MAX,"driver_first_name":get_driver.driver_first_name,"spec_pizza_description":get_pizza_type,"speculation_pizza_vetting_time":settings.SPECULATION_PIZZA_VETTING_TIME,"text_sent_or_not":text_sent_or_not})
        else:
            return HttpResponseRedirect("/driver-interface-login/?permission_denied=Sorry,+no+driver+with+the+cell+phone+number+you+have+provided+has+been+identified+in+our+sytem&pizza_order_id="+pizza_order_id+"&driver_id="+driver_id)
    else:
        return HttpResponse("Sorry, you are not allowed to access this page.")
        
def send_text_to_users_view(request):
    if(request.method=="POST"):
        date_and_time_text_sent = request.POST['date_and_time_text_sent']
        date_and_time_spec_pizza_vetting_ends = request.POST['date_and_time_spec_pizza_vetting_ends']
        initial_delivery_id = request.POST['pizza_order_id']
        get_primary_order = PizzaOrders.objects.filter(id=initial_delivery_id)
        primary_order = PizzaOrders.objects.get(id=initial_delivery_id)
        spec_pizza_radius = primary_order.spec_pizza_radius.replace(" miles","")
        num_of_miles = float(spec_pizza_radius)*1609.34
        get_initial_delivery_address = primary_order.delivery_addr1+", "+primary_order.delivery_city+", "+primary_order.delivery_state+" "+primary_order.delivery_zip_code
        list_of_destination_addresses = []     
        for entry in Users.objects.filter(registration_confirmed="yes"):
            get_address = entry.address+", "+entry.city+", "+entry.state+" "+entry.zip
            list_of_destination_addresses.append(get_address)
        if(len(list_of_destination_addresses)==0):
            return HttpResponse("All of the users are currently being targeted by other pizza merchants for speculation pizzas.")
        a = DM()
        a.make_request([get_initial_delivery_address], list_of_destination_addresses)
        list_of_final_results=[]
        if(a.get_closest_points(max_distance = num_of_miles)):
            for entry in a.get_closest_points(max_distance = num_of_miles):
                for entry2 in Users.objects.filter(registration_confirmed="yes"):
                     if(entry[0]==entry2.address+", "+entry2.city+", "+entry2.state+" "+entry2.zip):
                         list_of_final_results.append(entry2.id)
        for entry3 in list_of_final_results:
            get_user = Users.objects.get(id=entry3)
            text_message_body = "Hello "+get_user.first_name+","
            text_message_body += "\n\n"
            text_message_body += "Based on the preferences of you and your neighbors, "+primary_order.merchant_name+" is ready to deliver 1 "+primary_order.spec_pizza_type+" pizza for $"+str(primary_order.spec_pizza_price)+" to a lucky winner!\n\n"
            text_message_body += "Please sign in through the link below to snag that pizza before it's gone!\n\n"
            text_message_body += settings.ALLOWED_HOSTS[0]+"/login/?pizza_order_id="+str(initial_delivery_id)+" \n\n"
            text_message_body += "Brought to you by your friends at Pizza Impulse! \n\n"
            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token  = settings.TWILIO_AUTH_TOKEN
            client = TwilioRestClient(account_sid, auth_token)
            message = client.messages.create(body=text_message_body,to=get_user.phone,from_=settings.TWILIO_FROM_NUMBER)
            add_new_spec_pizza_candidate = SpecPizzaCandidateRecords(user_id=entry3,pizza_order_id=initial_delivery_id,interested_or_not="yes")
            add_new_spec_pizza_candidate.save()            
        get_primary_order.update(spec_pizza_vetting_begin=date_and_time_text_sent,spec_pizza_vetting_end=date_and_time_spec_pizza_vetting_ends,spec_pizza_sold_yes_or_no="no",)    
        return HttpResponse("A notification about this speculation pizza has been sent to all nearby Pizza Impulse users.")

def driver_user_intermediary_view(request):
    if((request.method=="GET") and len(request.GET['pizza_order_id'])>0):
        get_pizza_order = PizzaOrders.objects.get(id=request.GET['pizza_order_id'])
        return HttpResponse("<input type='hidden' name='begin_value' value='"+str(get_pizza_order.spec_pizza_vetting_begin)+"' /><input type='hidden' name='end_value' value='"+str(get_pizza_order.spec_pizza_vetting_end)+"' />")
    else:
        return HttpResponse("Sorry, you are not allowed to access this page.")                    

def notifications_to_driver_view(request):
    if((request.method=="GET") and len(request.GET['pizza_order_id'])>0 and len(request.GET['time_now'])>0):
        get_pizza_order = PizzaOrders.objects.get(id=request.GET['pizza_order_id'])
        if(int(request.GET['time_now']) < int(get_pizza_order.spec_pizza_vetting_end)):
            if(len(SpecPizzaCandidateRecords.objects.filter(pizza_order_id=request.GET['pizza_order_id'],interested_or_not="no"))==len(SpecPizzaCandidateRecords.objects.filter(pizza_order_id=request.GET['pizza_order_id']))):
                return HttpResponse("No one is interested in the speculation pizza.")
            elif(PizzaOrders.objects.get(id=request.GET['pizza_order_id']).spec_pizza_sold_yes_or_no == "yes"):
                get_pizza_type_id = PizzaTypes.objects.get(pizza_order_id=request.GET['pizza_order_id']).id
                get_spec_pizza_sale_id = SpecPizzaSales.objects.get(pizza_type_id=get_pizza_type_id).id
                get_spec_pizza_sale_user_id = SpecPizzaSales.objects.get(pizza_type_id=get_pizza_type_id).user_id
                get_user_address = Users.objects.get(id=get_spec_pizza_sale_user_id)
                if((get_user_address.address2 is not None) and (get_user_address.address2!="")):
                    street_address_2 = str(get_user_address.address2)+"<br />"
                else:
                    street_address_2 = ""
                response_to_driver = "<p class='width_75_percent center-block text-center text-success lead margin_top_30px'>Pizza sold to "+str(get_user_address.first_name)+" "+str(get_user_address.last_name)+" at the following address:</p>"
                response_to_driver += "<p class='width_75_percent center-block text-center lead margin_top_30px'>"+str(get_user_address.address)+"<br />"+street_address_2+str(get_user_address.city)+", "+str(get_user_address.state)+" "+str(get_user_address.zip)+"</p>"
                if(SpecPizzaSales.objects.get(pizza_type_id=get_pizza_type_id).delivery_time_stamp_user_time_zone == 0):
                    response_to_driver += "<p class='width_75_percent center-block text-center lead margin_top_30px'><span class='text-primary'>Please call the winner's phone number once you arrive at the destination:</span><br />"+str(get_user_address.phone)+"</p>"
                    response_to_driver += "<input type='hidden' name='spec_pizza_id' value='"+str(get_spec_pizza_sale_id)+"' />"
                    return HttpResponse(response_to_driver)
                else:
                    response_to_driver += "<p class='width_75_percent center-block text-center lead margin_top_30px'><span class='text-primary'>This order has already been delivered</span></p>"
                    return HttpResponse(response_to_driver)
            else:
                return HttpResponse("Continue waiting")
        else:
            return HttpResponse("Time has run out!")
    else:
        return HttpResponse("Sorry, you are not allowed to view this page.")

def add_spec_pizza_delivery_time_stamp_view(request):
    if(request.method == "POST"):
        spec_pizza_id = request.POST['spec_pizza_id']
        delivery_time_stamp = request.POST['delivery_time_stamp']        
        get_spec_pizza_sale = SpecPizzaSales.objects.filter(id=spec_pizza_id)
        add_time_stamp_to_spec_pizza_sale = get_spec_pizza_sale.update(delivery_time_stamp_user_time_zone=delivery_time_stamp)
        return HttpResponse("Thank you for confirming the speculation pizza delivery for this order!")
    else:
        return HttpResponse("Sorry, you are not allowed to access this page.")

def find_status_of_spec_pizza_if_any(request):
    if(request.method=="POST"):
        pizza_order_id = request.POST['pizza_order_id']
        user_id = request.POST['user_id']
        time_now = request.POST['time_now']
        if(PizzaOrders.objects.filter(id=pizza_order_id).exists()):
            if(SpecPizzaCandidateRecords.objects.filter(pizza_order_id=pizza_order_id,user_id=user_id).exists()):
                get_pizza_order = PizzaOrders.objects.get(id=pizza_order_id)
                if(int(get_pizza_order.spec_pizza_vetting_end)>int(time_now)):
                    if(get_pizza_order.spec_pizza_sold_yes_or_no == "no"):
                        return HttpResponse("The speculation pizza has not been sold yet.")
                    else:
                        return HttpResponse("This speculation pizza has already been sold.")
                else:
                    return HttpResponse("Time has run out! This speculation pizza vetting session is over.")
            else:
                return HttpResponse("There are no speculation pizzas in your area.")
        else:
            return HttpResponse("The pizza order id indicated does not exist.")
               
    else:
        return HttpResponse("Sorry, you are not allowed to access this page.")

def get_speculation_pizza_info_view(request):
    if(request.method=="GET"):
        if(int(request.GET['pizza_order_id'])>0):
            get_pizza_order = PizzaOrders.objects.get(id=request.GET['pizza_order_id'])
            response = {"spec_pizza_description":get_pizza_order.spec_pizza_type,"spec_pizza_price":str(get_pizza_order.spec_pizza_price),"spec_pizza_vetting_begin":get_pizza_order.spec_pizza_vetting_begin,"spec_pizza_vetting_end":get_pizza_order.spec_pizza_vetting_end}
            response_json = json.dumps(response)
            return HttpResponse(response_json)
        else:
            return HttpResponse("Sorry, no data could be returned from this request.")

def not_interested_view(request):
    if(request.method=="POST"):
        user_id = request.POST['user_id']
        pizza_order_id = request.POST['pizza_order_id']
        if(SpecPizzaCandidateRecords.objects.filter(pizza_order_id=pizza_order_id,user_id=user_id).exists()):
            get_spec_pizza_candidate_record = SpecPizzaCandidateRecords.objects.filter(pizza_order_id=pizza_order_id,user_id=user_id)
            get_spec_pizza_candidate_record.update(interested_or_not="no")
            return HttpResponse("User not interested in this speculation pizza.")
    else:
        return HttpResponse("Sorry, you are not allowed to access this page.")

def confirm_spec_pizza_purchase_view(request):
    if(request.method=="POST"):
        return render(request, "confirm-spec-pizza-purchase.html")
    elif((request.method=="GET") and ("/confirm-spec-pizza-purchase/" in request.META['HTTP_REFERER'])):
        return render(request, "confirm-spec-pizza-purchase.html")
    else:
        return HttpResponse("Sorry, you are not allowed to access this page.")

def winner_view(request):
    if(request.method=="POST"):
        get_pizza_order_time_out_or_no = PizzaOrders.objects.get(id=request.POST['pizza_order_id'])
        spec_pizza_vetting_end = get_pizza_order_time_out_or_no.spec_pizza_vetting_end
        if(int(request.POST['time_now'])<= spec_pizza_vetting_end):
            user_id = request.POST['user_id']
            pizza_order_id = request.POST['pizza_order_id']
            spec_pizza_description = request.POST['spec_pizza_description']
            spec_pizza_price = request.POST['spec_pizza_price']
            merchant_name = PizzaOrders.objects.get(id=pizza_order_id).merchant_name
            merchant_phone_number = PizzaMerchants.objects.get(merchant_name=merchant_name).phone_number
            get_user = Users.objects.get(id=user_id)
            profile_id = get_user.profile_id_authnet
            get_more_user_info = get_profile(profile_id)
            payment_profile_id = get_more_user_info['payment_profiles'][0]['payment_profile_id']
            transaction_type = "AuthOnly"
            amount = spec_pizza_price                             
            get_transaction_response = process_transaction(profile_id,payment_profile_id,transaction_type,amount)
            total_transactions_for_user = len(Response.objects.filter(cust_id=user_id))
            get_last_transaction_for_user = Response.objects.filter(cust_id=user_id).order_by('id')[total_transactions_for_user-1].id
            update_trans_id = Response.objects.filter(id=get_last_transaction_for_user).update(trans_id=pizza_order_id)
            if(Response.objects.get(id=get_last_transaction_for_user).response_code != str(1)):            
                return HttpResponseRedirect("/sorry/?response_code="+str(Response.objects.get(id=get_last_transaction_for_user).response_code)+"&response_reason_text="+Response.objects.get(id=get_last_transaction_for_user).response_reason_text+"&show_phone_number_or_not=no&show_logout_or_login=login&pizza_order_id="+pizza_order_id)
            else:
                if(PizzaOrders.objects.filter(id=pizza_order_id,spec_pizza_sold_yes_or_no="no").exists()):
                    get_pizza_order = PizzaOrders.objects.get(id=pizza_order_id)
                    get_primary_pizza_type = PizzaTypes.objects.get(pizza_order_id=pizza_order_id)
                    new_spec_pizza_sale = SpecPizzaSales(spec_pizza_type_name=get_pizza_order.spec_pizza_type,spec_pizza_price=get_pizza_order.spec_pizza_price,pizza_type_id=get_primary_pizza_type.id,user_id=user_id,addr1=get_user.address,addr2=get_user.address2,city=get_user.city,state=get_user.state,zip_code=get_user.zip,delivery_time_stamp_user_time_zone=0)
                    new_spec_pizza_sale.save()
                    update_pizza_order_as_sold = PizzaOrders.objects.filter(id=pizza_order_id).update(spec_pizza_sold_yes_or_no="yes")
                    find_driver_for_order = DriverPizzaOrders.objects.get(pizza_order_id=pizza_order_id)
                    get_driver_phone_number = Drivers.objects.get(id=find_driver_for_order.driver_id).driver_cell_phone
                    get_spec_pizza_sale = SpecPizzaSales.objects.filter(user_id=user_id).order_by('id')[len(SpecPizzaSales.objects.filter(user_id=user_id))-1]
                    get_user_for_pizza_sale = Users.objects.get(id=user_id)
                    account_sid = settings.TWILIO_ACCOUNT_SID
                    auth_token  = settings.TWILIO_AUTH_TOKEN
                    client = TwilioRestClient(account_sid, auth_token)
                    message_to_driver = "Pizza sold to "+get_user_for_pizza_sale.first_name+" "+get_user_for_pizza_sale.last_name+" at the following address:\n\n"
                    message_to_driver += get_user_for_pizza_sale.address+"\n"
                    if((get_user_for_pizza_sale.address2 is not None) and (get_user_for_pizza_sale.address2 != "")):
                        message_to_driver += str(get_user_for_pizza_sale.address2)+"\n"
                    message_to_driver += get_user_for_pizza_sale.city+","+get_user_for_pizza_sale.state+" "+get_user_for_pizza_sale.zip+"\n\n"
                    message_to_driver += "\n\n"
                    message_to_driver += "Please call the winner's phone number once you reach the destination: "+get_user_for_pizza_sale.phone+", then sign in to the driver interface below (if you are not already signed in) and confirm that the speculation pizza has been delivered:\n\n"
                    message_to_driver += settings.ALLOWED_HOSTS[0]+"/driver-interface-login/?pizza_order_id="+str(pizza_order_id)+"&driver_id="+str(find_driver_for_order.driver_id)
                    message_to_driver += "\n\n"                   
                    message = client.messages.create(body=message_to_driver,
                    to=get_driver_phone_number,
                    from_=settings.TWILIO_FROM_NUMBER)
                    return render(request, "winner.html")
                elif(PizzaOrders.objects.filter(id=pizza_order_id,spec_pizza_sold_yes_or_no="yes").exists()):                    
                    return HttpResponseRedirect("/sorry/?response_reason_text=Some+one+beat+you+to+it!,+but+you+can+still+get+a+fresh+pizza+within+30+minutes+by+calling:&show_phone_number_or_not=yes&show_logout_or_login=logout&pizza_order_id="+pizza_order_id+"&merchant_phone_number="+merchant_phone_number)
        elif(int(request.POST['time_now'])> spec_pizza_vetting_end):
            user_id = request.POST['user_id']
            pizza_order_id=request.POST['pizza_order_id']
            merchant_name = PizzaOrders.objects.get(id=user_id).merchant_name
            merchant_phone_number = PizzaMerchants.objects.get(merchant_name=merchant_name).phone_number
            return HttpResponseRedirect("/sorry/?response_reason_text=Time+has+run+out+for+this+speculation+pizza+order,+but+you+can+still+get+a+fresh+pizza+within+30+minutes+by+calling:&show_phone_number_or_not=yes&show_logout_or_login=logout&pizza_order_id="+pizza_order_id+"&merchant_phone_number="+merchant_phone_number)
    else:
        return HttpResponse("Sorry, you are not allowed to access this page.")
            
def sorry_view(request):
    if((request.method=="GET") and ("/confirm-spec-pizza-purchase/" in request.META['HTTP_REFERER'])):
        return render(request, "sorry.html")        





