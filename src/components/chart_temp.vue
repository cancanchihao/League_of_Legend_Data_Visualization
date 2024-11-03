<template>
    <div>
        <div class="player-list">
        <ul>
            <li v-for="player in players" :key="player.name" @click="selectPlayer(player)">
            {{ player.name }}
            </li>
        </ul>
        </div>
        <div class="radar-chart">
        <v-chart :options="chartOptions" />
        </div>
    </div>
    </template>
    
    <script>
    import * as echarts from 'echarts';
    import { defineComponent, ref } from 'vue';
    import { ECharts } from 'vue-echarts';
    import { use } from 'echarts/core';
    import {
    RadarChart,
    TitleComponent,
    TooltipComponent,
    GridComponent,
    } from 'echarts/components';
    
    use([RadarChart, TitleComponent, TooltipComponent, GridComponent]);
    
    export default defineComponent({
    components: {
        VChart: ECharts,
    },
    setup() {
        const players = ref([
        { name: 'Player 1', stats: [80, 70, 90, 85, 75] },
        { name: 'Player 2', stats: [70, 80, 60, 90, 95] },
        { name: 'Player 3', stats: [90, 85, 80, 75, 70] },
        ]);
    
        const selectedPlayer = ref(players.value[0]);
    
        const chartOptions = ref({
        title: {
            text: selectedPlayer.value.name,
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
            name: 'Player Stats',
            type: 'radar',
            data: [
                {
                value: selectedPlayer.value.stats,
                name: selectedPlayer.value.name,
                },
            ],
            },
        ],
        });
    
        const selectPlayer = (player) => {
        selectedPlayer.value = player;
        chartOptions.value.title.text = player.name;
        chartOptions.value.series[0].data[0].value = player.stats;
        };
    
        return {
        players,
        chartOptions,
        selectPlayer,
        };
    },
    });
    </script>
    
    <style>
    .player-list {
    float: left;
    width: 200px;
    }
    
    .radar-chart {
    float: right;
    width: 400px;
    }
    </style>
    