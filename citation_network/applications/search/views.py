from django.shortcuts import render
from .models import Paper
from .serializers import PaperSerializer
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework import viewsets
from elasticsearch import Elasticsearch

# Create your views here.

# client = Elasticsearch(hosts=['127.0.0.1'])
#
# def homepage(request):
#     return render(request, 'homepage.html')
#
# def paperdetail(request, id):
#     return render(request, 'paperdetail.html')

class PaperListView(viewsets.ModelViewSet):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer

    def get(self, request):
        return self.list(request)

def relation_graph(request):
    return render(request, 'homepage.html')

def paper_info(request):
    return render(request, 'homepage.html')

def sort_by_rank(request):
    return render(request, 'homepage.html')