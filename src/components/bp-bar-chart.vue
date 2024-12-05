<template>
  <div class="bp-bar-chart" ref="chart"></div>
</template>

<script setup>
  import {
    onMounted,
    ref,
    defineProps
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
</style>