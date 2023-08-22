from abc import ABC

from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import serializers
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

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

    def create(self, validated_data):
        department_name = validated_data.pop('department').get('name')
        try:
            department = Department.objects.filter(name=department_name).get()
        except Department.DoesNotExist:
            department = Department.objects.create(name=department_name)

        return Employee.objects.create(**validated_data, department=department)


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

    def get_queryset(self):
        department_id = self.request.query_params.get('department_id')
        queryset = self.queryset
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        return queryset.all()


class NameSerializers(serializers.Serializer):
    name = serializers.CharField()


class DemoSerializer(Serializer):
    employees = ShortEmployeeSerializer(many=True)
    employees_count = serializers.IntegerField()
    departments = ShortDepartmentSerializer(many=True)
    first_department = serializers.CharField()
    department_names = NameSerializers(many=True)


class DemoAPIView(APIView):
    def get(self, request):
        body = {
            'employees': Employee.objects.all(),
            'employees_count':Employee.objects.count(),
            'departments': Department.objects.all(),
            'first_department': Department.objects.first(),
            'department_names': Department.objects.all(),
        }

        serializer = DemoSerializer(body)
        #Not the same as HttpResponse, this comes from Django. Below comes from DRF
        return Response(serializer.data)


#viewsets - gives all CRUD operations
#they are registered to urls as 'routers'

class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer