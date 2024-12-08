<template>
    <div class="team">
        <img :src="'/src/assets/'+props.teamData[0].headimg+'.png'" alt="1">
        <el-button type="primary" class="elb" @click="change(1)">
            {{ props.teamData[0].name }}
        </el-button>
        <el-button type="primary" class="elb" @click="change(2)">
            {{ props.teamData[1].name }}
        </el-button>
        <img :src="'/src/assets/'+props.teamData[1].headimg+'.png'" alt="1">
    </div>
    <item 
        :line_name='"  胜率 "' 
        :data1="props.teamData[0].winRate" 
        :data2="props.teamData[1].winRate" 
        :obj1="props.teamData[0].name" 
        :obj2="props.teamData[1].name"
        :selectedItem="selectedItem"
    ></item>
    <item 
        :line_name='"一血率"' 
        :data1="props.teamData[0].BloodRate" 
        :data2="props.teamData[1].BloodRate" 
        :obj1="props.teamData[0].name" 
        :obj2="props.teamData[1].name"
        :selectedItem="selectedItem"
    ></item>
    <item 
        :line_name='"一塔率"' 
        :data1="props.teamData[0].TowerRate" 
        :data2="props.teamData[1].TowerRate" 
        :obj1="props.teamData[0].name" 
        :obj2="props.teamData[1].name"
        :selectedItem="selectedItem"
    ></item>
    <item 
        :line_name='"一龙率"' 
        :data1="props.teamData[0].DragonRate" 
        :data2="props.teamData[1].DragonRate" 
        :obj1="props.teamData[0].name" 
        :obj2="props.teamData[1].name"
        :selectedItem="selectedItem"
    ></item>
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
    position: relative; /* 使 z-index 生效 */
    z-index: 10; /* 设置更高的 z-index */
}
</style>
