<template>
    <div ref="chart" style="width: 100%; height: 40vh;"></div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';

const props = defineProps({
    data: {
        type: Array,
        required: true,
    },
});

const chart = ref(null);
let myChart = null;

// 计算均值和四分位数等统计信息
const calculateStatistics = (values) => {
    values.sort((a, b) => a - b);
    const sum = values.reduce((a, b) => a + b, 0);
    const average = (sum / values.length).toFixed(2);

    const median = values[Math.floor(values.length / 2)];
    const lowerHalf = values.slice(0, Math.floor(values.length / 2));
    const upperHalf = values.slice(Math.ceil(values.length / 2));

    const q1 = lowerHalf[Math.floor(lowerHalf.length / 2)];
    const q3 = upperHalf[Math.floor(upperHalf.length / 2)];

    return { average, q1, median, q3 };
};

// 数据处理，计算 Min, Q1, Average, Q3, Max
const processData = (data) => {
    const categories = ['kills', 'deaths', 'assists'];
    const result = categories.map((key) => {
        const values = data.map((item) => item[key]);

        const min = Math.min(...values);
        const max = Math.max(...values);
        const { average, q1, q3 } = calculateStatistics(values);

        const playerAtMin = data.find((item) => item[key] === min)?.player || '';
        const playerAtMax = data.find((item) => item[key] === max)?.player || '';

        return { key, min, average, q1, q3, max, playerAtMin, playerAtMax };
    });
    return result;
};

const renderChart = () => {
    const processedData = processData(props.data);

    const xAxisData = processedData.map((item) => item.key);
    const boxData = processedData.map((item) => {
        return [
            item.min,      // min
            item.q1,       // Q1
            item.average,  // average (instead of median)
            item.q3,       // Q3
            item.max       // max
        ];
    });

    const tooltipFormatter = (params) => {
        const { seriesName, value, dataIndex } = params;
        if (seriesName === 'Box Plot') {
            return `${xAxisData[dataIndex]}: Min(${value[0]}), Q1(${value[1]}), Average(${value[2]}), Q3(${value[3]}), Max(${value[4]})`;
        }
        const playerKey = seriesName === 'Min' ? 'playerAtMin' : 'playerAtMax';
        const player = processedData[dataIndex][playerKey];
        return `${seriesName}: ${value} (${player})`;
    };

    myChart.setOption({
        backgroundColor: '',
        title: {
            text: '选手击杀、死亡、助攻箱线图',
            left: "center",
            textStyle: {
                color: 'white',
            }
        },
        tooltip: {
            trigger: 'item',
            formatter: tooltipFormatter,
        },
        xAxis: {
            type: 'category',
            data: xAxisData,
            axisLabel: {
                color: 'white'
            },
            axisLine: {
                lineStyle: {
                    color: 'white', // x轴线条颜色白色
                }
            },
            splitLine: {
                show: true,
                lineStyle: {
                    color: 'white', // x轴网格线颜色白色
                }
            },
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                color: 'white'
            },
            axisLine: {
                lineStyle: {
                    color: 'white', // x轴线条颜色白色
                }
            },
            splitLine: {
                show: true,
                lineStyle: {
                    color: 'white', // x轴网格线颜色白色
                }
            },
        },
        series: [
            {
                name: 'Box Plot',
                type: 'boxplot',
                data: boxData,
                itemStyle: {
                    color: '#ff7f50', // Customize color if needed
                },
                tooltip: {
                    formatter: tooltipFormatter
                }
            },
            // We add individual series for Min and Max to show players
            {
                name: 'Min',
                type: 'scatter',
                data: processedData.map((item) => ({
                    value: item.min,
                    player: item.playerAtMin
                })),
                tooltip: {
                    formatter: (params) => {
                        return `Min: ${params.value} (Player: ${params.data.player})`;
                    }
                }
            },
            {
                name: 'Max',
                type: 'scatter',
                data: processedData.map((item) => ({
                    value: item.max,
                    player: item.playerAtMax
                })),
                tooltip: {
                    formatter: (params) => {
                        return `Max: ${params.value} (Player: ${params.data.player})`;
                    }
                }
            }
        ]
    });
};

onMounted(() => {
    myChart = echarts.init(chart.value,);
    renderChart();
});

onUnmounted(() => {
    if (myChart) {
        myChart.dispose();
    }
});

watch(
    () => props.data,
    () => {
        renderChart();
    }
);
</script>

<style scoped>
/* 样式可根据需要调整 */
</style>