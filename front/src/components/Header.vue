<template>
    <header class="header">
        <div class="header-content">
            <h2 class="header-title">Profile</h2>
            <button class="burger-menu" @click="$emit('toggleMenu')">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>
    </header>
</template>


<script>
export default {
    name: 'Header',
};
</script>


<style scoped>
.header {
    width: 100%; /* Ширина хедера занимает всю доступную ширину экрана */
    display: flex; /* Устанавливаем flex-контейнер для выравнивания содержимого */
    justify-content: space-between; /* Распределяем элементы хедера по краям */
    align-items: center; /* Выравниваем элементы по вертикали по центру */
    padding: 25px; /* Добавляем внутренние отступы вокруг содержимого */
    background-color: #44475A; /* Полупрозрачный тёмно-серый */
    position: fixed; /* Фиксируем хедер в верхней части экрана, даже при прокрутке */
    top: 0; /* Задаём позицию от верхнего края окна (0 пикселей) */
    left: 0; /* Задаём позицию от левого края окна (0 пикселей) */
    z-index: 10; /* Устанавливаем приоритет отображения (чем больше, тем выше элемент над другими) */
}

.header-title {
    color: #F8F8F2; /* Установите нужный цвет */
    font-size: 24px; /* Размер текста */
    font-weight: bold; /* Жирность */
    margin: 0; /* Убираем лишние отступы */
}

.header-content {
    display: flex; /* Используем flex-контейнер для расположения содержимого */
    justify-content: space-between; /* Элементы равномерно распределяются между началом и концом */
    align-items: center; /* Выравниваем элементы по вертикали по центру */
    width: 100%; /* Контент хедера занимает всю ширину родителя */
    max-width: 1024px; /* Максимальная ширина хедера, чтобы не растягивался на больших экранах */
    margin: 0 auto; /* Центрируем хедер на странице при ограничении ширины */
}

.burger-menu {
    display: flex; /* Устанавливаем flex-контейнер для кнопки бургер-меню */
    flex-direction: column; /* Элементы (линии) располагаются вертикально */
    justify-content: space-around; /* Распределяем линии с равным расстоянием между ними */
    width: 24px; /* Ширина кнопки бургер-меню */
    height: 24px; /* Высота кнопки бургер-меню */
    background: transparent; /* Прозрачный фон кнопки */
    border: none; /* Убираем границу у кнопки */
    cursor: pointer; /* Устанавливаем указатель мыши в виде руки при наведении */
    padding: 0; /* Убираем внутренние отступы кнопки */
    margin-right: 30px; /* Устанавливает отступ от правого края */
}

.burger-menu span {
    width: 100%; /* Каждая линия занимает всю ширину кнопки */
    height: 2px; /* Толщина линии (2 пикселя) */
    background-color: #FF79C6; /* Цвет линий */
    transition: background-color 0.3s ease, transform 0.3s ease; /* Плавный переход для изменения цвета и трансформации */
}

.burger-menu:hover span {
    background-color: #FFFFFF; /* Изменяем цвет линий на белый при наведении */
}

@media (max-width: 768px) {
    .header {
        padding: 12px;
    }
    .burger-menu {
        width: 20px;
        height: 20px;
    }
    .burger-menu span {
        height: 1.5px;
    }
}
</style>