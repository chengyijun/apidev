# -*- coding:utf-8 -*-
from rest_framework import exceptions, serializers
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Role, UserInfo
from api.utils import LoginAuthentication, MyPermission, MyThrottle, MyVersion, MyPageNumberPagination

from rest_framework.serializers import ModelSerializer


class RoleSerializer(ModelSerializer):
    def validate_title(self, value):
        print('验证title', value)
        from rest_framework import exceptions
        if not value:
            raise exceptions.ValidationError('不可为空')
        return value

    class Meta:
        model = Role
        fields = '__all__'
        ordering = ['id']


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'
        depth = 1


class UserSerializer(serializers.Serializer):
    type = serializers.IntegerField(source='user_type')
    user_type = serializers.CharField(source='get_user_type_display')  # choices字段显示
    username = serializers.CharField()
    pwd = serializers.CharField(source='password')  # 自定义serializer中的key值
    group_title = serializers.CharField(source='group.title')  # 关联对象属性
    roles = serializers.CharField(source='roles.all')  # 多对多关系
    roles_info = serializers.SerializerMethodField()  # 表示自定义方法，显示querytset对象详情

    def get_roles_info(self, row):
        roles = row.roles.all()
        ret = []
        for item in roles:
            ret.append(
                {
                    'id': item.id,
                    'title': item.title
                }
            )
        return ret


class UserInfosView(APIView):

    def get(self, request, *args, **kwargs):
        # role_objects_all = Role.objects.values('id', 'title')
        # roles = list(role_objects_all)
        # print(roles)

        userinfos = UserInfo.objects.all()
        ser = UserModelSerializer(instance=userinfos, many=True)
        print(ser.data)
        return Response({'code': 1, 'data': ser.data})


class RolesView(ListAPIView):
    serializer_class = RoleSerializer
    queryset = Role.objects.get_queryset().order_by()
    pagination_class = MyPageNumberPagination


# class RolesView(APIView):
#
#     def get(self, request, *args, **kwargs):
#         # role_objects_all = Role.objects.values('id', 'title')
#         # roles = list(role_objects_all)
#         # print(roles)
#
#         roles = Role.objects.all()
#         pagination = MyPageNumberPagination()
#         proles = pagination.paginate_queryset(queryset=roles, request=request, view=self)
#         ser = RoleSerializer(instance=proles, many=True)
#         print(ser.data)
#         return Response({'code': 1, 'data': ser.data})
#
#     def post(self, request, *args, **kwargs):
#         # 验证之前的数据
#         print(request.data)
#         # 序列化
#         ser = RoleSerializer(data=request.data)
#         if ser.is_valid():
#             print('通过验证 写数据库')
#             ser.save()
#         else:
#             print('没通过验证')
#
#         return Response({'code': 1, 'data': ser.data})


class TestView(APIView):
    # authentication_classes = [LoginAuthentication]
    # permission_classes = [MyPermission]
    # throttle_classes = [MyThrottle]
    # versioning_class = MyVersion
    parser_classes = [MultiPartParser]

    def get(self, request, *args, **kwargs):
        params_dict = request.query_params.dict()
        data = {
            'code': 1,
            'version': request.version,
            'params': params_dict
        }
        # print(type(kwargs.get('token')))
        # print(kwargs.get('token'))
        print(params_dict)
        return Response(data)

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('file', None)
        # type = request.POST['type']
        for file_obj in files:
            print(type(file_obj))
            print(file_obj)
            with open('a.jpg', 'wb+') as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)

        data = {
            'code': 1,
            'version': request.version,
            'msg': f'{file_obj.name}文件上传成功'
        }
        # print(request.data)
        return Response(data)

    def permission_denied(self, request, message=None):
        message = {
            'code': -100,
            'message': '您没有访问权限'
        }
        return super().permission_denied(request, message)

    def throttled(self, request, wait):
        class MyThrottled(exceptions.Throttled):
            default_detail = '请求被限制.'
            extra_detail_singular = 'Expected available in {wait} second.'
            extra_detail_plural = '还需要再等待{wait}'

        raise MyThrottled(wait)
