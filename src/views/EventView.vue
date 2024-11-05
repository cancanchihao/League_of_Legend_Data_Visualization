<script setup>
import Chart1 from '@/components/chart_1.vue';

import { inject } from 'vue';

// 子组件通过 inject 获取父组件提供的函数
const toPlayerListPage = inject('playerList');

// 调用传递下来的函数
const PlayerListPage = () => {
  toPlayerListPage(); // 调用父组件的 greet 函数
};
</script>

<template>
  <section class="mainbox">
    <div class="column">
      <div class="chart-container">
        <button class="chart1BUtton" @click="PlayerListPage">进入具体页面</button>
        <Chart1></Chart1>
      </div>
    </div>
    <div class="column">2</div>
    <div class="column">3</div>
  </section>
</template>

<style lang="less" scoped>
.mainbox {
  display: flex;
  min-width: 1024px;
  max-width: 1920px;
  margin: 0 auto;
  background-color: aqua;
  padding: 0.125rem 0.125rem 0;

  .column {
    flex: 3;

    &:nth-child(2) {
      flex: 5;
    }
  }
}

.chart-container {
  height: 200px;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  /* 轻微阴影效果 */
  border-radius: 10px;
  margin: 10px;
  transition: transform 0.3s ease;
}
</style>