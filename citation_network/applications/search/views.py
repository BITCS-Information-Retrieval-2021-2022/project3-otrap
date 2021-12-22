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
from django.http import HttpResponse,JsonResponse

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

class retrieval(View):
    """
    搜索显示逻辑
    """
    def get(self, request):
        key_words = request.GET.get('query')  # 接收一个query变量，query包含了输入框的词，以此返回给elasticsearch做分词匹配
        paper_count = int(client.count(index="otrap")["count"])
        page = request.GET.get("page")
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
        print(response)
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
            if "title" in hit["_source"]:
                hit_dict["title"] = hit["_source"]["title"]
            if "Sid" in hit["_source"]:
                hit_dict["Sid"] = hit["_source"]["Sid"]
            if "year" in hit["_source"]:
                hit_dict["year"] = int(hit["_source"]["year"])
            if "inCitationsCount" in hit["_source"]:
                hit_dict["inCitationsCount"] = int(hit["_source"]["inCitationsCount"])
            if "outCitationsCount" in hit["_source"]:
                hit_dict["outCitationsCount"] = int(hit["_source"]["outCitationsCount"])

            hit_list.append(hit_dict)
            print(hit_list)
        # return render(request, "result.html", {"all_list": hit_list,
        #                                        "key_words": key_words,
        #                                        "total_nums": total_nums,
        #                                        "page_nums": page_nums,
        #                                        "last_seconds": last_seconds,
        #                                        "page": page,
        #                                        "paper_count": paper_count})
        return JsonResponse(hit_list, safe=False)

def relation_graph(request):

    return render(request, "index.html")

def sort_by_rank(request):#按照重要性分数排序
    key_words = request.GET.get('query')  # 接收一个query变量，query包含了输入框的词，以此返回给elasticsearch做分词匹配
    paper_count = int(client.count(index="otrap")["count"])
    page = request.GET.get("page")
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
            "sort": [
                {
                    "score": "desc"
                }
            ],
            "highlight": {  # 词语高亮
                "pre_tags": ["<span class='keyWord'>"],
                "post_tags": ["</span>"],
                "fields": {
                    "title": {},
                }
            }
        }
    )
    print(response)
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
        if "title" in hit["_source"]:
            hit_dict["title"] = hit["_source"]["title"]
        if "Sid" in hit["_source"]:
            hit_dict["Sid"] = hit["_source"]["Sid"]
        if "year" in hit["_source"]:
            hit_dict["year"] = int(hit["_source"]["year"])
        if "inCitationsCount" in hit["_source"]:
            hit_dict["inCitationsCount"] = int(hit["_source"]["inCitationsCount"])
        if "outCitationsCount" in hit["_source"]:
            hit_dict["outCitationsCount"] = int(hit["_source"]["outCitationsCount"])
        if "score" in hit["_source"]:
            hit_dict["score"] = float(hit["_source"]["score"])

        hit_list.append(hit_dict)
        print(hit_list)
    # return render(request, "result.html", {"all_list": hit_list,
    #                                        "key_words": key_words,
    #                                        "total_nums": total_nums,
    #                                        "page_nums": page_nums,
    #                                        "last_seconds": last_seconds,
    #                                        "page": page,
    #                                        "paper_count": paper_count})
    return JsonResponse(hit_list, safe=False)
