<script setup>
import { RouterLink, RouterView } from 'vue-router'

</script>

<template>
  <header>
    <div class="wrapper">
      <ul>
        <li><RouterLink to="/log-in">Log in</RouterLink></li>
        <li><RouterLink to="/my-view">MyView</RouterLink></li>
      </ul>
    </div>
  </header>  
</template>
