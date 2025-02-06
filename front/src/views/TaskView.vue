<template>
    <div class="task-tracker-container">
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
                            v-for="task in tasks" :key="task.id"
                            class="post-item"
                            @mousedown="startSwipe(task, $event)"
                            @mousemove="onSwipe(task, $event)"
                            @mouseup="endSwipe(task)"
                            @touchstart="startSwipe(task, $event)"
                            @touchmove="onSwipe(task, $event)"
                            @touchend="endSwipe(task)"
                            @click="onTaskClick(task)" 
                            :class="{
                                'swipe-left': task.swipeAction === 'left' && activeTab === 1,
                                'swipe-right': task.swipeAction === 'right',
                            }"
                        >
                            <div class="task-content">
                                <h3 class="post-title">{{ task.text }}</h3>
                            </div>

                            <!-- Кнопки для свайпа -->
                            <div class="swipe-icons-left">
                                <template v-if="activeTab === 1">
                                    <span class="icon delete" @click="deleteTask(task.id)">
                                        <span class="material-icons">delete</span>
                                    </span>
                                </template>
                                <template v-else>
                                    <span class="icon delete" @click="deleteTask(task.id)">
                                        <span class="material-icons">delete</span>
                                    </span>
                                </template>
                            </div>
                            <div class="swipe-icons-right" v-if="activeTab === 1">
                                <span class="icon edit" @click="editTask(task)">
                                    <span class="material-icons">edit</span>
                                </span>
                                <span class="icon complete" @click="completeTask(task.id)">
                                    <span class="material-icons">done</span>
                                </span>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
            <!-- Ваша кнопка -->
            <CreateTaskButton :fetchTasks="fetchTasks" />
        </div>
        <EditTaskModal 
            :isVisible="isEditModalVisible"
            :taskId="editingTaskId"
            :oldText="editingTaskText"
            @closeModal="closeEditModal"
            @taskUpdated="fetchTasks"
        />
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { API_URL } from '../config.js';
import CreateTaskButton from '@/components/CreateTaskButton.vue';
import EditTaskModal from '@/components/EditTaskModal.vue';

export default {
    name: 'TaskView',
    components: {
        CreateTaskButton,
        EditTaskModal,
    },
    setup() {
        const isModalVisible = ref(false);
        const tasks = ref([]);
        const newTask = ref('');

        const activeTab = ref(1);
        const categories = ref({
            "Completed": [],
            "In Progress": []
        });
        const isSwiping = ref(false);
        const currentSwipedTask = ref(null);
        const startX = ref(0);
        const startY = ref(0);

        const isEditModalVisible = ref(false);
        const editingTaskId = ref(null);
        const editingTaskText = ref('');

        const fetchTasks = async () => {
            try {
                const tg_user = window.Telegram.WebApp.initDataUnsafe?.user;
                const response = await fetch(`${API_URL}/api/tasks/${tg_user.id}`, {
                    method: 'GET',
                    headers: { 'ngrok-skip-browser-warning': 'true' },
                });
                const data = await response.json();
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

        const startSwipe = (task, event) => {
            if (isSwiping.value) return;
            isSwiping.value = true;
            currentSwipedTask.value = task;
            startX.value = event.touches ? event.touches[0].clientX : event.clientX;
            startY.value = event.touches ? event.touches[0].clientY : event.clientY;
        };

        const onSwipe = (task, event) => {
            if (!isSwiping.value || currentSwipedTask.value !== task) return;

            const currentX = event.touches ? event.touches[0].clientX : event.clientX;
            const currentY = event.touches ? event.touches[0].clientY : event.clientY;

            const deltaX = currentX - startX.value;
            const deltaY = currentY - startY.value;

            if (Math.abs(deltaX) > Math.abs(deltaY)) {
                event.preventDefault();
                if (deltaX > 50) {
                    task.swipeAction = 'right';
                    task.showIcons = true;
                } else if (deltaX < -50 && activeTab.value === 1) {
                    task.swipeAction = 'left';
                    task.showIcons = true;
                }
            }
        };

        const endSwipe = (task) => {
            if (currentSwipedTask.value !== task) return;

            isSwiping.value = false;
            currentSwipedTask.value = null;
        };

        const resetAllSwipes = () => {
            Object.values(categories.value).forEach((tasks) => {
                tasks.forEach((t) => {
                    t.showIcons = false;
                    t.swipeAction = null;
                });
            });
        };

        const onTaskClick = (task) => {
            if (task.swipeAction) {
                task.swipeAction = null;
                task.showIcons = false;
            }
        };

        const deleteTask = async (taskId) => {
            try {
                const tg_user = window.Telegram.WebApp.initDataUnsafe?.user;
                console.log("Deleting task with ID:", taskId);
                const response = await fetch(`${API_URL}/api/tasks/delete/${taskId}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'ngrok-skip-browser-warning': 'true'
                    },
                    body: JSON.stringify({ tgId: tg_user.id })
                });

                if (response.ok) {
                    await fetchTasks();
                } else {
                    console.error('Ошибка при удалении задачи:', response.status);
                }
            } catch (error) {
                console.error('Ошибка при выполнении запроса:', error);
            }

            resetAllSwipes();
        };

        const editTask = (task) => {
            editingTaskId.value = task.id;
            editingTaskText.value = task.text;
            isEditModalVisible.value = true;
            resetAllSwipes();
        };

        const closeEditModal = () => {
            isEditModalVisible.value = false;
            editingTaskId.value = null;
            editingTaskText.value = '';
        };

        const completeTask = async (taskId) => {
            try {
                const tg_user = window.Telegram.WebApp.initDataUnsafe?.user;
                const response = await fetch(`${API_URL}/api/completed`, {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                        'ngrok-skip-browser-warning': 'true'
                    },
                    body: JSON.stringify({ id: taskId }),
                });

                if (response.ok) {
                    await fetchTasks();
                } else {
                    console.error('Ошибка при завершении задачи:', response.status);
                }
            } catch (error) {
                console.error('Ошибка при выполнении запроса:', error);
            }

            resetAllSwipes();
        };

        onMounted(() => {
            fetchTasks();
        });

        return {
            activeTab,
            categories,
            setActiveTab,
            startSwipe,
            onSwipe,
            endSwipe,
            deleteTask,
            editTask,
            completeTask,
            isSwiping,
            onTaskClick,
            isModalVisible,
            tasks,
            newTask,
            fetchTasks,
            isEditModalVisible,
            editingTaskId,
            editingTaskText,
            closeEditModal,
        };
    },
};
</script>

<style scoped>
.task-tracker-container {
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
    width: 100%;
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
    width: 100%;
    max-width: 400px;
    margin: 0 auto;
    overflow-x: hidden;
    max-height: calc(100vh - 160px);
}

ul {
    margin: 0;
    padding: 0;
    list-style: none;
}

/* Элементы задач */
.post-item {
    margin: 0 auto;
    margin-bottom: 16px;
    padding: 12px 16px;
    border-radius: 8px;
    background-color: #f9f9f9;
    transition: transform 0.3s ease, background-color 0.3s ease;
    overflow-x: hidden;
    position: relative;
    max-width: calc(100% - 32px);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.post-item:hover {
    background-color: #eaeaea;
}

.post-title {
    user-select: none;
    font-size: 16px;
    font-weight: bold;
    color: #000;
    overflow: hidden;
    text-overflow: ellipsis;
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
    bottom: 0;
    height: 100%;
    padding: 0 16px;
    border-radius: 8px;
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
    bottom: 0;
    height: 100%;
    padding: 0 16px;
    border-radius: 8px;
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
    padding: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
}

.icon .material-icons {
    font-size: 24px;
}

* {
    user-select: none;
    -webkit-user-select: none;
    -ms-user-select: none;
}
</style>