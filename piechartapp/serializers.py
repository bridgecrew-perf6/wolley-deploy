from rest_framework import serializers
from .models import PieChart


class PieChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = PieChart
        fields = '__all__'
