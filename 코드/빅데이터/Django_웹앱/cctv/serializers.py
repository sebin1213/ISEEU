from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Road, News,Fire

class RoadSerializer(ModelSerializer):
    class Meta:
        model = Road
        fields = '__all__'

class NewsSerializer(ModelSerializer):
    class Meta:
        model = News
        # fields = '__all__'
        fields = ('News_title','News_content','News_href','News_writer','News_write_time')

class FireSerializer(ModelSerializer):
    class Meta:
        model = Fire
        # fields = '__all__'
        fields = ('Fire_loc','Fire_time','Fire_state','Fire_area')