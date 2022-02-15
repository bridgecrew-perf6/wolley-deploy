import datetime
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from myapi.utils import make_response_content
from testapp.models import TestTable


def update_something():
    TestTable.objects.create(
        textfield=f"this function runs every 10 seconds {datetime.datetime.today()}"
    )
    # print(f"this function runs every 10 seconds {datetime.datetime.today()}")


@method_decorator(csrf_exempt, name='dispatch')
class StatRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        content = make_response_content("성공", {})
        return Response(content, status=status.HTTP_200_OK)