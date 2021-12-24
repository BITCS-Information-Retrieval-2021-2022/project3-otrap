<template>
  <q-card flat bordered class="my-card bg-grey-1">
    <q-card-section>
      <div class="row items-center no-wrap">
        <div class="col">
          <div class="text-h6">{{ nodeTitle }}</div>
          <div class="text-subtitle2">id: {{ nodeId }}</div>
        </div>
      </div>
    </q-card-section>
    <q-separator />
    <q-card-section>
      <div class="text-subtitle2">{{ lorem }}</div>
    </q-card-section>
    <q-card-section> abstract </q-card-section>
  </q-card>
</template>

<script>
export default {
  data() {
    return {
      lorem: "根据重要性分数，节点的大小或颜色应该有所区分.",
      data: null,
    };
  },
  computed: {
    nodeTitle: function () {
      return this.$store.getters["RelationGraph/getNodeTitle"];
    },
    nodeId: function () {
      return this.$store.getters["RelationGraph/getNodeId"];
    },
  },
  watch: {
    nodeId: async function (val, oldVal) {
      if (val) {
        let url = "/api/paper_info?sid=" + this.nodeId;
        let res = await this.$axios.get(url);
        console.log(res.data);
        this.data = res.data;
      }
    },
  },
};
</script>
