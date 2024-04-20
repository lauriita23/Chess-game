<script setup>
  import { RouterLink, RouterView } from 'vue-router';
</script>

<template>
  <header>
    <div class="wrapper">
      <ul>
        <li><RouterLink to="/log-in">LogIn</RouterLink></li>
        <li><RouterLink to="/my-view">MyView</RouterLink></li>
        <li><RouterLink to="/sign-up">SignUp</RouterLink></li>
        <li><RouterLink to="/log-out">LogOut</RouterLink></li>
        <li><RouterLink to="/creategame">CreateGame</RouterLink></li>
      </ul>
    </div>
  </header>
  <RouterView />  
</template>
