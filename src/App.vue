<template>
  <div id="app">
    <Index />
  </div>
</template>
<script>
import Index from "./views/Index"
export default {
  name: "App",
  components: {
    Index,
  },
}
</script>

<style lang="scss">
ul,
li {
  list-style: none;
  text-decoration: none;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
