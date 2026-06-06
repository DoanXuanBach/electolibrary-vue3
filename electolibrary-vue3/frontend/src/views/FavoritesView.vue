<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import LayoutCard from '../components/LayoutCard.vue'
import BookItem from '../components/BookItem.vue'
import { deleteBook, getBooks, updateBook } from '../services/bookApi'

const router = useRouter()
const books = ref([])
const favorites = computed(() => books.value.filter((book) => book.favorite))

async function loadBooks() {
  books.value = await getBooks()
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

async function toggleFavorite(book) {
  await updateBook(book.id, toFormData(book, { favorite: !book.favorite }))
  await loadBooks()
}

async function toggleStatus(book) {
  const nextStatus = book.status === 'available' ? 'reserved' : 'available'
  await updateBook(book.id, toFormData(book, { status: nextStatus }))
  await loadBooks()
}

async function reserveBook(book) {
  await updateBook(book.id, toFormData(book, { status: 'reserved' }))
  await loadBooks()
}

onMounted(loadBooks)
</script>

<template>
  <LayoutCard>
    <template #header>
      <div>
        <p class="eyebrow">Любимые книги</p>
        <h1>Избранное</h1>
      </div>
    </template>

    <p v-if="favorites.length === 0" class="empty-state">Пока нет любимых книг.</p>
    <div v-else class="book-list">
      <BookItem
        v-for="book in favorites"
        :key="book.id"
        :book="book"
        @delete="removeBook"
        @toggle-status="toggleStatus"
        @toggle-favorite="toggleFavorite"
        @reserve="reserveBook"
        @edit="router.push({ name: 'book-edit', params: { id: book.id } })"
      />
    </div>
  </LayoutCard>
</template>
