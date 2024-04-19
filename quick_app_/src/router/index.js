import { createRouter, createWebHistory } from 'vue-router'

import LogIn from '../views/LogIn.vue'
import MyView from '../views/MyView.vue'
import SignUp from '../views/SignUp.vue'
import LogOut from '../views/LogOut.vue'
import CreateGame from '../views/CreateGame.vue'


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'LogIn',
            component: LogIn
        },
        {
            path: '/log-in',
            name: 'LogIn',
            component: LogIn
        },
        {
            path: '/my-view',
            name: 'MyView',
            component: MyView
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