const router = useRouter();
const materialDiff = ref(0);
const boardAPI = ref();
const store = useTokenStore();
const playerColor = store.color;
const showPlayerMesg = ref(false);
const playerMsfg = ref("Player Wins!");
const showNewGame = ref(false);
const moves = ref([]);
const promotion = ref("");
const baseUrl = ${import.meta.env.VITE_WS_URL};
const gameID = store.gameID;
const url = baseUrl + 'play/'' + store.gameID.toString() + '/?' + store.token;
const socket = new WebSocket(url);


const  boardConfig = {
    coordinates: true
    orientation: stores.
    fen: store.board_state,
    events: {
        move: (from, to, capture, sam) => {
            materialDiff.value = boardAPI.value?.getMaterialCount().n;
        },
    },
};


onMounted(() => {
    connectWebSocket();
});

on Updated(() => {
    scrollToBottom();
});

onUnmounted(() => {
    socket.close();
});

function beep() {
    var snd = new Audio('data:audio/wav;base64,//uQRAAAAWMSLwUIYAAsYkXgoQwAEaYLWfkWgAI0wWs/ItAAAGDgYtAgAyN+QWaAAihwMWm4G8QQRDiMcCBcHfQwA//uQRAAAAWMSLwUIYAAsYkXgoQwAEaYLWfkWgAI0wWs/ItAAAGDgYtAgAyN+QWaAAihwMWm4G8QQRDiMcCBcHfQwA//uQRAAAAWMSLwUIYAAsYkXgoQwAEaYLWfkWgAI0wWs/ItAAAGDgYtAgAyN+QWaAAihwMWm4G8QQRDiMcCBcHfQwA');
    snd.play();
}

function newGame() {
    router.push("/creategame");
}

function scrollToBottom() {
    const tableContainer = document.querySelector('table-contain......')
    if(tableContainer) {
        tableContainer.scrollTop = tableContainer.scrollHeight;
    }
}

function connectWebSocket() {
    socket.onopen = () => {
        console.log('WebSocket Client Connected');
    };

    socket.onmessage = (e) => {
        const data = JSON.parse(e.data);
        const uci_move = data.form + data.to + data.promotion;
        if (data.type == 'game')
        {
            console.log("message received");
            console.log(data);
        }else if (data.type = 'move')
        {
            if (store.userID !== data.playerID)
            {
                console.log('move data', data.from, data.to, data.promotion);
                var result = boardAPI.value?.move(uci_move);
                console.log("BEEP");
                beep();
                console.log("result", result);
            }
        }
    };
}

// al final

console.log()
console.log()

if(move.color == store.color.charAt(0)){
    var promotion = "";
    if ("promotion" in move){
        console.log("promotion in move", move.promotion)
        promotion = move.promotion;
    }
}
await socket.send(JSON.stringify({
    'type': 'move',
    'from': move.from,
    'to': move.to,
    'promotion': promotion,
    'playerID': store.userID,
    'gameID': store.gameID,
    'token': store.token,
})

console.log()