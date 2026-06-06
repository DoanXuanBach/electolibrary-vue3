<script setup>
import LayoutCard from '../components/LayoutCard.vue'
</script>

<template>
  <LayoutCard>
    <template #header>
      <div>
        <p class="eyebrow">SPA-приложение</p>
        <h1>Электронная библиотека</h1>
      </div>
    </template>

    <p class="lead">
      ElectoLibrary помогает вести электронный каталог книг: добавлять, редактировать,
      удалять, фильтровать, сортировать, бронировать книги и сохранять любимые издания.
    </p>

    <div class="hero-actions">
      <RouterLink class="button-link" :to="{ name: 'books' }">Электронный каталог</RouterLink>
      <RouterLink class="button-link secondary" :to="{ name: 'book-create' }">Добавить книгу</RouterLink>
    </div>

    <template #footer="slotProps">
      <span>Проект подготовлен: {{ slotProps.createdBy }}, {{ slotProps.year }}</span>
    </template>
  </LayoutCard>
</template>
