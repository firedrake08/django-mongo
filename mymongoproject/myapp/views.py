from django.http import HttpResponse, JsonResponse
import json
from .models import Lead, Activity, User
from mongoengine.errors import DoesNotExist
from mongoengine import NotUniqueError


def add_lead(request):
    try:
        data = json.loads(request.body)
        # Validate that the provided source is one of the allowed choices, if provided
        if 'source' in data and data['source'] not in Lead.SOURCE_CHOICES:
            return HttpResponse('Invalid source provided', status=400)
        # Ensure the required 'source' field is present if it's not already validated
 # This check might be redundant if the model field is required and has choices
 # if 'source' not in data or data['source'] == '':
 # return HttpResponse('Invalid source provided', status=400)
        lead = Lead(**data)
        lead.save()
        return JsonResponse({
            'id': str(lead.id), 'first_name': lead.first_name, 'last_name': lead.last_name,
            'age': lead.age, 'phone': lead.phone, 'status': lead.status, 'source': lead.source
        })
    except Exception as e:
        return HttpResponse(str(e), status=400)


def get_all_leads(request):
    filters = {}
    if 'first_name' in request.GET:
        filters['first_name__icontains'] = request.GET['first_name']
    if 'last_name' in request.GET:
        filters['last_name__icontains'] = request.GET['last_name']
    if 'age' in request.GET:
        filters['age'] = int(request.GET['age'])
    if 'phone' in request.GET:
        filters['phone__icontains'] = request.GET['phone']
    leads = Lead.objects(**filters)
    data = [{'id': str(lead.id), 'first_name': lead.first_name, 'last_name': lead.last_name, 'age': lead.age, 'phone': lead.phone, 'status': lead.status, 'source': lead.source} for lead in leads]
    return JsonResponse(data, safe=False)

def update_lead(request, lead_id):
    try:
        data = json.loads(request.body)
        if 'status' in data:
            new_status = data['status']
            if new_status in Lead.STATUS_CHOICES:
                Lead.objects(id=lead_id).update(set__status=new_status)
                lead = Lead.objects.get(id=lead_id)
                return JsonResponse({'id': str(lead.id), 'first_name': lead.first_name, 'last_name': lead.last_name, 'age': lead.age, 'phone': lead.phone, 'status': lead.status, 'source': lead.source})
            else:
                return HttpResponse('Invalid status provided', status=400)
        return HttpResponse('Only status can be updated', status=400)
    except Exception as e:
 # Catch other exceptions during update
        return HttpResponse(str(e), status=400)

def delete_lead(request, lead_id):
    try:
        Lead.objects(id=lead_id).delete()
        return HttpResponse('Lead deleted')
    except Exception as e:
        return HttpResponse(str(e), status=400)

def get_lead_by_id(request, lead_id):
    try:
        lead = Lead.objects.get(id=lead_id)
        data = {'id': str(lead.id), 'first_name': lead.first_name, 'last_name': lead.last_name, 'age': lead.age, 'phone': lead.phone, 'status': lead.status, 'source': lead.source}
        return JsonResponse(data)
    except DoesNotExist:
        return HttpResponse('Lead not found', status=404)
    except Exception as e:
        return HttpResponse(str(e), status=400)

def get_lead_activities(request, lead_id):
    try:
        Lead.objects.get(id=lead_id) # Check if the lead exists
        activities = Activity.objects(lead=lead_id)
        data = [{'content': activity.content, 'timestamp': str(activity.timestamp)} for activity in activities]
        return JsonResponse(data, safe=False)
    except DoesNotExist:
        return HttpResponse('Lead not found', status=404)
    except Exception as e:
        return HttpResponse(str(e), status=400)

def add_lead_activity(request, lead_id):
    try:
        data = json.loads(request.body)
        lead = Lead.objects.get(id=lead_id)
        activity = Activity(content=data['content'], lead=lead)
        activity.save()
        return HttpResponse('Activity added')
    except Exception as e:
        return HttpResponse(str(e), status=400)


def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            if not email or not password:
                return JsonResponse({'error': 'Email and password are required'}, status=400)

            # Check if a user with this email already exists
            if User.objects(email=email).first():
                return JsonResponse({'error': 'Email address already in use'}, status=400)

            user = User(email=email)
            user.set_password(password)  # Hash the password
            user.save()  # Save the user to the database
            return JsonResponse({'message': 'User registered successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
