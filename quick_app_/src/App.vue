<script setup>
  import { RouterLink, RouterView } from 'vue-router';
</script>

<template>
  <header class="header">
    <div class="wrapper">
      <ul class="nav-links">
        <li><RouterLink to="/log-in">Home</RouterLink></li>
        <li><RouterLink to="/sign-up">SignUp</RouterLink></li>
        <li><RouterLink to="/log-out" data-cy="logOutLink">LogOut</RouterLink></li>
      </ul>
    </div>
  </header>
  <RouterView />  
</template>

<style scoped>
.wrapper {
  max-width: 1800px; 
  margin: 0 auto;
}

.nav-links {
  list-style: none; 
  padding: 0; 
  display: flex;
}

.nav-links li {
  margin-right: 20px; 
}

.nav-links li:last-child {
  margin-right: 0; 
}

.nav-links li a {
  text-decoration: none; 
  color: white; 
}

.nav-links li a:hover {
  color: rgb(133, 133, 133); 
}

.header {
  background-color: black;
  padding: 1px 0;
  font-family: Arial, Helvetica, sans-serif;
}
</style>
