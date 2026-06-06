<template>
  <section class="not-found">
    <h1>404</h1>
    <p>Страница не найдена.</p>
    <RouterLink class="button-link" :to="{ name: 'home' }">Вернуться на главную</RouterLink>
  </section>
</template>
