from rest_framework import serializers 
from homepage.models import Counter
 
 
class CounterSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Counter
        fields = ('id',
                  'creation_time',
                  'update_time',
                  'count')