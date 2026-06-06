<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import BookForm from '../components/BookForm.vue'
import LayoutCard from '../components/LayoutCard.vue'
import { createBook } from '../services/bookApi'

const router = useRouter()
const error = ref('')

async function submitBook(formData) {
  error.value = ''
  try {
    await createBook(formData)
    router.push({ name: 'books' })
  } catch (err) {
    error.value = err.message
  }
}
</script>

<template>
  <LayoutCard>
    <template #header>
      <div>
        <p class="eyebrow">Создание</p>
        <h1>Добавить новую книгу</h1>
      </div>
    </template>

    <p v-if="error" class="error">{{ error }}</p>
    <BookForm submit-text="Создать книгу" @submit="submitBook" />
  </LayoutCard>
</template>
