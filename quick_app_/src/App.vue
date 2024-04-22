<script setup>
  import { RouterLink, RouterView } from 'vue-router';
</script>

<template>
  <header class="header">
    <div class="wrapper">
      <ul class="nav-links">
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

<style scoped>
.wrapper {
  max-width: 1800px; /* Cambiar el ancho máximo según sea necesario */
  margin: 0 auto;
}

.nav-links {
  list-style: none; /* Quitar los puntos de la lista */
  padding: 0; /* Eliminar el relleno por defecto */
  display: flex; /* Mostrar los elementos en línea */
}

.nav-links li {
  margin-right: 20px; /* Espacio entre los elementos */
}

.nav-links li:last-child {
  margin-right: 0; /* No agregar margen al último elemento */
}

.nav-links li a {
  text-decoration: none; /* Quitar el subrayado del enlace */
  color: white; /* Cambiar el color del texto a blanco */
}

.nav-links li a:hover {
  color: rgb(133, 133, 133); /* Cambiar el color del texto al pasar el ratón */
}

.header {
  background-color: black; /* Fondo negro */
  padding: 1px 0; /* Agregar relleno superior e inferior al encabezado */
}
</style>
