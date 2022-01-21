from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from intervalapp.models import Interval


@method_decorator(csrf_exempt, name='dispatch')
class IntervalRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_interval_id = request.headers['intervalId']
        content = dict()

        try:
            interval_obj = Interval.objects.get(id=request_interval_id)
        except Interval.DoesNotExist:
            content['responseMsg'] = "Interval 기록 없음"
            content['data'] = dict()
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        content['responseMsg'] = "성공"
        content['data'] = dict()
        content['data']['id'] = interval_obj.id
        content['data']['category'] = interval_obj.category
        content['data']['location'] = interval_obj.location
        content['data']['address'] = interval_obj.address
        content['data']['coordinate'] = dict()
        content['data']['coordinate']['latitude'] = interval_obj.latitude
        content['data']['coordinate']['longitude'] = interval_obj.longitude
        content['data']['percnet'] = interval_obj.percent

        return Response(content, status=status.HTTP_200_OK)

    # def validate_emotion_type(self, choice):
    #     kor2eng = {"긍정": "positive", "중립": "normal", "부정": "normal"}
    #     return kor2eng[choice]

    def update_interval(self, request):
        # search
        interval_id = request.data["intervalId"]
        content = dict()

        try:
            interval_obj = Interval.objects.get(id=interval_id)
        except Interval.DoesNotExist:
            content['responseMsg'] = "Interval 기록 없음"
            content['data'] = dict()
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # update
        interval_obj.latitude = request.data["coordinate"]["latitude"]
        interval_obj.longitude = request.data["coordinate"]["longitude"]
        interval_obj.category = request.data["category"]
        interval_obj.location = request.data["location"]

        interval_obj.save()

        content['responseMsg'] = "성공"
        content['data'] = dict()
        content['data']['id'] = interval_obj.id
        content['data']['category'] = interval_obj.category
        content['data']['location'] = interval_obj.location
        content['data']['address'] = interval_obj.address
        content['data']['coordinate'] = dict()
        content['data']['coordinate']['latitude'] = interval_obj.latitude
        content['data']['coordinate']['longitude'] = interval_obj.longitude
        content['data']['percnet'] = interval_obj.percent
        return content

    def post(self, request):
        content = self.update_interval(request)
        return Response(content, status=status.HTTP_200_OK)
