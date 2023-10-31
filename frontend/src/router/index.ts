import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue';
import axios from 'axios';
import { endpoints } from '@/common/endpoints.js';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about/',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/login/',
    name: 'login',
    component: () => import('../views/LoginView.vue')
  }
  ,
  {
    path: '/signup/',
    name: 'signup',
    component: () => import('../views/SignUpView.vue')
  },
  {
    path: '/dashboard/',
    name: 'dashboard',
    component: () => import('../views/DashboardView.vue'),
    
  },
  {
    path: '/addtripform/',
    name: 'addtripform',
    component: () => import('../views/AddTripFormView.vue')
  }
]
async function isLoggedIn() {
  const endpoint = endpoints['isLoggedIn'];
  const response = await axios.get(endpoint);
  return response.data.isAuthenticated
}

const protectedRoutes = [
  "about",
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
  const isProtected = protectedRoutes.includes(to.name as string)
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
    if (isloggedin) {
      next()
    }
    else {
      console.log(`/accounts/login/`);
      window.location.href = '/accounts/login/';
    }
  } else next()
})

export default router
