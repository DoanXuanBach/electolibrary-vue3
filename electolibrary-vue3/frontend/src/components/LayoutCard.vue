<template>
  <section class="layout-card">
    <header v-if="$slots.header" class="layout-card__header">
      <slot name="header" />
    </header>

    <div class="layout-card__body">
      <slot />
    </div>

    <footer v-if="$slots.footer" class="layout-card__footer">
      <slot name="footer" :created-by="createdBy" :year="currentYear" />
    </footer>
  </section>
</template>

<script setup>
const createdBy = 'Доан Суан Бач'
const currentYear = new Date().getFullYear()
</script>
