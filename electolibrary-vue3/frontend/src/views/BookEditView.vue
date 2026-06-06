<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import BookForm from '../components/BookForm.vue'
import LayoutCard from '../components/LayoutCard.vue'
import { getBook, updateBook } from '../services/bookApi'

const props = defineProps({
  id: {
    type: String,
    required: true
  }
})

const router = useRouter()
const book = ref(null)
const loading = ref(false)
const error = ref('')

async function loadBook() {
  loading.value = true
  try {
    book.value = await getBook(props.id)
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

async function submitBook(formData) {
  error.value = ''
  try {
    await updateBook(props.id, formData)
    router.push({ name: 'books' })
  } catch (err) {
    error.value = err.message
  }
}

onMounted(loadBook)
</script>

<template>
  <LayoutCard>
    <template #header>
      <div>
        <p class="eyebrow">Редактирование</p>
        <h1>Редактировать книгу</h1>
      </div>
    </template>

    <p v-if="loading">Загрузка...</p>
    <p v-else-if="error" class="error">{{ error }}</p>
    <BookForm v-else-if="book" :initial-book="book" submit-text="Сохранить изменения" @submit="submitBook" />
  </LayoutCard>
</template>
