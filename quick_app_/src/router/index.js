import { createRouter, createWebHistory } from 'vue-router'

import LogIn from '../views/LogIn.vue'
import Play from '../views/Play.vue'
import SignUp from '../views/SignUp.vue'
import LogOut from '../views/LogOut.vue'
import CreateGame from '../views/CreateGame.vue'


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/log-in',
            name: 'LogIn',
            component: LogIn
        },
        {
            path: '/',
            redirect: '/log-in'
        },
        {
            path: '/play',
            name: 'Play',
            component: Play
        },
        {
            path: '/sign-up',
            name: 'SignUp',
            component: SignUp
        },
        {
            path: '/log-out',
            name: 'LogOut',
            component: LogOut
        },
        {
            path: '/creategame',
            name: 'CreateGame',
            component: CreateGame
        },
    ]
})

export default router