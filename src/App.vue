<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue'

const topic = ref('S14世界赛数据一览')

const setTopic = (param) => {
  if (param === '赛事') {
    topic.value = 'S14世界赛数据一览'
  } else {
    topic.value = '英雄联盟排位数据一览'
  }
}

</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/" class="button" @click="setTopic('赛事')">赛事</RouterLink>
        <RouterLink to="/rank" class="button" @click="setTopic('排位')">排位</RouterLink>
      </nav>
      <span class="title-style">
        {{ topic }}
      </span>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  line-height: 3;
  max-height: 100vh;
}

.wrapper {
  margin-bottom: 10px;
  height: 64px;
  margin-top: -20px;
  background-color: #d6e4f4; /* 背景颜色 */
  border-radius: 5px; /* 圆角边框 */
}

.button {
  padding: 10px 20px; /* 按钮内边距 */
  font-size: 16px; /* 字体大小 */
  font-weight: 600; /* 字体粗细 */
  color: #ffffff; /* 文字颜色 */
  background-color: #007bff; /* 背景颜色 */
  border: none; /* 无边框 */
  border-radius: 5px; /* 圆角边框 */
  cursor: pointer; /* 鼠标悬停时显示指针 */
  transition: all 0.3s ease; /* 平滑过渡效果 */
  outline: none; /* 去除焦点时的轮廓线 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2); /* 阴影效果 */
}

.button:hover {
  background-color: #0056b3; /* 鼠标悬停时的背景颜色 */
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2); /* 鼠标悬停时的阴影效果 */
}

.button:active {
  transform: translateY(2px); /* 点击时的下压效果 */
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2); /* 点击时的阴影效果 */
}

.button:focus {
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.5); /* 焦点时的阴影效果 */
}

nav {
  display: inline-block;
  font-size: 12px;
  /* text-align: center; */
  margin-right: 30px;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

span {
  padding-left: 30%;
}

.title-style {
  font-size: 24px;
  color: #333333;
  font-weight: bold;
}

</style>
