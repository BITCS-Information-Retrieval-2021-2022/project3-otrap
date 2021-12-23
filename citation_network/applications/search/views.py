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
from django.http import HttpResponse, JsonResponse

# Create your views here.

client = Elasticsearch(hosts=['127.0.0.1'])
#

class retrieval(View):
    """
    搜索显示逻辑
    """
    def get(self, request):
        key_words = request.GET.get('query')  # 接收一个query变量，query包含了输入框的词，以此返回给elasticsearch做分词匹配
        #key_words = 'for'
        paper_count = int(client.count(index="otrap")["count"])#总的paper数量
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
        result_total = response["hits"]["total"] #检索出来的paper总数
        if (page % 10) > 0:  # 总页数
            page_nums = int(result_total / 10) + 1
        else:
            page_nums = int(result_total / 10)
        hit_list = []
        for hit in response['hits']['hits']:
            print(hit)
            hit_dict = {}
            if "Sid" in hit["_source"]:
                hit_dict["Sid"] = hit["_source"]["Sid"]
            if "title" in hit["_source"]:
                hit_dict["title"] = hit["_source"]["title"]
            if "year" in hit["_source"]:
                hit_dict["year"] = int(hit["_source"]["year"])
            if "inCitationsCount" in hit["_source"]:
                hit_dict["inCitationsCount"] = int(hit["_source"]["inCitationsCount"])
            if "outCitationsCount" in hit["_source"]:
                hit_dict["outCitationsCount"] = int(hit["_source"]["outCitationsCount"])

            hit_list.append(hit_dict)
            print(hit_list)

        return JsonResponse({"paper_list": hit_list,
                             "page_nums": page_nums,
                             "last_seconds": last_seconds,
                             "page": page,
                             "result_total": result_total
                             })

def relation_graph(request):#画图

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
    result_total = response["hits"]["total"]
    if (page % 10) > 0:  # 总页数
        page_nums = int(result_total / 10) + 1
    else:
        page_nums = int(result_total / 10)
    hit_list = []
    for hit in response['hits']['hits']:
        hit_dict = {}
        if "Sid" in hit["_source"]:
            hit_dict["Sid"] = hit["_source"]["Sid"]
        if "title" in hit["_source"]:
            hit_dict["title"] = hit["_source"]["title"]
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

    return JsonResponse({"paper_list": hit_list,
                        "page_nums": page_nums,
                        "last_seconds": last_seconds,
                        "page": page,
                        "result_total": result_total
                        })

def paper_info(request):
    Sid = request.GET.get('sid')
    #id = 'f6370fe63ff9c7191335c3e5de8d4b6935ae1792'
    response = client.search(
        index="otrap",
        body={
            'query': {
                "term": {
                    "Sid": Sid,
                }
            },
        }
    )
    print(response)
    hit = response['hits']['hits'][0]
    paper = {}
    if "Sid" in hit["_source"]:
        paper["Sid"] = hit["_source"]["Sid"]
    if "title" in hit["_source"]:
        paper["title"] = hit["_source"]["title"]
    if "inCitations" in hit["_source"]:
        paper["inCitations"] = hit["_source"]["inCitations"].split(",")
    if "outCitations" in hit["_source"]:
        paper["outCitations"] = hit["_source"]["outCitations"].split(",")
    if "year" in hit["_source"]:
        paper["year"] = int(hit["_source"]["year"])
    if "inCitationsCount" in hit["_source"]:
        paper["inCitationsCount"] = int(hit["_source"]["inCitationsCount"])
    if "outCitationsCount" in hit["_source"]:
        paper["outCitationsCount"] = int(hit["_source"]["outCitationsCount"])
    print(paper)

    return JsonResponse(paper, safe=False)