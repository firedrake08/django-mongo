from django.http import HttpResponse, JsonResponse
import json
from .models import Lead

def add_lead(request):
    try:
        data = json.loads(request.body)
        lead = Lead(**data)
        lead.save()
        return HttpResponse('Lead added')
    except Exception as e:
        return HttpResponse(str(e), status=400)

def get_all_leads(request):
    leads = Lead.objects.all()
    data = [{'id': str(lead.id), 'first_name': lead.first_name, 'last_name': lead.last_name, 'age': lead.age} for lead in leads]
    return JsonResponse(data, safe=False)

def update_lead(request, lead_id):
    try:
        data = json.loads(request.body)
        Lead.objects(id=lead_id).update_one(**data)
        return HttpResponse('Lead updated')
    except Exception as e:
        return HttpResponse(str(e), status=400)

def delete_lead(request, lead_id):
    try:
        Lead.objects(id=lead_id).delete()
        return HttpResponse('Lead deleted')
    except Exception as e:
        return HttpResponse(str(e), status=400)
