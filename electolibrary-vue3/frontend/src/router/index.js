import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import BooksView from '../views/BooksView.vue'
import BooksCatalogView from '../views/BooksCatalogView.vue'
import BookCreateView from '../views/BookCreateView.vue'
import BookEditView from '../views/BookEditView.vue'
import FavoritesView from '../views/FavoritesView.vue'
import NotFoundView from '../views/NotFoundView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/books',
    component: BooksView,
    children: [
      {
        path: '',
        name: 'books',
        component: BooksCatalogView
      },
      {
        path: 'new',
        name: 'book-create',
        component: BookCreateView
      },
      {
        path: ':id/edit',
        name: 'book-edit',
        component: BookEditView,
        props: true
      },
      {
        path: 'favorites',
        name: 'book-favorites',
        component: FavoritesView
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFoundView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
