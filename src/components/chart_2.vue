<template>
    <div class="chart-container" ref="chart" style="width: 100%; height: 400px;"></div>
</template>

<script>
import * as echarts from 'echarts';

export default {
    name: 'HeroDataChart',
    data() {
        return {
            // 模拟的英雄数据
            heroData: [
                { name: '英雄1', matches: 200, pickRate: 0.4, winRate: 0.55 },
                { name: '英雄2', matches: 350, pickRate: 0.5, winRate: 0.45 },
                { name: '英雄3', matches: 100, pickRate: 0.25, winRate: 0.65 },
                { name: '英雄4', matches: 150, pickRate: 0.35, winRate: 0.50 },
                { name: '英雄5', matches: 500, pickRate: 0.6, winRate: 0.48 }
            ]
        };
    },
    mounted() {
        this.renderChart();
    },
    methods: {
        renderChart() {
            const chartDom = this.$refs.chart;
            const myChart = echarts.init(chartDom);

            // 图表配置
            const option = {
                title: {
                    text: '英雄数据轮播',
                    left: 'center',
                    textStyle: {
                        fontSize: 18,
                        fontWeight: 'bold'
                    }
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: { type: 'shadow' }
                },
                legend: {
                    data: ['出场次数', 'Pick比率', '胜率'],
                    top: '10%',
                    left: 'center'
                },
                xAxis: {
                    type: 'category',
                    data: this.heroData.map(hero => hero.name),
                    axisLabel: {
                        interval: 0,
                        rotate: 30  // 为了让文字显示不重叠，倾斜显示
                    }
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        name: '出场次数',
                        type: 'bar',
                        data: this.heroData.map(hero => hero.matches),
                        emphasis: { focus: 'series' },
                        label: { show: true, position: 'top' }
                    },
                    {
                        name: 'Pick比率',
                        type: 'line',
                        data: this.heroData.map(hero => hero.pickRate * 100),  // 百分比
                        yAxisIndex: 1,
                        smooth: true,
                        lineStyle: { color: '#ff7f0e' },
                        label: { show: true, position: 'top' }
                    },
                    {
                        name: '胜率',
                        type: 'line',
                        data: this.heroData.map(hero => hero.winRate * 100),  // 百分比
                        yAxisIndex: 1,
                        smooth: true,
                        lineStyle: { color: '#2ca02c' },
                        label: { show: true, position: 'top' }
                    }
                ],
                yAxis: [
                    {
                        type: 'value',
                        name: '出场次数'
                    },
                    {
                        type: 'value',
                        name: '比率 (%)',
                        axisLabel: {
                            formatter: '{value} %'
                        }
                    }
                ]
            };

            // 设置图表的配置项和数据
            myChart.setOption(option);
        }
    }
};
</script>

<style scoped>
.chart-container {
    width: 100%;
    height: 400px;
}
</style>