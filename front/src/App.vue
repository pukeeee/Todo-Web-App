<template>
	<div class="app-container">

	<div class="content">
		<router-view />
	</div>

	<Navbar />

	</div>
</template>

<script>
import Navbar from "./components/Navbar.vue"

export default {
	name: "App",
	components: {
	Navbar
	}
}
</script>


<style>
body, #app {
	margin: 0;
	padding: 0;
	box-sizing: border-box;
	overflow: hidden; /* Убираем горизонтальную прокрутку */
	width: 100%;
	min-height: 100vh; /* Занимаем всю высоту экрана */
	font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 
	Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
	background: linear-gradient(to bottom right, #FFCFEF, #AEEA94); /* Фон приложения */
	background-repeat: no-repeat; /* Запрещаем повторение */
	background-size: cover; /* Фон на всю область */
}

.app-container {
    display: flex;
    flex-direction: column;
    height: 100vh; /* Занимаем всю высоту экрана */
    overflow: hidden; /* Убираем скролл всего контейнера */
}

.content {
    flex: 1; /* Контейнер для основного содержимого */
    overflow-y: auto; /* Прокрутка только для задач */
}

</style>