<template>
    <div class="sidebar-menu" :class="{ show: isVisible }">
        <button class="close-button" @click="$emit('closeMenu')">×</button>
        <nav>
            <ul>
                <li><button @click="changeName">Изменить имя</button></li>
                <li><button @click="createCharacter">Создать персонажа</button></li>
            </ul>
        </nav>
    </div>
</template>

<script>
export default {
    name: 'SidebarMenu',
    props: {
        isVisible: {
            type: Boolean,
            default: false,
        },
    },

    methods: {
        changeName() {
            console.log('Изменение имени');
            // Логика для изменения имени
        },
        createCharacter() {
            console.log('Создание персонажа');
            // Логика для создания персонажа
        },
    },
};
</script>

<style scoped>
.sidebar-menu {
    position: fixed; /* Меню фиксируется относительно окна браузера */
    top: 0; /* Располагается от верхнего края экрана */
    right: 0; /* Привязано к правому краю экрана */
    width: 250px; /* Ширина меню */
    height: 100%; /* Меню занимает всю высоту экрана */
    background-color: rgba(74, 85, 104, 0.95); /* Полупрозрачный тёмно-серый */
    box-shadow: -2px 0 5px rgba(0, 0, 0, 0.5); /* Тень с левой стороны, создающая эффект глубины */
    display: flex; /* Устанавливаем flex-контейнер для управления содержимым */
    flex-direction: column; /* Размещаем элементы вертикально */
    align-items: flex-start; /* Выравниваем элементы по левому краю */
    padding: 16px; /* Внутренние отступы меню */
    transform: translateX(100%); /* Перемещаем меню за пределы экрана (справа) по умолчанию */
    transition: transform 0.3s ease-in-out, opacity 0.3s ease-in-out; /* Плавный переход для появления меню и изменения прозрачности */
    opacity: 0; /* Скрываем меню по умолчанию */
    z-index: 1000; /* Высокий z-index для отображения над остальными элементами */
}

.sidebar-menu.show {
    transform: translateX(0); /* Возвращаем меню в видимую область */
    opacity: 1; /* Делаем меню видимым */
}

.close-button {
    align-self: flex-end; /* Кнопка закрытия располагается справа */
    background: none; /* Убираем фон кнопки */
    border: none; /* Убираем рамку кнопки */
    font-size: 24px; /* Размер текста (крестика) */
    cursor: pointer; /* Изменяем указатель мыши на "руку" при наведении */
    color: #FF79C6; /* Цвет кнопки закрытия */
}

nav ul {
    list-style: none; /* Убираем стандартные маркеры списка */
    padding: 0; /* Убираем внутренние отступы списка */
    margin: 0; /* Убираем внешние отступы списка */
    width: 100%; /* Список занимает всю ширину меню */
}

nav li {
    margin: 12px 0; /* Отступы между элементами списка */
}

nav button {
    background: none; /* Убираем фон кнопки */
    border: none; /* Убираем рамку кнопки */
    color: #F8F8F2; /* Цвет текста кнопки */
    font-size: 18px; /* Размер текста кнопки */
    cursor: pointer; /* Указатель мыши меняется на "руку" при наведении */
    text-align: left; /* Текст выравнивается по левому краю */
    width: 100%; /* Кнопка занимает всю ширину списка */
    padding: 10px 12px; /* Внутренние отступы кнопки для удобства нажатия */
}

nav button:hover {
    text-decoration: underline; /* Добавляем подчёркивание текста при наведении */
}

@media (max-width: 768px) {
    .sidebar-menu {
        width: 200px; /* Уменьшаем ширину на узких экранах */
    }
}
</style>