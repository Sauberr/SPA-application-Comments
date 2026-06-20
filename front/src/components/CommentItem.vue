<script setup>
defineProps({
  comment: {
    type: Object,
    required: true,
  },
  isReply: {
    type: Boolean,
    default: false,
  },
})

function initials(name) {
  return name
    .split(' ')
    .map((part) => part[0])
    .join('')
    .slice(0, 2)
    .toUpperCase()
}
</script>

<template>
  <div class="comment">
    <div v-if="!isReply" class="comment-header">
      <div class="avatar" :style="{ background: comment.avatarColor }">
        {{ initials(comment.author) }}
      </div>

      <div class="head-meta">
        <span class="author">{{ comment.author }}</span>
        <time class="date">{{ comment.date }}</time>
      </div>

      <div class="head-icons">
        <button type="button" class="head-icon-btn" aria-label="Хештег">
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M5 9h14M5 15h14M11 4 7 20M17 4l-4 16" />
          </svg>
        </button>
        <button type="button" class="head-icon-btn" aria-label="Сохранить">
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M6 3.5C6 2.67 6.67 2 7.5 2h9c.83 0 1.5.67 1.5 1.5V21l-7-4-7 4V3.5Z" />
          </svg>
        </button>
        <button type="button" class="head-icon-btn" aria-label="Пожаловаться">
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M5 4v18" />
            <path d="M5 4h12l-3 3.5 3 3.5H5Z" />
          </svg>
        </button>
        <button type="button" class="head-icon-btn" aria-label="Ещё">
          <svg class="icon" viewBox="0 0 24 24" fill="currentColor" stroke="none">
            <circle cx="4" cy="12" r="1.7" />
            <circle cx="12" cy="12" r="1.7" />
            <circle cx="20" cy="12" r="1.7" />
          </svg>
        </button>
      </div>
    </div>

    <div class="comment-main" :class="{ 'comment-main--reply': isReply }">
      <div class="comment-body" v-html="comment.text"></div>

      <div class="comment-actions">
        <button v-if="!isReply" type="button" class="action-btn">
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78Z" />
          </svg>
          <span v-if="comment.likes">{{ comment.likes }}</span>
        </button>
        <button type="button" class="action-btn">
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 11.5a8.38 8.38 0 0 1-1.9 5.4L21 21l-4.1-1.1a8.38 8.38 0 0 1-3.9 1 8.5 8.5 0 1 1 8-9.4Z" />
          </svg>
          <span>Ответить</span>
        </button>
      </div>

      <div v-if="comment.replies?.length" class="replies">
        <CommentItem
          v-for="reply in comment.replies"
          :key="reply.id"
          :comment="reply"
          is-reply
        />
      </div>
    </div>
  </div>
</template>

<style scoped src="./CommentItem.css"></style>