<template>
  <div>
    <div class="row justify-center items-start no-wrap">
      <div id="relation_graph" class="my-graph"></div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
  computed: {
    global_query: function () {
      console.log(
        "get glb_query:" + this.$store.getters["GlobalSearch/getQuery"]
      );
      return this.$store.getters["GlobalSearch/getQuery"];
    },
  },
  watch: {
    global_query: async function (val, oldVal) {
      if (val) {
        console.log("re-render graph");
        this.rerender_graph3();
      }
    },
  },
  mounted() {
    let url = "/api/relation_graph?query=" + this.$route.query.user_query;
    var echarts = require("echarts");
    // this.graph_render(echarts, url);
    // this.toy_model_render(echarts); // 点击 “话题分析” 添加节点

    this.graph_render3(echarts, url);
  },
  methods: {
    // toy template 1
    async graph_render(echarts, url) {
      var ROOT_PATH =
        "https://cdn.jsdelivr.net/gh/apache/echarts-website@asf-site/examples";

      var myChart = echarts.init(document.getElementById("relation_graph"));

      myChart.showLoading();
      let res = await this.$axios.get(
        ROOT_PATH + "/data/asset/data/les-miserables.json"
      );
      let res2 = await this.$axios.get(url);
      myChart.hideLoading();
      // console.log(res.data);
      console.log("show data:");
      console.log(res2.data);

      var option = this.process_data(res.data);
      myChart.setOption(option);

      this.manipulate_data(myChart);
    },
    process_data(graph) {
      graph.nodes.forEach(function (node) {
        node.label = {
          show: node.symbolSize > 30,
        };
      });
      // console.log("show data:");
      // console.log(graph);
      // console.log(graph.links[0]);

      // console.log(graph.nodes[0]);
      // console.log(graph.nodes[1]);

      let option = {
        title: {
          text: "关系图",
          subtext: "Default layout",
          top: "bottom",
          left: "right",
        },
        tooltip: {},

        legend: [
          {
            // selectedMode: 'single',
            data: graph.categories.map(function (a) {
              return a.name;
            }),
          },
        ],
        animationDuration: 1500,
        animationEasingUpdate: "quinticInOut",
        series: [
          {
            name: "Les Miserables",
            type: "graph",
            layout: "none",
            data: graph.nodes,
            links: graph.links,
            categories: graph.categories,
            roam: true,
            label: {
              position: "right",
              formatter: "{b}",
            },
            lineStyle: {
              color: "source",
              curveness: 0.3,
            },
            emphasis: {
              focus: "adjacency",
              lineStyle: {
                width: 10,
              },
            },
            // edgeSymbol: ["none", "arrow"], 难看
          },
        ],
      };
      return option;
    },
    // template 3
    async graph_render3(echarts, url) {
      var myChart = echarts.init(document.getElementById("relation_graph"));
      myChart.showLoading();

      console.log(url);
      let res = await this.$axios.get(url);

      myChart.hideLoading();

      console.log("show graph data:");
      console.log(res.data);

      let webkitDep = res.data;
      // preprocess
      var dict = {};
      let smin = 1;
      let smax = -1;
      // let norm = 0;
      let symbolSizeScale = 30;
      webkitDep.nodes.map(function (node) {
        // node.symbolSize = Math.exp(node.score);
        // norm += node.symbolSize;
        smin = Math.min(smin, node.score);
        smax = Math.max(smax, node.score);
        return node;
      });
      webkitDep.nodes.forEach(function (node, idx) {
        node.id = idx;
        dict[node.Sid] = node.id;
        // node.symbolSize = (symbolSizeScale * node.symbolSize) / norm;
        node.score = (node.score - smin) / (smax - smin + smin);
        // node.symbolSize = symbolSizeScale * Math.pow(2 * node.score - 1, 3) + 1;
        let tmp = (1 / 5) * Math.tan(Math.PI * (node.score - 0.5)) + 0.5;
        if (tmp > 0.8) {
          tmp = Math.min(tmp, 0.8);
        }
        if (tmp < 0.1) {
          tmp = Math.max(tmp, 0.1);
        }
        node.symbolSize = symbolSizeScale * tmp;

        return node;
      });
      webkitDep.links.map(function (link) {
        link.source = dict[link.source];
        link.target = dict[link.target];
        return link;
      });

      var option = {
        legend: {
          data: ["引用", "搜索结果", "被引"],
        },
        series: [
          {
            type: "graph",
            layout: "force",
            animation: false,
            label: {
              position: "right",
              formatter: "{b}",
            },
            draggable: true,
            data: webkitDep.nodes,
            categories: webkitDep.categories,
            force: {
              edgeLength: 5,
              repulsion: 20,
              gravity: 0.2,
            },
            edges: webkitDep.links,
          },
        ],
      };

      option && myChart.setOption(option);
      this.manipulate_data(myChart);
    },
    manipulate_data(myChart) {
      myChart.on(
        "click",
        function (params) {
          console.log("show click params:");
          console.log(params);

          if (params.name == null) {
            return;
          }

          if (params.dataType == "node") {
            console.log("show click node");
            console.log(params.data);
            this.$store.commit("RelationGraph/setNodeId", params.data.Sid);
            // this.$store.commit("RelationGraph/setNodeTitle", params.data.name);
            // console.log(this.$store.state.RelationGraph.nodeId)
            // console.log(this.$store.getters["RelationGraph/getNodeId"]);
          } else if (params.dataType == "edge") {
            console.log("show click edge");
            console.log(params);
            this.$store.commit("RelationGraph/setEdge", params.data);
            let e = this.$store.getters["RelationGraph/getEdge"];
            console.log(e.source, "->", e.target);
          }
        }.bind(this)
      );
    },
    async rerender_graph3() {
      var echarts = require("echarts");
      this.graph_render3(echarts, url);
    },
    // toy template 2
    toy_model_render(echarts) {
      var myChart = echarts.init(document.getElementById("relation_graph"));
      var option = {
        backgroundColor: "#1a4377",

        tooltip: {},
        animationDurationUpdate: 1500,
        animationEasingUpdate: "quinticInOut",
        color: ["#83e0ff", "#45f5ce", "#b158ff"],
        series: [
          {
            type: "graph",
            layout: "force",
            force: {
              repulsion: 1000,
              edgeLength: 50,
            },
            roam: true,
            label: {
              normal: {
                show: true,
              },
            },
            data: this.toy_get_data(),
            links: this.toy_get_links(),
            lineStyle: {
              normal: {
                opacity: 0.9,
                width: 5,
                curveness: 0,
              },
            },
            categories: [{ name: "0" }, { name: "1" }, { name: "2" }],
          },
        ],
      };
      myChart.setOption(option);

      // 事件=>增加数据，重新渲染
      this.toy_append_data(myChart);
    },
    toy_get_links() {
      var linkmes = [];
      linkmes.push(
        {
          source: "校园大数据",
          target: "舆情大数据",
        },
        {
          source: "校园大数据",
          target: "图书馆分析",
        },
        {
          source: "舆情大数据",
          target: "用户分析",
        },
        {
          source: "舆情大数据",
          target: "话题分析",
        },
        {
          source: "舆情大数据",
          target: "评论分析",
        },
        {
          source: "校园大数据",
          target: "图书馆分析",
        },
        {
          source: "图书馆分析",
          target: "图书分析",
        },
        {
          source: "图书馆分析",
          target: "借阅分析",
        },
        {
          source: "图书馆分析",
          target: "借阅排行",
          value: "DNA",
        },
        {
          source: "图书馆分析",
          target: "图书收录",
        }
      );
      return linkmes;
    },
    toy_get_data() {
      var datas = [];
      datas.push(
        {
          name: "校园大数据",

          symbolSize: 120,
          draggable: true,
          category: 0,
          itemStyle: {
            normal: {
              borderColor: "#04f2a7",
              borderWidth: 6,
              shadowBlur: 20,
              shadowColor: "#04f2a7",
              color: "#001c43",
            },
          },
        },
        {
          name: "舆情大数据",
          symbolSize: 100,
          itemStyle: {
            normal: {
              borderColor: "#04f2a7",
              borderWidth: 4,
              shadowBlur: 10,
              shadowColor: "#04f2a7",
              color: "#001c43",
            },
          },
          category: 1,
        },
        {
          name: "用户分析",
          symbolSize: 80,
          category: 1,
          itemStyle: {
            normal: {
              borderColor: "#04f2a7",
              borderWidth: 4,
              shadowBlur: 10,
              shadowColor: "#04f2a7",
              color: "#001c43",
            },
          },
        },
        {
          name: "话题分析",
          symbolSize: 80,
          category: 1,
          itemStyle: {
            normal: {
              borderColor: "#82dffe",
              borderWidth: 4,
              shadowBlur: 10,
              shadowColor: "#04f2a7",
              color: "#001c43",
            },
          },
        },
        {
          name: "评论分析",
          symbolSize: 80,
          category: 1,
          itemStyle: {
            normal: {
              borderColor: "#82dffe",
              borderWidth: 4,
              shadowBlur: 10,
              shadowColor: "#04f2a7",
              color: "#001c43",
            },
          },
        },
        {
          name: "图书馆分析",
          symbolSize: 100,
          category: 2,
          itemStyle: {
            normal: {
              borderColor: "#82dffe",
              borderWidth: 4,
              shadowBlur: 10,
              shadowColor: "#04f2a7",
              color: "#001c43",
            },
          },
        },
        {
          name: "借阅分析",
          symbolSize: 80,
          category: 2,
          itemStyle: {
            normal: {
              borderColor: "#b457ff",
              borderWidth: 4,
              shadowBlur: 10,
              shadowColor: "#b457ff",
              color: "#001c43",
            },
          },
        },
        {
          name: "借阅排行",
          symbolSize: 80,
          itemStyle: {
            normal: {
              borderColor: "#82dffe",
              borderWidth: 4,
              shadowBlur: 10,
              shadowColor: "#04f2a7",
              color: "#001c43",
            },
          },
          category: 2,
        },
        {
          name: "图书收录",
          symbolSize: 80,
          itemStyle: {
            normal: {
              borderColor: "#82dffe",
              borderWidth: 4,
              shadowBlur: 10,
              shadowColor: "#04f2a7",
              color: "#001c43",
            },
          },
          category: 2,
        },
        {
          name: "图书分析",
          symbolSize: 80,
          category: 2,
          itemStyle: {
            normal: {
              borderColor: "#82dffe",
              borderWidth: 4,
              shadowBlur: 10,
              shadowColor: "#04f2a7",
              color: "#001c43",
            },
          },
        }
      );
      return datas;
    },
    toy_append_data(myChart) {
      var datas = this.toy_get_data();
      var linkmes = this.toy_get_links();
      myChart.on("click", function (params) {
        console.log("log params:");
        console.log(params);

        if (params.name != null) {
          //var mes=params.name.replace(/\d+/g,"")
          if (params.name == "话题分析") {
            //这里我用到了params.name，当我们点击的节点的name的值为“话题分析”时就会进入下面的方法

            datas.push({
              name: "图书分析a",
              symbolSize: 80,
              category: 2,
              itemStyle: {
                normal: {
                  borderColor: "#82dffe",
                  borderWidth: 4,
                  shadowBlur: 10,
                  shadowColor: "#04f2a7",
                  color: "#001c43",
                },
              },
            });
            //上面就是把新数据添加到datas里面
            linkmes.push({
              source: "图书分析a",
              target: "话题分析",
            });
            //上面就是把连接关系添加到linkmes数组中

            //重新画关系图
            myChart.setOption({
              series: [
                {
                  data: datas,
                  links: linkmes,
                },
              ],
            });
          }
        }
      });
    },
  },
};
</script>


<style lang="sass" scoped>
.my-graph
  width: 100%
  height: 100%
  background: $blue-grey-1
  position: absolute
</style>
