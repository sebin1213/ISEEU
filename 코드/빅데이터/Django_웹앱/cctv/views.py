from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Road, News, Fire
from .serializers import RoadSerializer, NewsSerializer, FireSerializer


# 포스팅 목록 및 새 포스팅 작성
class RoadListAPIView(APIView):
    def get(self, request):
        serializer = RoadSerializer(Road.objects.all(), many=True)
        return Response(serializer.data)

class News(generics.GenericAPIView):
    serializer_class = NewsSerializer
    queryset = News.objects.all()

    def get(self, request, News_area_name, *args, **kwargs):
        try:
            queryset = self.queryset.filter(News_area=News_area_name)

            serializer = NewsSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response(ex, status=status.HTTP_400_BAD_REQUEST)

class Fire(generics.GenericAPIView):
    serializer_class = FireSerializer
    queryset = Fire.objects.all()

    def get(self, request, Fire_area_name, *args, **kwargs):
        try:
            queryset = self.queryset.filter(Fire_area=Fire_area_name)

            serializer = FireSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response(ex, status=status.HTTP_400_BAD_REQUEST)