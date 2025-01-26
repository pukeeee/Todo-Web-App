<template>
    <button
        class="create-task-button"
        @click="handleClick"
    >
        ➕
    </button>
</template>

<script>
    export default {
        name: 'CreateTaskButton',
        props: {
            onClick: {
            type: Function,
            required: true,
            },
        },
        methods: {
            handleClick() {
                this.onClick();
            },
        },
    };
</script>

<style scoped>
.create-task-button {
    position: fixed;
    bottom: 125px; /* Над навбаром */
    right: 40px;
    width: 60px;
    height: 60px;
    background-color: #ff79c6;
    border: none;
    border-radius: 50%;
    font-size: 24px;
    cursor: pointer;
    transition: background-color 0.3s ease;

    /* Тень */
    box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.6); /* Делает тень более тёмной */
    transition: box-shadow 0.3s ease; /* Анимация при изменении */

    /* Выравнивание текста */
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: 1; /* Убираем дополнительные отступы у текста */
    text-align: center; /* Центровка текста */
}

/* Тень при наведении */
.create-task-button:hover {
    box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.8); /* Увеличиваем размытие и тёмность */
}

/* .create-task-button:hover {
    background-color: #e06bad;
}

.create-task-button:active {
    background-color: #ff79c6;
} */

/* Для мобильных устройств */
@media (max-width: 768px) {
    .create-task-button {
        right: 40px; /* Регулируем позицию справа для мобильных */
    }
}

* {
    user-select: none;
    -webkit-user-select: none;
    -ms-user-select: none;
}
</style>