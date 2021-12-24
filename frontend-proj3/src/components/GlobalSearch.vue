<template >
  <q-input
    :loading="loadingState"
    v-model="text"
    placeholder="Search"
    debounce="600"
    bottom-slots
  >
    <template v-slot:append>
      <q-icon name="search" v-show="!loadingState" @click="submit" />
    </template>

    <template v-slot:hint>
      {{ search_hint }}
    </template>
  </q-input>
</template>

<script>
export default {
  data() {
    return {
      text: "",
      loadingState: false,
    };
  },
  methods: {
    async submit() {
      this.loadingState = true;

      this.$q.notify({
        type: "positive",
        message: this.query,
        timeout: 1500,
        position: "top",
      });

      //   this.$store.commit("GobalSearch/setQuery", this.text);
      await this.$store.dispatch("GobalSearch/search", this.text);
      this.loadingState = false;
      // async 查询
      // global save
      console.log("update");
    },
  },
};
</script>