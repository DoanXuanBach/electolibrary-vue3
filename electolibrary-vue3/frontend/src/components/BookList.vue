<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import BookItem from './BookItem.vue'

const props = defineProps({
  books: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['delete', 'toggle-status', 'toggle-favorite', 'reserve', 'edit'])

const statusFilter = ref('all')
const sortMode = ref('created_at_desc')
const searchQuery = ref('')
const lastFilterMessage = ref('')
const searchInput = ref(null)

const filteredBooks = computed(() => {
  const query = searchQuery.value.toLowerCase().trim()
  return props.books.filter((book) => {
    const matchesStatus = statusFilter.value === 'all' || book.status === statusFilter.value
    const matchesQuery = !query || [book.title, book.author, book.publisher, book.theme]
      .join(' ')
      .toLowerCase()
      .includes(query)
    return matchesStatus && matchesQuery
  })
})

const sortedBooks = computed(() => {
  const items = [...filteredBooks.value]
  if (sortMode.value === 'title_asc') {
    return items.sort((a, b) => a.title.localeCompare(b.title, 'ru'))
  }
  return items.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
})

watch([statusFilter, sortMode, searchQuery], () => {
  lastFilterMessage.value = `Найдено книг: ${sortedBooks.value.length}`
})

onMounted(() => {
  searchInput.value?.focus()
  lastFilterMessage.value = `Найдено книг: ${sortedBooks.value.length}`
})
</script>

<template>
  <section>
    <div class="toolbar">
      <label>
        Поиск
        <input ref="searchInput" v-model.trim="searchQuery" type="text" placeholder="Название, автор, тема" />
      </label>

      <label>
        Статус
        <select v-model="statusFilter">
          <option value="all">Все</option>
          <option value="available">В наличии</option>
          <option value="reserved">Забронированные</option>
        </select>
      </label>

      <label>
        Сортировка
        <select v-model="sortMode">
          <option value="created_at_desc">По дате добавления</option>
          <option value="title_asc">По алфавиту</option>
        </select>
      </label>
    </div>

    <p class="hint">{{ lastFilterMessage }}</p>

    <p v-if="sortedBooks.length === 0" class="empty-state">
      Книги не найдены. Измените фильтр или добавьте новую книгу.
    </p>

    <div v-else class="book-list">
      <BookItem
        v-for="book in sortedBooks"
        :key="book.id"
        :book="book"
        @delete="emit('delete', $event)"
        @toggle-status="emit('toggle-status', $event)"
        @toggle-favorite="emit('toggle-favorite', $event)"
        @reserve="emit('reserve', $event)"
        @edit="emit('edit', $event)"
      />
    </div>
  </section>
</template>
