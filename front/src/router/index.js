// src/router.js
import { createRouter, createWebHistory } from 'vue-router'

const TasksView = () => import("../views/TaskView.vue")
const ProfileView = () => import("../views/ProfileView.vue")
const NotFound = () => import("../views/NotFound.vue")
const HabitTrackerView = () => import("../views/HabitTrackerView.vue")


const routes = [
  {
    path: "/profile",
    name: "Profile",
    component: ProfileView
  },

  {
    path: "/",
    name: "Tasks",
    component: TasksView
  },

  {
    path: "/habit-tracker",
    name: "HabitTracker",
    component: HabitTrackerView
  },

  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: NotFound
  }
]



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), routes
})

export default router
