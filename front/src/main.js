import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Vue3TouchEvents from "vue3-touch-events";

const app = createApp(App)

if (window.Telegram?.WebApp && window.Telegram.WebApp.disableVerticalSwipes) {
    window.Telegram.WebApp.ready(); // Сообщаем что WebApp готов
    window.Telegram.WebApp.expand(); // Делаем окно по всей высоте
    window.Telegram.WebApp.disableVerticalSwipes();
}

app.use(router)
app.use(Vue3TouchEvents, {
    swipeThreshold: 50, // Минимальное расстояние для срабатывания свайпа
    touchHoldTolerance: 500, // Длительность удержания до свайпа
});
app.mount('#app')

