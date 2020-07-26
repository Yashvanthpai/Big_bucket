from django.contrib import admin
from django.conf.urls import url,include
from firstapp import views
from django.contrib.auth.views import LoginView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView,PasswordChangeView,PasswordChangeDoneView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) +[
    url(r'^register/$',views.registerview,name="register"),
    url(r'^login/',LoginView.as_view(template_name='login_page.html'),name='login'),
    url(r'^homepage/$',views.login_homeview,name='homepage'),
    url(r'^homepage/(?P<id>\d+)/$',views.product_detail_view),
    url(r'User/(?P<id>\d+)/$',views.user_detail_view),
    url(r'cart_add/$',views.cart_add,name='cartadd'),
    url(r'cart_remove/$',views.cart_remove,name='cart_remove'),
    url(r'cart_view/$',views.cart_view,name='cart_view'),
    url(r'catogories/$',views.catogories,name='catogories'),
    url(r'cart_options/$',views.cart_options,name='cart_options'),
    url(r'remove_product/$',views.remove_product,name='remove_product'),

    url(r'create_order/$',views.create_order,name='create_order'),
    url(r'cancel_order/$',views.cancell_order,name='cancel_order'),
    url(r'product_sold/$',views.sell_product,name='product_sold'),





    url(r'logout/$',views.logoutviews,name='logout'),
    url(r'^password_reset/$', PasswordResetView.as_view(template_name='Registration/password_reset_form.html'), name='password_reset'),
    url(r'^password_reset/done/$', PasswordResetDoneView.as_view(template_name='Registration/password_reset_done.html'), name='password_reset_done'),
    url(r'^password_reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        PasswordResetConfirmView.as_view(template_name='Registration/password_reset_confirm.html'), name='password_reset_confirm'),
    url(r'^password_reset/compleate$', LoginView.as_view(template_name='login_page.html'), name='password_reset_complete'),
    url(r'^password_change/$',PasswordChangeView.as_view(template_name='password_change_form.html',success_url='/homepage/'), name='password_change'),
    url(r'^',views.indexview,name='appstartpoint'),
     
] 
