from rest_framework import serializers
from .models import DailyPath


class PieChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyPath
        fields = '__all__'
