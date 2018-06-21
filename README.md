# sample_django_api

USING TOKENAUTHENTICATION: 
1st API: DemoAPIView
Request: email, first_name, last_name, password, address
Response: token, id, email, address, status
URL : http://127.0.0.1:8000/api/user/demo/add/account/

2nd API: NextAPIAfterLoginView
Request: token
Response: List_user
URL :  http://127.0.0.1:8000/api/user/demo/user/listing/

USING JWTAUTHENTICATION:
1st API: AddBankAccount
Request: accountnumber, balance
Response: token, message(success/ error)
URL: http://127.0.0.1:8000/user/demo/add/account/

2nd API: CreateTransaction
Request: balance
Response: message(success/ error)
URL: http://127.0.0.1:8000/user/demo/create/transaction/

3rd API: TransactionHistoryList
Request: -
Response: datalist
URL: http://127.0.0.1:8000/user/demo/transaction/list/

For Security of Rest APIs:
- To make Rest API secure, Django Rest framework provides various Authentication schemes. One of them is 'TokenAuthentication' which comes default with DRF and is used in first 2 APIs above.
- Usage of JWTAuthentication can also done. It needs to be setup as per requirement through settings.py. The last 3 APIs  are examples for JWTAuthentication.
- We can also use SessionAuthentication  or  BasicAuthentication

- 'Permissions' is another way to increase security of APIs through which we determine whether a request should be granted or denied access. In above APIs, IsAuthenticated class is used to restrict the permissions

- Throttling is similar to permissions,  it determines if a request should be authorized. Throttles indicate a temporary state, and are used to control the rate of requests that clients can make to an API.
- The Throttle classes are defined in APIs globally as done in above APIs as well. 	








For multi request handling:
-  Throttling also allows to rate-limit requests. Various classes are provided through which the restriction can be imposed on number of requests handled per day/ per minute etc.
- UserRateThrottle, AnonRateThrottle classes are used in APIs here  to set limit on requests 
i.e.
        'DEFAULT_THROTTLE_RATES': { 
            'anon': '10000/day', 
            'user': '10000/day' 
        } 
}

All the above settings are done in settings.py with Rest framework integrations and various classes are called in APIs according to requirement.	
