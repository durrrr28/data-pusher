from django.urls import path
from . import views

urlpatterns = [

    path('get-create-accounts', views.account_get_post),
    path('get-delete-account/<int:account_id>', views.account_get_delete),
    path('get-create-destinations', views.destination_get_post),
    path('get-delete-destination/<int:destination_id>', views.destination_get_delete),
    path('get-destination-account/<str:account_id>', views.destination_get_account),
    path('server/incoming_data', views.handle_data),

    


]