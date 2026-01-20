from django.urls import path
from . import views

urlpatterns = [
    # Main Dashboard for the user
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # The UI page where you input messages for the CLI
    path('remote/', views.remote_input_page, name='remote_input'),

    # The logic endpoint for the laptop bridge (NFC scans)
    # Your bridge posts to http://192.168.197.11:8000/verify/
    path('verify/', views.verify_access, name='verify_access'),

    # The logic endpoint for the Appliance CLI
    # Your CLI polls http://192.168.197.11:8000/appliance-msg/
    path('appliance-msg/', views.send_to_appliance, name='appliance_msg'),

    # Utility endpoints
    path('clear_message/', views.clear_message, name='clear_message'),
    path('unlock-cheat/', views.reset_system, name='unlock_cheat'),
]
