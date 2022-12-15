from django.urls import path
from . import views, login_views

urlpatterns = [
    # This is our views urls
    # This is home page urls

    path('', views.start, name='start' ),
    path('home/', views.home, name='home' ),
    path('go-to-admin/', views.go_to_admin, name='admin' ),

    # This is explore page urls
    path('explore/', views.explore, name='explore' ),
    path('explore/delete-book/<int:id>', views.delete_book, name='delete-book' ),
    path('explore/add-book/', views.add_book, name='add-book' ),
    path('explore/update-book/<int:id>', views.update_book, name='update-book' ),
    path('explore/filter/<str:id>', views.explore_filter, name='explore-filter' ),
    path('explore/add-book-to-userlist/<int:id>', views.add_book_to_userlist, name='add-book-to-userlist' ),
    path('explore/no-permission/', views.no_permission, name='no-permission' ),
     
    #This is user table page urls
    path('user-table/', views.user_table, name='user-table' ),
    path('user-table/delete-from-userlist/<int:id>', views.delete_from_userlist, name='delete-from-userlist' ),
    path('user-table/update-status/<int:id>/<str:status>', views.update_status, name='update-status'),
    path('user-table/filter/<str:filter>', views.user_table_filter, name='user-table-filter' ),

    # This is our login_views urls
    # This is our views urls
    path('accounts/register/', login_views.register_user, name='register' ),
    path('accounts/login/', login_views.login_user, name='login' ),
    path('accounts/logout/', login_views.logout_user, name='logout' ),
    path('accounts/update-profile/', login_views.update_user_profile, name='Update-profile' ),
    path('accounts/delete-user/<int:id>', login_views.delete_user, name='delete-user' ),
    
]

