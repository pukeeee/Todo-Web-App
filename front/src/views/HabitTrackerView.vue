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
<<<<<<< HEAD
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
=======
                            class="post-item"
                            @mousedown="startSwipe(task, $event)"
                            @mousemove="onSwipe(task, $event)"
                            @mouseup="endSwipe(task)"
                            @touchstart="startSwipe(task, $event)"
                            @touchmove="onSwipe(task, $event)"
                            @touchend="endSwipe(task)"
                            @click="onTaskClick(task)" 
                            :class="{
                                'swipe-left': task.swipeAction === 'left',
                                'swipe-right': task.swipeAction === 'right',
                            }"
                        >
                            <div class="task-content">
                                <h3 class="post-title">{{ task.text }}</h3>
                            </div>

                            <!-- Кнопки для свайпа -->
                            <div class="swipe-icons-left">
                                <span class="icon delete" @click="deleteTask(task)">🗑</span>
                            </div>
                            <div class="swipe-icons-right">
                                <span class="icon edit" @click="editTask(task)">✏️</span>
                                <span class="icon complete" @click="completeTask(task)">✅</span>
>>>>>>> 889d46c (zbs swipes)
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
        const isSwiping = ref(false);
        const startX = ref(0);
        const startY = ref(0);

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

        const startSwipe = (task, event) => {
            isSwiping.value = true;
            startX.value = event.touches ? event.touches[0].clientX : event.clientX; // Координаты по X
            startY.value = event.touches ? event.touches[0].clientY : event.clientY; // Координаты по Y
        };

        const onSwipe = (task, event) => {
            if (!isSwiping.value) return;

            const currentX = event.touches ? event.touches[0].clientX : event.clientX;
            const currentY = event.touches ? event.touches[0].clientY : event.clientY;

            const deltaX = currentX - startX.value;
            const deltaY = currentY - startY.value;

            // Проверяем, что движение по горизонтали больше, чем по вертикали
            if (Math.abs(deltaX) > Math.abs(deltaY)) {
                event.preventDefault(); // Отключаем стандартное поведение прокрутки
                if (deltaX < -50) {
                    task.swipeAction = 'left'; // Свайп влево
                } else if (deltaX > 50) {
                    task.swipeAction = 'right'; // Свайп вправо
                }
            }
        };

        const endSwipe = (task) => {
            isSwiping.value = false;
            if (!task.swipeAction) {
                task.swipeAction = null;
            }
        };

        const resetAllSwipes = () => {
            Object.values(categories.value).forEach((tasks) => {
                tasks.forEach((t) => {
                    t.swipeAction = null;
                });
            });
        };

        const onTaskClick = (task) => {
            if (task.swipeAction) {
                // Сбрасываем свайп только у этой задачи
                task.swipeAction = null;
            }
        };

        const deleteTask = (task) => {
            console.log('Task deleted:', task.id);
            resetAllSwipes();
        };

        const editTask = (task) => {
            console.log('Edit task:', task.id);
            resetAllSwipes();
        };

        const completeTask = (task) => {
            console.log('Task completed:', task.id);
            resetAllSwipes();
        };

        fetchTasks();

        return {
            activeTab,
            categories,
            setActiveTab,
<<<<<<< HEAD
            onSwipeLeft,
            onSwipeRight,
            resetSwipe,
=======
            startSwipe,
            onSwipe,
            endSwipe,
            deleteTask,
            editTask,
            completeTask,
            isSwiping,
            onTaskClick,
>>>>>>> 889d46c (zbs swipes)
        };
    },
};
</script>

<style scoped>
.habit-tracker-container {
    width: 100%;
    margin: 0 auto;
    overflow: hidden;
    padding: 16px;
    box-sizing: border-box;
}

/* Стили для вкладок */
.tab-group {
    display: flex;
    flex-direction: column;
    align-items: center;
<<<<<<< HEAD
    width: 100%; /* Занимаем всю ширину родителя */
    margin-bottom: 0; /* Убираем синюю полоску снизу */
=======
    width: 100%;
>>>>>>> 889d46c (zbs swipes)
}

.tab-list {
    display: flex;
    justify-content: space-between;
    width: calc(100% - 32px);
    margin-bottom: 16px;
    background-color: #FF79C6;
    padding: 4px;
    border-radius: 12px;
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
    color: #F8F8F2;
    border-radius: 12px;
    text-align: center;
    transition: background-color 0.3s ease, color 0.3s ease;
}

.tab-button.active {
    background-color: #ffffff;
    color: #FF79C6;
    font-weight: 600;
}

/* Стили панелей с задачами */
.tab-panels {
<<<<<<< HEAD
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
=======
    width: 100%; /* Устанавливаем ширину табов по контейнеру */
    max-width: 400px; /* Максимальная ширина, чтобы не выходило за экран */
    margin: 0 auto; /* Центрирование содержимого */
    overflow-x: hidden; /* Убираем горизонтальный скролл */
    max-height: calc(100vh - 160px); /* Учет высоты экрана и отступов */
>>>>>>> 889d46c (zbs swipes)
}

ul {
    margin: 0;
    padding: 0;
    list-style: none;
}

<<<<<<< HEAD
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
=======
/* Элементы задач */
.post-item {
    margin: 0 auto;
    margin-bottom: 16px;
    padding: 12px 16px;
    border-radius: 8px;
    background-color: #f9f9f9;
    transition: transform 0.3s ease, background-color 0.3s ease;
    overflow-x: hidden; /* Убираем горизонтальные скроллы внутри */
    position: relative;
    max-width: calc(100% - 32px);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.post-item:hover {
    background-color: #eaeaea;
>>>>>>> 889d46c (zbs swipes)
}

.post-title {
    user-select: none; /* Запрет на выделение текста */
    font-size: 16px;
    font-weight: bold;
    color: #000;
    overflow: hidden;
    text-overflow: ellipsis; /* Троеточие при переполнении */
}

/* Стили для свайпа */
.task-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
    transition: transform 0.3s ease;
}

/* Фон для иконок, появляется только при свайпе */
.swipe-icons-left{
    display: flex;
    align-items: center;
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0; /* Увеличиваем область до всей высоты элемента */
    height: 100%;
    padding: 0 16px;
    border-radius: 8px; /* Совпадает с радиусом углов post-item */
    gap: 8px;
    transition: transform 0.3s ease, background-color 0.3s ease;
    background-color: transparent;
    opacity: 0;
}
.swipe-icons-right {
    display: flex;
    align-items: center;
    position: absolute;
    right: 0;
    top: 0;
    bottom: 0; /* Увеличиваем область до всей высоты элемента */
    height: 100%;
    padding: 0 16px;
    border-radius: 8px; /* Совпадает с радиусом углов post-item */
    gap: 8px;
    transition: transform 0.3s ease, background-color 0.3s ease;
    background-color: transparent;
    opacity: 0;
}

/* Левая область (удаление) */
.swipe-icons-left {
    left: 0;
    transform: translateX(-100%);
}

.swipe-right .swipe-icons-left {
    background-color: rgba(255, 121, 198, 0.8);
    transform: translateX(0);
    opacity: 1;
}

/* Правая область (редактирование и завершение) */
.swipe-icons-right {
    right: 0;
    transform: translateX(100%);
}

.swipe-left .swipe-icons-right {
    background-color: rgba(255, 121, 198, 0.8);
    transform: translateX(0);
    opacity: 1;
}

/* Общие стили кнопок */
.icon {
    font-size: 20px;
    cursor: pointer;
}

/* .icon.delete {
    color: red;
}

.icon.edit {
    color: orange;
}

.icon.complete {
    color: green;
} */
</style>