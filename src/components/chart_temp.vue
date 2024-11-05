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

// 玩家组
const groups = ref([
  [players.value[0], players.value[1]], // 组 1
  [players.value[2], players.value[3]], // 组 2
  [players.value[4], players.value[5]], // 组 3
]);

// 选中的组
const selectedGroup = ref(groups.value[0]); // 默认选中第一组

// ECharts配置生成函数
const createChartOptions = (player) => ({
  title: {
    text: player.name, // 标题为玩家名称
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
      name: `${player.name} Stats`,
      type: 'radar',
      data: [{
        value: player.stats,
        name: player.name,
      }],
    },
  ],
});

// 监听选中组变化，更新图表
watch(selectedGroup, () => {
  if (chartInstanceLeft) {
    chartInstanceLeft.setOption(createChartOptions(selectedGroup.value[0])); // 更新左侧图表
  }
  if (chartInstanceRight) {
    chartInstanceRight.setOption(createChartOptions(selectedGroup.value[1])); // 更新右侧第一个图表
  }
});

// 选择组的方法
const selectGroup = (group) => {
  selectedGroup.value = group;
};

let chartInstanceLeft;
let chartInstanceRight;

onMounted(() => {
  // 初始化左侧图表
  const chartDomLeft = document.getElementById('radar-chart-left');
  chartInstanceLeft = echarts.init(chartDomLeft);
  chartInstanceLeft.setOption(createChartOptions(selectedGroup.value[0]));

  // 初始化右侧第一个图表
  const chartDomRight = document.getElementById('radar-chart-right');
  chartInstanceRight = echarts.init(chartDomRight);
  chartInstanceRight.setOption(createChartOptions(selectedGroup.value[1]));

  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    chartInstanceLeft.resize();
    chartInstanceRight.resize();
  });
});

onUnmounted(() => {
  if (chartInstanceLeft) {
    chartInstanceLeft.dispose();
  }
  if (chartInstanceRight) {
    chartInstanceRight.dispose();
  }
  window.removeEventListener('resize', chartInstanceLeft.resize);
  window.removeEventListener('resize', chartInstanceRight.resize);
});
</script>

<template>
  <div>
    <div class="player-list">
      <ul>
        <li @click="selectGroup(groups[0])">组 1: Player 1 和 Player 2</li>
        <li @click="selectGroup(groups[1])">组 2: Player 3 和 Player 4</li>
        <li @click="selectGroup(groups[2])">组 3: Player 5 和 Player 6</li>
      </ul>
    </div>
    <div class="radar-container">
      <!-- 左侧雷达图 -->
      <div class="radar-chart" id="radar-chart-left"></div>
      <!-- 右侧雷达图 -->
      <div class="radar-chart" id="radar-chart-right"></div>
    </div>
  </div>
</template>

<style lang="less" scoped>
.player-list {
  width: 150px;
  font-size: 12px;
  display: inline-block;
  vertical-align: top;
  ul {
    list-style: none;
    padding: 10px;
    margin: 0;
    li {
      font-size: 16px;
      cursor: pointer;
      border-bottom: 1px solid blue;
      padding: 3px;
      margin-bottom: 5px;
      transition: font-size 0.3s ease, color 0.3s ease;
    }
    li:hover {
      font-size: 20px;
      color: rgb(73, 11, 217);
    }
  }
}

.radar-container {
  display: flex;
  // justify-content: space-between;
}

.radar-chart {
  width: 300px;
  padding-top: 10px;
  width: 30%;
  height: 300px;
}
</style>
