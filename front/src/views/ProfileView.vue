<template>
    <div class="profile-container">
        <Header @toggleMenu="toggleMenu"></Header>
        <!-- Отображение загрузки -->
        <div v-if="isLoading" class="loading">Loading...</div>

        <div class="profile-content">
            <!-- Картинка профиля -->
            <div v-if="profile.image_path" class="profile-image">
                <img :src="`${API_URL}/${profile.image_path}`" alt="Profile Image" />
            </div>

            <!-- Информация о профиле -->
            <div class="profile-info">
                <p><strong>Name:</strong> {{ profile.user_name }}</p>
                <p><strong>Race:</strong> {{ profile.race }}</p>
                <p><strong>Class:</strong> {{ profile.clas }}</p>
            </div>
        </div>

        <!-- Сайдбар -->
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
            API_URL,
            profile: {
                user_name: 'Guest',
                race: 'Human',
                clas: 'Exile',
                image_path: ''
            },
            isLoading: true,
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
                this.profile = {
                    user_name: data.user_name || 'Guest',
                    race: data.race || 'Human',
                    clas: data.clas || 'Warrior',
                    sex: data.sex || 'Male',
                    image_path: data.image_path || ''
                };
                
            } catch (error) {
                console.log(error)
            } finally {
                // Убираем состояние загрузки
                this.isLoading = false;
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

.profile-content {
    display: flex; /* Flexbox для горизонтального расположения */
    flex-direction: row; /* Размещаем элементы по горизонтали */
    align-items: center; /* Выравниваем элементы по вертикали */
    margin-top: 80px; /* Отступ от хедера */
    gap: 16px; /* Расстояние между картинкой и информацией */
}

.profile-info {
    background-color: #ffffffcc; /* Задаём полупрозрачный белый фон для блока информации */
    backdrop-filter: blur(8px); /* Добавляем эффект размытия для фона за элементом */
    padding: 16px; /* Внутренние отступы внутри блока (от текста до границ) */
    border-radius: 8px; /* Скругляем углы блока, чтобы выглядело эстетично */
    text-align: left; /* Выравниваем текст внутри блока по левому краю */
    box-shadow: 4px 4px 10px 2px rgba(0, 0, 0, 0.2); 
/* 4px по горизонтали, 4px по вертикали, 10px размытие, 2px расширение, цвет черный с прозрачностью */

    width: 100%; /* Блок занимает всю доступную ширину контейнера */
    max-width: 320px; /* Ограничиваем максимальную ширину блока для удобного чтения на больших экранах */
}

.loading {
    margin-top: 80px; /* Отступ для размещения ниже хедера */
    font-size: 18px;
    color: #666;
    text-align: center;
}

.profile-image img {
    width: 200px; /* Ширина картинки */
    border-radius: 10%; /* Скругляем изображение для аватара */
    object-fit: cover; /* Устанавливаем пропорции без обрезки */
}
</style>