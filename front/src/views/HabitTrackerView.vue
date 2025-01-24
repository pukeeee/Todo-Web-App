<template>
    <div class="habit-tracker-container">
        <div class="tab-group">
            <div class="tab-list">
                <button
                    v-for="(category, index) in Object.keys(categories)"
                    :key="index"
                    @click="setActiveTab(index)"
                    :class="['tab-button', { active: activeTab === index }]"
                >
                    {{ category }}
                </button>
            </div>
            <div class="tab-panels">
                <div
                    v-for="(tasks, index) in Object.values(categories)"
                    :key="index"
                    v-show="activeTab === index"
                    class="tab-panel"
                >
                    <ul>
                        <li
                            v-for="task in tasks"
                            :key="task.id"
                            class="post-item"
                        >
                            <h3 class="post-title">{{ task.text }}</h3>

                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';
import { API_URL } from '../config.js';

export default {
    name: 'HabitTrackerView',
    setup() {
        const activeTab = ref(1);
        const categories = ref({
            "Completed": [],
            "In Progress": []
        });

        const fetchTasks = async () => {
            try {
                const tg_user = window.Telegram.WebApp.initDataUnsafe?.user;
                const response = await fetch(`${API_URL}/api/tasks/${tg_user.id}`, {
                    method: 'GET',
                    headers: { 'ngrok-skip-browser-warning': 'true' },
                });
                const data = await response.json();
                // Разделение задач по статусу
                categories.value['In Progress'] = data.filter((task) => task.status == 0);
                categories.value['Completed'] = data.filter((task) => task.status == 1);
            } catch (error) {
                console.log('Error fetching tasks:', error);
            }
        };

        const setActiveTab = async (index) => {
            activeTab.value = index;
            await fetchTasks();
        };

        fetchTasks();

        return {
            activeTab,
            categories,
            setActiveTab,
        };
    },
};
</script>

<style scoped>
.habit-tracker-container {
    width: 100%;
    /* max-width: 600px; */
    margin: 0 auto;
    overflow: hidden; /* Убираем выход за границы */
    padding: 16px;
    box-sizing: border-box; /* Включаем отступы в ширину контейнера */
    /* background: linear-gradient(180deg, #60a5fa, #2563eb); Градиентный фон
    border-radius: 16px; Скругленные углы основного контейнера 
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); Легкая тень для объема */
}

.tab-group {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%; /* Занимаем всю ширину родителя */
}

.tab-list {
    display: flex;
    justify-content: space-between;
    width: calc(100% - 32px);
    margin: 0 auto; /* Центрируем группу вкладок */
    margin-bottom: 16px;
    background-color: #FF79C6; /* Синий фон для вкладок */
    padding: 4px;
    border-radius: 12px; /* Закруглённые края группы вкладок */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.tab-button {
    flex: 1;
    padding: 12px 16px;
    border: none;
    background: none;
    cursor: pointer;
    font-size: 14px;
    font-weight: bold;
    color: #F8F8F2; /* Светлый текст для неактивных вкладок */
    border-radius: 12px;
    transition: background-color 0.3s ease, color 0.3s ease;
    text-align: center;
}

.tab-button.active {
    background-color: #ffffff; /* Белый фон для активной вкладки */
    color: #FF79C6; /* Синий текст для активной вкладки */
    font-weight: 600; /* Чуть жирнее текст */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); /* Легкая тень для выделения */
}

.tab-panels {
    width: 100%;
    margin: 0 auto;
    /* background-color: #ffffff; */
    padding: 16px;
    /* border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); */
    list-style-type: none;
    box-sizing: border-box; /* Включаем отступы в ширину контейнера */
    overflow-y: auto; /* Добавляем прокрутку */
    max-height: calc(100vh - 160px); /* Учитываем высоту экрана и оставляем отступ снизу */
}

.post-item {
    margin-bottom: 16px;
    padding: 12px 16px;
    border-radius: 8px;
    background-color: #f9f9f9; /* Легкий серый фон для поста */
    transition: background-color 0.3s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Легкая тень для поста */
    list-style-type: none; /* Убираем точки перед элементами списка */
}

.post-item:hover {
    background-color: #e6e6e6; /* Светлый фон при наведении */
}

.post-title {
    font-size: 16px;
    font-weight: bold;
    margin: 4px;
    color: #1f2937; /* Темный текст */
}

.post-meta {
    display: flex;
    gap: 4px;
    font-size: 12px;
    color: #6b7280; /* Средне-серый текст для метаинформации */
    flex-wrap: wrap;
    align-items: center;
    list-style-type: none; /* Убираем точки перед метаинформацией */
}

ul {
    padding: 0; /* Убираем отступы списка */
    margin: 0; /* Убираем внешние отступы */
    list-style-type: none; /* Убираем точки у всех списков */
}

.tab-group {
    margin-bottom: 0; /* Убираем синюю полоску снизу */
}



@media (max-width: 768px) {
    .habit-tracker-container {
        padding: 8px;
    }

    .tab-button {
        font-size: 12px;
    }

    .post-item {
        padding: 8px;
    }
}
</style>