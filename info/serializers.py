from rest_framework import serializers
from . import models as info_models



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = info_models.Tag
        fields = ['id', 'name', 'description']

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = info_models.Schedule
        fields = ['id', 'start_date', 'end_date', 'type']

class FynderBasicTypeSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(max_length=255)
    # description = serializers.CharField(max_length=255)
    tags = serializers.SerializerMethodField()
    schedules = serializers.SerializerMethodField()

    class Meta:
        model = info_models.FynderBasicType
        fields = [ 'id', 'name', 'description', 'tags', 'schedules'] # 'img'

    def get_tags(self, obj):
        return TagSerializer(obj.get_tags(), many=True).data
        

    def get_schedules(self, obj):
        return ScheduleSerializer(obj.get_schedules(), many=True).data