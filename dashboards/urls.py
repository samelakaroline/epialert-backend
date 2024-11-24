from django.urls import path
from .views import WeeklyAlertsPieChartView, WeeklyAlertsChartView

urlpatterns = [
    path('unresolved-alerts-pie-chart/', WeeklyAlertsPieChartView.as_view(), name='unresolved-alerts-pie-chart'),
    path('weekly-alerts-chart/', WeeklyAlertsChartView.as_view(), name='weekly-alerts-chart'),
]
