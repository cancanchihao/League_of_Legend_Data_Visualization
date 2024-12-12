<template>
  <v-app>

    <!-- 全屏覆盖层 -->
    <!-- <v-overlay v-if="showOverlay">
      <v-container class="overlay-container" absolute>
        <v-img src="src/assets/overLay.jpg" contain class="overlay-image"></v-img>
        <div class="overlay-content">
          <h1 class="overlay-title">欢迎来到比赛数据平台</h1>
          <p class="overlay-description">
            这里提供了多赛季比赛数据分析，包括战队对抗、选手表现、英雄统计等，
            帮助您快速了解赛事动态。
          </p>
          <v-btn color="primary" large @click="startApp">开始</v-btn>
        </div>
      </v-container>
    </v-overlay> -->

    <!-- 全屏遮罩层 -->
    <div v-if="showOverlay" class="full-screen-overlay">
      <v-img src="src/assets/overLay.jpg" cover class="overlay-image full-screen-image">
        <div class="overlay-content centered-content">
          <div class="overlay-box">
            <h1 class="overlay-title">欢迎来到比赛数据平台</h1>
            <p class="overlay-description">
              这里提供了多赛季比赛数据分析，包括战队对抗、选手表现、英雄统计等，
              帮助您快速了解赛事动态。
            </p>
            <v-btn color="primary" large @click="startApp">开始</v-btn>
          </div>
        </div>
      </v-img>
    </div>



    <!-- 主页面内容 -->
    <template v-else>
      <!-- 顶部导航栏 -->
      <v-app-bar class="wrapper">
        <v-container class="title-container">
          <span class="big-title">
            {{ topic }}
          </span>
        </v-container>
        <v-select label="选择赛段" v-model='topic' class="ml-auto" @update:model-value="getData" style="width: 20vh;"
          :items="[
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
              <template v-if="Data.chart2.isChartVisible">
                <!-- 图1 -->
                <v-data-table-virtual :headers="Data.chart1.headers" :items="Data.chart1.teams" item-value="name"
                  class="elevation-1" style="width: 100%;height:100%">
                </v-data-table-virtual>
              </template>
              <template v-else>
                <v-progress-circular indeterminate color="primary" size="64" class="progress-center" />
              </template>
            </v-container>


            <v-container class="chart-2-container">
              <template v-if="Data.chart2.isChartVisible">
                <!-- 图2 -->
                <heatMap :teamNames="Data.chart2.teamNames" :data="Data.chart2.heatMapData" @wordClick="heatmapclick"
                  style="position: relative;" title="战队对抗胜率热力图" />
              </template>
              <template v-else>
                <v-progress-circular indeterminate color="primary" size="64" class="progress-center" />
              </template>
            </v-container>


            <v-container class="chart-3-container">
              <template v-if="Data.chart2.isChartVisible">
                <!-- 图3 -->
                <teamAgainstChart :teamData="Data.chart3.teamData"></teamAgainstChart>
              </template>
              <template v-else>
                <v-progress-circular indeterminate color="primary" size="64" class="progress-center" />
              </template>
            </v-container>
          </div>


          <div class="column">
            <div class="little-title">
              选手
            </div>

            <v-container class="chart-4-container">
              <template v-if="Data.chart2.isChartVisible">
                <!-- 图4 -->
                <boxPlot :data="Data.chart4.playerBoxPlotData"></boxPlot>
              </template>
              <template v-else>
                <v-progress-circular indeterminate color="primary" size="64" class="progress-center" />
              </template>
            </v-container>


            <v-container class="chart-5-container">
              <template v-if="Data.chart2.isChartVisible">
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
              </template>
              <template v-else>
                <v-progress-circular indeterminate color="primary" size="64" class="progress-center" />
              </template>
            </v-container>


            <v-container class="chart-6-container">
              <template v-if="Data.chart2.isChartVisible">
                <!-- 图6 -->
                <contestantRadarChart :players="Data.chart6.players"></contestantRadarChart>
              </template>
              <template v-else>
                <v-progress-circular indeterminate color="primary" size="64" class="progress-center" />
              </template>
            </v-container>

          </div>


          <div class="column">
            <div class="little-title">
              英雄
            </div>

            <v-container class="chart-7-container">
              <template v-if="Data.chart2.isChartVisible">
                <!-- 图7 -->
                <bpWordcloudChart :data="Data.chart7.bpWordCloudData" @wordClick="bpwordcloudclick"></bpWordcloudChart>
              </template>
              <template v-else>
                <v-progress-circular indeterminate color="primary" size="64" class="progress-center" />
              </template>
            </v-container>


            <v-container class="chart-8-container">
              <template v-if="Data.chart2.isChartVisible">
                <!-- 图8 -->
                <v-select label="排序方式" class="ml-auto" v-model='Data.chart8.sortWay' :items="[
                  '胜率', 'ban率', 'pick率',]">
                </v-select>
                <bpBarChart :herodata="Data.chart8.heroData" style="max-height: 23vh;"></bpBarChart>
                <v-pagination v-model="Data.chart8.currentPage" :length="Data.chart8.totalPage" :total-visible="5">
                </v-pagination>
              </template>
              <template v-else>
                <v-progress-circular indeterminate color="primary" size="64" class="progress-center" />
              </template>
            </v-container>


            <v-container class="chart-9-container">
              <template v-if="Data.chart2.isChartVisible">
                <!-- 图9 -->
                <heroAgainstChart :heroData="Data.chart9.herodata"></heroAgainstChart>
              </template>
              <template v-else>
                <v-progress-circular indeterminate color="primary" size="64" class="progress-center" />
              </template>
            </v-container>

          </div>
        </section>
      </v-main>
    </template>
  </v-app>
</template>


<script setup lang="ts">
import { ref, reactive, onMounted, onBeforeMount } from 'vue'
import axios from 'axios'
import 'echarts-wordcloud';

import contestantRadarChart from './components/contestant-radar-chart.vue';
import bpBarChart from './components/bp-bar-chart.vue';
import bpWordcloudChart from './components/bp-wordcloud-chart.vue';
import heroAgainstChart from './components/hero-against-chart.vue';
import teamAgainstChart from './components/team-against-chart.vue';
import heatMap from './components/heatMap.vue';
import boxPlot from './components/box-plot.vue';
import scatterChart from './components/scatter-chart.vue';



const topic = ref('2024 全球总决赛')
const showOverlay = ref(true)

function startApp() {
  showOverlay.value = false
}


interface Header {
  title: string;
  align: "start" | "end" | "center";  // 限定 align 的值
  key: string;
}

const Data = reactive({

  chart1: {
    isChartVisible: true,
    headers: [
      { title: '战队', align: 'start', key: 'team', },
      { title: '胜场', align: 'end', key: 'matches_won' },
      { title: '负场', align: 'end', key: 'matches_lose' },
      { title: '胜率%', align: 'end', key: 'win_rate', }
    ] as Header[],
    teams: [
      {
        "team": "T1",
        "matches_won": 13,
        "matches_lose": 4,
        "win_rate": 76.47
      },
      {
        "team": "BLG",
        "matches_won": 13,
        "matches_lose": 6,
        "win_rate": 68.42
      },
      {
        "team": "LNG",
        "matches_won": 4,
        "matches_lose": 3,
        "win_rate": 57.14
      },
      {
        "team": "HLE",
        "matches_won": 6,
        "matches_lose": 5,
        "win_rate": 54.55
      },
      {
        "team": "GEN",
        "matches_won": 7,
        "matches_lose": 6,
        "win_rate": 53.85
      },
      {
        "team": "TL",
        "matches_won": 5,
        "matches_lose": 5,
        "win_rate": 50
      },
      {
        "team": "FLY",
        "matches_won": 7,
        "matches_lose": 7,
        "win_rate": 50
      },
      {
        "team": "WBG",
        "matches_won": 8,
        "matches_lose": 8,
        "win_rate": 50
      },
      {
        "team": "TES",
        "matches_won": 4,
        "matches_lose": 4,
        "win_rate": 50
      },
      {
        "team": "GAM",
        "matches_won": 3,
        "matches_lose": 5,
        "win_rate": 37.5
      },
      {
        "team": "G2",
        "matches_won": 3,
        "matches_lose": 5,
        "win_rate": 37.5
      },
      {
        "team": "FNC",
        "matches_won": 2,
        "matches_lose": 4,
        "win_rate": 33.33
      },
      {
        "team": "DK",
        "matches_won": 3,
        "matches_lose": 6,
        "win_rate": 33.33
      },
      {
        "team": "PSG",
        "matches_won": 1,
        "matches_lose": 4,
        "win_rate": 20
      },
      {
        "team": "MDK",
        "matches_won": 1,
        "matches_lose": 4,
        "win_rate": 20
      },
      {
        "team": "PNG",
        "matches_won": 0,
        "matches_lose": 4,
        "win_rate": 0
      }
    ],
  },

  // 热力图数据
  chart2: {
    isChartVisible: true,
    isDataReady: false,
    teamNames: [
      "PSG",
      "T1",
      "FNC",
      "TL",
      "GEN",
      "FLY",
      "GAM",
      "WBG",
      "G2",
      "HLE",
      "LNG",
      "PNG",
      "BLG",
      "TES",
      "MDK",
      "DK"
    ],
    heatMapData: [
      [
        0,
        0,
        "-"
      ],
      [
        0,
        1,
        "-"
      ],
      [
        0,
        2,
        "-"
      ],
      [
        0,
        3,
        "-"
      ],
      [
        0,
        4,
        "-"
      ],
      [
        0,
        5,
        100.0
      ],
      [
        0,
        6,
        "-"
      ],
      [
        0,
        7,
        "-"
      ],
      [
        0,
        8,
        "-"
      ],
      [
        0,
        9,
        100.0
      ],
      [
        0,
        10,
        "-"
      ],
      [
        0,
        11,
        "-"
      ],
      [
        0,
        12,
        100.0
      ],
      [
        0,
        13,
        "-"
      ],
      [
        0,
        14,
        0.0
      ],
      [
        0,
        15,
        "-"
      ],
      [
        1,
        0,
        "-"
      ],
      [
        1,
        1,
        "-"
      ],
      [
        1,
        2,
        "-"
      ],
      [
        1,
        3,
        "-"
      ],
      [
        1,
        4,
        25.0
      ],
      [
        1,
        5,
        "-"
      ],
      [
        1,
        6,
        "-"
      ],
      [
        1,
        7,
        "-"
      ],
      [
        1,
        8,
        0.0
      ],
      [
        1,
        9,
        "-"
      ],
      [
        1,
        10,
        "-"
      ],
      [
        1,
        11,
        0.0
      ],
      [
        1,
        12,
        33.33
      ],
      [
        1,
        13,
        25.0
      ],
      [
        1,
        14,
        "-"
      ],
      [
        1,
        15,
        "-"
      ],
      [
        2,
        0,
        "-"
      ],
      [
        2,
        1,
        "-"
      ],
      [
        2,
        2,
        "-"
      ],
      [
        2,
        3,
        "-"
      ],
      [
        2,
        4,
        "-"
      ],
      [
        2,
        5,
        "-"
      ],
      [
        2,
        6,
        0.0
      ],
      [
        2,
        7,
        66.67
      ],
      [
        2,
        8,
        "-"
      ],
      [
        2,
        9,
        "-"
      ],
      [
        2,
        10,
        "-"
      ],
      [
        2,
        11,
        "-"
      ],
      [
        2,
        12,
        "-"
      ],
      [
        2,
        13,
        100.0
      ],
      [
        2,
        14,
        "-"
      ],
      [
        2,
        15,
        100.0
      ],
      [
        3,
        0,
        "-"
      ],
      [
        3,
        1,
        "-"
      ],
      [
        3,
        2,
        "-"
      ],
      [
        3,
        3,
        "-"
      ],
      [
        3,
        4,
        "-"
      ],
      [
        3,
        5,
        66.67
      ],
      [
        3,
        6,
        33.33
      ],
      [
        3,
        7,
        100.0
      ],
      [
        3,
        8,
        "-"
      ],
      [
        3,
        9,
        "-"
      ],
      [
        3,
        10,
        100.0
      ],
      [
        3,
        11,
        0.0
      ],
      [
        3,
        12,
        "-"
      ],
      [
        3,
        13,
        "-"
      ],
      [
        3,
        14,
        "-"
      ],
      [
        3,
        15,
        "-"
      ],
      [
        4,
        0,
        "-"
      ],
      [
        4,
        1,
        75.0
      ],
      [
        4,
        2,
        "-"
      ],
      [
        4,
        3,
        "-"
      ],
      [
        4,
        4,
        "-"
      ],
      [
        4,
        5,
        40.0
      ],
      [
        4,
        6,
        "-"
      ],
      [
        4,
        7,
        0.0
      ],
      [
        4,
        8,
        "-"
      ],
      [
        4,
        9,
        50.0
      ],
      [
        4,
        10,
        "-"
      ],
      [
        4,
        11,
        "-"
      ],
      [
        4,
        12,
        "-"
      ],
      [
        4,
        13,
        0.0
      ],
      [
        4,
        14,
        "-"
      ],
      [
        4,
        15,
        "-"
      ],
      [
        5,
        0,
        0.0
      ],
      [
        5,
        1,
        "-"
      ],
      [
        5,
        2,
        "-"
      ],
      [
        5,
        3,
        33.33
      ],
      [
        5,
        4,
        60.0
      ],
      [
        5,
        5,
        "-"
      ],
      [
        5,
        6,
        0.0
      ],
      [
        5,
        7,
        "-"
      ],
      [
        5,
        8,
        "-"
      ],
      [
        5,
        9,
        66.67
      ],
      [
        5,
        10,
        "-"
      ],
      [
        5,
        11,
        "-"
      ],
      [
        5,
        12,
        "-"
      ],
      [
        5,
        13,
        "-"
      ],
      [
        5,
        14,
        "-"
      ],
      [
        5,
        15,
        100.0
      ],
      [
        6,
        0,
        "-"
      ],
      [
        6,
        1,
        "-"
      ],
      [
        6,
        2,
        100.0
      ],
      [
        6,
        3,
        66.67
      ],
      [
        6,
        4,
        "-"
      ],
      [
        6,
        5,
        100.0
      ],
      [
        6,
        6,
        "-"
      ],
      [
        6,
        7,
        "-"
      ],
      [
        6,
        8,
        "-"
      ],
      [
        6,
        9,
        "-"
      ],
      [
        6,
        10,
        "-"
      ],
      [
        6,
        11,
        "-"
      ],
      [
        6,
        12,
        "-"
      ],
      [
        6,
        13,
        "-"
      ],
      [
        6,
        14,
        33.33
      ],
      [
        6,
        15,
        "-"
      ],
      [
        7,
        0,
        "-"
      ],
      [
        7,
        1,
        "-"
      ],
      [
        7,
        2,
        33.33
      ],
      [
        7,
        3,
        0.0
      ],
      [
        7,
        4,
        100.0
      ],
      [
        7,
        5,
        "-"
      ],
      [
        7,
        6,
        "-"
      ],
      [
        7,
        7,
        "-"
      ],
      [
        7,
        8,
        100.0
      ],
      [
        7,
        9,
        "-"
      ],
      [
        7,
        10,
        25.0
      ],
      [
        7,
        11,
        "-"
      ],
      [
        7,
        12,
        100.0
      ],
      [
        7,
        13,
        "-"
      ],
      [
        7,
        14,
        "-"
      ],
      [
        7,
        15,
        33.33
      ],
      [
        8,
        0,
        "-"
      ],
      [
        8,
        1,
        100.0
      ],
      [
        8,
        2,
        "-"
      ],
      [
        8,
        3,
        "-"
      ],
      [
        8,
        4,
        "-"
      ],
      [
        8,
        5,
        "-"
      ],
      [
        8,
        6,
        "-"
      ],
      [
        8,
        7,
        0.0
      ],
      [
        8,
        8,
        "-"
      ],
      [
        8,
        9,
        100.0
      ],
      [
        8,
        10,
        "-"
      ],
      [
        8,
        11,
        0.0
      ],
      [
        8,
        12,
        66.67
      ],
      [
        8,
        13,
        "-"
      ],
      [
        8,
        14,
        "-"
      ],
      [
        8,
        15,
        "-"
      ],
      [
        9,
        0,
        0.0
      ],
      [
        9,
        1,
        "-"
      ],
      [
        9,
        2,
        "-"
      ],
      [
        9,
        3,
        "-"
      ],
      [
        9,
        4,
        50.0
      ],
      [
        9,
        5,
        33.33
      ],
      [
        9,
        6,
        "-"
      ],
      [
        9,
        7,
        "-"
      ],
      [
        9,
        8,
        0.0
      ],
      [
        9,
        9,
        "-"
      ],
      [
        9,
        10,
        "-"
      ],
      [
        9,
        11,
        "-"
      ],
      [
        9,
        12,
        75.0
      ],
      [
        9,
        13,
        "-"
      ],
      [
        9,
        14,
        "-"
      ],
      [
        9,
        15,
        "-"
      ],
      [
        10,
        0,
        "-"
      ],
      [
        10,
        1,
        "-"
      ],
      [
        10,
        2,
        "-"
      ],
      [
        10,
        3,
        0.0
      ],
      [
        10,
        4,
        "-"
      ],
      [
        10,
        5,
        "-"
      ],
      [
        10,
        6,
        "-"
      ],
      [
        10,
        7,
        75.0
      ],
      [
        10,
        8,
        "-"
      ],
      [
        10,
        9,
        "-"
      ],
      [
        10,
        10,
        "-"
      ],
      [
        10,
        11,
        "-"
      ],
      [
        10,
        12,
        "-"
      ],
      [
        10,
        13,
        "-"
      ],
      [
        10,
        14,
        "-"
      ],
      [
        10,
        15,
        0.0
      ],
      [
        11,
        0,
        "-"
      ],
      [
        11,
        1,
        100.0
      ],
      [
        11,
        2,
        "-"
      ],
      [
        11,
        3,
        100.0
      ],
      [
        11,
        4,
        "-"
      ],
      [
        11,
        5,
        "-"
      ],
      [
        11,
        6,
        "-"
      ],
      [
        11,
        7,
        "-"
      ],
      [
        11,
        8,
        100.0
      ],
      [
        11,
        9,
        "-"
      ],
      [
        11,
        10,
        "-"
      ],
      [
        11,
        11,
        "-"
      ],
      [
        11,
        12,
        "-"
      ],
      [
        11,
        13,
        "-"
      ],
      [
        11,
        14,
        "-"
      ],
      [
        11,
        15,
        "-"
      ],
      [
        12,
        0,
        0.0
      ],
      [
        12,
        1,
        66.67
      ],
      [
        12,
        2,
        "-"
      ],
      [
        12,
        3,
        "-"
      ],
      [
        12,
        4,
        "-"
      ],
      [
        12,
        5,
        "-"
      ],
      [
        12,
        6,
        "-"
      ],
      [
        12,
        7,
        0.0
      ],
      [
        12,
        8,
        33.33
      ],
      [
        12,
        9,
        25.0
      ],
      [
        12,
        10,
        "-"
      ],
      [
        12,
        11,
        "-"
      ],
      [
        12,
        12,
        "-"
      ],
      [
        12,
        13,
        "-"
      ],
      [
        12,
        14,
        0.0
      ],
      [
        12,
        15,
        "-"
      ],
      [
        13,
        0,
        "-"
      ],
      [
        13,
        1,
        75.0
      ],
      [
        13,
        2,
        0.0
      ],
      [
        13,
        3,
        "-"
      ],
      [
        13,
        4,
        100.0
      ],
      [
        13,
        5,
        "-"
      ],
      [
        13,
        6,
        "-"
      ],
      [
        13,
        7,
        "-"
      ],
      [
        13,
        8,
        "-"
      ],
      [
        13,
        9,
        "-"
      ],
      [
        13,
        10,
        "-"
      ],
      [
        13,
        11,
        "-"
      ],
      [
        13,
        12,
        "-"
      ],
      [
        13,
        13,
        "-"
      ],
      [
        13,
        14,
        "-"
      ],
      [
        13,
        15,
        0.0
      ],
      [
        14,
        0,
        100.0
      ],
      [
        14,
        1,
        "-"
      ],
      [
        14,
        2,
        "-"
      ],
      [
        14,
        3,
        "-"
      ],
      [
        14,
        4,
        "-"
      ],
      [
        14,
        5,
        "-"
      ],
      [
        14,
        6,
        66.67
      ],
      [
        14,
        7,
        "-"
      ],
      [
        14,
        8,
        "-"
      ],
      [
        14,
        9,
        "-"
      ],
      [
        14,
        10,
        "-"
      ],
      [
        14,
        11,
        "-"
      ],
      [
        14,
        12,
        100.0
      ],
      [
        14,
        13,
        "-"
      ],
      [
        14,
        14,
        "-"
      ],
      [
        14,
        15,
        "-"
      ],
      [
        15,
        0,
        "-"
      ],
      [
        15,
        1,
        "-"
      ],
      [
        15,
        2,
        0.0
      ],
      [
        15,
        3,
        "-"
      ],
      [
        15,
        4,
        "-"
      ],
      [
        15,
        5,
        0.0
      ],
      [
        15,
        6,
        "-"
      ],
      [
        15,
        7,
        66.67
      ],
      [
        15,
        8,
        "-"
      ],
      [
        15,
        9,
        "-"
      ],
      [
        15,
        10,
        100.0
      ],
      [
        15,
        11,
        "-"
      ],
      [
        15,
        12,
        "-"
      ],
      [
        15,
        13,
        100.0
      ],
      [
        15,
        14,
        "-"
      ],
      [
        15,
        15,
        "-"
      ]
    ],
  },

  //队伍对抗图
  chart3: {
    isChartVisible: true,
    teamData: [
      { name: 'BLG', baron: 1, dragon: 2, turts: 3, KDA: 7, winCount: 2 },
      { name: 'T1', baron: 3, dragon: 1, turts: 5, KDA: 10, winCount: 1 }
    ],
  },

  // 箱线图数据
  chart4: {
    isChartVisible: true,
    playerBoxPlotData: [
      {
        "player": "369",
        "kills": 20,
        "deaths": 19,
        "assists": 39
      },
      {
        "player": "Azhi",
        "kills": 11,
        "deaths": 15,
        "assists": 24
      },
      {
        "player": "Bin",
        "kills": 66,
        "deaths": 38,
        "assists": 99
      },
      {
        "player": "Breathe",
        "kills": 61,
        "deaths": 44,
        "assists": 85
      },
      {
        "player": "Brokenblade",
        "kills": 27,
        "deaths": 20,
        "assists": 47
      },
      {
        "player": "Bwipo",
        "kills": 30,
        "deaths": 58,
        "assists": 68
      },
      {
        "player": "Doran",
        "kills": 36,
        "deaths": 31,
        "assists": 62
      },
      {
        "player": "Impact",
        "kills": 25,
        "deaths": 29,
        "assists": 47
      },
      {
        "player": "Kiin",
        "kills": 25,
        "deaths": 33,
        "assists": 75
      },
      {
        "player": "Kingen",
        "kills": 15,
        "deaths": 32,
        "assists": 42
      },
      {
        "player": "Myrwn",
        "kills": 11,
        "deaths": 18,
        "assists": 11
      },
      {
        "player": "Oscarinin",
        "kills": 12,
        "deaths": 21,
        "assists": 29
      },
      {
        "player": "Wizer",
        "kills": 12,
        "deaths": 13,
        "assists": 9
      },
      {
        "player": "Zeus",
        "kills": 44,
        "deaths": 32,
        "assists": 108
      },
      {
        "player": "Zika",
        "kills": 31,
        "deaths": 23,
        "assists": 47
      },
      {
        "player": "Canyon",
        "kills": 26,
        "deaths": 26,
        "assists": 97
      },
      {
        "player": "Cariok",
        "kills": 2,
        "deaths": 17,
        "assists": 24
      },
      {
        "player": "Elyoya",
        "kills": 6,
        "deaths": 18,
        "assists": 27
      },
      {
        "player": "Inspired",
        "kills": 15,
        "deaths": 29,
        "assists": 121
      },
      {
        "player": "Junjia",
        "kills": 9,
        "deaths": 18,
        "assists": 40
      },
      {
        "player": "Lucid",
        "kills": 17,
        "deaths": 41,
        "assists": 54
      },
      {
        "player": "Oner",
        "kills": 45,
        "deaths": 29,
        "assists": 127
      },
      {
        "player": "Peanut",
        "kills": 12,
        "deaths": 35,
        "assists": 120
      },
      {
        "player": "Razork",
        "kills": 12,
        "deaths": 19,
        "assists": 47
      },
      {
        "player": "Tarzan",
        "kills": 26,
        "deaths": 49,
        "assists": 145
      },
      {
        "player": "Tian",
        "kills": 16,
        "deaths": 18,
        "assists": 63
      },
      {
        "player": "Umti",
        "kills": 24,
        "deaths": 24,
        "assists": 66
      },
      {
        "player": "Wei",
        "kills": 3,
        "deaths": 6,
        "assists": 27
      },
      {
        "player": "Weiwei",
        "kills": 16,
        "deaths": 24,
        "assists": 72
      },
      {
        "player": "Xun",
        "kills": 37,
        "deaths": 38,
        "assists": 157
      },
      {
        "player": "Yike",
        "kills": 25,
        "deaths": 19,
        "assists": 61
      },
      {
        "player": "Apa",
        "kills": 35,
        "deaths": 32,
        "assists": 42
      },
      {
        "player": "Caps",
        "kills": 19,
        "deaths": 22,
        "assists": 60
      },
      {
        "player": "Chovy",
        "kills": 53,
        "deaths": 18,
        "assists": 65
      },
      {
        "player": "Creme",
        "kills": 25,
        "deaths": 19,
        "assists": 43
      },
      {
        "player": "Dynquedo",
        "kills": 14,
        "deaths": 12,
        "assists": 15
      },
      {
        "player": "Faker",
        "kills": 60,
        "deaths": 36,
        "assists": 97
      },
      {
        "player": "Fresskowy",
        "kills": 18,
        "deaths": 21,
        "assists": 9
      },
      {
        "player": "Humanoid",
        "kills": 14,
        "deaths": 20,
        "assists": 29
      },
      {
        "player": "Knight",
        "kills": 91,
        "deaths": 35,
        "assists": 130
      },
      {
        "player": "Maple",
        "kills": 17,
        "deaths": 18,
        "assists": 23
      },
      {
        "player": "Quad",
        "kills": 56,
        "deaths": 25,
        "assists": 75
      },
      {
        "player": "Scout",
        "kills": 27,
        "deaths": 9,
        "assists": 52
      },
      {
        "player": "Showmaker",
        "kills": 32,
        "deaths": 24,
        "assists": 43
      },
      {
        "player": "Xiaohu",
        "kills": 59,
        "deaths": 37,
        "assists": 117
      },
      {
        "player": "Zeka",
        "kills": 42,
        "deaths": 29,
        "assists": 70
      },
      {
        "player": "Aiming",
        "kills": 45,
        "deaths": 18,
        "assists": 42
      },
      {
        "player": "Betty",
        "kills": 22,
        "deaths": 10,
        "assists": 22
      },
      {
        "player": "Elk",
        "kills": 87,
        "deaths": 48,
        "assists": 116
      },
      {
        "player": "Gala",
        "kills": 34,
        "deaths": 11,
        "assists": 43
      },
      {
        "player": "Gumayusi",
        "kills": 73,
        "deaths": 25,
        "assists": 88
      },
      {
        "player": "Hans Sama",
        "kills": 38,
        "deaths": 25,
        "assists": 39
      },
      {
        "player": "Jackeylove",
        "kills": 32,
        "deaths": 21,
        "assists": 40
      },
      {
        "player": "Light",
        "kills": 75,
        "deaths": 31,
        "assists": 84
      },
      {
        "player": "Massu",
        "kills": 59,
        "deaths": 29,
        "assists": 70
      },
      {
        "player": "Noah",
        "kills": 27,
        "deaths": 9,
        "assists": 26
      },
      {
        "player": "Peyz",
        "kills": 50,
        "deaths": 16,
        "assists": 78
      },
      {
        "player": "Supa",
        "kills": 13,
        "deaths": 20,
        "assists": 19
      },
      {
        "player": "Titan",
        "kills": 7,
        "deaths": 12,
        "assists": 15
      },
      {
        "player": "Viper",
        "kills": 64,
        "deaths": 25,
        "assists": 56
      },
      {
        "player": "Yeon",
        "kills": 38,
        "deaths": 18,
        "assists": 50
      },
      {
        "player": "Alvaro",
        "kills": 1,
        "deaths": 22,
        "assists": 31
      },
      {
        "player": "Busio",
        "kills": 15,
        "deaths": 35,
        "assists": 113
      },
      {
        "player": "Corejj",
        "kills": 8,
        "deaths": 29,
        "assists": 97
      },
      {
        "player": "Crisp",
        "kills": 7,
        "deaths": 52,
        "assists": 170
      },
      {
        "player": "Delight",
        "kills": 5,
        "deaths": 35,
        "assists": 112
      },
      {
        "player": "Hang",
        "kills": 3,
        "deaths": 30,
        "assists": 79
      },
      {
        "player": "Jun",
        "kills": 4,
        "deaths": 19,
        "assists": 51
      },
      {
        "player": "Keria",
        "kills": 8,
        "deaths": 33,
        "assists": 167
      },
      {
        "player": "Kuri",
        "kills": 4,
        "deaths": 14,
        "assists": 24
      },
      {
        "player": "Lehends",
        "kills": 6,
        "deaths": 48,
        "assists": 114
      },
      {
        "player": "Meiko",
        "kills": 3,
        "deaths": 25,
        "assists": 75
      },
      {
        "player": "Mikyx",
        "kills": 5,
        "deaths": 45,
        "assists": 75
      },
      {
        "player": "Moham",
        "kills": 4,
        "deaths": 46,
        "assists": 83
      },
      {
        "player": "On",
        "kills": 10,
        "deaths": 67,
        "assists": 185
      },
      {
        "player": "Woody",
        "kills": 5,
        "deaths": 16,
        "assists": 48
      },
      {
        "player": "Kiaya",
        "kills": 27,
        "deaths": 21,
        "assists": 42
      },
      {
        "player": "Levi",
        "kills": 18,
        "deaths": 29,
        "assists": 49
      },
      {
        "player": "Emo",
        "kills": 22,
        "deaths": 19,
        "assists": 38
      },
      {
        "player": "Easylove",
        "kills": 31,
        "deaths": 19,
        "assists": 34
      },
      {
        "player": "Elio",
        "kills": 5,
        "deaths": 25,
        "assists": 66
      }
    ]

  },

  // 散点图数据
  chart5: {
    isChartVisible: true,
    xAxis: ref('gold'),
    yAxis: ref('damage'),
    axisOptions: ['gold', 'damage', 'tanking', 'cs'],
    scatterDiagramData: [
      {
        "player": "369",
        "gold": 365.6,
        "damage": 16723.4,
        "tanking": 21500.4,
        "cs": 7.5
      },
      {
        "player": "Azhi",
        "gold": 360.4,
        "damage": 17605.9,
        "tanking": 20437.7,
        "cs": 7.6
      },
      {
        "player": "Bin",
        "gold": 393.2,
        "damage": 15968.1,
        "tanking": 19708.8,
        "cs": 7.9
      },
      {
        "player": "Breathe",
        "gold": 412.3,
        "damage": 18924.3,
        "tanking": 27014.9,
        "cs": 8.0
      },
      {
        "player": "Brokenblade",
        "gold": 377.2,
        "damage": 17809.4,
        "tanking": 30175.0,
        "cs": 7.7
      },
      {
        "player": "Bwipo",
        "gold": 379.8,
        "damage": 17222.0,
        "tanking": 33643.5,
        "cs": 8.0
      },
      {
        "player": "Doran",
        "gold": 389.1,
        "damage": 15466.8,
        "tanking": 26332.8,
        "cs": 7.9
      },
      {
        "player": "Impact",
        "gold": 380.2,
        "damage": 15484.6,
        "tanking": 25146.7,
        "cs": 7.3
      },
      {
        "player": "Kiin",
        "gold": 372.6,
        "damage": 17044.8,
        "tanking": 24267.9,
        "cs": 7.9
      },
      {
        "player": "Kingen",
        "gold": 361.2,
        "damage": 17356.0,
        "tanking": 25510.5,
        "cs": 7.4
      },
      {
        "player": "Myrwn",
        "gold": 338.9,
        "damage": 12736.1,
        "tanking": 23216.4,
        "cs": 6.9
      },
      {
        "player": "Oscarinin",
        "gold": 355.3,
        "damage": 11521.6,
        "tanking": 23502.4,
        "cs": 7.3
      },
      {
        "player": "Wizer",
        "gold": 372.1,
        "damage": 12302.1,
        "tanking": 22574.4,
        "cs": 8.2
      },
      {
        "player": "Zeus",
        "gold": 401.0,
        "damage": 14177.6,
        "tanking": 19482.6,
        "cs": 8.0
      },
      {
        "player": "Zika",
        "gold": 432.0,
        "damage": 18590.3,
        "tanking": 34016.3,
        "cs": 8.4
      },
      {
        "player": "Canyon",
        "gold": 339.2,
        "damage": 11454.2,
        "tanking": 35890.7,
        "cs": 6.2
      },
      {
        "player": "Cariok",
        "gold": 293.6,
        "damage": 9058.6,
        "tanking": 34006.0,
        "cs": 5.4
      },
      {
        "player": "Elyoya",
        "gold": 302.3,
        "damage": 7979.3,
        "tanking": 28585.0,
        "cs": 5.6
      },
      {
        "player": "Inspired",
        "gold": 333.7,
        "damage": 11527.1,
        "tanking": 31182.4,
        "cs": 6.2
      },
      {
        "player": "Junjia",
        "gold": 322.3,
        "damage": 9856.7,
        "tanking": 39455.7,
        "cs": 5.8
      },
      {
        "player": "Lucid",
        "gold": 304.1,
        "damage": 10010.0,
        "tanking": 38647.1,
        "cs": 5.2
      },
      {
        "player": "Oner",
        "gold": 362.5,
        "damage": 10463.5,
        "tanking": 29986.9,
        "cs": 6.6
      },
      {
        "player": "Peanut",
        "gold": 321.3,
        "damage": 10396.6,
        "tanking": 33551.4,
        "cs": 5.7
      },
      {
        "player": "Razork",
        "gold": 345.8,
        "damage": 13044.5,
        "tanking": 28566.9,
        "cs": 6.6
      },
      {
        "player": "Tarzan",
        "gold": 312.8,
        "damage": 12110.8,
        "tanking": 31534.8,
        "cs": 5.4
      },
      {
        "player": "Tian",
        "gold": 322.9,
        "damage": 10040.4,
        "tanking": 33943.2,
        "cs": 5.9
      },
      {
        "player": "Umti",
        "gold": 335.6,
        "damage": 11311.5,
        "tanking": 37138.0,
        "cs": 5.9
      },
      {
        "player": "Wei",
        "gold": 341.6,
        "damage": 16187.4,
        "tanking": 31824.9,
        "cs": 5.6
      },
      {
        "player": "Weiwei",
        "gold": 328.1,
        "damage": 10474.9,
        "tanking": 35198.7,
        "cs": 5.8
      },
      {
        "player": "Xun",
        "gold": 334.8,
        "damage": 11710.1,
        "tanking": 30734.5,
        "cs": 5.7
      },
      {
        "player": "Yike",
        "gold": 341.3,
        "damage": 14977.3,
        "tanking": 36204.5,
        "cs": 6.0
      },
      {
        "player": "Apa",
        "gold": 409.3,
        "damage": 20244.8,
        "tanking": 17639.8,
        "cs": 8.6
      },
      {
        "player": "Caps",
        "gold": 382.6,
        "damage": 21740.1,
        "tanking": 24905.2,
        "cs": 8.3
      },
      {
        "player": "Chovy",
        "gold": 428.5,
        "damage": 20467.7,
        "tanking": 19712.1,
        "cs": 9.3
      },
      {
        "player": "Creme",
        "gold": 380.0,
        "damage": 22232.8,
        "tanking": 21105.6,
        "cs": 8.0
      },
      {
        "player": "Dynquedo",
        "gold": 388.8,
        "damage": 18064.4,
        "tanking": 17104.7,
        "cs": 8.5
      },
      {
        "player": "Faker",
        "gold": 404.3,
        "damage": 16110.5,
        "tanking": 19988.3,
        "cs": 8.2
      },
      {
        "player": "Fresskowy",
        "gold": 384.7,
        "damage": 20547.7,
        "tanking": 21162.2,
        "cs": 8.4
      },
      {
        "player": "Humanoid",
        "gold": 397.8,
        "damage": 17413.0,
        "tanking": 22651.9,
        "cs": 9.1
      },
      {
        "player": "Knight",
        "gold": 412.5,
        "damage": 22252.9,
        "tanking": 19086.7,
        "cs": 8.3
      },
      {
        "player": "Maple",
        "gold": 404.5,
        "damage": 24002.0,
        "tanking": 22960.9,
        "cs": 8.8
      },
      {
        "player": "Quad",
        "gold": 402.1,
        "damage": 21174.2,
        "tanking": 16527.9,
        "cs": 8.4
      },
      {
        "player": "Scout",
        "gold": 415.5,
        "damage": 18250.5,
        "tanking": 22116.9,
        "cs": 8.8
      },
      {
        "player": "Showmaker",
        "gold": 384.0,
        "damage": 22350.0,
        "tanking": 21806.9,
        "cs": 8.0
      },
      {
        "player": "Xiaohu",
        "gold": 402.0,
        "damage": 22554.4,
        "tanking": 19425.1,
        "cs": 8.4
      },
      {
        "player": "Zeka",
        "gold": 415.0,
        "damage": 22983.5,
        "tanking": 23853.9,
        "cs": 9.0
      },
      {
        "player": "Aiming",
        "gold": 442.7,
        "damage": 23427.8,
        "tanking": 16429.4,
        "cs": 9.9
      },
      {
        "player": "Betty",
        "gold": 444.5,
        "damage": 26280.7,
        "tanking": 16828.0,
        "cs": 10.0
      },
      {
        "player": "Elk",
        "gold": 434.8,
        "damage": 24383.6,
        "tanking": 14102.8,
        "cs": 9.1
      },
      {
        "player": "Gala",
        "gold": 448.3,
        "damage": 27205.2,
        "tanking": 13335.0,
        "cs": 9.8
      },
      {
        "player": "Gumayusi",
        "gold": 469.7,
        "damage": 20139.1,
        "tanking": 11701.9,
        "cs": 10.3
      },
      {
        "player": "Hans Sama",
        "gold": 418.2,
        "damage": 21089.3,
        "tanking": 16849.9,
        "cs": 8.8
      },
      {
        "player": "Jackeylove",
        "gold": 428.0,
        "damage": 19858.7,
        "tanking": 12708.9,
        "cs": 9.5
      },
      {
        "player": "Light",
        "gold": 440.3,
        "damage": 21660.3,
        "tanking": 14838.9,
        "cs": 9.6
      },
      {
        "player": "Massu",
        "gold": 428.4,
        "damage": 21901.3,
        "tanking": 15883.7,
        "cs": 9.2
      },
      {
        "player": "Noah",
        "gold": 445.3,
        "damage": 21082.7,
        "tanking": 10157.4,
        "cs": 9.7
      },
      {
        "player": "Peyz",
        "gold": 431.7,
        "damage": 21587.2,
        "tanking": 12350.9,
        "cs": 9.4
      },
      {
        "player": "Supa",
        "gold": 394.3,
        "damage": 18908.8,
        "tanking": 15619.2,
        "cs": 9.0
      },
      {
        "player": "Titan",
        "gold": 386.7,
        "damage": 14612.2,
        "tanking": 15613.2,
        "cs": 9.6
      },
      {
        "player": "Viper",
        "gold": 465.2,
        "damage": 27876.1,
        "tanking": 15002.2,
        "cs": 10.4
      },
      {
        "player": "Yeon",
        "gold": 439.7,
        "damage": 24385.6,
        "tanking": 15395.7,
        "cs": 9.9
      },
      {
        "player": "Alvaro",
        "gold": 221.5,
        "damage": 4897.7,
        "tanking": 18565.9,
        "cs": 1.2
      },
      {
        "player": "Busio",
        "gold": 242.6,
        "damage": 5418.3,
        "tanking": 13753.3,
        "cs": 1.1
      },
      {
        "player": "Corejj",
        "gold": 245.9,
        "damage": 5535.4,
        "tanking": 13862.4,
        "cs": 1.0
      },
      {
        "player": "Crisp",
        "gold": 241.8,
        "damage": 5702.6,
        "tanking": 17653.2,
        "cs": 1.1
      },
      {
        "player": "Delight",
        "gold": 241.6,
        "damage": 5163.0,
        "tanking": 14787.7,
        "cs": 1.2
      },
      {
        "player": "Hang",
        "gold": 237.6,
        "damage": 5286.8,
        "tanking": 16107.0,
        "cs": 1.1
      },
      {
        "player": "Jun",
        "gold": 235.5,
        "damage": 4662.3,
        "tanking": 14276.2,
        "cs": 1.0
      },
      {
        "player": "Keria",
        "gold": 255.5,
        "damage": 6263.7,
        "tanking": 12998.1,
        "cs": 1.2
      },
      {
        "player": "Kuri",
        "gold": 223.5,
        "damage": 5319.1,
        "tanking": 15341.3,
        "cs": 1.1
      },
      {
        "player": "Lehends",
        "gold": 238.1,
        "damage": 5756.0,
        "tanking": 15936.1,
        "cs": 1.0
      },
      {
        "player": "Meiko",
        "gold": 234.4,
        "damage": 5256.1,
        "tanking": 15102.8,
        "cs": 1.2
      },
      {
        "player": "Mikyx",
        "gold": 231.6,
        "damage": 4354.0,
        "tanking": 21198.4,
        "cs": 1.0
      },
      {
        "player": "Moham",
        "gold": 234.1,
        "damage": 5371.3,
        "tanking": 20135.5,
        "cs": 1.0
      },
      {
        "player": "On",
        "gold": 241.5,
        "damage": 4747.9,
        "tanking": 14681.1,
        "cs": 1.2
      },
      {
        "player": "Woody",
        "gold": 236.0,
        "damage": 4257.5,
        "tanking": 15693.2,
        "cs": 0.9
      },
      {
        "player": "Kiaya",
        "gold": 379.7,
        "damage": 18304.7,
        "tanking": 23246.4,
        "cs": 7.7
      },
      {
        "player": "Levi",
        "gold": 339.4,
        "damage": 11555.1,
        "tanking": 32249.5,
        "cs": 6.2
      },
      {
        "player": "Emo",
        "gold": 386.4,
        "damage": 15049.6,
        "tanking": 19670.4,
        "cs": 8.8
      },
      {
        "player": "Easylove",
        "gold": 400.8,
        "damage": 17620.5,
        "tanking": 13165.4,
        "cs": 9.0
      },
      {
        "player": "Elio",
        "gold": 232.7,
        "damage": 5018.7,
        "tanking": 15533.8,
        "cs": 1.2
      }
    ]

  },


  //选手雷达图数据
  chart6: {
    isChartVisible: true,
    //KDA  CS   gold  damage   tanking
    players: [
      { name: 'Bin', stats: [20, 10.1, 400, 28885, 22275] },
      { name: 'Zeus', stats: [30, 10.2, 400, 22290, 22295] },
      { name: 'Xun', stats: [20, 9.9, 400, 21370, 22270] },
      { name: 'Oner', stats: [10, 9, 400, 21165, 22265] },
      { name: 'knight', stats: [17, 9, 400, 12395, 22235] },
      { name: 'Faker', stats: [23, 9, 400, 22380, 22275] },
      { name: 'elk', stats: [11, 9, 400, 17795, 22235] },
      { name: 'gumayusi', stats: [5, 9, 400, 22280, 22275] },
      { name: 'On', stats: [13, 9, 400, 14495, 22235] },
      { name: 'Keria', stats: [12, 9, 400, 22280, 22275] },
    ],

  },

  // bp词云图数据
  chart7: {
    isChartVisible: true,
    isDataReady: false,
    bpWordCloudData: [
      {
        "name": "双界灵兔",
        "value": 77
      },
      {
        "name": "封魔剑魂",
        "value": 76
      },
      {
        "name": "上古领主",
        "value": 70
      },
      {
        "name": "武器大师",
        "value": 66
      },
      {
        "name": "寒冰射手",
        "value": 64
      },
      {
        "name": "复仇之矛",
        "value": 60
      },
      {
        "name": "镕铁少女",
        "value": 59
      },
      {
        "name": "虚空之女",
        "value": 55
      },
      {
        "name": "迷失之牙",
        "value": 51
      },
      {
        "name": "机械公敌",
        "value": 45
      },
      {
        "name": "皮城执法官",
        "value": 45
      },
      {
        "name": "爆破鬼才",
        "value": 45
      },
      {
        "name": "圣锤之毅",
        "value": 43
      },
      {
        "name": "发条魔灵",
        "value": 42
      },
      {
        "name": "幻翎",
        "value": 42
      },
      {
        "name": "探险家",
        "value": 41
      },
      {
        "name": "北地之怒",
        "value": 38
      },
      {
        "name": "荒漠屠夫",
        "value": 37
      },
      {
        "name": "炼金男爵",
        "value": 34
      },
      {
        "name": "九尾妖狐",
        "value": 33
      },
      {
        "name": "曙光女神",
        "value": 32
      },
      {
        "name": "解脱者",
        "value": 31
      },
      {
        "name": "逆羽",
        "value": 29
      },
      {
        "name": "戏命师",
        "value": 27
      },
      {
        "name": "炽炎雏龙",
        "value": 27
      },
      {
        "name": "永恒梦魇",
        "value": 26
      },
      {
        "name": "扭曲树精",
        "value": 24
      },
      {
        "name": "翠神",
        "value": 22
      },
      {
        "name": "纳祖芒荣耀",
        "value": 22
      },
      {
        "name": "牛头酋长",
        "value": 21
      },
      {
        "name": "万花通灵",
        "value": 20
      },
    ],

  },


  //bp柱状图数据
  chart8: {
    isChartVisible: true,
    heroData: [
      { name: '封魔剑魂', banRate: 30, pickRate: 33, winRate: 54 },
      { name: '双界灵兔', banRate: 17, pickRate: 32, winRate: 43 },
      { name: '武器大师', banRate: 13, pickRate: 12, winRate: 54 },
      { name: '寒冰射手', banRate: 22, pickRate: 54, winRate: 34 },
      { name: '上古领主', banRate: 5, pickRate: 32, winRate: 70 },
      { name: '圣锤之毅', banRate: 23, pickRate: 43, winRate: 56 },
      { name: '虚空之女', banRate: 12, pickRate: 100, winRate: 76 },
    ],
    // heroData: [],
    sortWay: '胜率',
    totalPage: 6,
    currentPage: 1
  },

  //英雄对抗图数据
  chart9: {
    isChartVisible: true,
    herodata: [
      { name: '疾风剑豪', winCount: 1, KDA: 4, gold: 23451, damage: 12343, tanking: 23323 },
      { name: '盲僧', winCount: 3, KDA: 3, gold: 13451, damage: 22343, tanking: 13323 },
    ],
    // heroAgainstData: [
    //   { name: '剑魔', winCount: 1, KDA: 4, gold: 23451, damage: 12343, tanking: 23323 },
    //   { name: '剑豪', winCount: 3, KDA: 3, gold: 13451, damage: 22343, tanking: 13323 },
    // ]
  },
})

const bpwordcloudclick = (clickname: string) => {
  console.log('点击英雄：', clickname);
  console.log('当前 heroagainst.herodata:', Data.chart9.herodata);

  // TODO:
  // 获取新英雄数据
  // getChart9Data();
  // if ( !== -1) {
  //   [Data.chart9.herodata[0], Data.chart9.herodata[1]] = [, Data.chart9.herodata[0]];
  // } else {
  //   console.log('未找到对应的英雄');
  // }
};

const heatmapclick = (team1: string, team2: string) => {
  console.log('点击队伍：', team1, team2);
  console.log('当前队伍:', Data.chart3.teamData[0].name, Data.chart3.teamData[1].name);
  // TODO:
  // 获取新英雄数据
  // getChart3Data();
  // getChart6Data();
  // if ( !== -1) {
  //   [Data.chart9.herodata[0], Data.chart9.herodata[1]] = [, Data.chart9.herodata[0]];
  // } else {
  //   console.log('未找到对应的英雄');
  // }
};

onMounted(() => {
})

onBeforeMount(() => {
  // getData()
})

function getData() {
  console.log(topic.value)
  getChart2Data()
  getChart7Data()


  getChart1Data()
  getChart4Data()
  getChart5Data()
  // getChart8Data()

  // while (!Data.chart2.isDataReady || !Data.chart7.isDataReady) {
  // }
  // getChart3Data()
  // getChart6Data()
  // getChart9Data()
}

function getChart1Data() {
  // newValue 可以替换topic
  console.log('正在获取图1的数据')
  Data.chart1.isChartVisible = false
  axios.get('http://192.168.198.10:8080/team/getWinRate', {
    params: {
      matchType: topic.value
    }
  }).then(response => {
    console.log('图1的数据:', response)
    if (response.data.code == 200) {
      console.log('code=200')
      Data.chart1.isChartVisible = true
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
  Data.chart2.isChartVisible = false
  axios.get('http://192.168.198.10:8080/team/getHeatMap', {
    params: {
      matchType: topic.value
    }
  }).then(response => {
    console.log('图2的数据:', response)
    if (response.data.code == 200) {
      console.log('code=200')
      Data.chart2.isChartVisible = true
      Data.chart2.isDataReady = true
      Data.chart2.teamNames = response.data.data.teams
      Data.chart2.heatMapData = response.data.data.heatMapDatas

    }
    else {
      console.log("code=", response.data.code)
    }
  }).catch(error => {
    console.log(error)
  })
}


function getChart4Data() {
  console.log('正在获取图4的数据')
  Data.chart4.isChartVisible = false
  axios.get('http://192.168.198.10:8080/player/getBoxPlot', {
    params: {
      matchType: topic.value
    }
  }).then(response => {
    console.log('图4的数据:', response)
    if (response.data.code == 200) {
      console.log('code=200')
      Data.chart4.isChartVisible = true
      Data.chart4.playerBoxPlotData = response.data.data

    }
    else {
      console.log("code=", response.data.code)
    }
  }).catch(error => {
    console.log(error)
  })
}


function getChart5Data() {
  console.log('正在获取图5的数据')
  Data.chart5.isChartVisible = false
  axios.get('http://192.168.198.10:8080/player/getScatterDiagram', {
    params: {
      matchType: topic.value
    }
  }).then(response => {
    console.log('图5的数据:', response)
    if (response.data.code == 200) {
      console.log('code=200')
      Data.chart5.isChartVisible = true
      Data.chart5.scatterDiagramData = response.data.data
    }
    else {
      console.log("code=", response.data.code)
    }
  }).catch(error => {
    console.log(error)
  })
}


function getChart7Data() {
  console.log('正在获取图7的数据')
  Data.chart7.isChartVisible = false
  axios.get('http://192.168.198.10:8080/hero/getCloudDiagram', {
    params: {
      matchType: topic.value
    }
  }).then(response => {
    console.log('图7的数据:', response)
    if (response.data.code == 200) {
      console.log('code=200')
      Data.chart7.isChartVisible = true
      Data.chart7.isDataReady = true
      Data.chart7.bpWordCloudData = response.data.data
    }
    else {
      console.log("code=", response.data.code)
    }
  }).catch(error => {
    console.log(error)
  })
}


function getChart8Data() {
  console.log('正在获取图8的数据')
  Data.chart8.isChartVisible = false
  axios.get('http://192.168.198.10:8080/', {
    params: {
      matchType: topic.value
    }
  }).then(response => {
    console.log('图8的数据:', response)
    if (response.data.code == 200) {
      console.log('code=200')
      Data.chart8.isChartVisible = true
      //


    }
    else {
      console.log("code=", response.data.code)
    }
  }).catch(error => {
    console.log(error)
  })
}


function getChart3Data() {
  console.log('正在获取图3的数据')
  Data.chart3.isChartVisible = false
  axios.get('http://192.168.198.10:8080/', {
    params: {
      matchType: topic.value,
      team1: Data.chart3.teamData[0].name,
      team2: Data.chart3.teamData[1].name,
    }
  }).then(response => {
    console.log('图3的数据:', response)
    if (response.data.code == 200) {
      console.log('code=200')
      Data.chart3.isChartVisible = true
      //


    }
    else {
      console.log("code=", response.data.code)
    }
  }).catch(error => {
    console.log(error)
  })
}


function getChart6Data() {
  console.log('正在获取图6的数据')
  Data.chart6.isChartVisible = false
  axios.get('http://192.168.198.10:8080/', {
    params: {
      matchType: topic.value,
      team1: Data.chart3.teamData[0].name,
      team2: Data.chart3.teamData[1].name,
    }
  }).then(response => {
    console.log('图6的数据:', response)
    if (response.data.code == 200) {
      console.log('code=200')
      Data.chart6.isChartVisible = true
      //


    }
    else {
      console.log("code=", response.data.code)
    }
  }).catch(error => {
    console.log(error)
  })
}


function getChart9Data() {
  console.log('正在获取图9的数据')
  Data.chart9.isChartVisible = false
  axios.get('http://192.168.198.10:8080/', {
    params: {
      matchType: topic.value,
      hero1: Data.chart9.herodata[0].name,
      hero2: Data.chart9.herodata[1].name,
    }
  }).then(response => {
    console.log('图9的数据:', response)
    if (response.data.code == 200) {
      console.log('code=200')
      Data.chart9.isChartVisible = true
      //


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
  /* min-width: 1024px;
  max-width: 1920px; */
  min-width: 100%;
  max-width: 100%;
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
  height: 40vh;
  width: 33.3vh;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  margin: 1vh;
  transition: transform 0.3s ease;
  position: relative;
}


.chart-2-container {
  height: 40vh;
  width: 33.3vh;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  margin: 1vh;
  transition: transform 0.3s ease;
  position: relative;
}

.chart-3-container {
  height: 40vh;
  width: 33.3vh;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  margin: 1vh;
  transition: transform 0.3s ease;
  position: relative;
}

.chart-4-container {
  height: 40vh;
  width: 33.3vh;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  margin: 1vh;
  transition: transform 0.3s ease;
  position: relative;
}

.chart-5-container {
  height: 40vh;
  width: 33.3vh;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  margin: 1vh;
  transition: transform 0.3s ease;
  position: relative;
}

.chart-6-container {
  height: 40vh;
  width: 33.3vh;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  margin: 1vh;
  transition: transform 0.3s ease;
  position: relative;
}

.chart-7-container {
  height: 40vh;
  width: 33.3vh;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  margin: 1vh;
  transition: transform 0.3s ease;
  position: relative;
}

.chart-8-container {
  height: 40vh;
  width: 33.3vh;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  margin: 1vh;
  transition: transform 0.3s ease;
  position: relative;
}

.chart-9-container {
  height: 40vh;
  width: 33.3vh;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  margin: 1vh;
  transition: transform 0.3s ease;
  position: relative;
}

.progress-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.full-screen-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1000;
}

.full-screen-image {
  width: 100%;
  height: auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
}

.centered-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.7);
}

.overlay-box {
  background-color: rgba(255, 255, 255, 0.8);
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.overlay-title {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: #333;
  text-shadow: none;
}

.overlay-description {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  color: #555;
  text-shadow: none;
}
</style>
