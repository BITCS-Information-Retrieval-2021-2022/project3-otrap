<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="left = !left" />

        <q-toolbar-title>
          <q-icon class="q-pr-md" name="eva-home" @click="toHomePage" />
          引文网络子图
        </q-toolbar-title>

        <q-btn dense flat round icon="menu" @click="right = !right" />
      </q-toolbar>
    </q-header>

    <!-- left drawer content -->
    <q-drawer
      show-if-above
      v-model="left"
      side="left"
      elevated
      content-class="bg-grey-3"
    >
      <div class="q-pa-sm">
        <search-table :query="search_query" enableToggle="true" />
      </div>
    </q-drawer>

    <q-page-container class="fit">
      <router-view />
    </q-page-container>

    <!-- right drawer content -->
    <q-drawer
      show-if-above
      v-model="right"
      side="right"
      elevated
      content-class="bg-grey-3"
    >
      <div class="q-pa-sm">
        <paper-info-card class="fit" />
      </div>
    </q-drawer>
  </q-layout>
</template>

<script>
import SearchTable from "src/components/SearchTable.vue";
import PaperInfoCard from "src/components/PaperInfoCard.vue";

export default {
  components: { SearchTable, PaperInfoCard },
  data() {
    return {
      left: false,
      right: false,
      search_query: "",
    };
  },
  methods: {
    toHomePage() {
      this.$router.push("/");
    },
  },
};
</script>


<style lang="sass" scoped>
.drawer-bg
  color: $blue-grey-10
</style>