<template>
    <div class="tasks_container">
        <div class="tasks-header">
            <input 
                v-model="newTask"
                type="text"
                placeholder="Enter a task..."
                class="task-input"
                @keyup.enter="createTask"
            />
            <button @click="createTask" class="add-button">+</button>
        </div>

        <div class="tasks-list">
            <div
                v-for="task in tasks"
                :key="task.id"
                class="task-item"
            >
                <div class="task-text">
                    {{ task.text }}
                </div>
                <button
                    class="complete-button"
                    @click="completeTask(task.id)">
                    Mark as done
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import { API_URL } from '../config.js';

export default {
    name: 'TasksView',
    data() {
        return {
            tasks: [],
            newTask: ''
        }
    },
    async mounted() {
        await this.fetchTasks()
    },
    methods: {
        async fetchTasks() {
            try {
                const tg_user = window.Telegram.WebApp.initDataUnsafe?.user
                const response = await fetch(`${API_URL}/api/tasks/${tg_user.id}`, {
                    method: 'GET',
                    headers: {'ngrok-skip-browser-warning': 'true'}
                })
                const data = await response.json()
                this.tasks = data
            } catch (error) {
                console.log('error', error)
            }
        },


        async createTask() {
            if (!this.newTask) return

            try {
                const tg_user = window.Telegram.WebApp.initDataUnsafe?.user
                const response = await fetch(`${API_URL}/api/add`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'ngrok-skip-browser-warning': 'true'
                    },
                    body: JSON.stringify({ tgId: tg_user.id, text: this.newTask })
                })
                if (response.ok) {
                    this.newTask = ''
                    await this.fetchTasks()
                } else {
                    console.error('Ошибка', response.status)
                }
            } catch (error) {
                console.log('Ошибка', error)
            }
        },
        async completeTask(taskId) {
            try {
                const response = await fetch(`${API_URL}/api/completed`, {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                        'ngrok-skip-browser-warning': 'true'
                    },
                    body: JSON.stringify({ id: taskId })
                })
                if (response.ok) {
                    await this.fetchTasks()
                } else {
                    console.error('Ошибка', response.status)
                }
            } catch (error) {
                console.log('Ошибка', error)
            }
        }
    }
}
</script>

<style scoped>
.tasks-container {
    display: flex;
    flex-direction: column;
    flex-grow: 1; /* Позволяет контейнеру занимать доступное пространство */
    padding: 0 16px;
    height: calc(100vh - 80px); /* Учитываем высоту навбара */
    background: none; /* Убираем повторяющийся фон */
}

.tasks-header {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    margin-bottom: 16px;
    position: sticky; /* Фиксируем заголовок */
    top: 0; /* Фиксируем его у верхней границы контейнера */
    z-index: 5;
    padding: 8px 0;
}

.task-input {
    flex: 1;
    padding: 8px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 8px;
    margin-right: 8px;
}

.add-button {
    background-color: #FF79C6; /* Цвет в стиле iOS */
    color: white;
    border: none;
    font-size: 24px;
    border-radius: 50%;
    cursor: pointer;
    outline: none;
    height: 40px;
    width: 40px;
}

.tasks-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex-grow: 1; /* Растягиваем список задач */
    overflow-y: auto; /* Прокрутка, если задач много */
    background: none; /* Убедись, что фон отсутствует */
    max-height: calc(100vh - 80px - 60px); /* Высота экрана - навбар - шапка */
}

.task-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #ffffffcc;
    padding: 8px 12px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.task-text {
    font-size: 16px;
}

.complete-button {
    background-color: #4caf50;
    color: white;
    border: none;
    padding: 6px 12px;
    border-radius: 8px;
    cursor: pointer;
}
</style>