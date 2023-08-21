from django.urls import path

from drf_demos.api.views import EmployeesListApiView, DepartmentsListAPIView, DemoAPIView

urlpatterns = (
    path('employees/', EmployeesListApiView.as_view(), name='api list employees'),
    path('departments/', DepartmentsListAPIView.as_view(), name='api list departments'),
    path('demo/', DemoAPIView.as_view(), name='demo view'),
)