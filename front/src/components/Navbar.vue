<template>
    <nav class="navbar">
        <router-link to="/profile" class="nav-link">
            <i class="fas fa-user"></i> Profile
        </router-link>

        <router-link to="/" class="nav-link">
            <i class="fas fa-tasks"></i> Task Tracker
        </router-link>

        <router-link to="/habit-tracker" class="nav-link">
            <i class="fas fa-calendar-check"></i> Habit Tracker
        </router-link>
    </nav>
</template>


<script>
export default {
    name: "Navbar"
}
</script>



<style scoped>
.navbar {
    display: flex;
    justify-content: space-around; /* Равномерное распределение кнопок */
    align-items: center;
    position: fixed; /* Фиксируем навбар */
    bottom: 0; /* Закрепляем у нижнего края экрана */
    left: 0;
    width: 100%; /* Растягиваем на всю ширину экрана */
    height: 80px;
    background-color: #B771E5;
    backdrop-filter: blur(10px);
    border-top: 1px solid #ccc;
    z-index: 10; /* Обеспечиваем, чтобы навбар находился поверх остальных элементов */
}

.nav-link {
    flex: 1; /* Каждая кнопка занимает равную долю ширины */
    text-align: center; /* Выравнивание текста по центру */
    text-decoration: none;
    color: #FFFBCA;
    font-size: 18px;
    font-weight: 500;
    display: flex;
    justify-content: center; /* Центрирование текста и иконок */
    align-items: center;
    gap: 10px;
    border-right: 1px solid #AEEA94; /* Разделитель */
    padding: 0 10px; /* Внутренние отступы */
}

.nav-link:last-child {
    border-right: none; /* Убираем разделитель у последней кнопки */
}

.nav-link i {
    font-size: 22px; /* Размер иконок */
}

.nav-link:hover {
    color: white;
}
</style>