from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import re,base64,hashlib,json
from datetime import timedelta, datetime
from datetime import time as Time
# Create your views here.
from .models import GuardCredentials,GuardSession,LocationDetails,AdminOfficer,AdminOfficerToken
from .serializers import LocationDetailsSerializer,GuardCredentialsSerializer,GuardSessionSerializer

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

## Guard Views

# Class based login view

class GuardLogin(View):

	def post(self,request):
		credentials = {}
		credentials = request.META['HTTP_AUTHORIZATION']
		lattitude = request.META['HTTP_LATTITUDE']
		longitude = request.META['HTTP_LONGITUDE']
		date = request.META['HTTP_CDATE']
		time = request.META['HTTP_TIME']
		# remove it for changes
#		timestamp = request.META['HTTP_TIMESTAMP']
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
				g_session.logindate = date
				g_session.logintime = time
				comptime = datetime.strptime(time, "%H:%M:%S").time()
				if  comptime >= datetime.Time(12,0,0) :
					testdate = datetime.strptime(str(date),'%Y-%m-%d').date()
					testdate = testdate + timedelta(1,0,0,0,0,0,0)
					g_session.logoutdate = testdate.strftime('%Y-%m-%d')
					testtime = datetime.strptime(str(time),'%H:%M:%S')
					testtime = testtime + timedelta(0,0,0,0,0,12,0)
					g_session.logouttime = testtime.strftime('%H:%M:%S')					
				else : 
					g_session.logoutdate = date
					testtime = datetime.strptime(str(time),'%H:%M:%S')
					testtime = testtime + timedelta(0,0,0,0,0,12,0)
					g_session.logouttime = testtime.strftime('%H:%M:%S')
				#remove it for changes
				#g_session.login_timestamp = timestamp
				#logouttime = datetime.strptime(str(timestamp),'%Y-%m-%d %H:%M:%S')
				#logouttime = logouttime + timedelta(0,0,0,0,0,12,0)
				#g_session.logout_timestamp = logouttime.strftime('%Y-%m-%d %H:%M:%S') # default timeout of 12 hours
				g_session.save()
				session_id = g_session.token
				locationdet = LocationDetails()
				locationdet.token = g_session
				locationdet.lattitude = float(lattitude)
				locationdet.longitude = float(longitude)
				locationdet.arivaldate = date
				locationdet.arivaltime = time
				# changed
				#locationdet.timestamp = timestamp
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
		date = request.META['HTTP_CDATE']
		time = request.META['HTTP_TIME']
		#changed
		#timestamp = request.META['HTTP_TIMESTAMP']
		try:
			session = GuardSession.objects.get(token=token)
			if( session.active == True ):				
				locationdet = LocationDetails()
				locationdet.token = session
				locationdet.lattitude = float(lattitude)
				locationdet.longitude = float(longitude)
				locationdet.arivaldate = date
				locationdet.arivaltime = time
				#changed
				#locationdet.timestamp = timestamp
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
		date = request.META['HTTP_CDATE']
		time = request.META['HTTP_TIME']	
		#changed
		#timestamp = request.META['HTTP_TIMESTAMP']
		try:
			session = GuardSession.objects.get(token=token)
			if ( session.active == True ):
				locationdet = LocationDetails()
				locationdet.token = session
				locationdet.lattitude = float(lattitude)
				locationdet.longitude = float(longitude)
				locationdet.arivaldate = date
				locationdet.arivaltime = time
				#changed
				#locationdet.timestamp = timestamp
				locationdet.save()
				GuardSession.objects.filter(token=token).update(active=False)
				GuardSession.objects.filter(token=token).update(logoutdate=date)
				GuardSession.objects.filter(token=token).update(logouttime=time)
				return JSONResponse({'ok':'done'},'')
			else:
				return JSONResponse({'error':'Inactive Token'},'')
		except GuardSession.DoesNotExist:
			return JSONResponse({'error' : 'Invalid Session'},'')

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(GuardLogout, self).dispatch(*args, **kwargs)

## Officer views

# Class based offficer login view

class OfficerLogin(View):

	def post(self,request):
		credentials = {}
		credentials = request.META['HTTP_AUTHORIZATION']
		date = request.META['HTTP_CDATE']
		time = request.META['HTTP_TIME']	
		#changed
		#timestamp = request.META['HTTP_TIMESTAMP']
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
				token.logindate = date
				token.logintime = time
				comptime = datetime.strptime(str(time),"%H:%M:%S").time()
				if ( comptime >= Time(12,0,0) ):
					testdate = datetime.strptime(str(date),'%Y-%m-%d').date()
					testdate = testdate + timedelta(1,0,0,0,0,0,0)
					token.logoutdate = testdate.strftime('%Y-%m-%d')
					testtime = datetime.strptime(str(time),'%H:%M:%S')
					testtime = testtime + timedelta(0,0,0,0,0,12,0)
					token.logouttime = testtime.strftime('%H:%M:%S')					
				else : 
					token.logoutdate = date
					testtime = datetime.strptime(str(time),'%H:%M:%S')
					testtime = testtime + timedelta(0,0,0,0,0,12,0)
					token.logouttime = testtime.strftime('%H:%M:%S')
				#changed
				#token.login_timestamp = timestamp
				#logouttime = datetime.strptime(str(timestamp),'%Y-%m-%d %H:%M:%S')
				#logouttime = logouttime + timedelta(0,0,0,0,0,12,0)
				#token.logout_timestamp = logouttime.strftime('%Y-%m-%d %H:%M:%S') # default timeout of 12 hours
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
		date = request.META['HTTP_CDATE']
		time = request.META['HTTP_TIME']
		#changed
		#timestamp = request.META['HTTP_TIMESTAMP']
		try:
			session = AdminOfficerToken.objects.get(token=token)
			if ( session.active == True ):
				AdminOfficerToken.objects.filter(token=token).update(logoutdate=date)
				AdminOfficerToken.objects.filter(token=token).update(logouttime=time)
				#changed
				#AdminOfficerToken.objects.filter(token=token).update(logout_timestamp=timestamp)
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

#Class based view for returning name recomendation

class NameRecomendation(View):

	def post(self,request):
		officerertoken = request.META['HTTP_TOKEN']
		firstname = request.META['HTTP_FIRSTNAME']
		lastname = request.META['HTTP_LASTNAME']
		try:
			officer = AdminOfficerToken.objects.get(token = officerertoken)
			if ( officer.active == True ) :
				if ( lastname == ' ' ) :
					guards = GuardCredentials.objects.filter(first_name__istartswith=firstname)
					serializers = GuardCredentialsSerializer(guards,many=True)
					return JSONResponse(serializers.data,'')
				else:
					guards = GuardCredentials.objects.filter(first_name__istartswith=firstname,last_name__istartswith=lastname)
					serializers = GuardCredentialsSerializer(guards,many=True)
					return JSONResponse(serializers.data,'')
			else:
				return JSONResponse({'error':'Inactive Token'},'')
		except AdminOfficerToken.DoesNotExist:
			return JSONResponse({'error':'Invalid Officer Token'},'')

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(NameRecomendation, self).dispatch(*args, **kwargs)

#Class based view for last location

class LastLocation(View):

	def post(self,request):
		officerertoken = request.META['HTTP_TOKEN']
		guard_id = request.META['HTTP_GUARD']
		try:
			officer = AdminOfficerToken.objects.get(token = officerertoken)
			if ( officer.active == True ) :
				guard_id = int(guard_id)
				try:
					guard = GuardCredentials.objects.get(guard_id=guard_id)
					g_session = GuardSession.objects.filter(guard_id=guard).last()
					location = LocationDetails.objects.filter(token=g_session).last()
					serializers = LocationDetailsSerializer(location)
					return JSONResponse(serializers.data,'')
				except GuardCredentials.DoesNotExist:
					return JSONResponse({'error' : 'Invalid Guard'},'')
			else:
				return JSONResponse({'error':'Inactive Token'},'')
		except AdminOfficerToken.DoesNotExist:
			return JSONResponse({'error':'Invalid Officer Token'},'')

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(LastLocation, self).dispatch(*args, **kwargs)


#Class based Last query function view

class LastSession(View):

	def post(self,request):
		officerertoken = request.META['HTTP_TOKEN']
		guard_id = request.META['HTTP_GUARD']
		try:
			officer = AdminOfficerToken.objects.get(token = officerertoken)
			if ( officer.active == True ) :
				guard_id = int(guard_id)
				try:
					guard = GuardCredentials.objects.get(guard_id=guard_id)
					g_session = GuardSession.objects.filter(guard_id=guard).last()
					serializers = GuardSessionSerializer(g_session)
					return JSONResponse(serializers.data,'')
				except GuardCredentials.DoesNotExist:
					return JSONResponse({'error' : 'Invalid Guard'},'')
			else:
				return JSONResponse({'error':'Inactive Token'},'')
		except AdminOfficerToken.DoesNotExist:
			return JSONResponse({'error':'Invalid Officer Token'},'')

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(LastSession, self).dispatch(*args, **kwargs)

#Class based login logout based session query

class SessionTimestampQuery(View):

	def post(self,request):
		officertoken = request.META['HTTP_TOKEN']
		querydata = request.body
		querydata = querydata.replace('\"','"')
		querydata = querydata.replace("\n","")
		querydata = json.loads(querydata)
		try:
			officer = AdminOfficerToken.objects.get(token = officertoken)
			if ( officer.active == True ) :
				queryparameters = {}
				if ( querydata['login']['data'] == '1' ):
					queryparameters['logindate__gte'] = str( querydata['login']['logindatestart'] )
					queryparameters['logindate__lte'] = str( querydata['login']['logindateend'] )
					queryparameters['logintime__gte'] = str( querydata['login']['logintimestart'] )
					queryparameters['logintime__lte'] = str( querydata['login']['logintimeend'] )
				else:
					pass
				if ( querydata['logout']['data'] == '1' ):
					queryparameters['logoutdate__gte'] = str( querydata['logout']['logoutdatestart'] )
					queryparameters['logoutdate__lte'] = str( querydata['logout']['logoutdateend'] )
					queryparameters['logouttime__gte'] = str( querydata['logout']['logouttimestart'] )
					queryparameters['logouttime__lte'] = str( querydata['logout']['logouttimeend'] )
				else:
					pass
				if ( querydata['guard']['data'] == '1' ):
					queryparameters['guard_id'] = int( querydata['guard']['guard_id'] )
				else:
					pass
				sessions = GuardSession.objects.filter(**queryparameters)
				serializers = GuardSessionSerializer(sessions,many=True)
				return  JSONResponse(serializers.data,'')
			else:
				return JSONResponse({'error':'Inactive Token'},'')
		except AdminOfficerToken.DoesNotExist:
			return JSONResponse({'error':'Invalid Officer Token'},'')

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(SessionTimestampQuery, self).dispatch(*args, **kwargs)

#Class based view for position based query

class LocationQuery(View):

	def post(self,request):
		officertoken = request.META['HTTP_TOKEN']
		querydata = request.body
		querydata = querydata.replace('\"','"')
		querydata = querydata.replace("\n","")
		querydata = json.loads(querydata)
		try:
			officer = AdminOfficerToken.objects.get(token = officertoken)
			if ( officer.active == True ) :
				queryparameters = {}
				if ( querydata['lattitude']['data'] == '1' ):
					queryparameters['lattitude__gte'] = float( querydata['lattitude']['lattitudestart'] )
					queryparameters['lattitude__lte'] = float( querydata['lattitude']['lattitudeend'] )
				else:
					pass
				if ( querydata['longitude']['data'] == '1' ):
					queryparameters['longitude__gte'] = float( querydata['longitude']['longitudestart'] )
					queryparameters['longitude__lte'] = float( querydata['longitude']['longitudeend'] )
				else:
					pass
				if ( querydata['date']['data'] == '1' ):
					queryparameters['arivaldate__gte'] = str( querydata['date']['datestart'] )
					queryparameters['arivaldate__lte'] = str( querydata['date']['dateend'] )
				else:
					pass
				if ( querydata['time']['data'] == '1' ):
					queryparameters['arivaltime__gte'] = str( querydata['time']['timestart'] )
					queryparameters['arivaltime__lte'] = str( querydata['time']['timeend'] )
				else:
					pass
				if ( querydata['guard']['data'] == '1' ):
					queryparameters['token'] = str( querydata['guard']['guard_id'] )
				else:
					pass
				sessions = LocationDetails.objects.filter(**queryparameters)
				serializers = LocationDetailsSerializer(sessions,many=True)
				return  JSONResponse(serializers.data,'')
			else:
				return JSONResponse({'error':'Inactive Token'},'')
		except AdminOfficerToken.DoesNotExist:
			return JSONResponse({'error':'Invalid Officer Token'},'')

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(LocationQuery, self).dispatch(*args, **kwargs)
