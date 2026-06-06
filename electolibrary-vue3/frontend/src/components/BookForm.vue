<script setup>
import { computed, reactive, ref, watch } from 'vue'

const props = defineProps({
  initialBook: {
    type: Object,
    default: null
  },
  submitText: {
    type: String,
    default: 'Сохранить'
  }
})

const emit = defineEmits(['submit'])

const publishers = ['Эксмо', 'АСТ', 'Питер', 'МИФ', 'Просвещение']
const categories = ['0+', '6+', '12+', '16+', '18+']
const coverFile = ref(null)

const form = reactive({
  title: '',
  author: '',
  description: '',
  year: new Date().getFullYear(),
  publisher: 'Эксмо',
  category: '12+',
  theme: 'Классика',
  status: 'available',
  favorite: false
})

const errors = reactive({})

watch(
  () => props.initialBook,
  (book) => {
    if (book) {
      form.title = book.title || ''
      form.author = book.author || ''
      form.description = book.description || ''
      form.year = Number(book.year) || new Date().getFullYear()
      form.publisher = book.publisher || 'Эксмо'
      form.category = book.category || '12+'
      form.theme = book.theme || 'Классика'
      form.status = book.status || 'available'
      form.favorite = Boolean(book.favorite)
    }
  },
  { immediate: true }
)

const isValid = computed(() => {
  return form.title.trim().length >= 2 &&
    form.author.trim().length >= 2 &&
    form.year >= 1500 &&
    form.year <= new Date().getFullYear() + 1
})

function validate() {
  Object.keys(errors).forEach((key) => delete errors[key])

  if (form.title.trim().length < 2) errors.title = 'Введите заголовок минимум из 2 символов.'
  if (form.author.trim().length < 2) errors.author = 'Введите автора минимум из 2 символов.'
  if (form.year < 1500 || form.year > new Date().getFullYear() + 1) {
    errors.year = 'Год должен быть реалистичным.'
  }
  if (coverFile.value && !['image/jpeg', 'image/jpg'].includes(coverFile.value.type)) {
    errors.cover = 'Разрешён только файл JPG.'
  }

  return Object.keys(errors).length === 0
}

function onFileChange(event) {
  coverFile.value = event.target.files?.[0] || null
}

function handleSubmit() {
  if (!validate()) return

  const data = new FormData()
  Object.entries(form).forEach(([key, value]) => data.append(key, value))
  if (coverFile.value) data.append('cover', coverFile.value)

  emit('submit', data)
}
</script>

<template>
  <form class="book-form" @submit.prevent="handleSubmit">
    <label>
      Заголовок
      <input v-model.trim="form.title" type="text" placeholder="Например: Мастер и Маргарита" />
      <small v-if="errors.title" class="error">{{ errors.title }}</small>
    </label>

    <label>
      Автор
      <input v-model.trim="form.author" type="text" placeholder="Например: М. А. Булгаков" />
      <small v-if="errors.author" class="error">{{ errors.author }}</small>
    </label>

    <label>
      Описание
      <textarea v-model.lazy.trim="form.description" rows="5" placeholder="Краткое описание книги"></textarea>
    </label>

    <div class="form-grid">
      <label>
        Год издания
        <input v-model.number="form.year" type="number" min="1500" :max="new Date().getFullYear() + 1" />
        <small v-if="errors.year" class="error">{{ errors.year }}</small>
      </label>

      <label>
        Издательство
        <select v-model="form.publisher">
          <option v-for="publisher in publishers" :key="publisher" :value="publisher">
            {{ publisher }}
          </option>
        </select>
      </label>
    </div>

    <fieldset>
      <legend>Категория / возрастной рейтинг по ГОСТ 2018</legend>
      <label v-for="category in categories" :key="category" class="radio-label">
        <input v-model="form.category" type="radio" name="category" :value="category" />
        {{ category }}
      </label>
    </fieldset>

    <div class="form-grid">
      <label>
        Тематическая подборка
        <input v-model.trim="form.theme" type="text" placeholder="Классика, IT, история" />
      </label>

      <label>
        Статус
        <select v-model="form.status">
          <option value="available">В наличии</option>
          <option value="reserved">Забронирована</option>
        </select>
      </label>
    </div>

    <label class="checkbox-label">
      <input v-model="form.favorite" type="checkbox" />
      Добавить в любимые
    </label>

    <label>
      Обложка JPG
      <input type="file" accept="image/jpeg" @change="onFileChange" />
      <small v-if="errors.cover" class="error">{{ errors.cover }}</small>
    </label>

    <button type="submit" :disabled="!isValid">{{ submitText }}</button>
  </form>
</template>
