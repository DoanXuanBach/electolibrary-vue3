<template>
  <header class="app-header">
    <RouterLink class="logo" :to="{ name: 'home' }">ElectoLibrary</RouterLink>
    <nav class="nav">
      <RouterLink :to="{ name: 'home' }">Главная</RouterLink>
      <RouterLink :to="{ name: 'books' }">Каталог</RouterLink>
      <RouterLink :to="{ name: 'book-create' }">Добавить книгу</RouterLink>
      <RouterLink :to="{ name: 'book-favorites' }">Любимые</RouterLink>
    </nav>
  </header>
</template>
