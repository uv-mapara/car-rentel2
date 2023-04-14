from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import razorpay

# Create your views here.
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

def index(request):
    cars = Car.objects.all()
    return render(request, "index.html", {'cars':cars})

Dealer=CarDealer()
def car_dealer_signup(request):
    location = Location.objects.all()
    if request.method == "POST":
        user = CarDealer()
        user.username = request.POST['username']        
        user.email = request.POST['email']
        user.location = request.POST['city']        
        user.phone = request.POST['phone']
        user.password = request.POST['password1']  

        if CarDealer.objects.filter(email=Dealer.email).exists():            
            return redirect('CarDealerSignup') 
        else:
            user.save() 
            return redirect('CarDealerLogin')
    return render(request,"car_dealer_signup.html",{'l':location})

def car_dealer_signout(request):
    if request.session.has_key('email'):
        email = request.session['email']
        user = CarDealer.objects.get(email=email)
        del user
        return redirect('CarDealerLogin')

def car_dealer_login(request):
    if request.method=="POST":
        try:
            e=request.POST['email'] 
            request.session['email']=e            
            p=request.POST['password']                       
            x=CarDealer.objects.get(email=e)                         
            if x.password==p:
                # messages.success(request, f'you are now logged')                
                return redirect('/all_cars')
            else:
                return redirect('/CarDealerLogin')
        except:
            return redirect('/CarDealerLogin')
    return render(request, "car_dealer_login.html")

def add_car(request):
    if request.session.has_key('email'):
        location = Location.objects.all()
        user = CarDealer.objects.get(email = request.session['email'])
        if request.method == "POST":
            car = Car()
            car.car_dealer = user
            car.name = request.POST['car_name']
            car.location = request.POST['city']
            car.image = request.FILES['image']
            car.capacity = request.POST['capacity']
            car.rent = request.POST['rent']                  
            car.save()                
        return render(request, "add_car.html",{'l':location})

def all_cars(request):
    if request.session.has_key('email'):
        dealer = CarDealer.objects.filter(email=request.session['email']).first()
        cars = Car.objects.filter(car_dealer=dealer)
    return render(request, "all_cars.html", {'cars':cars})

def update_car(request,pk):
    location = Location.objects.all()    
    car = Car.objects.get(pk=pk)
    if request.method == 'POST':            
        car.name = request.POST.get('car_name')        
        car.location = request.POST.get('city')        
        car.image = request.POST.get('image')        
        car.capacity = request.POST.get('capacity')        
        car.rent = request.POST.get('rent')        
        car.save()                 
    return render(request,'update_car.html',{'car':car,'l':location})       

def customer_navbar(request):
    user=request.session['email']
    per=Customer.objects.get(email=user)
    return render(request,'customer_navbar.html',{'per':per})

def customer_signup(request):
    location = Location.objects.all()
    if request.method == "POST":
        user = Customer()
        user.username = request.POST['username']        
        user.email = request.POST['email']
        user.location = request.POST['city']        
        user.phone = request.POST['phone']
        user.password = request.POST['password1']        
        if Customer.objects.filter(email=user.email).exists():            
            messages.warning(request, 'Email is already Exist.')
        else:
            user.save()
        return redirect('customer_login')
    return render(request, "customer_signup.html")

def customer_login(request): 
    if request.method=="POST":
        try:
            e=request.POST['email'] 
            request.session['email']=e            
            p=request.POST['password']                       
            x=Customer.objects.get(email=e)                         
            if x.password==p:                
                return redirect('/customer_homepage')
            else:
                messages.warning(request, 'Please input correct password')                
        except:
            messages.warning(request,'Enter Username And Password.')
    return render(request, "customer_login.html")

def signout(request):
    if request.session.has_key('email'):
        email = request.session['email']
        user = Customer.objects.get(email=email)
        del user
        return redirect('customer_login')

def customer_homepage(request): 
    if request.session.has_key('email'):
        location = Location.objects.all()
        user=request.session['email']
        per=Customer.objects.get(email=user)
        if request.method == 'POST':
            city = request.POST.get('city')
            vehicles_list = []
            location = Location.objects.filter(city = city)   
            for a in location:
                cars = Car.objects.filter(location=a)
                for car in cars:
                    if car.is_available == True:
                        vehicle_dictionary = {'name':car.name, 'id':car.id, 'image':car.image.url, 'city':car.location,'capacity':car.capacity}
                        vehicles_list.append(vehicle_dictionary)
            request.session['vehicles_list'] = vehicles_list            
            return redirect('search_results')
        return render(request, "customer_homepage.html",{'l':location,'per':per})

def search_results(request):               
    if request.session.has_key('email'):
        user=request.session['email']
        per=Customer.objects.get(email=user)
        if request.method == 'POST':
            car_id = request.POST.get('id')          
            return redirect('car_rent',pk=car_id)
    return render(request, "search_results.html",{'per':per})

def car_rent(request,pk):
    if request.session.has_key('email'):        
        car = get_object_or_404(Car, pk=pk) 
        cost_per_day = int(car.rent)
        user=request.session['email']
        per=Customer.objects.get(email=user)
        if request.method == 'POST':
            days = request.POST.get('days') 
            date = request.POST.get('date') 
            return redirect('confirm-details',pk=car.pk,days=int(days),date=date)    
    return render(request, 'car_rent.html', {'car':car, 'cost_per_day':cost_per_day,'per':per})

def confirm_details(request,pk,days,date):
    if request.session.has_key('email'):
        user = Customer.objects.get(email=request.session['email'])
        per=Customer.objects.get(email=user)
        days = days  
        date = date
        car = get_object_or_404(Car, pk=pk) 
        if car.is_available:
            car_dealer = car.car_dealer   
            rent = (int(car.rent))*(int(days))
            car_dealer.earnings += rent
            car_dealer.save()

            payment = client.order.create({
                'amount':rent*100,
                'currency':'INR',
                'payment_capture':'1',
            })
            order_id=payment['id']              

            if request.method=="POST":
                payment=request.POST['payment']            
                order_id=request.POST.get('order_id')

                #order = Order(car=car, dealer=car_dealer, Customer=email, rent=rent, days=days , payment_id = order_id , paid = True)
                #order.save()
                order = Order()                
                order.customer = user                
                order.dealer =  car_dealer                      
                order.car = car                
                order.rent = rent                
                order.days = days                            
                order.date = date
                order.payment_id = order_id                
                order.paid = True                
                order.save()
                car.is_available = False                                                             
        context={  
            'car_dealer':car_dealer,
            'car':car,
            'rent':rent,
            'days':days,
            'date':date,
            'order_id':order_id,
            'payment':payment ,
            'per':per,
        }
    return render(request, "confirm-details.html",context)

def order_details(request):
    if request.session.has_key('email'):
        email=Customer.objects.get(email=request.session['email'])
        user=request.session['email']
        per=Customer.objects.get(email=user)
        print(per)
        all_orders = []
        try:
            orders = Order.objects.filter(customer=email)  
            print(orders.email)
        except:
            orders = None
        if orders is not None:
            for order in orders:
                if order.is_complete == False:
                    order_dictionary = {'id':order.id, 'rent':order.rent, 'car':order.car, 'days':order.days, 'car_dealer':order.dealer,'paid':order.paid}
                    all_orders.append(order_dictionary)
        return render(request, "order_details.html",{'all_orders':all_orders,'per':per})

def delete_order(request, id):
    if request.session.has_key('email'):
        order = Order.objects.filter(id=id)
        order.delete()
        return redirect("/order_details")

def all_orders(request):
    if request.session.has_key('email'):
        email = request.session['email']
        user = Customer.objects.get(email=email)
        car_dealer = CarDealer.objects.get(username=user.username)
        orders = Order.objects.filter(dealer=car_dealer)
        all_orders = []
        for order in orders:
            if order.is_complete == False:
                all_orders.append(order)
        return render(request, "all_orders.html", {'all_orders':all_orders})

def complete_order(request):
    if request.session.has_key('email'):
        order_id = request.POST['id']
        order = Order.objects.get(id=order_id)
        car = order.car
        order.is_complete = True
        order.save()
        car.is_available = True
        car.save()
        return redirect('/all_orders/')

def earnings(request):
    if request.session.has_key('email'):
        email = request.session['email']
        user = Customer.objects.get(email=email)
        car_dealer = CarDealer.objects.get(username=user.username)
        orders = Order.objects.filter(dealer=car_dealer)
        all_orders = []
        for order in orders:
            all_orders.append(order)
        return render(request, "earnings.html", {'amount':car_dealer.earnings, 'all_orders':all_orders})

@csrf_exempt
def success(request): 
    return render(request,'success.html')