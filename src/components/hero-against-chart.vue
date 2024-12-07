<template>
    <div class="hero">
        <img :src="'/src/assets/'+props.heroData[0].headimg+'.png'" alt="1">
        <span class="first_hero">{{ props.heroData[0].name }}</span>
        <span>{{ props.heroData[1].name }}</span>
        <img :src="'/src/assets/'+props.heroData[0].headimg+'.png'" alt="1">
    </div>
    <item :line_name='"  胜率 "' :data1="props.heroData[0].winRate" :data2="props.heroData[1].winRate" :hero1="props.heroData[0].name" :hero2="props.heroData[1].name"></item>
    <item :line_name='"pick率"' :data1="props.heroData[0].pickRate" :data2="props.heroData[1].pickRate" :hero1="props.heroData[0].name" :hero2="props.heroData[1].name"></item>
    <item :line_name='"ban率 "' :data1="props.heroData[0].banRate" :data2="props.heroData[1].banRate" :hero1="props.heroData[0].name" :hero2="props.heroData[1].name"></item>
</template>

<script setup>
import {
    onMounted,
    ref
} from 'vue';
import * as echarts from 'echarts';
import item from './against-chart-item.vue';

const props = defineProps({
    heroData: {
      type: Array,
      required: true,
    },
});

</script>

<style scoped>
.hero {
    display: flex;
    justify-content: space-between;
    width: 100%;
    text-align: center;
    padding: 0 3vw;
}

span {
    display: inline-flex;
    align-items: center;
}
</style>
