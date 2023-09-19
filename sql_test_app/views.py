from django.shortcuts import render
from .models import *
from django.http import JsonResponse

# cursor
from django.db import connection

# methods
def update_sql():
     with connection.cursor() as cursor:
            cursor.execute("UPDATE sql_test_app_personel SET name = 'Halil' WHERE id = 5")
            # row = cursor.fetchone()
            return True
     
def create_sql():
     with connection.cursor() as cursor:
            print("cur:", cursor)
            cursor.execute("INSERT INTO sql_test_app_personel (name, lastname, salary, role) VALUES ('Burak', 'Işık', 4000, 'Mühendis');")
            # row = cursor.fetchone()
            return True

def delete_sql():
        with connection.cursor() as cursor:
            print("cur:", cursor)
            cursor.execute("DELETE FROM sql_test_app_personel WHERE id = 4")
            # row = cursor.fetchone()
            return True
    


# Create your views here.
def return_all_personel(request):
    response = {}
    personels = Personel.objects.raw("SELECT * FROM sql_test_app_personel")

    for personel in personels:

        print("ALL SQL DATA:", personel)

    personel = Personel.objects.raw("SELECT id FROM sql_test_app_personel WHERE id = 1")
   
    for data in personel:
        print("spesifik veri:", data)




    response['message'] = "Terminal konsoluna bak"
    return JsonResponse(response)
    


def remove_person(request):
    response = {}
    delete_sql()

    response['message'] = "deleted"
    return JsonResponse(response)


def create_person(request):
    response = {}
    create_sql()
    response['message'] = "created"

    return JsonResponse(response)


def update_person(request):
    response = {}
    update_sql()
    response['message'] = "updated"

    return JsonResponse(response)