
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import UserRateThrottle
from adminapi.models import AddbankAccount, TransactionList
from django.db.models import F
import json
import requests
from rest_framework_simplejwt.tokens import RefreshToken 

class DemoAPIView(APIView):

	throttle_classes = (UserRateThrottle,)

	#Now we are using token based api
	def post(self, request, format = None):
		if not 'email' in request.data  or  not 'first_name' in request.data or  not 'password' in request.data or not 'last_name' in request.data or not 'address' in request.data:
			return Response(StatusCode.statuscode401())

		# We are returning response in json format

		checkemail = User.objects.filter(email = str(request.data['email']).strip())
		if checkemail:
			token = Token.objects.get_or_create(user=checkemail)

			response = {
				'id':checkemail[0].id,
				'email': checkemail[0].email,
				'address': checkemail[0].address,
				'token': token[0].key,
				'status':"200",
			}
		else:
			saveuser = User()
			saveuser.email = request.data['email'].strip()
			saveuser.username = request.data['email'].strip()
			saveuser.first_name = request.data['first_name'].strip()
			saveuser.last_name = request.data['last_name'].strip()
			saveuser.password = make_password(request.data['password'])
			saveuser.address = request.data['address']
			saveuser.save()

			token = Token.objects.get_or_create(user=saveuser)
			response = {
				'id':saveuser.id,
				'email': saveuser.email,
				'address': saveuser.address,
				'token': token[0].key,
				'status':"200",
			}
		return Response(response)


class NextAPIAfterLoginView(APIView):

	# We need token, we have sent to u sign up time 

	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	throttle_classes = (UserRateThrottle,)
	# We can also  use SessionAuthentication authentication  and BasicAuthentication authentication

	def post(self, request, format = None):
		List_user = []
		get_register_user = User.objects.all()
		if get_register_user.count() > 0:
			for user in get_register_user:
				List_user.append({
						'first_name':user.first_name,
						'last_name':user.last_name,
						'email':user.email,
						'address':user.address
					})
			response = List_user
		else:
			response ="No Data"

		# Return all user with json reponse
		content = {'data':response}
		return Response(response)


# Creating API based on client documentation

class AddBankAccount(APIView):


	#Now we are using token based api
	def post(self, request, format = None):
		if not 'accountnumber' in request.data  or  not 'balance' in request.data :
			return Response(StatusCode.statuscode401())
			
		# We are returning response in json format

		headers = {'content-type': 'application/json'}
		data = {"username":"sristi_singh@seologistics.com","password":"123456789"}
		check_user_token = Token.objects.filter(user_id=request.data['id']) 
		jwt_token = requests.post('http://127.0.0.1:8000/api/api-token-auth/', data=json.dumps(data), headers=headers)
		if jwt_token.status_code == 200:
			token = jwt_token.json()['access']
		else:
			return Response({'messge':"Invalid credentail"})

		try:
			saveuser = AddbankAccount()
			saveuser.accountnumber = request.data['accountnumber']
			saveuser.balance = request.data['balance']
			saveuser.save()
			mesg = "Your account added succesfully."
		except:
			mesg = "Something went wrong."

		response = {
			'message':mesg,
			'token' : token
		}
		return Response(response)		


class CreateTransaction(APIView):

	permission_classes = (IsAuthenticated,)

	#Now we are using token based api
	def post(self, request, format = None):
		if not 'balance' in request.data:
			return Response(StatusCode.statuscode401())
			
		# We are returning response in json format

		savetransaction = TransactionList()
		savetransaction.balance = request.data['balance']
		savetransaction.save()

		tranlist  = AddbankAccount.objects.all()
		divide_money = float(request.data['balance'])/ float(tranlist.count())
		tranlist.update(balance =F('balance') - divide_money)
		mesg = "transaction create succesfully."


		response = {
			'message':mesg
		}
		return Response(response)


class TransactionHistoryList(APIView):
	permission_classes = (IsAuthenticated,)

	#Now we are using token based api
	def post(self, request, format = None):

		querySet = TransactionList.objects.all()
		paginator = Paginator(paginator, 10)
		page = request.data.get('page')
		try:
			contacts = paginator.page(page)
		except PageNotAnInteger:
			contacts = paginator.page(1)
		except EmptyPage:
			contacts = []
		dataList = []
		if contacts:
			for data in querySet:
				dataList.append({
					'balance':data
					})

		response = {
			'response':dataList
		}
		return Response(response)