<template>
  <q-table
    :data="tdata"
    :columns="dy_columns"
    :title="table_title"
    :rows-per-page-options="[10, 15, 20]"
    :row-key="dy_sid"
    :filter="search_filter"
  >
    <template v-slot:top="props">
      <q-space />
      <q-input flat debounce="300" label="在结果中查找" v-model="search_filter">
        <template v-slot:append>
          <q-icon name="search" />
        </template>
      </q-input>
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
      <q-tr :props="props">
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
    field: "sid",
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
];

export default {
  name: "SearchTable",
  props: {
    query: {
      type: String,
    },
  },
  data() {
    return {
      columns,
      show_es_res: false,
      loading_state: true,
      tdata: [],
      expandAll: false,
      search_filter: "",
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
  },
  async mounted() {
    let refined_url = "/api/search-result/belif-refined/" + "[query]";

    // let res = await this.$axios.get(refined_url);
    // this.data = res.data;
    this.tdata = [
      {
        sid: "1213.32",
        title: "Scaphopoda (Bronn, 1862): Work in progress",
        inCitations: [],
        outCitations: [],
        year: 2020,
        inCitationsCount: 0,
        outCitationsCount: 3,
      },
      {
        sid: "212.33",
        title: "Mooda (Bronn, 1862): Work in progress",
        inCitations: [],
        outCitations: [],
        year: 2021,
        inCitationsCount: 20,
        outCitationsCount: 3,
      },
      {
        sid: "3231.32",
        title: "Work in progress",
        inCitations: [],
        outCitations: [],
        year: 2000,
        inCitationsCount: 0,
        outCitationsCount: 33,
      },
    ];
  },
  methods: {
    expand_table() {
      this.expandAll = !this.expandAll;
    },
    // toggleFullscreen() {
    //   this.expandAll = !this.expandAll;
    // },
  },
};
</script>
