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
      <!-- <div > -->
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
        debounce="500"
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
      <!-- </div> -->
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
    dquery: function () {
      return this.query;
    },
  },
  watch: {
    dquery: async function (val, oldVal) {
      if (val) {
        this.commit_new_query = true;
      }
    },
  },
  async mounted() {
    // this.dquery = this.query;
    // let refined_url = "/api/search-result/belif-refined/" + "[query]";
    // let res = await this.$axios.get(refined_url);
    // this.data = res.data;
    // this.data_intensified = [
    //   {
    //     sid: "1213.32",
    //     title: "Scaphopoda (Bronn, 1862): Work in progress",
    //     inCitations: [],
    //     outCitations: [],
    //     year: 2020,
    //     inCitationsCount: 0,
    //     outCitationsCount: 3,
    //   },
    //   {
    //     sid: "212.33",
    //     title: "Mooda (Bronn, 1862): Work in progress",
    //     inCitations: [],
    //     outCitations: [],
    //     year: 2021,
    //     inCitationsCount: 20,
    //     outCitationsCount: 3,
    //   },
    //   {
    //     sid: "3231.32",
    //     title: "Work in progress",
    //     inCitations: [],
    //     outCitations: [],
    //     year: 2000,
    //     inCitationsCount: 0,
    //     outCitationsCount: 33,
    //   },
    // ];
  },
  methods: {
    expand_table() {
      this.expandAll = !this.expandAll;
    },
    focus_node(id) {
      if (this.enableFocus) {
        console.log("enableFocus!");
      }
      console.log("get:" + id);
    },
    shift_search_type() {
      this.search_in_table = !this.search_in_table;
      this.search_filter = "";
    },
    async submit() {
      this.$q.loading.show();
      let url = "/api/retrieval/intensified?query=" + this.dquery;
      let num = 100;

      if (this.data_intensified.length == 0 || this.commit_new_query) {
        console.log(url);

        let res = await this.$axios.get(url);
        this.data_intensified = res.data.paper_list;
        this.data_intensified.forEach((nd) => {
          if (nd.title.length > num) {
            nd.title = nd.title.substr(0, num) + "...";
          }
        });
        this.commit_new_query = false;
      }
      this.$q.loading.hide();
    },
  },
};
</script>
