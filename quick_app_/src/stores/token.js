import { defineStore } from 'pinia'

export const useTokenStore = defineStore("tokens",
{
    // id : 'token',
    state: () => ({
        token: null,
        isAuthenticated: false,
        gameID: null,
        userID: null,
        board_state: null,
    }),
    actions: {
        setToken(token) {
            this.token = token
            this.isAuthenticated = true
        },
        removeToken() {
            this.token = null
            this.isAuthenticated = false
        }
    }
})