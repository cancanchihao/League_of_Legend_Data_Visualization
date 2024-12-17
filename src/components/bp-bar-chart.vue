<!-- BarChart.vue -->
<template>
  <div ref="chart" style="width: 100%; height: 36vh;"></div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  herodata: Array
})

const chart = ref(null)

onMounted(() => {
  const myChart = echarts.init(chart.value, 'dark')

  const names = props.herodata.map(hero => hero.name)
  const banRates = props.herodata.map(hero => hero.banRate)
  const pickRates = props.herodata.map(hero => hero.pickRate)
  const winRates = props.herodata.map(hero => hero.winRate)

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    legend: {
      data: ['Ban率', 'Pick率', '胜率'],
      orient: 'vertical', // 垂直排列
      right: '10%', // 设置legend位置
      top: '10%',
      textStyle: {
        fontSize: 14, // 设置文字大小
      },
      itemWidth: 12, // 设置legend图标宽度
      itemHeight: 12, // 设置legend图标高度
    },
    xAxis: {
      type: 'category',
      data: names,
      axisLabel: {
        interval: 0, // 使标签全部显示
        rotate: 45, // 旋转X轴标签
        fontSize: 12 // 设置字体大小
      },
      barCategoryGap: '5%', // 不同name之间的间隙为15%
      barGap: '0%' // 同一系列柱子之间没有间隙
    },
    yAxis: {
      type: 'value',
      max: 100,
      axisLabel: {
        fontSize: 12 // 设置字体大小
      }
    },
    series: [
      {
        name: 'Ban率',
        type: 'bar',
        data: banRates,
        color: '#e74c3c', // 更鲜艳的红色
        barWidth: 12, // 控制柱状图的宽度
        itemStyle: {
          shadowColor: 'rgba(231, 76, 60, 0.5)', // 阴影效果
          shadowBlur: 10
        }
      },
      {
        name: 'Pick率',
        type: 'bar',
        data: pickRates,
        color: '#2ecc71', // 活力绿色
        barWidth: 12, // 控制柱状图的宽度
        itemStyle: {
          shadowColor: 'rgba(46, 204, 113, 0.5)', // 阴影效果
          shadowBlur: 10
        }
      },
      {
        name: '胜率',
        type: 'bar',
        data: winRates,
        color: '#3498db', // 清新的蓝色
        barWidth: 12, // 控制柱状图的宽度
        itemStyle: {
          shadowColor: 'rgba(52, 152, 219, 0.5)', // 阴影效果
          shadowBlur: 10
        }
      }
    ]
  }

  myChart.setOption(option)
})
</script>

<style scoped>
/* 样式根据需要调整 */
</style>






<!-- <template>
  <div class="bp-bar-chart" ref="chart"></div>
</template>

<script setup>
  import {
    onMounted,
    ref,
  } from 'vue';
  import * as echarts from 'echarts';

  // 定义接收的 props
  const props = defineProps({
    heroData: {
      type: Array,
      required: true,
    },
  });

  // 使用 ref 引用 DOM 元素
  const chart = ref(null);

  // 渲染图表的函数
  const renderChart = () => {
    const chartDom = chart.value;
    const myChart = echarts.init(chartDom);

    const option = {
      title: {
        text: 'bp柱状图',
        left: 'center',
        textStyle: {
          fontSize: 18,
          fontWeight: 'bold',
        },
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        },
      },
      legend: {
        data: ['出场次数', 'Pick比率', '胜率'],
        top: '10%',
        left: 'center',
      },
      xAxis: {
        type: 'category',
        data: props.heroData.map((hero) => hero.name),
        axisLabel: {
          interval: 0,
          rotate: 30, // 为了让文字显示不重叠，倾斜显示
        },
      },
      yAxis: [{
          type: 'value',
          name: '出场次数',
        },
        {
          type: 'value',
          name: '比率 (%)',
          axisLabel: {
            formatter: '{value} %',
          },
        },
      ],
      series: [{
          name: '出场次数',
          type: 'bar',
          data: props.heroData.map((hero) => hero.matches),
          emphasis: {
            focus: 'series'
          },
          label: {
            show: true,
            position: 'top'
          },
        },
        {
          name: 'Pick比率',
          type: 'line',
          data: props.heroData.map((hero) => hero.pickRate * 100), // 百分比
          yAxisIndex: 1,
          smooth: true,
          lineStyle: {
            color: '#ff7f0e'
          },
          label: {
            show: true,
            position: 'top'
          },
        },
        {
          name: '胜率',
          type: 'line',
          data: props.heroData.map((hero) => hero.winRate * 100), // 百分比
          yAxisIndex: 1,
          smooth: true,
          lineStyle: {
            color: '#2ca02c'
          },
          label: {
            show: true,
            position: 'top'
          },
        },
      ],
    };

    myChart.setOption(option);
  };

  // 使用 onMounted 生命周期钩子
  onMounted(() => {
    renderChart();
  });
</script>

<style scoped>
  .bp-bar-chart {
    width: 100%;
    height: 32vh;
  }
</style> -->