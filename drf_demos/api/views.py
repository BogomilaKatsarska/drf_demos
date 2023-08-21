from abc import ABC

from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import serializers
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.views import APIView

from drf_demos.api.models import Employee, Department


class ShortEmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class DepartmentSerializer(ModelSerializer):
    employee_set = ShortEmployeeSerializer(many=True)

    class Meta:
        model = Department
        fields = '__all__'


class ShortDepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class EmployeeSerializer(ModelSerializer):
    department = ShortDepartmentSerializer()

    class Meta:
        model = Employee
        fields = '__all__'


class DemoOneSerializer(Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    key = serializers.CharField()
    value = serializers.IntegerField()

#Server-side rendering: the result is HTML
class EmployeesListView(ListView):
    model = Employee
    template_name = ''


class DepartmentsListAPIView(ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


#ListAPIView // ListCreateAPIView // HyperlinkedModelSerializer
#JSON Serialization: parse models into JSON
class EmployeesListApiView(ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class DemoSerializer(Serializer):
    employees = ShortEmployeeSerializer(many=True)
    departments = ShortDepartmentSerializer(many=True)


class DemoAPIView(APIView):
    def get(self, request):
        body = {
            'employees': Employee.objects.all(),
            'departments': Department.objects.all()
        }

        serializer = DemoSerializer
