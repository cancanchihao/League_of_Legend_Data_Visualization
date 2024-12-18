<template>
    <div class="hero">
        <v-avatar class="avatar1" color="grey-darken-1" size="48" style="cursor: pointer;">
            <v-img :src="'http://192.168.198.10:8080/hero/heroImg?heroName=' + props.heroData[0].name"
                :alt=props.heroData[0].name></v-img>
        </v-avatar>
        <el-button type="success" class="elb button1" @click="change(1)">
            {{ props.heroData[0].name }}
        </el-button>
        <el-button type="info" class="elb button2" @click="change(2)">
            {{ props.heroData[1].name }}
        </el-button>
        <v-avatar class="avatar1" color="grey-darken-1" size="48" style="cursor: pointer;">
            <v-img :src="'http://192.168.198.10:8080/hero/heroImg?heroName=' + props.heroData[1].name"
                :alt=props.heroData[1].name></v-img>
        </v-avatar>
    </div>

    <!-- 当两个 winCount 都为 0 时，显示提示信息 -->
    <div v-if="props.heroData[0].winCount === 0 && props.heroData[1].winCount === 0" class="no-matches">
        该英雄间无对位情况
    </div>

    <div v-else>
        <item :line_name='"对位胜场"' :data1="props.heroData[0].winCount" :data2="props.heroData[1].winCount"
            :obj1="props.heroData[0].name" :obj2="props.heroData[1].name" :selectedItem="selectedItem" 
            :color1="'#fce38a'" :color2="'#f38181'">
        </item>
        <item :line_name='"   KDA   "' :data1="props.heroData[0].kda" :data2="props.heroData[1].kda"
            :obj1="props.heroData[0].name" :obj2="props.heroData[1].name" :selectedItem="selectedItem" 
            :color1="'#fce38a'" :color2="'#f38181'">
        </item>
        <item :line_name='"场均经济"' :data1="props.heroData[0].gold" :data2="props.heroData[1].gold"
            :obj1="props.heroData[0].name" :obj2="props.heroData[1].name" :selectedItem="selectedItem" 
            :color1="'#fce38a'" :color2="'#f38181'">
        </item>
        <item :line_name='"场均伤害"' :data1="props.heroData[0].damage" :data2="props.heroData[1].damage"
            :obj1="props.heroData[0].name" :obj2="props.heroData[1].name" :selectedItem="selectedItem" 
            :color1="'#fce38a'" :color2="'#f38181'">
        </item>
        <item :line_name='"场均承伤"' :data1="props.heroData[0].tanking" :data2="props.heroData[1].tanking"
            :obj1="props.heroData[0].name" :obj2="props.heroData[1].name" :selectedItem="selectedItem" 
            :color1="'#fce38a'" :color2="'#f38181'">
        </item>
    </div>
    
</template>

<script setup>
import { onMounted, ref } from "vue";
import * as echarts from "echarts";
import item from "./against-chart-item.vue";

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

.button1 {
  background-color: #fce38a; /* 设置第一个按钮的背景色 */
  font-size: 18px;
}

.button2 {
  background-color: #f38181; /* 设置第二个按钮的背景色 */
  font-size: 18px;
}

.no-matches {
  font-size: 20px;
  text-align: center;
  color: white;
  padding-top: 10vh;
}

.no-matches {
  font-size: 20px;
  text-align: center;
  color: white;
  padding-top: 10vh;
}
</style>
