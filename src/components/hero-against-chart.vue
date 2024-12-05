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

const heroData = [{
    name: '铁血猎手',
    winRate: 46.91,
    kda: 1.65,
    killContribution: 50.72,
    damageToHero: 23875
},
{
    name: '雷克顿夫',
    winRate: 53,
    kda: 2.01,
    killContribution: 49.28,
    damageToHero: 21545
}
];

const renderChart = () => {
    const chartDom = chart.value;
    const myChart = echarts.init(chartDom);

    // 计算总数据
    const totalData = [{
        totalwinRate: heroData[0].winRate + heroData[1].winRate,
        totalkda: heroData[0].kda + heroData[1].kda,
        totalkillContribution: heroData[0].killContribution + heroData[1].killContribution,
        totaldamageToHero: heroData[0].damageToHero + heroData[1].damageToHero
    }];

    // 指标数组
    const 指标 = ['胜率', 'KDA', '击杀贡献率', '对英雄造成的伤害'];

    // 使用数组动态生成 seriesData
    const seriesData = heroData.map(hero => [
        hero.winRate / totalData[0].totalwinRate,
        hero.kda / totalData[0].totalkda,
        hero.killContribution / totalData[0].totalkillContribution,
        hero.damageToHero / totalData[0].totaldamageToHero
    ]);

    // 使用 heroData 数组的 name 属性作为 legend 和 series 的名字
    const legendData = heroData.map(hero => hero.name);

    const option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                // Use axis to trigger tooltip
                type: 'shadow' // 'shadow' as default; can also be 'line' or 'shadow'
            }
        },
        legend: {},
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'value'
        },
        yAxis: {
            type: 'category',
            data: ['Mon']
        },
        series: [{
            name: 'Direct',
            type: 'bar',
            stack: 'total',
            label: {
                show: true
            },
            emphasis: {
                focus: 'series'
            },
            data: [320]
        },
        {
            name: 'Mail Ad',
            type: 'bar',
            stack: 'total',
            label: {
                show: true
            },
            emphasis: {
                focus: 'series'
            },
            data: [210]
        },
        ]
    };

    myChart.setOption(option);
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
    width: 100%;
    height: 28vh;
}
</style>