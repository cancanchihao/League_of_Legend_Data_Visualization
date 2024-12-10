<template>
    <div ref="chartContainer" style="width: 100%; height: 37vh;"></div>
</template>

<script setup>
import { onMounted, watch, ref } from 'vue';
import * as echarts from 'echarts';

const props = defineProps({
    data: Array,
    xAxis: String,
    yAxis: String
});

const chartContainer = ref(null);

// 更新图表函数
const updateChart = () => {
    if (!chartContainer.value) return;

    const myChart = echarts.init(chartContainer.value); // 初始化图表

    // 准备数据，确保 x 和 y 是有效的数据字段
    const seriesData = props.data.map(item => ({
        value: [item[props.xAxis], item[props.yAxis]], // 对应 x 和 y 坐标的值
        player: item.player // 用来显示 tooltip
    }));

    const option = {
        tooltip: {
            trigger: 'item',
            formatter: function (params) {
                const { player } = params.data;
                return `Player: ${player}<br />${props.xAxis}: ${params.data.value[0]}<br />${props.yAxis}: ${params.data.value[1]}`;
            }
        },
        xAxis: {
            name: props.xAxis,
            type: 'value',
            min: 'dataMin', // 动态根据数据设置最小值
            max: 'dataMax'  // 动态根据数据设置最大值
        },
        yAxis: {
            name: props.yAxis,
            type: 'value',
            min: 'dataMin', // 动态根据数据设置最小值
            max: 'dataMax'  // 动态根据数据设置最大值
        },
        series: [
            {
                symbolSize: 20, // 点的大小
                data: seriesData, // 数据源
                type: 'scatter'
            }
        ]
    };

    myChart.setOption(option); // 设置图表配置

    // 响应式
    window.onresize = myChart.resize;
};

onMounted(() => {
    updateChart(); // 初次渲染
});

// 监听坐标轴变化
watch([() => props.xAxis, () => props.yAxis], () => {
    updateChart(); // 更新图表
});
</script>

<style scoped>
/* 可根据需要调整样式 */
</style>