import simplejson

now_id = 0
vertex_dict = {}
graph = {}


def BuildData(data_prefix, write_prefix):
    file_num = 6000
    global now_id, vertex_dict, graph
    for i in range(1, file_num):
        if i % 50 == 0:
            print("i = ", i)
        this_file = data_prefix + "citationLine" + str(i) + ".jsonl"
        with open(this_file, "r") as f:
            line = f.readline()
            while line is not None and line != "":
                json_data = simplejson.loads(line, encoding="utf-8", strict=False)
                vertex_name = json_data["Sid"]
                if vertex_name not in vertex_dict:
                    vertex_dict[vertex_name] = now_id
                    now_id += 1
                in_edge_list = json_data["inCitations"]
                for in_edge in in_edge_list:
                    if in_edge not in vertex_dict:
                        vertex_dict[in_edge] = now_id
                        now_id += 1
                    if vertex_dict[in_edge] not in graph:
                        graph[vertex_dict[in_edge]] = []
                    graph[vertex_dict[in_edge]].append(vertex_dict[vertex_name])
                out_edge_list = json_data["outCitations"]
                for out_edge in out_edge_list:
                    if out_edge not in vertex_dict:
                        vertex_dict[out_edge] = now_id
                        now_id += 1
                    if vertex_dict[vertex_name] not in graph:
                        graph[vertex_dict[vertex_name]] = []
                    graph[vertex_dict[vertex_name]].append(vertex_dict[out_edge])
                line = f.readline()
    # print vertex num,edge num
    print("vertex num is ", len(vertex_dict))
    edge_sum = 0
    for k, v in graph.items():
        edge_sum += len(v)
    print("edge num = ", edge_sum)
    vertex_file = write_prefix + "citation.v"
    edge_file = write_prefix + "citation.e"
    map_file = write_prefix + "vertex.map"
    with open(vertex_file, "w") as f:
        for i in range(now_id):
            f.write(str(i) + "\t" + "0\n")
    with open(edge_file, "w") as f:
        for k, v in graph.items():
            for out_edge in v:
                f.write(str(k) + "\t" + str(out_edge) + "\t" + "1\n")
    with open(map_file, "w") as f:
        for k, v in vertex_dict.items():
            f.write(str(k) + "\t" + str(v) + "\n")


'''
data_prefix = "Project3_citation/"
write_prefix = "citation_graph/"

BuildData(data_prefix, write_prefix)
'''


def WriteResult(data_prefix, graph_prefix, write_prefix):
    vertex_map_file = graph_prefix + "citation_graph/vertex.map"
    score_map_file = graph_prefix + "pagerank_result/result_frag_0"
    vertex_map = {}
    score_map = {}
    with open(vertex_map_file, "r") as f:
        line = f.readline()
        while line is not None and line != "":
            arr = line.split("\t")
            sid = arr[0]
            vertex_id = int(arr[1].replace("\n", ""))
            vertex_map[sid] = vertex_id
            line = f.readline()
    with open(score_map_file, "r") as f:
        line = f.readline()
        while line is not None and line != "":
            arr = line.split(" ")
            vertex_id = int(arr[0])
            vertex_score = float(arr[1].replace("\n", ""))
            score_map[vertex_id] = vertex_score
            line = f.readline()
    for i in range(1, 6000):
        if i % 50 == 0:
            print("i = ", i)
        this_file = data_prefix + "citationLine" + str(i) + ".jsonl"
        f1 = open(write_prefix + "citationLine" + str(i) + ".jsonl", "w")
        with open(this_file, "r") as f:
            line = f.readline()
            while line is not None and line != "":
                json_data = simplejson.loads(line, encoding="utf-8", strict=False)
                json_data["Sid"] = vertex_map[json_data["Sid"]]
                if json_data["Sid"] in score_map:
                    json_data["score"] = score_map[json_data["Sid"]] * 100000000
                else:
                    json_data["score"] = 0.01
                in_edge_list = json_data["inCitations"]
                for i in range(len(in_edge_list)):
                    in_edge_list[i] = vertex_map[in_edge_list[i]]
                out_edge_list = json_data["outCitations"]
                for i in range(len(out_edge_list)):
                    out_edge_list[i] = vertex_map[out_edge_list[i]]
                json_str = simplejson.dumps(json_data)
                f1.write(json_str + "\n")
                line = f.readline()
        f1.close()


data_prefix = "Project3_citation/"
graph_prefix = ""
write_prefix = "rewrite_citation/"
WriteResult(data_prefix, graph_prefix, write_prefix)
