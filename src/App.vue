<script setup>
import { ref, reactive, onMounted } from 'vue'
import contestantRadarChart from './components/contestant-radar-chart.vue';
import bpBarChart from './components/bp-bar-chart.vue';
import bpWordcloudChart from './components/bp-wordcloud-chart.vue';

import 'echarts-wordcloud';

const topic = ref('big-title')
const setTopic = (param) => {
    topic.value = param
}

const Data = reactive({

  // bp词云图数据
  bpwordcloud: {
    series: [
      {
        gridSize: 20,
        data: [
          { name: '封魔剑魂', value: 50, },
          { name: '双界灵兔', value: 40 },
          { name: '武器大师', value: 35 },
          { name: '寒冰射手', value: 30 },
          { name: '圣锤之毅', value: 25 },
          { name: "上古领主", value: 20 },
          { name: '迷失之牙', value: 18 },
          { name: '虚空之女', value: 15 },
          { name: '熔铁少女', value: 10 },
          { name: '爆破鬼才', value: 8 },
        ],
      },
    ],
  },

  //选手雷达图数据
  contestantradar: {
    players: [
      { name: 'Player 1', stats: [80, 70, 90, 85, 75] },
      { name: 'Player 2', stats: [70, 80, 60, 90, 95] },
      { name: 'Player 3', stats: [90, 85, 80, 70, 70] },
      { name: 'Player 4', stats: [60, 90, 50, 65, 65] },
      { name: 'Player 5', stats: [50, 60, 70, 95, 35] },
      { name: 'Player 6', stats: [40, 65, 99, 80, 75] },
      { name: 'Player 7', stats: [50, 60, 70, 95, 35] },
      { name: 'Player 8', stats: [40, 65, 99, 80, 75] },
      { name: 'Player 9', stats: [50, 60, 70, 95, 35] },
      { name: 'Player 10', stats: [40, 65, 99, 80, 75] },
    ]
  },

  //bp柱状图数据
  bpbar: {
    herodata: [
      { name: '英雄1', matches: 200, pickRate: 0.4, winRate: 0.55 },
      { name: '英雄2', matches: 350, pickRate: 0.5, winRate: 0.45 },
      { name: '英雄3', matches: 100, pickRate: 0.25, winRate: 0.65 },
      { name: '英雄4', matches: 150, pickRate: 0.35, winRate: 0.50 },
      { name: '英雄5', matches: 500, pickRate: 0.6, winRate: 0.48 }
    ]
  }

})

onMounted(() => { })

</script>

<template>
  <header class="wrapper">
    <span class="big-title">
      {{ topic }}
    </span>
  </header>

  <section class="mainbox">
    <div class="column">
      <div class="little-title">
        战队
      </div>
      <div class="chart-container">
        战队胜场数据轮播
      </div>
      <div class="chart-container">
        战队对战数据热力图
      </div>
      <div class="chart-container">
        战队数据对抗图
      </div>
    </div>
    <div class="column">
      <div class="little-title">
        选手
      </div>
      <div class="chart-container">
        选手数据之最
      </div>
      <div class="chart-container">
        选手mvp次数饼图
      </div>
      <div class="chart-container">
        <contestantRadarChart :players="Data.contestantradar.players"></contestantRadarChart>
        <div class="history-hero-compete">
          历史英雄对位（近五场）
        </div>
        
      </div>
    </div>
    <div class="column">
      <div class="little-title">
        英雄
      </div>
      <div class="chart-container">
        <bpWordcloudChart :options="Data.bpwordcloud"></bpWordcloudChart>
      </div>
      <div class="chart-container">
        <bpBarChart :heroData="Data.bpbar.herodata"></bpBarChart>
      </div>
      <div class="chart-container">
        英雄数据对抗图
      </div>
    </div>
  </section>
</template>

<style>
html, body {
  margin: 0;
}

header {
  line-height: 3;
}

.wrapper {
  /* padding-bottom: 5px;
  margin-top: -20px; */
  height: 6vh;
  background-color: #d6e4f4;
  /* 背景颜色 */
  border-radius: 5px;
  /* 圆角边框 */
  text-align: center;
}

.big-title {
  font-size: 24px;
  line-height: 100%;
  color: #333333;
  font-weight: bold;
}

.mainbox {
  display: flex;
  min-width: 1024px;
  max-width: 1920px;
  margin: 0 auto;
  background-color: rgb(0, 255, 255);
  padding: 0.125rem 0.125rem 0;

  .column {
    flex: 1;
    &:nth-child(2) {
      border-left: 4px solid rgb(108, 197, 232);
      border-right: 4px solid rgb(108, 197, 232);
      .chart-container:nth-child(2) {
        height: 24vh;
      }
      .chart-container:nth-child(4) {
        height: 32vh;
      }
    }
  }
}

.history-hero-compete {
  border-top: 2px solid rgb(0, 255, 255);
}

.chart-container {
  height: 28vh;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  /* 轻微阴影效果 */
  border-radius: 10px;
  margin: 1vh;
  transition: transform 0.3s ease;
}

.little-title {
  text-align: center;
  height: 5vh;
}

</style>
