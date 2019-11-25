from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.DebtorsListView.as_view(), name='debtors-list'),
    path('createdebtor/', views.DebtorCreateView.as_view(), name='debtors-create'),
    path('deletedebtor/<int:id>', views.deletedebtor, name='debtors-delete'),
    path('debtor/<int:pk>', views.DebtorDetailView.as_view(), name='debtor'),
    path('action_sendmail/<int:id>', views.action_sendmail, name='action-sendmail'),
]
    