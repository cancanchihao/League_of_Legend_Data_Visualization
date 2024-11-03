<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';

// 玩家数据
const players = ref([
  { name: 'Player 1', stats: [80, 70, 90, 85, 75] },
  { name: 'Player 2', stats: [70, 80, 60, 90, 95] },
  { name: 'Player 3', stats: [90, 85, 80, 75, 70] },
]);

// 选中的玩家
const selectedPlayer = ref(players.value[0]);

// ECharts配置
const chartOptions = ref({
  title: {
    text: selectedPlayer.value.name,
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

watch(chartOptions, (newOptions) => {
  if (chartInstance) {
    chartInstance.setOption(newOptions);
  }
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
        <v-chart :options="chartOptions" />
        </div>
    </div>
</template>

<style>
.player-list {
  width: 200px;
  display: inline-block;
  vertical-align: top;
}

.radar-chart {
  width: 300px;
  height: 300px;
  display: inline-block;
  vertical-align: top;
}
</style>