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
                            :class="['post-item', { 'swipe-left': task.swipeAction === 'left', 'swipe-right': task.swipeAction === 'right' }]"
                            @click="resetSwipe(task)"
                            v-touch:swipe.left="() => onSwipeLeft(task)"
                            v-touch:swipe.right="() => onSwipeRight(task)"
                        >
                            <div class="task-content">
                                <h3 class="post-title">{{ task.text }}</h3>
                                <div v-if="task.showIcons" class="swipe-icons">
                                    <span v-if="task.swipeAction === 'right'" class="icon delete" @click="deleteTask(task.id)">🗑️</span>
                                    <span v-if="task.swipeAction === 'left'" class="icon edit" @click="editTask(task.id)">✏️</span>
                                    <span v-if="task.swipeAction === 'left'" class="icon done" @click="markAsDone(task.id)">✅</span>
                                </div>
                            </div>
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

                // Добавляем свойства showIcons и swipeAction
                const processedData = data.map(task => ({
                    ...task,
                    showIcons: false,  // Изначально кнопки скрыты
                    swipeAction: null, // Нет активного свайпа
                }));

                // Разделение задач по статусу
                categories.value['In Progress'] = processedData.filter((task) => task.status == 0);
                categories.value['Completed'] = processedData.filter((task) => task.status == 1);

            } catch (error) {
                console.log('Error fetching tasks:', error);
            }
        };


        const setActiveTab = async (index) => {
            activeTab.value = index;
            // Повторно вызываем fetchTasks только если данных нет
            if (!categories.value['In Progress'].length && !categories.value['Completed'].length) {
                await fetchTasks();
            }
        };

        const resetAllSwipes = () => {
            categories.value['In Progress'].forEach((t) => {
                t.showIcons = false;
                t.swipeAction = null;
            });
            categories.value['Completed'].forEach((t) => {
                t.showIcons = false;
                t.swipeAction = null;
            });
        };

        const onSwipeLeft = (task) => {
            console.log('Swipe left detected for task:', task);

            // Проверяем, есть ли активный свайп на текущей задаче
            if (!task.showIcons || task.swipeAction !== 'left') {
                resetAllSwipes(); // Сбрасываем свайпы у всех задач
                task.showIcons = true; // Включаем иконки для текущей задачи
                task.swipeAction = 'left'; // Устанавливаем направление свайпа
            } else {
                task.showIcons = false; // Если свайп уже активен, убираем его
                task.swipeAction = null;
            }
        };

        const onSwipeRight = (task) => {
            console.log('Swipe right detected for task:', task);

            // Проверяем, есть ли активный свайп на текущей задаче
            if (!task.showIcons || task.swipeAction !== 'right') {
                resetAllSwipes(); // Сбрасываем свайпы у всех задач
                task.showIcons = true; // Включаем иконки для текущей задачи
                task.swipeAction = 'right'; // Устанавливаем направление свайпа
            } else {
                task.showIcons = false; // Если свайп уже активен, убираем его
                task.swipeAction = null;
            }
        };
        
        const resetSwipe = (task) => {
            task.showIcons = false;
            task.swipeAction = null;
        };

        const editTask = (taskId) => {
            console.log('Edit task with ID:', taskId);
            // Добавьте функционал редактирования
        };

        const markAsDone = (taskId) => {
            console.log('Mark as done task with ID:', taskId);
            // Добавьте функционал выполнения задачи
        };

        const deleteTask = (taskId) => {
            console.log('Delete task with ID:', taskId);
            // Добавьте функционал удаления задачи
        };

        fetchTasks();

        return {
            activeTab,
            categories,
            setActiveTab,
            onSwipeLeft,
            onSwipeRight,
            resetSwipe,
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
    margin-bottom: 0; /* Убираем синюю полоску снизу */
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

.task-content {
    flex: 1;
}

.post-item {
    margin-bottom: 16px;
    padding: 12px 16px;
    border-radius: 8px;
    background-color: #f9f9f9; /* Легкий серый фон для поста */
    transition: background-color 0.3s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Легкая тень для поста */
    list-style-type: none; /* Убираем точки перед элементами списка */
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    user-select: none; /* Отключает выделение текста */
    -webkit-user-drag: none; /* Отключает перетаскивание на iOS */
    touch-action: none; /* Отключает стандартные жесты браузера */
}

.post-item.swipe-right {
    background-color: #ffcccc; /* Красный фон для свайпа вправо */
    transition: background-color 0.3s;
}

.post-item.swipe-left {
    background-color: #ccffcc; /* Зеленый фон для свайпа влево */
    transition: background-color 0.3s;
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

.swipe-icons {
    display: flex;
    gap: 8px;
    position: absolute;
    right: 16px;
    top: 50%;
    transform: translateY(-50%);
    opacity: 1 !important; /* По умолчанию скрыто */
    transition: opacity 0.3s ease; /* Анимация появления */
    z-index: 10; /* Убедитесь, что кнопка выше других элементов */
}

.task.swipe-left .swipe-icons,
.task.swipe-right .swipe-icons {
    opacity: 1; /* Показать кнопки */
}


.icon {
    font-size: 18px;
    cursor: pointer;
    padding: 4px;
    border-radius: 50%;
    background-color: #fff; /* Цвет фона для видимости */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Легкая тень для эффекта */
    transition: background-color 0.3s;
}

.icon:hover {
    background-color: #f0f0f0;
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