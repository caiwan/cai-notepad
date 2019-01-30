import Vue from 'vue';
import Router from 'vue-router';
import Dashboard from '@/components/dashboard/component';
import Tasks from '@/components/tasks/component';
import Notes from '@/components/notes/component';

Vue.use(Router);

// We'll need to put this into /router/*
// and slpit to separate files as we grow

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Dashboard',
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
    }
  ]
});
