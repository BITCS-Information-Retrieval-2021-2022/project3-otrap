from elasticsearch import Elasticsearch
from django.views.generic.base import View
from datetime import datetime
from django.http import HttpResponse, JsonResponse

# Create your views here.

client = Elasticsearch(hosts=["127.0.0.1"])
#


class retrieval(View):
    """
    搜索显示逻辑
    """

    def get(self, request):
        key_words = request.GET[
            "query"
        ]  # 接收一个query变量，query包含了输入框的词，以此返回给elasticsearch做分词匹配
        # paper_count = int(client.count(index="otrap")["count"])  # 总的paper数量
        # page = request.GET.get("page")
        # max_query = request.GET['max_query']
        max_query = 100
        if not max_query:
            max_query = 100
        response = client.search(
            index="otrap",
            body={
                "query": {
                    "multi_match": {
                        "query": key_words,
                        "fields": ["title"]
                    }
                },
                "size": max_query,
            },
        )
        # print(response)
        result_total = response["hits"]["total"]  # 检索出来的paper总数
        hit_list = []
        for hit in response["hits"]["hits"]:
            # print(hit)
            hit_dict = {}
            if "Sid" in hit["_source"]:
                hit_dict["Sid"] = hit["_source"]["Sid"]
            if "title" in hit["_source"]:
                hit_dict["title"] = hit["_source"]["title"]
            if "year" in hit["_source"]:
                hit_dict["year"] = int(hit["_source"]["year"])
            if "inCitationsCount" in hit["_source"]:
                hit_dict["inCitationsCount"] = \
                    int(hit["_source"]["inCitationsCount"])
            if "outCitationsCount" in hit["_source"]:
                hit_dict["outCitationsCount"] = \
                    int(hit["_source"]["outCitationsCount"])

            hit_list.append(hit_dict)
        # print(hit_list)
        return JsonResponse({"paper_list": hit_list,
                             "result_total": result_total})


def relation_graph(request):  # 画图
    # key_words = "people"
    key_words = request.GET["query"]  # 从前端获取query
    # 检索出存在title中存在key_words的结果
    results1 = client.search(
        index="otrap",
        body={
            "query": {
                "multi_match": {
                    "query": key_words,
                    "fields": ["title"]
                }
            },
            "size": 200,
        },
    )
    nodes = []  # 检索出的所有点集
    old_links = []
    links = []  # 最后处理后的边
    for paper1 in results1["hits"]["hits"]:
        node1 = {}
        link = {}
        sid = []
        sid.append(paper1["_source"]["Sid"])  # 已经加入nodes列表的sid
        node1["Sid"] = paper1["_source"]["Sid"]
        node1["title"] = paper1["_source"]["title"]
        node1["category"] = 1
        node1["score"] = paper1["_source"]["score"]
        nodes.append(node1)  # 符合query的点
        if "outCitations " in paper1["_source"]:
            for target in paper1["_source"]["outCitations"]:
                if target:
                    results2 = client.search(
                        index="otrap",
                        body={
                            "query": {
                                "term": {
                                    "Sid": target,
                                }
                            },
                            "size": 100,
                        },
                    )
                    if results2["hits"]["total"] != 0:
                        paper2 = results2["hits"]["hits"][0]
                        link["source"] = paper1["_source"]["Sid"]
                        link["target"] = target
                        old_links.append(link)  # 可以形成边
                        node2 = {}
                        if paper2["_source"]["Sid"] in sid:  # 如果这个点已经在nodes中
                            continue
                        else:
                            sid.append(paper2["_source"]["Sid"])
                            node2["Sid"] = paper2["_source"]["Sid"]
                            node2["title"] = paper2["_source"]["title"]
                            node2["category"] = 2
                            node2["score"] = paper2["_source"]["score"]
                            nodes.append(node2)
                            for i in paper2["_source"]["inCitations"]:
                                if i in sid:
                                    link1 = {}
                                    link1["source"] = i
                                    link1["target"] = paper2["_source"]["Sid"]
                                    old_links.append(link1)
                            for i in paper2["_source"]["outCitations"]:
                                if i in sid:
                                    link1 = {}
                                    link1["source"] = paper2["_source"]["Sid"]
                                    link1["target"] = i
                                    old_links.append(link1)

        if "inCitations" in paper1["_source"]:
            for source in paper1["_source"]["inCitations"]:
                if source:
                    results2 = client.search(
                        index="otrap",
                        body={
                            "query": {
                                "term": {
                                    "Sid": source,
                                }
                            },
                            "size": 100,
                        },
                    )
                    if results2["hits"]["total"] != 0:
                        paper2 = results2["hits"]["hits"][0]
                        link["source"] = source
                        link["target"] = paper1["_source"]["Sid"]
                        old_links.append(link)  # 可以形成边
                        if paper2["_source"]["Sid"] in sid:
                            continue
                        else:
                            node2 = {}
                            sid.append(paper2["_source"]["Sid"])
                            node2["Sid"] = paper2["_source"]["Sid"]
                            node2["title"] = paper2["_source"]["title"]
                            node2["category"] = 0
                            node2["score"] = paper2["_source"]["score"]
                            nodes.append(node2)
                            for i in paper2["_source"]["inCitations"]:
                                if i in sid:
                                    link1 = {}
                                    link1["source"] = i
                                    link1["target"] = paper2["_source"]["Sid"]
                                    old_links.append(link1)
                            for i in paper2["_source"]["outCitations"]:
                                if i in sid:
                                    link1 = {}
                                    link1["source"] = paper2["_source"]["Sid"]
                                    link1["target"] = i
                                    old_links.append(link1)
    for i in old_links:
        if i not in links:
            links.append(i)
    print(nodes)
    print(links)
    categories = []
    categories.append({"name": "引用"})
    categories.append({"name": "搜索结果"})
    categories.append({"name": "被引"})
    return JsonResponse({"nodes": nodes,
                         "links": links,
                         "categories": categories})


def sort_by_rank(request):  # 按照重要性分数排序
    key_words = request.GET.get(
        "query"
    )  # 接收一个query变量，query包含了输入框的词，以此返回给elasticsearch做分词匹配
    # key_words = 'for'
    # paper_count = int(client.count(index="otrap")["count"])
    # page = request.GET.get("page")
    # max_query = request.GET.get("max_query")
    max_query = 100
    if not max_query:
        max_query = 100
    start_time = datetime.now()
    response = client.search(
        index="otrap",
        body={
            "query": {
                "multi_match": {
                    "query": key_words,
                    "fields": ["title"]
                }
            },
            "size": max_query,
            "sort": [{"score": "desc"}],
        },
    )
    # print(response)
    end_time = datetime.now()
    last_seconds = (end_time - start_time).total_seconds()
    result_total = response["hits"]["total"]
    hit_list = []
    for hit in response["hits"]["hits"]:
        hit_dict = {}
        if "Sid" in hit["_source"]:
            hit_dict["Sid"] = hit["_source"]["Sid"]
        if "title" in hit["_source"]:
            hit_dict["title"] = hit["_source"]["title"]
        if "year" in hit["_source"]:
            hit_dict["year"] = int(hit["_source"]["year"])
        if "inCitationsCount" in hit["_source"]:
            hit_dict["inCitationsCount"] = \
                int(hit["_source"]["inCitationsCount"])
        if "outCitationsCount" in hit["_source"]:
            hit_dict["outCitationsCount"] = \
                int(hit["_source"]["outCitationsCount"])
        if "score" in hit["_source"]:
            hit_dict["score"] = round(float(hit["_source"]["score"]), 2)

        hit_list.append(hit_dict)

    return JsonResponse(
        {
            "paper_list": hit_list,
            "last_seconds": last_seconds,
            "result_total": result_total,
        }
    )


def paper_info(request):
    Sid = request.GET.get("Sid")
    # Sid = 'f6370fe63ff9c7191335c3e5de8d4b6935ae1792'
    response = client.search(
        index="otrap",
        body={
            "query": {
                "term": {
                    "Sid": Sid,
                }
            },
        },
    )
    # print(response)
    hit = response["hits"]["hits"][0]
    paper = {}
    if "Sid" in hit["_source"]:
        paper["Sid"] = hit["_source"]["Sid"]
    if "title" in hit["_source"]:
        paper["title"] = hit["_source"]["title"]
    if "year" in hit["_source"]:
        paper["year"] = int(hit["_source"]["year"])
    if "inCitationsCount" in hit["_source"]:
        paper["inCitationsCount"] = int(hit["_source"]["inCitationsCount"])
    if "outCitationsCount" in hit["_source"]:
        paper["outCitationsCount"] = int(hit["_source"]["outCitationsCount"])
    # print(paper)

    return JsonResponse(paper, safe=False)


def index(request):
    return HttpResponse("hello")
