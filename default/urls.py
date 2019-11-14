from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import picture_add, picture_delete, test, user_login, verify_view, user_register, cooker_register, Home, \
    add_food, ProfileUser, SettingUser, order, AllFood, orders, close_foods, close_foods_helper, detail, \
    setting_social, changepassword, like_view, time_day, search, Delete

urlpatterns = [
    path('', Home, name='index'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user_login/', user_login, name='login'),
    path('profile/<int:id>', ProfileUser, name='profile'),
    path('user_register/', user_register, name='user_register'),
    path('cooker_register/', cooker_register, name='cooker_register'),
    path('verify/<str:token>/<int:id>/', verify_view, name='verify_view'),
    path('user_register/', user_register, name='user_register'),
    path('cooker_register/', cooker_register, name='cooker_register'),
    path('add/', add_food.as_view(), name="add-food"),
    path('pic-add/', picture_add, name='picture-add'),
    path('pic-delete/', picture_delete, name='picture-delete'),
    path('detail/<int:id>/', detail, name="detail-food"),
    path('test/', test, name="test"),
    path('settings/', SettingUser, name="settings"),
    path('social/', setting_social, name="social"),
    path('password/', changepassword, name="password"),
    path('like/', like_view, name="like-view"),
    path('test/',test,name='test'),
    path('all/', AllFood, name="all-food"),
    path('order/<int:id>',order, name="order"),
    path('orders/<int:id>',orders, name="orders"),
    path('close_foods/',close_foods, name='close_food'),
    path('close_foods_helper/',close_foods_helper, name='close_foods_helper'),
    path('category/', time_day, name="category"),
    path('search/<str:str>/', search, name="search"),
    path('delete/<int:pk>', Delete.as_view(), name="delete"),

    # url(r'^search/$',search, name='search_view')
]
