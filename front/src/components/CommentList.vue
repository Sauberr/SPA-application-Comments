<script setup>
import { ref } from 'vue'
import CommentItem from './CommentItem.vue'

const comments = ref([
  {
    id: 1,
    author: 'Алексей Смирнов',
    date: '18.06.2026 в 14:32',
    avatarColor: '#aa3bff',
    likes: 12,
    text: 'Это тестовый комментарий с <strong>выделением</strong> и <code>немного кода</code> внутри текста.',
    replies: [
      {
        id: 2,
        author: 'Мария Иванова',
        date: '18.06.2026 в 15:10',
        avatarColor: '#3b82f6',
        likes: 4,
        text: 'Согласна, отличный пример! А ссылку на документацию можно глянуть <a href="#">тут</a>.',
        replies: [
          {
            id: 3,
            author: 'Алексей Смирнов',
            date: '18.06.2026 в 15:25',
            avatarColor: '#aa3bff',
            likes: 1,
            text: 'Спасибо за ответ, рад что пригодилось!',
            replies: [],
          },
        ],
      },
    ],
  },
  {
    id: 4,
    author: 'Игорь Петров',
    date: '17.06.2026 в 09:05',
    avatarColor: '#10b981',
    likes: 0,
    text: 'Это очень длинный тестовый комментарий, который специально написан так, чтобы не влезать в одну строку целиком и обязательно обрезался многоточием в конце, как это принято делать в большинстве социальных сетей.',
    replies: [
      {
        id: 5,
        author: 'Мария Иванова',
        date: '17.06.2026 в 10:12',
        avatarColor: '#3b82f6',
        likes: 2,
        text: 'Это тестовый комментарий с <strong>выделением</strong> и <code>немного кода</code> внутри текста.',
        replies: [],
      },
    ],
  },
  {
    id: 6,
    author: 'Игорь Петров',
    date: '17.06.2026 в 09:05',
    avatarColor: '#10b981',
    likes: 0,
    text: 'Это тестовый комментарий с <strong>выделением</strong> и <code>немного кода</code> внутри текста.',
    replies: [],
  },
])
</script>

<template>
  <section class="comment-list">
    <h2 class="comment-list-title">Комментарии <span class="count">{{ comments.length }}</span></h2>
    <div class="comment-list-items">
      <CommentItem v-for="comment in comments" :key="comment.id" :comment="comment" />
    </div>
  </section>
</template>

<style scoped src="./CommentList.css"></style>