<script setup>
import { ref, watch, onMounted, onUnmounted, reactive } from 'vue';
import * as echarts from 'echarts';
import VChart from 'vue-echarts';

// 位置数组
const positions = reactive([
  '上单',
  '打野',
  '中单',
  'ADC',
  '辅助'
]);

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
    text: positions[0], // 默认标题
  },
  textStyle: {
    fontSize: 10,
  },
  tooltip: {},
  radar: {
    name: {
      textStyle: {
        color: '#999',
        fontWeight: 'bold', // 设置字体为加粗
        fontSize: 14,

      }
    },
    indicator: [ // KDA，CS，gold，damage，tanking
      { name: 'KDA', max: 30 },
      { name: '场均补刀', max: 11 },
      { name: '场均经济', max: 500 },
      { name: '场均输出', max: 50000 },
      { name: '场均承伤', max: 50000 },
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
  chartOptions.value.title.text = `${positions[groupIndex - 1]}`; // 更新标题为位置1、2或3
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
  chartOptions.value.title.text = `${positions[groupIndex - 1]}`; // 更新标题为位置1、2或3
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

// 监听传入的 players 数据变化，重新绘制图表
watch(() => props.players, (newPlayers) => {
  // 更新图表
  if (chartInstance) {
    chartInstance.setOption(chartOptions.value);
  }
}, { deep: true }); // deep: true 确保能够监听 players 数组中每个对象的变化

</script>

<template>
  <div class="container">
    <div class="player-list">
      <ul>
        <li @click="selectGroup([props.players[0], props.players[1]])">{{ positions[0] }}</li>
        <li @click="selectGroup([props.players[2], props.players[3]])">{{ positions[1] }}</li>
        <li @click="selectGroup([props.players[4], props.players[5]])">{{ positions[2] }}</li>
        <li @click="selectGroup([props.players[6], props.players[7]])">{{ positions[3] }}</li>
        <li @click="selectGroup([props.players[8], props.players[9]])">{{ positions[4] }}</li>
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
      font-size: 16px;
      cursor: pointer;
      border-bottom: 1px solid blue;
      padding: 2vh 0 2vh 1vw;
      transition: font-size 0.3s ease, color 0.3s ease;
    }

    li:last-child {
      border-bottom: none;
      /* 移除最后一个 li 的 bottom border */
    }

    li:hover {
      font-size: 18px;
      color: rgb(73, 11, 217);
    }
  }
}

.container {
  display: flex;
  margin-bottom: 2vh;
}

#radar-chart {
  padding-top: 10px;
  flex-grow: 1;
  height: 30vh;
  display: inline-block;
  vertical-align: top;
  margin-bottom: -15px;
}
</style>
