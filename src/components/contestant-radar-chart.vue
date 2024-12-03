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
  { name: 'Player 6', stats: [40, 65, 99, 80, 75] },
]);

// 选中的组
const selectedGroup = ref([players.value[0], players.value[1]]); // 默认选中第一组

// ECharts配置
const chartOptions = ref({
  title: {
    text: '位置1', // 默认标题
  },
  textStyle: {
      fontSize: 10,
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
      data: selectedGroup.value.map(player => ({
        value: player.stats,
        name: player.name,
      })),
    },
  ],
});

// 监听选中组的变化，更新ECharts配置
watch(selectedGroup, (newGroup) => {
  let groupIndex;
  if (newGroup[0] === players.value[0]) {
    groupIndex = 1;
  } else if (newGroup[0] === players.value[2]) {
    groupIndex = 2;
  } else {
    groupIndex = 3;
  }
  chartOptions.value.title.text = `位置${groupIndex}`; // 更新标题为位置1、2或3
  chartOptions.value.series[0].data = newGroup.map(player => ({
    value: player.stats,
    name: player.name,
  }));
  if (chartInstance) {
    chartInstance.setOption(chartOptions.value); // 更新图表
  }
});

// 选择组的方法
const selectGroup = (group) => {
  selectedGroup.value = group;
  let groupIndex;
  if (group[0] === players.value[0] && group[1] === players.value[1]) {
    groupIndex = 1;
  } else if (group[0] === players.value[2] && group[1] === players.value[3]) {
    groupIndex = 2;
  } else {
    groupIndex = 3;
  }
  chartOptions.value.title.text = `位置${groupIndex}`; // 更新标题为位置1、2或3
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
  <div class="container">
    <div class="player-list">
      <ul>
        <li @click="selectGroup([players[0], players[1]])">位置1</li>
        <li @click="selectGroup([players[2], players[3]])">位置2</li>
        <li @click="selectGroup([players[4], players[5]])">位置3</li>
      </ul>
    </div>
    <div id="radar-chart">
      <v-chart :options="chartOptions" :auto-resize="true" />
    </div>
  </div>
</template>

<style lang="less" scoped>
.player-list {
  width: 100px;
  font-size: 8px;
  display: inline-block;
  vertical-align: top;
  height: 100px;
  margin-right: 50px;
  ul {
    list-style: none; 
    padding: 10px; 
    li {
      font-size: 12px;
      cursor: pointer;
      border-bottom: 1px solid blue;
      padding: 10px;
      // margin-bottom: 15px;
      transition: font-size 0.3s ease, color 0.3s ease;
    }
    li:hover {
      font-size: 14px;
      color: rgb(73, 11, 217);
    }
  }
}

.container {
  display: flex;
}

#radar-chart {
  padding-top: 10px;
  flex-grow: 1;
  height: 24vh;
  display: inline-block;
  vertical-align: top;
  margin-bottom: -15px;
}
</style>
