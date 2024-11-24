from django.urls import path
from .views import LocalAlertsView, GlobalAlertsView, CombinedAlertsView, AlertsMetricsView, AlertsListView

urlpatterns = [
    path('local/', LocalAlertsView.as_view(), name='local-alerts'),
    path('global/', GlobalAlertsView.as_view(), name='global-alerts'),
    path('combined/', CombinedAlertsView.as_view(), name='combined-alerts'),
    path('metrics/', AlertsMetricsView.as_view(), name='alerts-metrics'),
    path('list/', AlertsListView.as_view(), name='alerts-list'),
]
