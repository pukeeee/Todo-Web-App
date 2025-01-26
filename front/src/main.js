import { createApp } from 'vue'
import App from './App.vue'
import router from './router'


const app = createApp(App)

if (window.Telegram?.WebApp && window.Telegram.WebApp.disableVerticalSwipes) {
    window.Telegram.WebApp.ready(); // Сообщаем что WebApp готов
    window.Telegram.WebApp.expand(); // Делаем окно по всей высоте
    window.Telegram.WebApp.disableVerticalSwipes();
}

app.use(router)
app.mount('#app')

