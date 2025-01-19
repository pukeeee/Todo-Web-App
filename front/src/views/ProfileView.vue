<template>
    <div class="profile-container">
        <h2>Профиль</h2>
        <div class="profile-info">
            <p><strong>ID:</strong> {{ user.id }}</p>
            <p><strong>Name:</strong> {{ user.name }}</p>
            <p><strong>Tasks completed:</strong> {{ user.completedTasksCounter }}</p>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ProfileView',
    data() {
        return {
            user: {
                id: '',
                name: '',
                completedTasksCounter: 0
            }
        }
    },
    async mounted() {
        await this.fetchProfile()
    },
    methods: {
        async fetchProfile() {
            try {
                const tg_user = window.Telegram.WebApp.initDataUnsafe?.user
                const response = await fetch(`https://peaceful-curious-kite.ngrok-free.app/api/profile/${tg_user.id}`, {
                    method: 'GET',
                    headers: {'ngrok-skip-browser-warning': 'true'}
                })
                const data = await response.json()
                this.user.id = tg_user.id
                this.user.name = tg_user.first_name
                this.user.completedTasksCounter = data.completedTasksCounter
            } catch (error) {
                console.log(error)
            }
        }
    }
}
</script>

<style scoped>
.profile-container {
    height: 100vh; /* Занимаем всю высоту */
    display: flex;
    justify-content: center;
    align-items: center;
    /* background-color: linear-gradient(to bottom right, #441752, #69247C);  Тот же цвет фона */
}

.profile-info {
    background-color: #ffffffcc;
    backdrop-filter: blur(8px);
    padding: 16px;
    border-radius: 8px;
    text-align: left;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    margin-top: 16px;
    width: 100%;
    max-width: 320px;
}
</style>