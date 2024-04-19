// import { createApp } from 'vue'
// import App from './App.vue'

// import './assets/main.css'

// createApp(App).mount('#app')

import { createApp } from 'vue'
import { createPinia } from 'pinia'

// Importa el componente principal App desde el archivo App.vue
import App from './App.vue'
import router from './router'

const myapp = createApp(App)
const pinia = createPinia()

myapp.use(pinia)
myapp.use(router)
myapp.mount('#app')