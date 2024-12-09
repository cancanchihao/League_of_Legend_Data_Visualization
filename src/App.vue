<template>
  <v-app>

    <!-- 顶部导航栏 -->
    <v-app-bar class="wrapper">
      <v-container class="title-container">
        <span class="big-title">
          {{ topic }}
        </span>
      </v-container>

      <v-select label="选择赛段" v-model='topic' class="ml-auto" @change="getChart1Data" style="max-width: 250px;" :items="[
        '2017 LPL 春季赛', '2017 LPL 夏季赛', '2017 全球总决赛',
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

          <v-container class="chart-1-container">
            <!-- 图1 -->
            <v-data-table-virtual :headers="Data.chart1.headers" :items="Data.chart1.teams" item-value="name"
              class="elevation-1" height="16vh">
            </v-data-table-virtual>
          </v-container>


          <v-container class="chart-2-container">
            <!-- 图2 -->
            <heatMap :teamNames="Data.chart2.teamNames" :data="Data.chart2.heatMapData" title="16支战队对抗胜率热力图" />
          </v-container>

          <v-container class="chart-3-container">
            <!-- 图3 -->
            <teamAgainstChart :teamData="Data.chart3.teamData"></teamAgainstChart>
          </v-container>

        </div>


        <div class="column">
          <div class="little-title">
            选手
          </div>

          <v-container class="chart-4-container">
            <!-- 图4 -->
            <boxPlot :data="Data.chart4.playerBoxPlotData"></boxPlot>
          </v-container>

          <v-container class="chart-5-container">
            <!-- 图5 -->
            <v-row>
              <v-col>
                <v-select v-model="Data.chart5.xAxis" :items="Data.chart5.axisOptions" dense outlined label="横坐标"
                  style="max-height: 50px;" />
              </v-col>
              <v-col>
                <v-select v-model="Data.chart5.yAxis" :items="Data.chart5.axisOptions" dense outlined label="纵坐标"
                  style="max-height: 50px;" />
              </v-col>
            </v-row>

            <scatterChart :data="Data.chart5.scatterDiagramData" :x-axis="Data.chart5.xAxis"
              :y-axis="Data.chart5.yAxis" />
          </v-container>

          <v-container class="chart-6-container">
            <!-- 图6 -->
            <contestantRadarChart :players="Data.chart6.players"></contestantRadarChart>
          </v-container>

        </div>


        <div class="column">
          <div class="little-title">
            英雄
          </div>

          <v-container class="chart-7-container">
            <!-- 图7 -->
            <bpWordcloudChart :options="Data.chart7" @wordClick="bpwordcloudclick"></bpWordcloudChart>
          </v-container>

          <v-container class="chart-8-container">
            <!-- 图8 -->
            <bpBarChart :heroData="Data.chart8.herodata"></bpBarChart>
          </v-container>

          <v-container class="chart-9-container">
            <!-- 图9 -->
            <heroAgainstChart :heroData="Data.chart9.herodata"></heroAgainstChart>
          </v-container>

        </div>
      </section>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onBeforeMount } from 'vue'
import contestantRadarChart from './components/contestant-radar-chart.vue';
import bpBarChart from './components/bp-bar-chart.vue';
import bpWordcloudChart from './components/bp-wordcloud-chart.vue';
import heroAgainstChart from './components/hero-against-chart.vue';
import teamAgainstChart from './components/team-against-chart.vue';
import heatMap from './components/heatMap.vue';
import boxPlot from './components/box-plot.vue';
import scatterChart from './components/scatter-chart.vue';

import axios from 'axios'
import 'echarts-wordcloud';


const topic = ref('2024 全球总决赛')


const Data = reactive({

  chart1: {
    headers: [
      { title: '战队', align: 'start', key: 'team', },
      { title: '胜场', align: 'end', key: 'matches_won' },
      { title: '负场', align: 'end', key: 'matches_lose' },
      { title: '胜率', align: 'end', key: 'win_rate', }
    ],
    teams: []
  },

  chart2: {
    teamNames: [],
    heatMapData: []
  },


  //队伍对抗图
  chart3: {
    teamData: [
      { name: '队伍1', headimg: '1', winRate: 42, BloodRate: 47, TowerRate: 57, DragonRate: 55 },
      { name: '队伍2', headimg: '1', winRate: 55, BloodRate: 62, TowerRate: 55, DragonRate: 48 }
    ]
  },

  chart4: {
    playerBoxPlotData: [
      { player: 'xiaohu', kills: 7, deaths: 5, assists: 6 },
      { player: 'faker', kills: 8, deaths: 8, assists: 7 },
      { player: 'knight', kills: 9, deaths: 7, assists: 12 },
      { player: 'bin', kills: 10, deaths: 15, assists: 10 },
      { player: 'on', kills: 11, deaths: 9, assists: 6 },
      { player: 'jkl', kills: 12, deaths: 9, assists: 7 },
      { player: 'theshy', kills: 14, deaths: 14, assists: 6 },
      { player: 'doinb', kills: 19, deaths: 12, assists: 7 },
    ],
  },

  chart5: {
    xAxis: ref('gold'),
    yAxis: ref('damage'),
    axisOptions: ['gold', 'damage', 'tanking', 'cs'],
    scatterDiagramData: [
      { player: 'xiaohu', gold: 7785, damage: 8545, tanking: 16456, cs: 456, },
      { player: 'xiaohu', gold: 7457, damage: 5455, tanking: 8456, cs: 123, },
      { player: 'xiaohu', gold: 6547, damage: 12545, tanking: 7456, cs: 333, },
      { player: 'xiaohu', gold: 4745, damage: 7545, tanking: 9456, cs: 222, },
      { player: 'xiaohu', gold: 5745, damage: 4545, tanking: 5456, cs: 389, },
      { player: 'xiaohu', gold: 6666, damage: 13545, tanking: 6456, cs: 356, },
    ]
  },


  //选手雷达图数据
  chart6: {
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

  // bp词云图数据
  chart7: {
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


  //bp柱状图数据
  chart8: {
    herodata: [
      { name: '英雄1', matches: 200, pickRate: 0.4, winRate: 0.55 },
      { name: '英雄2', matches: 350, pickRate: 0.5, winRate: 0.45 },
      { name: '英雄3', matches: 100, pickRate: 0.25, winRate: 0.65 },
      { name: '英雄4', matches: 150, pickRate: 0.35, winRate: 0.50 },
      { name: '英雄5', matches: 500, pickRate: 0.6, winRate: 0.48 }
    ]
  },

  //英雄对抗图数据
  chart9: {
    herodata: [
      { name: '英雄1', headimg: '1', winRate: 42, pickRate: 20, banRate: 10 },
      { name: '英雄2', headimg: '1', winRate: 55, pickRate: 40, banRate: 20 },
      { name: '英雄2', headimg: '1', winRate: 55, pickRate: 40, banRate: 20 },
      { name: '封魔剑魂', headimg: '2', winRate: 55, pickRate: 40, banRate: 20 },
    ]
  },


})

const bpwordcloudclick = (word: string) => {
  console.log('点击了词：', word);
  console.log('当前 heroagainst.herodata:', Data.chart9.herodata);

  if (!Data.chart9 || !Data.chart9.herodata) {
    console.error('heroagainst 或 heroagainst.herodata 未定义');
    return;
  }

  const targetIndex = Data.chart9.herodata.findIndex(item => item.name === word);
  if (targetIndex !== -1) {
    [Data.chart9.herodata[0], Data.chart9.herodata[targetIndex]] = [Data.chart9.herodata[targetIndex], Data.chart9.herodata[0]];
    console.log('互换成功', Data.chart9.herodata[0]);
  } else {
    console.log('未找到对应的英雄');
  }
};

onMounted(() => {
})

onBeforeMount(() => {
  getChart1Data()
  getChart2Data()
})



function getChart1Data() {
  // newValue 可以替换topic
  console.log('正在获取图1的数据')
  axios.get('http://192.168.198.10:8080/team/getWinRate', {
    // headers: {
    //   "x-requested-with": "XMLHttpRequest"
    // },
    params: {
      matchType: topic.value
    }
  }).then(response => {
    console.log(response)
    if (response.data.code == 200) {
      console.log('code=200')
      Data.chart1.teams = response.data.data
    }
    else {
      console.log("code=", response.data.code)
    }
  }).catch(error => {
    console.log(error)
  })
}


function getChart2Data() {
  console.log('正在获取图2的数据')
  axios.get('http://192.168.198.10:8080/team/getWinRate', {
    params: {
      matchType: topic.value
    }
  }).then(response => {
    console.log(response)
    if (response.data.code == 200) {
      console.log('code=200')


    }
    else {
      console.log("code=", response.data.code)
    }
  }).catch(error => {
    console.log(error)
  })
}



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

.little-title {
  text-align: center;
  height: 5vh;
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



.chart-1-container {
  height: 350px;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  /* 轻微阴影效果 */
  border-radius: 10px;
  margin: 1vh;
  transition: transform 0.3s ease;
}


.chart-2-container {
  height: 350px;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  /* 轻微阴影效果 */
  border-radius: 10px;
  margin: 1vh;
  transition: transform 0.3s ease;
}

.chart-3-container {
  height: 350px;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  /* 轻微阴影效果 */
  border-radius: 10px;
  margin: 1vh;
  transition: transform 0.3s ease;
}

.chart-4-container {
  height: 350px;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  /* 轻微阴影效果 */
  border-radius: 10px;
  margin: 1vh;
  transition: transform 0.3s ease;
}

.chart-5-container {
  height: 350px;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  /* 轻微阴影效果 */
  border-radius: 10px;
  margin: 1vh;
  transition: transform 0.3s ease;
}

.chart-6-container {
  height: 350px;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  /* 轻微阴影效果 */
  border-radius: 10px;
  margin: 1vh;
  transition: transform 0.3s ease;
}

.chart-7-container {
  height: 350px;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  /* 轻微阴影效果 */
  border-radius: 10px;
  margin: 1vh;
  transition: transform 0.3s ease;
}

.chart-8-container {
  height: 350px;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  /* 轻微阴影效果 */
  border-radius: 10px;
  margin: 1vh;
  transition: transform 0.3s ease;
}

.chart-9-container {
  height: 350px;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  /* 轻微阴影效果 */
  border-radius: 10px;
  margin: 1vh;
  transition: transform 0.3s ease;
}
</style>
