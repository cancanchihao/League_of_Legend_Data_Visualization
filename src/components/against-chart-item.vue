<template>
    <div class="bp-bar-chart" ref="chart"></div>
</template>

<script setup>
import {
    onMounted,
    ref
} from 'vue';
import * as echarts from 'echarts';

const chart = ref(null);

const line_name = '数据名'
const data1 = 320;
const data2 = 210;
const hero1 = 'Hero1';
const hero2 = 'Hero2';

const renderChart = () => {
    const chartDom = chart.value;
    const myChart = echarts.init(chartDom);

    const option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        legend: {
            data: [hero1, hero2],
            orient: 'horizontal',
            itemGap: 10,
            bottom: '60%',
            left: '50vw',
            show: false,
            selected: {
                [hero1]: true,  // 不允许点击选中或取消选中
                [hero2]: true,   // 不允许点击选中或取消选中
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            top: '40%',
            bottom: '20%',
            containLabel: true
            
        },
        xAxis: {
            type: 'value',
            axisLabel: {
                show: false
            },
            splitLine: {
                show: false // 隐藏 x 轴的分割线
            },
            min: 0,
            max: data1 + data2
        },
        yAxis: {
            type: 'category',
            // 删除 'Mon' 字段，如果只需要一个类别，可以设置 data 为空数组
            data: [line_name],
            axisTick: {
                show: false
            },
        },
        series: [{
                name: hero1,
                type: 'bar',
                stack: 'total',
                label: {
                    show: true,
                    fontSize: 10, // 设置标签文本的字体大小
                    formatter: function (params) {
                        return params.value; // 可修改显示数值
                    }
                },
                emphasis: {
                    focus: 'series'
                },
                data: [data1]
            },
            {
                name: hero2,
                type: 'bar',
                stack: 'total',
                label: {
                    show: true,
                    fontSize: 10, // 设置标签文本的字体大小
                    formatter: function (params) {
                        return params.value;
                    }
                },
                emphasis: {
                    focus: 'series'
                },
                data: [data2]
            }
        ]
    };

    myChart.setOption(option);

    const itemGap = window.innerWidth * 0.11;
    const itemWidth = window.innerWidth * 0.015;
    myChart.setOption({
        legend: {
            itemWidth: itemWidth,
            itemGap: itemGap
        }
    });

    window.addEventListener('resize', () => {
        myChart.resize();
    });
};

onMounted(() => {
    renderChart();

});
</script>

<style scoped>
.bp-bar-chart {
    margin-left: 2vw;
    width: 27vw;
    height: 5vh;
}
</style>