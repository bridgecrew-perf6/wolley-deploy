from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class RecommendationRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.headers["user"]
        content = dict()
        content["responseMsg"] = "성공"
        content["data"] = dict()
        content["data"]["id"] = 2
        content["data"]["place"] = "집사야 오늘 날씨가 좋은데 \n사브레 과자 전문점에 가보는 거 어때?"

        return Response(content, status=status.HTTP_200_OK)

