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

const clickedStates = ref([true, false, false, false, false]);

// 玩家数据
const props = defineProps({
  players: {
    type: Array,
    required: true,
  },
  team: {
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
    textStyle: {
      color: 'white',
    }
  },
  legend: {
    data: selectedGroup.value.map(player => ({
      name: player.name,
    })),
    itemGap: 100, // 设置项之间的间距
    padding: [5, 0], // 增加左右内边距
    left: '20%',
    right: '5%',
    textStyle: {
      fontSize: 16, // 增加文字大小
    },
    itemWidth: 30, // 增加图例项宽度
    itemHeight: 17,
    selectedMode: false,
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
      { name: 'KDA', max: 12 },
      { name: '分均补刀', max: 11 },
      { name: '分均经济', max: 500 },
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
  clickedStates.value = clickedStates.value.map(() => false);
  clickedStates.value[groupIndex - 1] = true;
  chartOptions.value.title.text = `${positions[groupIndex - 1]}`; // 更新标题为位置1、2或3
  chartOptions.value.legend.data = newGroup.map(player => ({
    name: player.name,
  }));
  chartOptions.value.series[0].data = newGroup.map(player => ({
    value: player.stats,
    name: player.name,
  }));
  if (chartInstance.value) {
    chartInstance.value.setOption(chartOptions.value); // 更新图表
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

const chartInstance = ref(null);

onMounted(() => {
  const chartDom = document.getElementById('radar-chart');
  chartInstance.value = echarts.init(chartDom, 'dark');
  chartInstance.value.setOption(chartOptions.value);

  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    chartInstance.value.resize();
  });
});

onUnmounted(() => {
  if (chartInstance.value) {
    chartInstance.value.dispose();
  }
  window.removeEventListener('resize', chartInstance.value.resize);
});

// 监听传入的 players 数据变化，重新绘制图表
watch(() => props.players, () => {
  console.log('触发刷新');
  console.log(chartInstance.value);

  chartOptions.value.series[0].data = selectedGroup.value.map(player => ({
    value: player.stats,
    name: player.name,
  }));

  if (chartInstance.value) {
    chartInstance.value.setOption(chartOptions.value, true); // 第二个参数 true 表示完全刷新
  }
  selectedGroup.value = [props.players[0], props.players[1]];
}, { deep: true }); // deep: true 确保能够监听 players 数组中每个对象的变化

</script>

<template>
  <div class="container">
    <div class="player-list">
      <ul>
        <li @click="selectGroup([props.players[0], props.players[1]])" :class="{ clicked: clickedStates[0] }" >{{ positions[0] }}</li>
        <li @click="selectGroup([props.players[2], props.players[3]])" :class="{ clicked: clickedStates[1] }" >{{ positions[1] }}</li>
        <li @click="selectGroup([props.players[4], props.players[5]])" :class="{ clicked: clickedStates[2] }" >{{ positions[2] }}</li>
        <li @click="selectGroup([props.players[6], props.players[7]])" :class="{ clicked: clickedStates[3] }" >{{ positions[3] }}</li>
        <li @click="selectGroup([props.players[8], props.players[9]])" :class="{ clicked: clickedStates[4] }" >{{ positions[4] }}</li>
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
    padding-top: 1vh;
    margin: 0;

    li {
      color: rgb(240, 215, 183);
      font-size: 18px;
      cursor: pointer;
      padding: 3vh 0 0 0;
      transition: font-size 0.3s ease, color 0.3s ease;
    }

    li:hover {
      font-size: 22px;
      color: rgb(238, 78, 78);
    }
  }
}

.clicked {
  font-size: 22px !important;
  font-weight: 600;
  color: rgb(255, 0, 0) !important;
}

.container {
  display: flex;
  margin-bottom: 2vh;
}

#radar-chart {
  padding-top: 3vh;
  flex-grow: 1;
  height: 37vh;
  display: inline-block;
  vertical-align: top;
  margin-bottom: -15px;
}
</style>
