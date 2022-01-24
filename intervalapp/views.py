from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from intervalapp.models import IntervalStay
from myapi.utils import make_response_content, make_interval_to_data


@method_decorator(csrf_exempt, name='dispatch')
class IntervalRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_interval_id = request.headers['intervalId']

        try:
            interval_obj = IntervalStay.objects.get(id=request_interval_id)
        except IntervalStay.DoesNotExist:
            content = make_response_content("Interval 기록 없음", {})
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        data = make_interval_to_data(interval_obj)
        content = make_response_content("성공", data)
        return Response(content, status=status.HTTP_200_OK)

    def post(self, request):
        request_interval_id = request.data["intervalId"]

        try:
            interval_obj = IntervalStay.objects.get(id=request_interval_id)
        except IntervalStay.DoesNotExist:
            content = make_response_content("Interval 기록 없음", {})
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        interval_obj.category = request.data["category"]
        interval_obj.location = request.data["location"]
        interval_obj.latitude = request.data["coordinates"]["latitude"]
        interval_obj.longitude = request.data["coordinates"]["longitude"]
        interval_obj.save()

        data = make_interval_to_data(interval_obj)
        content = make_response_content("성공", data)
        return Response(content, status=status.HTTP_200_OK)