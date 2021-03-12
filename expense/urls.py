from django.urls import path

from expense.views import (CategoryCreateView, CategoryUpdateView,
                           ExpenseCreateView, ExpenseDeleteView,
                           ExpenseUpdateView, MonthView, TodayView, WeekView)

urlpatterns = [
    path('create/', ExpenseCreateView.as_view(), name='expense-create'),
    path('<int:pk>/update/', ExpenseUpdateView.as_view(), name='expense-update'),
    path('<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense-delete'),

    path('category/create/', CategoryCreateView.as_view(), name='category-create'),
    path('category/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),

    path('<int:year>/<str:month>/<int:day>/', TodayView.as_view(), name="archive_day"),
    path('<int:year>/<int:week>/week/', WeekView.as_view(), name="archive_week"),
    path('<int:year>/<str:month>/', MonthView.as_view(), name="archive_month"),
]