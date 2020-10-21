from django.urls import path


from. import views
urlpatterns = [
    path('upload', views.upload_file, name="upload_pdf"),
    path('connection', views.connection, name="connection"),
    path('disconnection', views.disconnection, name="disconnection"),
    path('workshop', views.workshop, name="workshop"),
    path('detailWorkshop/<int:id_workshop>/<int:id_client>',
         views.detail_workshop, name="detailWorkshop"),
    path('contactMail', views.contact_email, name="mail_contact"),
    path('register', views.register, name="register"),
    path('espace', views.my_espace, name="espace"),
    path('inscribe/<int:id_workshop>/<int:id_client>',
         views.inscribe_workshop, name="inscribe"),
    path('unsubscribe/<int:id_workshop>/<int:id_client>',
         views.unsubscribe_workshop, name="unsubscribe"),
    path('registrationValid/<str:username>/<str:email>',
         views.registration_valid, name="registrationValid"),
    path('deleteAccount', views.delete_account, name="delete_account"),
    path('resetPassword', views.reset_password, name="reset_password"),
    path('resetPasswordStep/<str:username>/<str:adresse_mail>',
         views.reset_password_step_2, name="resset_password_step"),
]
