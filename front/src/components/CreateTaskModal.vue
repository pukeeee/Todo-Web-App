<template>
    <div v-if="isVisible" class="modal-overlay" @click.self="closeModal">
        <div class="modal">
            <h2>Create Task</h2>
            <input
                type="text"
                v-model="taskText"
                placeholder="Enter task text"
                @keyup.enter="createTask"
            />
            <div class="modal-buttons">
                <button @click="createTask" class="confirm">Create</button>
                <button @click="closeModal" class="cancel">Close</button>
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
    background: rgba(0, 0, 0, 0.5);
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
}

/* Поле ввода */
input {
    width: 100%;
    padding: 10px;
    margin-top: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 16px;
}

/* Кнопки */
.modal-buttons {
    display: flex;
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
    background-color: #28a745;
    color: white;
}

.cancel {
    background-color: #dc3545;
    color: white;
}
</style>