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

    def validate_emotion_type(self, choice):
        kor2eng = {"긍정": "positive", "중립": "normal", "부정": "normal"}
        return kor2eng[choice]

    def update_interval(self, request):
        # search
        interval_id = request.data["intervalId"]
        interval_obj = Interval.objects.filter(id=interval_id)[0]

        # update
        interval_obj.latitude = request.data["coordinate"]["latitude"]
        interval_obj.longitude = request.data["coordinate"]["longitude"]
        interval_obj.category = request.data["intervalCategory"]
        interval_obj.location = request.data["intervalLocation"]
        interval_obj.emotion = self.validate_emotion_type(request.data["emotion"])

        interval_obj.save()

    def post(self, request):
        self.update_interval(request)
        return Response({"responseMsg": "성공"}, status=status.HTTP_200_OK)
