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
                    v-for="(posts, index) in Object.values(categories)"
                    :key="index"
                    v-show="activeTab === index"
                    class="tab-panel"
                >
                    <ul>
                        <li
                            v-for="post in posts"
                            :key="post.id"
                            class="post-item"
                        >
                            <h3 class="post-title">{{ post.title }}</h3>

                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';

export default {
    name: 'HabitTrackerView',
    setup() {
        const activeTab = ref(0);
        const categories = ref({
            "Completed": [
                {
                    id: 1,
                    title: 'Does drinking coffee make you smarter? Хуй пенис Хуй пенис Хуй пенис'
                },
                {
                    id: 2,
                    title: "So you've bought coffee... now what?"
                },
            ],
            "In Progress": [
                {
                    id: 1,
                    title: 'Is tech making coffee better or worse?'
                },
                {
                    id: 2,
                    title: 'The most innovative things happening in coffee'
                },
            ]
            // Trending: [
            //     {
            //         id: 1,
            //         title: 'Ask Me Anything: 10 answers to your questions about coffee',
            //         date: '2d ago',
            //         commentCount: 9,
            //         shareCount: 5,
            //     },
            //     {
            //         id: 2,
            //         title: "The worst advice we've ever heard about coffee",
            //         date: '4d ago',
            //         commentCount: 1,
            //         shareCount: 2,
            //     },
            // ],
        });

        const setActiveTab = (index) => {
            activeTab.value = index;
        };

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


/* Адаптивность
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
} */
</style>