<template>
  <q-card flat bordered class="my-card bg-grey-1">
    <q-card-section>
      <div class="row items-center no-wrap">
        <div class="col">
          <div class="text-h6">{{ data.title }}</div>
          <div class="text-subtitle2">id: {{ data.Sid }}</div>
        </div>
      </div>
    </q-card-section>
    <q-separator />
    <q-card-section>
      <div class="text-subtitle2">标题：{{ data.title }}</div>
    </q-card-section>
    <q-card-section>
      <div class="text-subtitle2">发表年份：{{ data.year }}</div>
    </q-card-section>
    <q-card-section>
      <div class="text-subtitle2">引文数量：{{ data.inCitationsCount }}</div>
    </q-card-section>
    <q-card-section>
      <div class="text-subtitle2">被引数量：{{ data.outCitationsCount }}</div>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  data() {
    return {
      lorem: "根据重要性分数，节点的大小或颜色应该有所区分.",
      data: {
        Sid: null,
        title: null,
        year: null,
        inCitationsCount: null,
        outCitationsCount: null,
      },
    };
  },
  computed: {
    nodeId: function () {
      return this.$store.getters["RelationGraph/getNodeId"];
    },
    defaultNodeSid: function () {
      return this.$store.getters["GlobalSearch/getFirstNodeSid"];
    },
  },
  watch: {
    nodeId: async function (val, oldVal) {
      if (val) {
        if (val != this.defaultNodeSid) {
          this.getPaperInfoBySid(val);
        }
      }
    },
    defaultNodeSid: async function (val, oldVal) {
      if (val) {
        this.getPaperInfoBySid(val);
      }
    },
  },
  methods: {
    async getPaperInfoBySid(sid) {
      this.$q.loading.show();

      let url = "/api/paper_info?Sid=" + sid;
      let res = await this.$axios.get(url);
      this.data = res.data;

      this.$q.loading.hide();
      console.log(res.data);
    },
  },
};
</script>
