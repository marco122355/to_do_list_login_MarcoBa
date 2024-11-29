from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDeleteView, CustomLoginView, RegisterPage, TaskReorder
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import crypto_prices_view
cv
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),
    path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),
    path('crypto-prices/', crypto_prices_view, name='crypto-prices'),

     # URL temporal para probar crypto_prices_view
    path('crypto-prices/', crypto_prices_view, name='crypto-prices'),  # Nueva línea
]
