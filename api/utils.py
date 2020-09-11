# -*- coding: utf-8 -*-
# @Author  : chengyijun
# @Time    : 2020/9/1 16:19
# @File    : utils.py
# @desc:
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.versioning import URLPathVersioning, QueryParameterVersioning


class LoginAuthentication(BaseAuthentication):
    """登录验证"""

    def authenticate(self, request):
        params = request.query_params.dict()
        if 'token' in params.keys():
            return 'abel', '123sgsg'
        detail = {
            'msg': '登录验证失败',
            'code': 111
        }
        raise exceptions.AuthenticationFailed(detail=detail)


class MyPermission(BasePermission):
    """权限控制"""

    def has_permission(self, request, view):
        params = request.query_params.dict()
        if 'perm' in params.keys():
            return True
        return False


class MyThrottle(SimpleRateThrottle):
    """节流控制"""
    scope = 'guest'
    THROTTLE_RATES = {
        'guest': '5/m'
    }

    def get_cache_key(self, request, view):
        return self.get_ident(request)


class MyVersion(URLPathVersioning):
    """版本控制"""
    default_version = 'v1'
    allowed_versions = ['v1', 'v2']
    version_param = 'version'

    invalid_version_message = {
        'code': -111,
        'msg': '错误的版本号'
    }


from rest_framework.pagination import PageNumberPagination


class MyPageNumberPagination(PageNumberPagination):
    page_size = 2
    max_page_size = 5
    page_size_query_param = 'size'
    page_query_param = 'page'
