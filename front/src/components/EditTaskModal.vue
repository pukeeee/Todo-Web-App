<template>
    <div v-if="isVisible" class="modal-overlay" @click.self="$emit('closeModal')">
        <div class="modal">
            <button @click="$emit('closeModal')" class="close-button">
                <span class="material-icons">close</span>
            </button>
            <h2>Edit Task</h2>
            <div class="old-text">{{ oldText }}</div>
            <input
                type="text"
                v-model="taskText"
                placeholder="Enter new task text"
                @keyup.enter="updateTask"
            />
            <div class="modal-buttons">
                <button @click="updateTask" class="confirm">
                    <span class="material-icons">save</span>
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import { ref } from "vue";
import { API_URL } from "../config.js";

export default {
    name: "EditTaskModal",
    props: {
        isVisible: Boolean,
        taskId: Number,
        oldText: String,
    },
    setup(props, { emit }) {
        const taskText = ref("");

        const updateTask = async () => {
            if (!taskText.value.trim()) return;

            try {
                const tg_user = window.Telegram.WebApp.initDataUnsafe?.user;
                const response = await fetch(`${API_URL}/api/tasks/update/${props.taskId}`, {
                    method: "PATCH",
                    headers: {
                        "Content-Type": "application/json",
                        "ngrok-skip-browser-warning": "true",
                    },
                    body: JSON.stringify({ 
                        tgId: tg_user.id, 
                        text: taskText.value 
                    }),
                });

                if (response.ok) {
                    emit("taskUpdated");
                    taskText.value = "";
                    emit("closeModal");
                } else {
                    console.error("Ошибка обновления задачи:", response.status);
                }
            } catch (error) {
                console.error("Ошибка:", error);
            }
        };

        return {
            taskText,
            updateTask,
        };
    },
};
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    align-items: flex-start;
    justify-content: center;
    z-index: 1000;
    padding-top: 20vh;
}

@media screen and (max-height: 500px) {
    .modal-overlay {
        padding-top: 10px;
    }
}

.modal {
    background: #fff;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    width: 300px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    position: relative;
}

.old-text {
    margin: 10px 0;
    padding: 10px;
    background: #f5f5f5;
    border-radius: 5px;
    font-style: italic;
    color: #666;
}

input {
    width: calc(100% - 20px);
    padding: 10px;
    margin: 10px;
    border: 1px solid #ff79c6;
    border-radius: 5px;
    font-size: 16px;
    box-sizing: border-box;
    outline: none;
}

.modal-buttons {
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
