from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("car_dealer_signup/", views.car_dealer_signup, name="CarDealerSignup"),
    path("car_dealer_login/", views.car_dealer_login, name="CarDealerLogin"),
    path("car_dealer_signout/", views.car_dealer_signout, name="car_dealer_signout"),
    path("add_car/", views.add_car, name="add_car"),
    path("all_cars/", views.all_cars, name="all_cars"),
    path("update_car/<int:pk>", views.update_car, name="updateCar"),
    path("customer_signup/", views.customer_signup, name="customer_signup"),
    path("customer_login/", views.customer_login, name="customer_login"),   
    path("signout/", views.signout, name="signout"), 
    path("customer_homepage/", views.customer_homepage, name="customer_homepage"),
    path("search_results/", views.search_results, name="search_results"),
    path("car_rent/<int:pk>", views.car_rent, name="car_rent"),    
    path("confirm-details/<int:pk>/<int:days>/<str:date>", views.confirm_details, name="confirm-details"),    
    path("order_details/", views.order_details, name="order_details"),
    path("delete_order/<int:id>", views.delete_order, name="delete_order"),
    path("all_orders/", views.all_orders, name="all_orders"),
    path("complete_order/", views.complete_order, name="complete_order"),
    path("earnings/", views.earnings, name="earnings"),
    path("success/", views.success, name="success"),
    #path("past_orders/", views.past_orders, name="past_orders"),
]
