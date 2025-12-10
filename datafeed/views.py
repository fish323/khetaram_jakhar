from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Workmodels, Strengthmodel, Equipmentmodel

# --- Display Views ---

def workexpview(request):
    # Remove .values() to pass full Model Objects. Now properties will work.
    mywork = Workmodels.objects.all().order_by('order')
    template = loader.get_template('workexperience.html')
    context = {
        'mywork': mywork,
    }
    return HttpResponse(template.render(context, request))


def strengthview(request):
    # Added .order_by('order')
    mywork = Strengthmodel.objects.all().order_by('order').values()
    template = loader.get_template('strength.html')
    context = {
        'mywork': mywork,
    }
    return HttpResponse(template.render(context, request))

def equipmentview(request):
    # Added .order_by('order')
    mywork = Equipmentmodel.objects.all().order_by('order').values()
    template = loader.get_template('equipment.html')
    context = {
        'mywork': mywork,
    }
    return HttpResponse(template.render(context, request))

# --- Reorder Logic Views ---

@csrf_exempt
def reorder_equipment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            order_list = data.get('order', [])
            for index, item_id in enumerate(order_list):
                Equipmentmodel.objects.filter(id=item_id).update(order=index)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'invalid method'})

@csrf_exempt
def reorder_work(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            order_list = data.get('order', [])
            for index, item_id in enumerate(order_list):
                Workmodels.objects.filter(id=item_id).update(order=index)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'invalid method'})

@csrf_exempt
def reorder_strength(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            order_list = data.get('order', [])
            for index, item_id in enumerate(order_list):
                Strengthmodel.objects.filter(id=item_id).update(order=index)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'invalid method'})