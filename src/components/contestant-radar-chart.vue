<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';
import VChart from 'vue-echarts';

// 玩家数据
const props = defineProps({
  players: {
    type: Array,
    required: true,
  },
});

// 选中的组
const selectedGroup = ref([props.players[0], props.players[1]]); // 默认选中第一组

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
  if (newGroup[0] === props.players[0]) {
    groupIndex = 1;
  } else if (newGroup[0] === props.players[2]) {
    groupIndex = 2;
  } else if (newGroup[0] === props.players[4]) {
    groupIndex = 3;
  } else if (newGroup[0] === props.players[6]) {
    groupIndex = 4;
  } else {
    groupIndex = 5;
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
  if (group[0] === props.players[0]) {
    groupIndex = 1;
  } else if (group[0] === props.players[2]) {
    groupIndex = 2;
  } else if (group[0] === props.players[4]) {
    groupIndex = 3;
  } else if (group[0] === props.players[6]) {
    groupIndex = 4;
  } else {
    groupIndex = 5;
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
        <li @click="selectGroup([props.players[0], props.players[1]])">位置1</li>
        <li @click="selectGroup([props.players[2], props.players[3]])">位置2</li>
        <li @click="selectGroup([props.players[4], props.players[5]])">位置3</li>
        <li @click="selectGroup([props.players[6], props.players[7]])">位置4</li>
        <li @click="selectGroup([props.players[8], props.players[9]])">位置5</li>
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
  margin: 0 5vh;

  ul {
    list-style: none;
    padding: 0 2vh;
    margin: 0;

    li {
      font-size: 14px;
      cursor: pointer;
      border-bottom: 1px solid blue;
      padding: 1vh 0 1vh 0.5vw;
      transition: font-size 0.3s ease, color 0.3s ease;
    }
    li:hover {
      font-size: 18px;
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
