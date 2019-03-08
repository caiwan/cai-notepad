import Vue from 'vue';
import Router from 'vue-router';
import Dashboard from '@/components/dashboard/component';
import User from '@/components/user/component';
import Login from '@/components/login/component';
import Tasks from '@/components/tasks/component';
import Notes from '@/components/notes/component';
import Categories from '@/components/categories/component';

Vue.use(Router);

// We'll need to put this into /router/*
// and slpit to separate files as we grow

export const router = new Router({
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: Dashboard
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/settings',
      name: 'Settings',
      component: Dashboard
    },

    {
      path: '/tasks',
      name: 'Tasks',
      component: Tasks
    },
    {
      path: '/notes',
      name: 'Notes',
      component: Notes
    },

    {
      path: '/categories',
      name: 'Categories',
      component: Categories
    },
    {
      path: '/user',
      name: 'User',
      component: User
    }
  ]
});

router.beforeEach((to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/login'];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = localStorage.getItem('user');

  if (authRequired && !loggedIn) {
    return next('/login');
  }

  next();
});
