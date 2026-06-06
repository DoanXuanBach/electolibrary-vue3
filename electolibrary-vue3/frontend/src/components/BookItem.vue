<script setup>
defineProps({
  book: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['delete', 'toggle-status', 'toggle-favorite', 'reserve', 'edit'])
</script>

<template>
  <article class="book-card">
    <div class="book-card__cover" :class="{ 'book-card__cover--empty': !book.cover_url }">
      <img v-if="book.cover_url" :src="book.cover_url" :alt="`Обложка: ${book.title}`" />
      <span v-else>Нет обложки</span>
    </div>

    <div class="book-card__content">
      <div class="book-card__topline">
        <p class="badge" :class="book.status === 'available' ? 'badge--green' : 'badge--orange'">
          {{ book.status === 'available' ? 'В наличии' : 'Забронирована' }}
        </p>
        <button class="icon-button" type="button" @click="emit('toggle-favorite', book)">
          {{ book.favorite ? '♥' : '♡' }}
        </button>
      </div>

      <h3>{{ book.title }}</h3>
      <p class="muted">{{ book.author }} · {{ book.year }} · {{ book.publisher }}</p>
      <p>{{ book.description }}</p>
      <p class="theme">Тематика: {{ book.theme || 'Общая' }} · Категория: {{ book.category }}</p>

      <div class="book-card__actions">
        <button type="button" @click="emit('edit', book)">Редактировать</button>
        <button type="button" class="secondary" @click="emit('toggle-status', book)">Изменить статус</button>
        <button type="button" class="secondary" @click="emit('reserve', book)">Бронировать</button>
        <button type="button" class="danger" @click="emit('delete', book)">Удалить</button>
      </div>
    </div>
  </article>
</template>
