<template>
    <div v-if="isVisible" class="modal-overlay" @click.self="$emit('closeModal')">
        <div class="modal">
            <button @click="$emit('closeModal')" class="close-button">
                <span class="material-icons">close</span>
            </button>
            <h2>Create Task</h2>
            <input
                type="text"
                v-model="taskText"
                placeholder="Enter task text"
                @keyup.enter="createTask"
            />
            <div class="modal-buttons">
                <button @click="createTask" class="confirm">
                    <span class="material-icons">add_task</span>
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import { ref } from "vue";
import { API_URL } from "../config.js";

export default {
    name: "CreateTaskModal",
    props: {
        isVisible: Boolean,
    },
    setup(props, { emit }) {
        const taskText = ref("");

        const createTask = async () => {
            if (!taskText.value.trim()) return;

            try {
                const tg_user = window.Telegram.WebApp.initDataUnsafe?.user;
                const response = await fetch(`${API_URL}/api/task/add`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "ngrok-skip-browser-warning": "true",
                    },
                    body: JSON.stringify({ tgId: tg_user.id, text: taskText.value }),
                });

                if (response.ok) {
                    emit("taskCreated"); // Сообщаем, что задача создана
                    taskText.value = ""; // Очищаем поле ввода
                    emit("closeModal"); // Закрываем модалку
                } else {
                    console.error("Ошибка создания задачи:", response.status);
                }
            } catch (error) {
                console.error("Ошибка:", error);
            }
        };

        return {
            taskText,
            createTask,
        };
    },
};
</script>

<style scoped>
/* Затемняющий фон */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

/* Само модальное окно */
.modal {
    background: #fff;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    width: 300px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    position: relative;
}

/* Поле ввода */
input {
    width: calc(100% - 20px); /* Уменьшаем ширину на размер отступов */
    padding: 10px;
    margin: 10px;  /* Добавляем отступ со всех сторон */
    border: 1px solid #ff79c6;
    border-radius: 5px;
    font-size: 16px;
    box-sizing: border-box; /* Учитываем padding в общей ширине */
    outline: none; /* Убираем обводку при фокусе */
}

/* Кнопки */
.modal-buttons {
    /* display: flex; */
    justify-content: space-between;
    margin-top: 15px;
}

button {
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
}

.confirm {
    background-color: #ff79c6;
    color: white;
    /* display: flex; */
    align-items: center;
    gap: 8px;
}

.confirm .material-icons {
    font-size: 20px;
}

.close-button {
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #666;
    padding: 0;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.close-button:hover {
    color: #333;
}

.close-button .material-icons {
    font-size: 20px;
}
</style>