<template>
  <q-layout view="lHh LpR fFf">
    <q-header elevated>
      <q-toolbar>
        <q-toolbar-title>
          <q-icon class="q-pr-md" name="eva-home" @click="toHomePage" />
          otrap of project 3
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
export default {
  name: "MainLayout",
  methods: {
    toHomePage() {
      if (this.$route.path != "/") {
        this.$router.push("/");
      }
    },
  },
};
</script>
