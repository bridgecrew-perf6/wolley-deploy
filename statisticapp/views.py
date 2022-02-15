from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from myapi.utils import make_response_content


@method_decorator(csrf_exempt, name='dispatch')
class StatRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        data = {
            "labels": [
                {
                    "title": "워커홀릭",
                    "desc": "회사에서 보낸 시간이 상위 10%",
                    "part": "work"
                }
            ]
        }
        content = make_response_content("성공", data)
        return Response(content, status=status.HTTP_200_OK)
