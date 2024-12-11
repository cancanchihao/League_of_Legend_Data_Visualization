<template>
    <div class="hero">
        <!-- <img :src="'/src/assets/' + props.heroData[0].headimg + '.png'" alt="1"> -->
        <v-avatar class="avatar1" color="grey-darken-1" size="48" style="cursor: pointer;">
            <v-img :src="'http://192.168.198.10:8080/hero/heroImg?heroName=' + '暗裔剑魔'"></v-img>
        </v-avatar>
        <el-button type="primary" class="elb" @click="change(1)">
            {{ props.heroData[0].name }}
        </el-button>
        <el-button type="primary" class="elb" @click="change(2)">
            {{ props.heroData[1].name }}
        </el-button>
        <!-- <img :src="'/src/assets/' + props.heroData[1].headimg + '.png'" alt="1"> -->
        <v-avatar class="avatar1" color="grey-darken-1" size="48" style="cursor: pointer;">
            <v-img :src="'http://192.168.198.10:8080/hero/heroImg?heroName=' + '暗裔剑魔'"></v-img>
        </v-avatar>
    </div>
    <item :line_name='"  胜率 "' :data1="props.heroData[0].winRate" :data2="props.heroData[1].winRate"
        :obj1="props.heroData[0].name" :obj2="props.heroData[1].name" :selectedItem="selectedItem">
    </item>
    <item :line_name='"pick率"' :data1="props.heroData[0].pickRate" :data2="props.heroData[1].pickRate"
        :obj1="props.heroData[0].name" :obj2="props.heroData[1].name" :selectedItem="selectedItem">
    </item>
    <item :line_name='"ban率"' :data1="props.heroData[0].banRate" :data2="props.heroData[1].banRate"
        :obj1="props.heroData[0].name" :obj2="props.heroData[1].name" :selectedItem="selectedItem">
    </item>
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
.hero {
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
