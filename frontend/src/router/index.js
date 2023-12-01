import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios';
import { endpoints } from '../common/endpoints.js'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/about/',
    name: 'about',
    component: () => import('../views/AboutView.vue')
  },
  {
    path: '/profile/',
    name: 'profile',
    component: () => import('../views/ProfileView.vue')
  },
  {
    path: '/dashboard/',
    name: 'dashboard',
    component: () => import('../views/DashboardView.vue'),
    
  }
]
async function isLoggedIn() {
  const endpoint = endpoints['isLoggedIn'];
  const response = await axios.get(endpoint);
  return response.data.isAuthenticated
}

const protectedRoutes = [
  "dashboard",
  "profile",
]

/*const skippableRoutes = [
  "login",
  "signup",
]*/

const router = createRouter({
  history: createWebHistory("/"),
  routes
})

router.beforeEach(async (to, from, next) => {
  const isProtected = protectedRoutes.includes(to.name)
  //const isSkippable = skippableRoutes.includes(to.name as string)

  /*if (isSkippable) {
    const isloggedin = await isLoggedIn()
    if (isloggedin) {
      router.push('/home/')
    }
    else {
      next()
    }
  }*/

  if (isProtected) {
    const isloggedin = await isLoggedIn();
    console.log(isloggedin)
    if (isloggedin) {
      next()
    }
    else {
      window.location.href = '/accounts/login/';
    }
  } else next()
})

export default router
