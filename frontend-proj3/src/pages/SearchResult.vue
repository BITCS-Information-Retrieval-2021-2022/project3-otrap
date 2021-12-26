<template>
  <div class="q-pa-md">
    <q-table
      :data="data"
      :columns="columns"
      :rows-per-page-options="[15, 30, 60]"
      row-key="Sid"
      :filter="filter"
    >
      <template v-slot:top coloum>
        <h5 class="q-pr-sm">{{ table_title }}</h5>
        <q-icon
          :name="toggle_icon"
          :color="toggle_icon_color"
          size="md"
          @click="exchange_result()"
        />

        <q-space />
        <q-btn
          flat
          rounded
          color="secondary"
          icon="eva-repeat-outline"
          @click="shift_search_type"
        />
        <q-input
          class="q-px-md"
          v-model="filter"
          flat
          debounce="300"
          label="在结果中查找"
          style="width: 300px"
          v-if="search_in_table"
        >
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
        <q-input
          class="q-px-md"
          v-model="query"
          placeholder="Search"
          debounce="500"
          label="新的查询"
          bottom-slots
          style="width: 300px"
          v-else
        >
          <template v-slot:append>
            <q-icon name="search" @click="submit" />
          </template>
        </q-input>
      </template>

      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td key="PaperId" :props="props">
            {{ props.row.Sid }}
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
          <q-td key="Score" :props="props" v-if="!show_es_res">
            {{ props.row.score }}
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
  data() {
    return {
      columns,
      show_es_res: false,
      data_basic: [],
      data_intensified: [],
      filter: "",
      query: "",
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
    retrieval_type: function () {
      if (this.show_es_res) {
        return "basic";
      } else {
        return "intensified";
      }
    },
    data: function () {
      if (this.show_es_res) {
        return this.data_basic;
      } else {
        return this.data_intensified;
      }
    },
  },
  watch: {
    query: async function (val, oldVal) {
      if (val) {
        this.commit_new_query = true;
      }
    },
    show_es_res: function (val, oldVal) {
      if (this.show_es_res) {
        this.columns = this.columns.slice(0, -1);
      } else {
        this.columns.push({
          name: "Score",
          label: "重要性分数",
          field: "score",
          align: "left",
          sortable: true,
        });
      }
    },
  },
  async mounted() {
    this.query = this.$route.query.user_query;
    this.submit();
  },
  methods: {
    async exchange_result() {
      this.show_es_res = !this.show_es_res;

      this.submit();
    },
    async submit() {
      this.$q.loading.show();
      let url =
        "/api/retrieval/" + this.retrieval_type + "?query=" + this.query;
      let num = 100;

      if (
        this.retrieval_type == "basic" &&
        (this.data_basic.length == 0 || this.commit_new_query)
      ) {
        console.log(url);

        let res = await this.$axios.get(url);
        this.data_basic = res.data.paper_list;
        this.data_basic.forEach((nd) => {
          if (nd.title.length > num) {
            nd.title = nd.title.substr(0, num) + "...";
          }
        });
        this.commit_new_query = false;
      } else if (
        this.retrieval_type == "intensified" &&
        (this.data_intensified.length == 0 || this.commit_new_query)
      ) {
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
    shift_search_type() {
      this.search_in_table = !this.search_in_table;
      this.filter = "";
    },
  },
};
</script>
