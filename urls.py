# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from adminapi.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
	url(r'^user/demo/user/listing/$', NextAPIAfterLoginView.as_view(), name='demouserlisting'),
	url(r'^user/demo/add/account/$', AddBankAccount.as_view(), name='add_account'),
	url(r'^user/demo/create/transaction/$', CreateTransaction.as_view(), name='create_transcation'),
	url(r'^user/demo/transaction/list/$', TransactionHistoryList.as_view(), name='list_transcation'),
	url(r'^api-token-auth/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
	url(r'^api/token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
	url(r'^api/token/verify/$', TokenVerifyView.as_view(), name='token_verify'),
]
