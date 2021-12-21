from rest_framework import serializers
from .models import PaperType

class PaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperType
        fields = '__all__'