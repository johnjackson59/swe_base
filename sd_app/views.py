from django.shortcuts import render, redirect

from django.views.generic import TemplateView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import NewUserForm, ProfileForm, BuyForm

from .models import Transaction, UserProfile

class PricingModule:
    pass

class LoginPageView(TemplateView):
    template_name = 'sd_app/login.html'

class HomePageView(TemplateView):
    template_name = 'sd_app/home.html'
    #print("\t\tHome page rendered\n")

@login_required
def profilePage(request):
    ''' Display user profile information and allow them to update profile information.
        Display transaction history of User.'''    
    if request.method == 'POST': # Form has been submitted
        #print("\t\tPOST request received\n")
        #user_form = NewUserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.userprofile)
        if profile_form.is_valid():
            #print("\t\tForms are valid\n")
            #user_form.save()
            profile_form.save()            
            return redirect('sd_app:profile')
    else: # GET request, display current information
        profile_form = ProfileForm(instance=request.user.userprofile)
    #     print("\t\tGET request received\n") 
    context = {'profile_form': profile_form}    
    return render(request, 'sd_app/profile.html', context)    

def registerPage(request):
    # '''Prompt user to register, after registering redirect to login page'''
    # return render(request, 'registration/register.html')  
    #print("\t\tRegister page view call\n")
    if request.method != 'POST':
        # Display a blank registration form.
        #print("\t\tGET request received\n")
        form = NewUserForm()
    if request.method == "POST":
        #print("\t\tPOST request received\n")
        form = NewUserForm(data=request.POST)
        if form.is_valid():
            #print("\t\tForm is valid\n")
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("sd_app:home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    
    return render (request=request, template_name="registration/register.html", context={"register_form":form})

@login_required
def buyPage(request):
    '''Prompt user to buy, after buying refresh page.
    Display total price of transaction.
    Link to logout.'''
    price = 0.0
    total_amount = 0.0
    addressItems = UserProfile.objects.filter(user=request.user)
    if request.method != 'POST': 
        #print("\t\tbuyPage: GET request received\n")
        form = BuyForm()
        price = 0.0
        total_amount = 0.00
    elif 'submit' in request.POST: # POST
        #print("\t\tbuyPage: POST request received\n")
        form = BuyForm(data=request.POST)
        if form.is_valid():
            #print("\n\t\tbuyPage Submit: Form is valid\n")
            #form.initial['user_id'] = request.user.id
            new_purchase = form.save(commit=False)
            new_purchase.user = request.user
            #calculate the price and total amount
            #amount = int(request.POST['gallons_requested'])
            #location = addressItems[0].state
            count = Transaction.objects.filter(user=request.user).count()
            if count != 0:
                history = 1
            else:
                history = 0
            price = priceModel(addressItems[0].state, history, int(request.POST['gallons_requested']))
            total_amount = price * int(request.POST['gallons_requested'])
            #save the data to database
            new_purchase.address_1 = addressItems[0].address_1
            new_purchase.address_2 = addressItems[0].address_2
            new_purchase.city = addressItems[0].city
            new_purchase.state = addressItems[0].state
            new_purchase.zipcode = addressItems[0].zipcode
            new_purchase.suggested_price = price
            new_purchase.total_amount_due = total_amount
            new_purchase.save()
            #return redirect('sd_app:buy')
        #print("\n\t\tbuyPage Submit: Form is invalid\n")

    elif 'quotet' in request.POST:
        #print("\n\t\tbuyPage: GET QUOTE request received\n")
        form = BuyForm(data=request.POST)
        #amount = int(request.POST['gallons_requested'])
        #location = addressItems[0].state
        # if form.is_valid():
        #     #print("\n\t\tbuyPage: GET QUOTE Form is valid\n")
        # else:
        #     #print("\n\t\tbuyPage: GET QUOTE Form is invalid\n")
        count = Transaction.objects.filter(user=request.user).count()
        if count != 0:
            history = 1
        else:
            history = 0
        price = priceModel(addressItems[0].state, history, int(request.POST['gallons_requested']))
        total_amount = price * int(request.POST['gallons_requested'])

    context = {'price':price, 'total_amount':total_amount, 'buy_form': form, 'address_1' : addressItems[0].address_1, 'address_2' : addressItems[0].address_2, 'city' : addressItems[0].city, 'state' : addressItems[0].state, 'zipcode' : addressItems[0].zipcode}
    return render(request, 'sd_app/buy.html', context)

@login_required
def purchaseHistoryPage(request):
    purchases = Transaction.objects.filter(user=request.user)
    #context = {'purchases': purchases}    
    return render(request, 'sd_app/purchase_history.html', {'purchases': purchases})

def priceModel(location, history, gallons_requested):
    if location=="tx":
        location_rate = 0.02
    else:
        location_rate = 0.04
    if history ==1:
        history_rate = 0.01
    else:
        history_rate = 0
    if gallons_requested >= 1000:
        gallons_requested_rate = 0.02
    else:
        gallons_requested_rate = 0.03
    company_profit_rate = 0.1
    margin = (location_rate - history_rate + gallons_requested_rate + company_profit_rate) * 1.50
    price = margin + 1.50
    return price

