<template>
  <div class="q-pa-md">
    <q-table
      :data="data"
      :columns="columns"
      :rows-per-page-options="[10, 15, 20]"
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
        <q-input
          v-model="query"
          placeholder="Search"
          debounce="500"
          bottom-slots
        >
          <template v-slot:append>
            <q-icon name="search" @click="submit" />
          </template>

          <template v-slot:hint>
            {{ search_hint }}
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
      // loading_state: true,
      data: [],
      filter: "",
      query: "",
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
    search_hint: function () {
      return this.query;
    },
    retrieval_type: function () {
      if (this.show_es_res) {
        return "basic";
      } else {
        return "intensified";
      }
    },
  },
  async mounted() {
    this.query = this.$route.query.user_query;
    this.submit();

    // this.data = [
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
    // ];
  },
  methods: {
    async exchange_result() {
      this.show_es_res = !this.show_es_res;

      this.submit();
    },
    async submit() {
      let res = await this.$axios.get(
        "/api/retrieval/" + this.retrieval_type + "?query=" + this.query
      );
      console.log(res.data);
      this.data = res.data;
    },
  },
};
</script>
