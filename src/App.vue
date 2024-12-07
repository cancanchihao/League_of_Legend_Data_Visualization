<template>
  <v-app>

    <!-- 顶部导航栏 -->
    <v-app-bar class="wrapper">
      <v-container class="title-container">
        <span class="big-title">
          {{ topic }}
        </span>
      </v-container>

      <v-select label="选择赛段" v-model='topic' class="ml-auto" style="max-width: 250px;" :items="['2017 LPL 春季赛', '2017 LPL 夏季赛', '2017 全球总决赛',
        '2018 LPL 春季赛', '2018 LPL 夏季赛', '2018 全球总决赛',
        '2019 LPL 春季赛', '2019 LPL 夏季赛', '2019 全球总决赛',
        '2020 LPL 春季赛', '2020 LPL 夏季赛', '2020 全球总决赛',
        '2021 LPL 春季赛', '2021 LPL 夏季赛', '2021 全球总决赛',
        '2022 LPL 春季赛', '2022 LPL 夏季赛', '2022 全球总决赛',
        '2023 LPL 春季赛', '2023 LPL 夏季赛', '2023 全球总决赛',
        '2024 LPL 春季赛', '2024 LPL 夏季赛', '2024 全球总决赛',]">
      </v-select>
    </v-app-bar>


    <!-- 主体部分 -->
    <v-main>
      <section class="mainbox">
        <div class="column">
          <div class="little-title">
            战队
          </div>
          <div class="chart-container">
            战队胜场数据轮播
          </div>
          <div class="chart-container">
            <!-- 战队对战数据热力图 -->
            <heatMap :teamNames="Data.heatMap.teamNames" :data="Data.heatMap.heatmapData" title="16支战队对抗胜率热力图" />

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
          <!-- <div class="chart-container">
        选手mvp次数饼图
      </div> -->
          <div class="hero-compete-chart-container">
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
            <heroAgainstChart :heroData="Data.bpbar.herodata"></heroAgainstChart>
          </div>
        </div>
      </section>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import contestantRadarChart from './components/contestant-radar-chart.vue';
import bpBarChart from './components/bp-bar-chart.vue';
import bpWordcloudChart from './components/bp-wordcloud-chart.vue';
import 'echarts-wordcloud';
import heroAgainstChart from './components/hero-against-chart.vue';

import heatMap from './components/heatMap.vue';

const topic = ref('big-title')
const setTopic = (param) => {
  topic.value = param
}


function generateHeatmapData(teamCount) {
  const data = [];

  for (let i = 0; i < teamCount; i++) {
    for (let j = 0; j < teamCount; j++) {
      if (i === j) {
        data.push([i, j, "-"]);
      } else {
        const winRate = Math.floor(Math.random() * 101); // 随机生成一个 0 到 100 之间的胜率
        data.push([i, j, winRate]);
      }
    }
  }

  return data;
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
  },

  //英雄对抗图数据
  heroagainst: {
  },

  heatMap: {
    teamNames: [
      "BLG", "EDG", "RNG", "RA",
      "WE", "JDG", "IG", "FPX",
      "AL", "LGD", "OMG", "UP",
      "TT", "WBG", "TES", "NIP",
    ],

    heatmapData: generateHeatmapData(16)
    // heatmapData: [
    //   [0, 0, "-"], [0, 1, 70], [0, 2, 50], [0, 3, 60],
    //   [1, 0, 30], [1, 1, "-"], [1, 2, 40], [1, 3, 80],
    //   [2, 0, 50], [2, 1, 60], [2, 2, "-"], [2, 3, 70],
    //   [3, 0, 40], [3, 1, 20], [3, 2, 30], [3, 3, "-"],
    // ]

  }



})

onMounted(() => { })

</script>



<style>
html,
body {
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

  display: flex;
  /* 使用 flex 布局 */
  justify-content: space-between;
  /* 保证子元素分布在两侧 */
  align-items: center;
  /* 垂直居中对齐 */
  position: relative;
  /* 相对定位，使绝对定位生效 */
}

.title-container {
  position: absolute;
  /* 绝对定位，让标题位于父容器中央 */
  left: 50%;
  /* 水平居中 */
  transform: translateX(-50%);
  /* 修正偏移 */
  text-align: center;
  /* 文本居中 */
}

.big-title {
  font-size: 24px;
  line-height: 100%;
  color: #333333;
  font-weight: bold;

  text-align: center;
  /* flex-grow: 1; */

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

.hero-compete-chart-container {
  height: 61vh;
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
