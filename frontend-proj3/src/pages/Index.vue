<template>
  <q-page class="flex flex-center">
    <div class="q-gutter-y-md column" style="width: 40%">
      <q-input v-model="query" placeholder="Search" debounce="500" bottom-slots>
        <template v-slot:prepend>
          <q-btn-dropdown flat dense>
            <template v-slot:label>
              <q-icon left name="menu" />
            </template>

            <q-list>
              <q-item clickable v-close-popup @click="onItemClick('table')">
                <q-item-section>
                  <q-item-label>table</q-item-label>
                </q-item-section>
              </q-item>

              <q-item clickable v-close-popup @click="onItemClick('graph')">
                <q-item-section>
                  <q-item-label>graph</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </template>

        <template v-slot:append>
          <q-icon name="search" @click="submit" />
        </template>

        <template v-slot:hint>
          {{ search_hint }}
        </template>
      </q-input>
    </div>
  </q-page>
</template>

<script>
export default {
  name: "PageIndex",
  data() {
    return {
      query: "",
      search_type: "graph",
    };
  },
  computed: {
    search_hint: function () {
      switch (this.search_type) {
        case "graph":
          return "for Relation Graph";
        case "table":
          return "for Table";

        default:
          return null;
      }
    },
  },
  methods: {
    async submit() {
      // this.loadingState = true;

      // this.$q.notify({
      //   type: "positive",
      //   message: this.query,
      //   timeout: 1500,
      //   position: "top",
      // });

      let url = "/search-result/" + this.search_type;
      this.$router.push({ path: url, query: { user_query: this.query } });
    },
    onItemClick(choice) {
      this.search_type = choice;
    },
  },
};
</script>
