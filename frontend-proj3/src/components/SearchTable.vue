<template>
  <q-table
    :data="data_intensified"
    :columns="dy_columns"
    :title="table_title"
    :rows-per-page-options="[50, 100]"
    :row-key="dy_sid"
    :filter="search_filter"
  >
    <template v-slot:top="props" class="row items-center no-wrap">
      <q-input
        class="q-px-md"
        v-model="search_filter"
        flat
        debounce="300"
        label="在结果中查找"
        v-if="search_in_table"
      >
        <template v-slot:append>
          <q-icon name="search" />
        </template>
      </q-input>
      <q-input
        class="q-px-md"
        v-model="dquery"
        placeholder="Search"
        debounce="300"
        label="新的查询"
        bottom-slots
        v-else
      >
        <template v-slot:append>
          <q-icon name="search" @click="submit" />
        </template>
      </q-input>

      <q-btn
        flat
        rounded
        color="secondary"
        icon="eva-repeat-outline"
        @click="shift_search_type"
      />
      <q-btn
        flat
        round
        dense
        :icon="props.inFullscreen ? 'fullscreen_exit' : 'fullscreen'"
        @click="
          props.toggleFullscreen();
          expand_table();
        "
        class="q-ml-md"
      />
    </template>

    <template v-slot:body="props">
      <q-tr :props="props" @mouseenter="focus_node(props.row.sid)">
        <template v-if="expandAll">
          <q-td key="PaperId" :props="props">
            {{ props.row.sid }}
          </q-td>
        </template>
        <q-td key="Title" :props="props" class="">
          {{ props.row.title }}
        </q-td>
        <template v-if="expandAll">
          <q-td key="Year" :props="props">
            {{ props.row.year }}
          </q-td>
          <q-td key="InCitationsCount" :props="props">
            {{ props.row.inCitationsCount }}
          </q-td>
          <q-td key="OutCitationsCount" :props="props">
            {{ props.row.outCitationsCount }}
          </q-td>
        </template>
      </q-tr>
    </template>
  </q-table>
</template>

<script>
const columns = [
  {
    name: "PaperId",
    label: "标识符",
    field: "Sid",
    align: "center",
  },
  {
    name: "Title",
    label: "论文题目",
    field: "title",
    align: "center",
  },
  {
    name: "Year",
    label: "年份",
    field: "year",
    align: "left",
    sortable: true,
  },
  {
    name: "InCitationsCount",
    label: "被引次数",
    field: "inCitationsCount",
    align: "left",
    sortable: true,
  },
  {
    name: "OutCitationsCount",
    label: "引文数量",
    field: "outCitationsCount",
    align: "left",
    sortable: true,
  },
  {
    name: "Score",
    label: "重要性分数",
    field: "score",
    align: "left",
    sortable: true,
  },
];

export default {
  name: "SearchTable",
  props: {
    query: {
      type: String,
    },
    enableFocus: {
      type: Boolean,
    },
  },
  data() {
    return {
      columns,
      show_es_res: false,
      loading_state: true,
      data_intensified: [],
      expandAll: false,
      search_filter: "",
      search_in_table: false,
      commit_new_query: false,
      dquery: "",
    };
  },
  computed: {
    show_belif_refined_res: function () {
      return !this.show_es_res;
    },
    table_title: function () {
      if (this.show_es_res) {
        return "ElasticSearch基础检索结果";
      } else {
        return '基于"引文网络重要性分数"改善后的检索结果';
      }
    },
    dy_columns: function () {
      if (this.expandAll) {
        return this.columns;
      } else {
        return this.columns.slice(1, 2);
      }
    },
    dy_sid: function () {
      if (this.expandAll) {
        return "sid";
      } else {
        // console.log("dy_sid:" + this.dy_columns[0].field);
        return this.dy_columns[0].field;
      }
    },
    paperTitle: function () {
      return this.$store.getters["RelationGraph/getNodeTitle"];
    },
    global_query: function () {
      return this.$store.getters["GlobalGraph/getQuery"];
    },
  },
  watch: {
    dquery: async function (val, oldVal) {
      if (val) {
        // console.log("detected");
        this.commit_new_query = true;
        // this.submit();
      }
    },
  },
  async mounted() {
    this.dquery = this.query; // props to data
    this.submit();
    console.log(this.global_query);
  },
  methods: {
    expand_table() {
      this.expandAll = !this.expandAll;
    },
    focus_node(id) {
      // if (this.enableFocus) {
      //   console.log("enableFocus!");
      // }
      // console.log("get:" + id);
    },
    shift_search_type() {
      this.search_in_table = !this.search_in_table;
      this.search_filter = "";
    },
    async submit() {
      this.$q.loading.show();
      let url = "/api/retrieval/intensified?query=" + this.dquery;
      let num = 20;

      if (this.data_intensified.length == 0 || this.commit_new_query) {
        console.log(url);

        let res = await this.$axios.get(url);
        console.log("show table data");
        console.log(res.data);
        this.data_intensified = res.data.paper_list;
        this.data_intensified.forEach((nd) => {
          if (nd.title.length > num) {
            nd.title = nd.title.substr(0, num) + "...";
          }
        });
        this.commit_new_query = false;
        // used for PaperInfo initialization
        this.$store.commit(
          "GlobalSearch/setFirstNodeSid",
          this.data_intensified[0].Sid
        );
        // used for relation graph re-rendering
        this.$store.commit("GlobalSearch/setQuery", this.dquery);
      }
      this.$q.loading.hide();
    },
  },
};
</script>
