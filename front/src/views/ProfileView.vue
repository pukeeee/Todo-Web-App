<template>
    <div class="profile-container">
        <Header @toggleMenu="toggleMenu"></Header>
        <div class="profile-info">
            <p><strong>ID:</strong> {{ user.id }}</p>
            <p><strong>Name:</strong> {{ user.name }}</p>
            <p><strong>Tasks completed:</strong> {{ user.completedTasksCounter }}</p>
        </div>
        <SidebarMenu :isVisible="isMenuOpen" @closeMenu="toggleMenu" />
    </div>
</template>


<script>
import { API_URL } from '../config.js';

import Header from '@/components/Header.vue';
import SidebarMenu from '@/components/SidebarMenu.vue';

export default {
    name: 'ProfileView',
    components: {
        Header,
        SidebarMenu,
    },
    data() {
        return {
            user: {
                id: '',
                name: '',
                completedTasksCounter: 0
            },
            isMenuOpen: false,
        }
    },
    async mounted() {
        await this.fetchProfile()
    },
    methods: {
        toggleMenu() {
            this.isMenuOpen = !this.isMenuOpen;
        },
        async fetchProfile() {
            try {
                const tg_user = window.Telegram.WebApp.initDataUnsafe?.user
                const response = await fetch(`${API_URL}/api/profile/${tg_user.id}`, {
                    method: 'GET',
                    headers: {'ngrok-skip-browser-warning': 'true'}
                })
                const data = await response.json()
                this.user.id = tg_user.id
                this.user.name = tg_user.first_name || 'Guest';
                this.user.completedTasksCounter = data.completedTasksCounter
            } catch (error) {
                console.log(error)
            }
        }
    }
}
</script>

<style scoped>
.profile-container {
    height: 100vh; /* Устанавливаем высоту контейнера на всю высоту окна браузера */
    display: flex; /* Устанавливаем flex-контейнер для удобного управления дочерними элементами */
    flex-direction: column; /* Размещаем дочерние элементы (хедер, информация) вертикально */
    align-items: center; /* Выравниваем все дочерние элементы по горизонтальному центру */
    overflow: hidden; /* Убираем прокрутку для контейнера, даже если содержимое выходит за границы */
}

.profile-info {
    background-color: #ffffffcc; /* Задаём полупрозрачный белый фон для блока информации */
    backdrop-filter: blur(8px); /* Добавляем эффект размытия для фона за элементом */
    padding: 16px; /* Внутренние отступы внутри блока (от текста до границ) */
    border-radius: 8px; /* Скругляем углы блока, чтобы выглядело эстетично */
    text-align: left; /* Выравниваем текст внутри блока по левому краю */
    box-shadow: 4px 4px 10px 2px rgba(0, 0, 0, 0.2); 
/* 4px по горизонтали, 4px по вертикали, 10px размытие, 2px расширение, цвет черный с прозрачностью */
    margin-top: 80px; /* Отступ сверху, чтобы разместить блок ниже хедера */
    width: 100%; /* Блок занимает всю доступную ширину контейнера */
    max-width: 320px; /* Ограничиваем максимальную ширину блока для удобного чтения на больших экранах */
}
</style>