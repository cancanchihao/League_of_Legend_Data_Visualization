<template>
    <div class="team">
        <img :src="'http://192.168.198.10:8080/team/teamImg?teamName=' + props.teamData[0].name"
            :alt=props.teamData[0].name>
        <el-button type="primary" class="elb" @click="change(1)">
            {{ props.teamData[0].name }}
        </el-button>
        <el-button type="warning" class="elb" @click="change(2)">
            {{ props.teamData[1].name }}
        </el-button>
        <img :src="'http://192.168.198.10:8080/team/teamImg?teamName=' + props.teamData[1].name"
            :alt=props.teamData[1].name>
    </div>
    <item :line_name='"历史比分"' :data1="props.teamData[0].winCount" :data2="props.teamData[1].winCount"
        :obj1="props.teamData[0].name" :obj2="props.teamData[1].name" :selectedItem="selectedItem"></item>
    <item :line_name='"   KDA   "' :data1="props.teamData[0].kda" :data2="props.teamData[1].kda"
        :obj1="props.teamData[0].name" :obj2="props.teamData[1].name" :selectedItem="selectedItem"></item>
    <item :line_name='"场均大龙"' :data1="props.teamData[0].baron" :data2="props.teamData[1].baron"
        :obj1="props.teamData[0].name" :obj2="props.teamData[1].name" :selectedItem="selectedItem"></item>
    <item :line_name='"场均小龙"' :data1="props.teamData[0].dragon" :data2="props.teamData[1].dragon"
        :obj1="props.teamData[0].name" :obj2="props.teamData[1].name" :selectedItem="selectedItem"></item>
    <item :line_name='"场均推塔"' :data1="props.teamData[0].turts" :data2="props.teamData[1].turts"
        :obj1="props.teamData[0].name" :obj2="props.teamData[1].name" :selectedItem="selectedItem"></item>
</template>

<script setup>
import {
    onMounted,
    ref
} from 'vue';
import * as echarts from 'echarts';
import item from './against-chart-item.vue';

const props = defineProps({
    teamData: {
        type: Array,
        required: true,
    },
});

const selectedItem = ref(0); // 响应式的 selectedItem

// 更新 selectedItem
const change = (id) => {
    if (selectedItem.value === id) {
        selectedItem.value += 2;
    } else {
        selectedItem.value = id;
    }
};

</script>

<style scoped>
.team {
    display: flex;
    justify-content: space-between;
    width: 100%;
    align-items: center;
    padding: 0 3vw;
}

.elb {
    display: inline-flex;
    align-items: center;
    position: relative;
    /* 使 z-index 生效 */
    z-index: 10;
    /* 设置更高的 z-index */
}
</style>
