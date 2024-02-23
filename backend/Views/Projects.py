import logging

import coreapi
import coreschema
from rest_framework import permissions
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView

from api_test.utils import response
from api_test.utils.api_response import JsonResponse
from api_test.utils.auth import ExpiringTokenAuthentication
from backend.models import Projects
from backend.serializers import ProjectsSerializer

logger = logging.getLogger("api_automation_test")


class CustomSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        """Example adding per-method fields."""

        extra_fields = list()

        if method == 'GET':
            extra_fields = [
                coreapi.Field(name='Authorization', required=True, location='header', description='token',
                              schema=coreschema.String(), type="string", example="Token string"),
            ]
        manual_fields = super().get_manual_fields(path, method)

        return manual_fields + extra_fields


class ProjectManager(APIView):
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    schema = CustomSchema()

    def get(self, request):
        """
        获取项目列表
        """
        obi = Projects.objects.all().order_by("id")
        serialize = ProjectsSerializer(obi, many=True)
        return JsonResponse(data=serialize.data, code_msg=response.SUCCESS)