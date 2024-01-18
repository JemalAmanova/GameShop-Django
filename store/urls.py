from django.urls import path

from . import views

#oluşturduğumuz viewleri çağırmak için yol oluşturduk:

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
 path('update_item/', views.updateItem, name="update_item"),
 path('process_order/', views.processOrder, name="process_order"),
 path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
        path('signup', views.signup, name='signup'),
                path('cat1', views.store, {'cat':'0'}, name='category1'),
                path('cat2', views.store, {'cat':'1'}, name='category2'),
                path('cat3', views.store, {'cat':'2'}, name='category3'),
                path('cat4', views.store, {'cat':'3'}, name='category4'),
                path('cat4', views.store, {'cat':'4'}, name='category5'),

]