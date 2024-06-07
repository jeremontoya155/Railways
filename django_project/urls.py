from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('blog.urls')),
    path('api/', include('tasks.urls')),
    path('', include('home.urls')),
    path('excel/', include('excel_app.urls')),
    path('myapp/', include('myapp.urls')),  # Incluir las rutas de myapp
    path('accounts/login/', LoginView.as_view(), name='login'),  # URL de inicio de sesión
    path('accounts/logout/', LogoutView.as_view(next_page='/accounts/login/?next=/myapp/'), name='logout'),
]
