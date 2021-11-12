<template>
  <div class="q-pa-md">
    <q-table
      :data="data"
      :columns="columns"
      :rows-per-page-options="[10, 15, 20]"
      row-key="sid"
      :filter="filter"
    >
      <template v-slot:top>
        <h5 class="q-pr-sm">{{ table_title }}</h5>
        <q-icon
          :name="toggle_icon"
          :color="toggle_icon_color"
          size="md"
          @click="exchange_result()"
        />

        <q-space />
        <q-input
          flat
          dense
          debounce="300"
          label="在结果中查找"
          v-model="filter"
        >
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
      </template>

      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td key="PaperId" :props="props">
            {{ props.row.sid }}
          </q-td>
          <q-td key="Title" :props="props">
            {{ props.row.title }}
          </q-td>
          <q-td key="Year" :props="props">
            {{ props.row.year }}
          </q-td>
          <q-td key="InCitationsCount" :props="props">
            {{ props.row.inCitationsCount }}
          </q-td>
          <q-td key="OutCitationsCount" :props="props">
            {{ props.row.outCitationsCount }}
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </div>
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
  },
  {
    name: "InCitationsCount",
    label: "被引次数",
    field: "inCitationsCount",
    align: "left",
  },
  {
    name: "OutCitationsCount",
    label: "引文数量",
    field: "outCitationsCount",
    align: "left",
  },
];

export default {
  data() {
    return {
      columns,
      show_es_res: false,
      loading_state: true,
      data: [],
      filter: "",
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
    toggle_icon: function () {
      if (this.show_es_res) {
        return "eva-toggle-left-outline";
      } else {
        return "eva-toggle-right";
      }
    },
    toggle_icon_color: function () {
      if (this.show_es_res) {
        return "grey";
      } else {
        return "green";
      }
    },
  },
  async mounted() {
    let refined_url = "/api/search-result/belif-refined/" + "[query]";
    // console.log(this.table_title)

    // let res = await this.$axios.get(refined_url);
    // this.data = res.data;
    this.data = [
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
    exchange_result() {
      this.show_es_res = !this.show_es_res;
      if (this.show_es_res) {
        console.log("/api/es_result/query/get");
      } else {
        console.log("/api/belif_refined_result/query/get");
      }
    },
  },
};
</script>
