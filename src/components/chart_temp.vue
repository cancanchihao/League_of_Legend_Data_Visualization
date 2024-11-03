<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';
import VChart from 'vue-echarts';

// 注册vchart组件
const components = {
  VChart,
};

// 玩家数据
const players = ref([
  { name: 'Player 1', stats: [80, 70, 90, 85, 75] },
  { name: 'Player 2', stats: [70, 80, 60, 90, 95] },
  { name: 'Player 3', stats: [90, 85, 80, 70, 70] },
  { name: 'Player 4', stats: [60, 90, 50, 65, 65] },
  { name: 'Player 5', stats: [50, 60, 70, 95, 35] },
  { name: 'Player 6', stats: [40, 65, 100, 80, 75] },
]);

// 选中的玩家
const selectedPlayer = ref(players.value[0]);

// ECharts配置
const chartOptions = ref({
  title: {
    text: selectedPlayer.value.name,
  },
  textStyle: {
      fontSize: 10
  },
  tooltip: {},
  radar: {
    indicator: [
      { name: 'Attack', max: 100 },
      { name: 'Defense', max: 100 },
      { name: 'Skill', max: 100 },
      { name: 'Strategy', max: 100 },
      { name: 'Teamwork', max: 100 },
    ],
  },
  series: [
    {
      name: 'Player Stats',
      type: 'radar',
      data: [
        {
          value: selectedPlayer.value.stats,
          name: selectedPlayer.value.name,
        },
      ],
    },
  ],
});

// 监听选中玩家的变化，更新ECharts配置
watch(selectedPlayer, (newPlayer) => {
  chartOptions.value.title.text = newPlayer.name;
  chartOptions.value.series[0].data[0].value = newPlayer.stats;
  // 这里直接调用更新
  if (chartInstance) {
    chartInstance.setOption(chartOptions.value); // 更新图表
  }
});

// 选择玩家的方法
const selectPlayer = (player) => {
  selectedPlayer.value = player;
};

let chartInstance;

onMounted(() => {
  const chartDom = document.getElementById('radar-chart');
  chartInstance = echarts.init(chartDom);
  chartInstance.setOption(chartOptions.value);

  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    chartInstance.resize();
  });
});

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose();
  }
  window.removeEventListener('resize', chartInstance.resize);
});

</script>

<template>
    <div>
        <div class="player-list">
        <ul>
            <li v-for="player in players" :key="player.name" @click="selectPlayer(player)">
            {{ player.name }}
            </li>
        </ul>
        </div>
        <div class="radar-chart" id="radar-chart">
        <v-chart :options="chartOptions" :auto-resize="true" />
        </div>
    </div>
</template>

<style lang="less" scoped>

.player-list {
  width: 90px;
  font-size: 12px;
  display: inline-block;
  vertical-align: top;
  height: 180px;
  ul {
    list-style: none; 
    padding: 10px; 
    margin: 0; 
    li {
      cursor: pointer;
      border-bottom: 1px solid blue;
      padding: 3px;
      margin-bottom: 5px;
      transition: font-size 0.3s ease, color 0.3s ease;
    }
    li:hover {
      font-size: 16px;
      color: rgb(73, 11, 217);
    }
  }
}

.radar-chart {
  z-index: 1000;
  padding-top: 10px;
  width: 270px;
  height: 200px;
  display: inline-block;
  vertical-align: top;
}
</style>