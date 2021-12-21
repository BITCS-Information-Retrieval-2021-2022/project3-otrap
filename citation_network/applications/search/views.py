from django.shortcuts import render
from .models import PaperType
from .serializers import PaperSerializer
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
#from rest_framework import viewsets
from elasticsearch import Elasticsearch
from django.http import HttpResponse
from django.views.generic.base import View
from datetime import datetime

# Create your views here.

client = Elasticsearch(hosts=['127.0.0.1'])
#
class IndexView(View):
    def get(self, request):
        return render(request, "index.html")
#
# def paperdetail(request, id):
#     return render(request, 'paperdetail.html')

# class PaperListView(viewsets.ModelViewSet):
#     queryset = Paper.objects.all()
#     serializer_class = PaperSerializer
#
#     def get(self, request):
#         return self.list(request)

class search(View):
    """
    搜索显示逻辑
    """
    def get(self, request):
        key_words = request.GET.get('q', '')  # 接收一个s变量，s包含了输入框的词，以此返回给elasticsearch做分词匹配
        paper_count = int(client.count(index="otrap")["count"])
        page = request.GET.get("p", "")
        try:
            page = int(page)
        except:
            page = 1
        start_time = datetime.now()
        response = client.search(
            index="otrap",
            body={
                'query': {
                    "multi_match": {
                        "query": key_words,
                        "fields": ["title"]
                    }
                },
                "from": (page - 1) * 10,
                "size": 10,
                "highlight": {  # 词语高亮
                    "pre_tags": ["<span class='keyWord'>"],
                    "post_tags": ["</span>"],
                    "fields": {
                        "title": {},
                    }
                }
            }
        )
        end_time = datetime.now()
        last_seconds = (end_time - start_time).total_seconds()
        total_nums = response["hits"]["total"]
        if (page % 10) > 0:  # 总页数
            page_nums = int(total_nums / 10) + 1
        else:
            page_nums = int(total_nums / 10)
        hit_list = []
        for hit in response['hits']['hits']:
            hit_dict = {}
            if "highlight" in hit:
                if "title" in hit["highlight"]:
                    hit_dict["title"] = "".join(hit["highlight"]["title"])
                else:
                    hit_dict["title"] = hit["_source"]["title"]
            if "Sid" in hit["_score"]:
                hit_dict["Sid"] = hit["_source"]["Sid"]
            if "year" in hit["_score"]:
                hit_dict["year"] = hit["_source"]["year"]
            if "inCitationscount" in hit["_score"]:
                hit_dict["inCitationscount"] = hit["_source"]["inCitationscount"]
            if "outCitationscount" in hit["_score"]:
                hit_dict["outCitationscount"] = hit["_source"]["outCitationscount"]

            hit_list.append(hit_dict)
        return render(request, "result.html", {"all_list": hit_list,
                                               "key_words": key_words,
                                               "total_nums": total_nums,
                                               "page_nums": page_nums,
                                               "last_seconds": last_seconds,
                                               "page": page,
                                               "paper_count": paper_count})

def relation_graph(request):

    return render(request, "index.html")

def sort_by_rank(request):
    return render(request, 'homepage.html')