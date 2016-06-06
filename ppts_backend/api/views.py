from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import re,base64,hashlib
from datetime import timedelta, datetime
# Create your views here.
from .models import GuardCredentials,GuardSession,LocationDetails,AdminOfficer,AdminOfficerToken
from .serializers import LocationDetailsSerializer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data,session_data):
        content = JSONRenderer().render(data)
        super(JSONResponse, self).__init__(content)
        self['Content-Type'] = 'application/json'
        self['Access-Control-Expose-Headers'] = 'session_id'
        self['session_id'] = session_data

# Class based login view
class GuardLogin(View):

	def post(self,request):
		credentials = {}
		credentials = request.META['HTTP_AUTHORIZATION']
		lattitude = request.META['HTTP_LATTITUDE']
		longitude = request.META['HTTP_LONGITUDE']
		timestamp = request.META['HTTP_TIMESTAMP']
		data = str(credentials)
		data = data.replace('Basic ','')
		data = base64.b64decode(data)
		reg=re.compile('(\w+)[:=] ?"?(\w+)"?')
		data = dict(reg.findall(data))
		for key in data:
			username = key
		password = data[username]
		try:
			guard = GuardCredentials.objects.get(username=username)
			password = hashlib.sha224(password).hexdigest()
			if str(guard.password) == password : 
				g_session = GuardSession()
				g_session.guard_id = guard
				g_session.active = True
				g_session.login_timestamp = timestamp
				logouttime = datetime.strptime(str(timestamp),'%Y-%m-%d %H:%M:%S')
				logouttime = logouttime + timedelta(0,0,0,0,0,12,0)
				g_session.logout_timestamp = logouttime.strftime('%Y-%m-%d %H:%M:%S') # default timeout of 12 hours
				g_session.save()
				session_id = g_session.token
				locationdet = LocationDetails()
				locationdet.token = g_session
				locationdet.lattitude = float(lattitude)
				locationdet.longitude = float(longitude)
				locationdet.timestamp = timestamp
				locationdet.save()
				return JSONResponse({'done' : 'ok'},session_id)
			else : 
				return JSONResponse({'error' : 'Password'},'')
		except GuardCredentials.DoesNotExist :
			return JSONResponse({'error' : 'Username'},'')

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(GuardLogin, self).dispatch(*args, **kwargs)

# Class based recieve cordinates view
class RecieveCordinates(View):

	def post(self,request):
		token = request.META['HTTP_TOKEN']
		lattitude = request.META['HTTP_LATTITUDE']
		longitude = request.META['HTTP_LONGITUDE']
		timestamp = request.META['HTTP_TIMESTAMP']
		try:
			session = GuardSession.objects.get(token=token)
			if( session.active == True ):				
				locationdet = LocationDetails()
				locationdet.token = session
				locationdet.lattitude = float(lattitude)
				locationdet.longitude = float(longitude)
				locationdet.timestamp = timestamp
				locationdet.save()
				return JSONResponse({'ok':'done'},'')
			else:
				return JSONResponse({'error':'Inactive Token'},'')
		except GuardSession.DoesNotExist:
			return JSONResponse({'error' : 'Invalid Session'},'')

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(RecieveCordinates, self).dispatch(*args, **kwargs)


# Class based logout view
class GuardLogout(View):

	def post(self,request):
		token = request.META['HTTP_TOKEN']
		lattitude = request.META['HTTP_LATTITUDE']
		longitude = request.META['HTTP_LONGITUDE']
		timestamp = request.META['HTTP_TIMESTAMP']
		try:
			session = GuardSession.objects.get(token=token)
			if ( session.active == True ):
				locationdet = LocationDetails()
				locationdet.token = session
				locationdet.lattitude = float(lattitude)
				locationdet.longitude = float(longitude)
				locationdet.timestamp = timestamp
				locationdet.save()
				GuardSession.objects.filter(token=token).update(active=False)
				return JSONResponse({'ok':'done'},'')
			else:
				return JSONResponse({'error':'Inactive Token'},'')
		except GuardSession.DoesNotExist:
			return JSONResponse({'error' : 'Invalid Session'},'')

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(GuardLogout, self).dispatch(*args, **kwargs)


# Class based offficer login view
class OfficerLogin(View):

	def post(self,request):
		credentials = {}
		credentials = request.META['HTTP_AUTHORIZATION']
		timestamp = request.META['HTTP_TIMESTAMP']
		data = str(credentials)
		data = data.replace('Basic ','')
		data = base64.b64decode(data)
		reg=re.compile('(\w+)[:=] ?"?(\w+)"?')
		data = dict(reg.findall(data))
		for key in data:
			username = key
		password = data[username]
		try:
			officer = AdminOfficer.objects.get(username=username)
			password = hashlib.sha224(password).hexdigest()
			if str(officer.password) == password : 
				token = AdminOfficerToken()
				token.officer = officer
				token.active = True
				token.login_timestamp = timestamp
				logouttime = datetime.strptime(str(timestamp),'%Y-%m-%d %H:%M:%S')
				logouttime = logouttime + timedelta(0,0,0,0,0,12,0)
				token.logout_timestamp = logouttime.strftime('%Y-%m-%d %H:%M:%S') # default timeout of 12 hours
				token.save()
				session_id = token.token
				return JSONResponse({'done' : 'ok'},session_id)
			else : 
				return JSONResponse({'error' : 'Password'},'')
		except AdminOfficer.DoesNotExist :
			return JSONResponse({'error' : 'Username'},'')

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(OfficerLogin, self).dispatch(*args, **kwargs)

# Class based officer logout
class OfficerLogout(View):

	def post(self,request):
		token = request.META['HTTP_TOKEN']
		timestamp = request.META['HTTP_TIMESTAMP']
		try:
			session = AdminOfficerToken.objects.get(token=token)
			if ( session.active == True ):
				AdminOfficerToken.objects.filter(token=token).update(logout_timestamp=timestamp)
				AdminOfficerToken.objects.filter(token=token).update(active=False)
				return JSONResponse({'ok':'done'},'')
			else:
				return JSONResponse({'error':'Inactive Token'},'')
		except GuardSession.DoesNotExist:
			return JSONResponse({'error' : 'Invalid Session'},'')

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(OfficerLogout, self).dispatch(*args, **kwargs)

# Class based officer get cordinates
class GetCordinates(View):

	def post(self,request):
		officerertoken = request.META['HTTP_AUTHTOKEN']
		guardtoken = request.META['HTTP_GUARDTOKEN']
		try:
			officer = AdminOfficerToken.objects.get(token = officerertoken)
			if ( officer.active == True ):
				try:
					gaurd = GuardSession.objects.get(token = guardtoken)
					locationdetails = LocationDetails.objects.all().filter(token = gaurd)
					serializers = LocationDetailsSerializer(locationdetails,many=True)
					return JSONResponse( serializers.data , '' )
				except GuardSession.DoesNotExist :
					return JSONResponse({'error':'Invalid Guard Token'})
			else : 
				return JSONResponse({'error':'Inactive Token'},'')
		except AdminOfficerToken.DoesNotExist :
			return JSONResponse({'error':'Invalid Officer Token'},'')

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(GetCordinates, self).dispatch(*args, **kwargs)

