<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import BookList from '../components/BookList.vue'
import LayoutCard from '../components/LayoutCard.vue'
import { deleteBook, getBooks, updateBook } from '../services/bookApi'

const router = useRouter()
const books = ref([])
const loading = ref(false)
const error = ref('')

async function loadBooks() {
  loading.value = true
  error.value = ''
  try {
    books.value = await getBooks()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

function toFormData(book, overrides = {}) {
  const updated = { ...book, ...overrides }
  const formData = new FormData()
  ;['title', 'author', 'description', 'year', 'publisher', 'category', 'theme', 'status', 'favorite'].forEach((key) => {
    formData.append(key, updated[key])
  })
  return formData
}

async function removeBook(book) {
  if (!confirm(`Удалить книгу «${book.title}»?`)) return
  await deleteBook(book.id)
  await loadBooks()
}

async function toggleStatus(book) {
  const nextStatus = book.status === 'available' ? 'reserved' : 'available'
  await updateBook(book.id, toFormData(book, { status: nextStatus }))
  await loadBooks()
}

async function toggleFavorite(book) {
  await updateBook(book.id, toFormData(book, { favorite: !book.favorite }))
  await loadBooks()
}

async function reserveBook(book) {
  await updateBook(book.id, toFormData(book, { status: 'reserved' }))
  await loadBooks()
}

function editBook(book) {
  router.push({ name: 'book-edit', params: { id: book.id } })
}

onMounted(loadBooks)
</script>

<template>
  <LayoutCard>
    <template #header>
      <div class="page-heading">
        <div>
          <p class="eyebrow">Каталог</p>
          <h1>Список книг</h1>
        </div>
        <RouterLink class="button-link" :to="{ name: 'book-create' }">Новая книга</RouterLink>
      </div>
    </template>

    <p v-if="loading">Загрузка...</p>
    <p v-else-if="error" class="error">{{ error }}</p>
    <BookList
      v-else
      :books="books"
      @delete="removeBook"
      @toggle-status="toggleStatus"
      @toggle-favorite="toggleFavorite"
      @reserve="reserveBook"
      @edit="editBook"
    />
  </LayoutCard>
</template>
