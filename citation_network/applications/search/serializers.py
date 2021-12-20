from rest_framework_mongoengine import serializers
from applications.search.models import Paper

class PaperSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Paper
        fields = '__all__'