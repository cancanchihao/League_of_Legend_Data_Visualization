<template>
  <div class="team">


    <v-img :src="'http://1.14.45.200:8080/team/teamImg?teamName=' +
      props.teamData[0].name +
      '&&matchType=' +
      props.matchType
      " height="7vh" width="3vw">
    </v-img>
    <el-button type="primary" class="elb button1" @click="change(1)">
      {{ props.teamData[0].name }}
    </el-button>
    <el-button type="warning" class="elb button2" @click="change(2)">
      {{ props.teamData[1].name }}
    </el-button>
    <v-img :src="'http://1.14.45.200:8080/team/teamImg?teamName=' +
      props.teamData[1].name +
      '&&matchType=' +
      props.matchType
      " height=" 7vh" width="3vw">
    </v-img>


  </div>
  <item :line_name="'历史比分'" :data1="props.teamData[0].winCount" :data2="props.teamData[1].winCount"
    :obj1="props.teamData[0].name" :obj2="props.teamData[1].name" :selectedItem="selectedItem" :color1="'#95e1d3'"
    :color2="'#eaffd0'"></item>
  <item :line_name="'   KDA   '" :data1="props.teamData[0].kda" :data2="props.teamData[1].kda"
    :obj1="props.teamData[0].name" :obj2="props.teamData[1].name" :selectedItem="selectedItem" :color1="'#95e1d3'"
    :color2="'#eaffd0'"></item>
  <item :line_name="'场均大龙'" :data1="props.teamData[0].baron" :data2="props.teamData[1].baron"
    :obj1="props.teamData[0].name" :obj2="props.teamData[1].name" :selectedItem="selectedItem" :color1="'#95e1d3'"
    :color2="'#eaffd0'"></item>
  <item :line_name="'场均小龙'" :data1="props.teamData[0].dragon" :data2="props.teamData[1].dragon"
    :obj1="props.teamData[0].name" :obj2="props.teamData[1].name" :selectedItem="selectedItem" :color1="'#95e1d3'"
    :color2="'#eaffd0'"></item>
  <item :line_name="'场均推塔'" :data1="props.teamData[0].turts" :data2="props.teamData[1].turts"
    :obj1="props.teamData[0].name" :obj2="props.teamData[1].name" :selectedItem="selectedItem" :color1="'#95e1d3'"
    :color2="'#eaffd0'"></item>
</template>

<script setup>
import { onMounted, ref } from "vue";
import * as echarts from "echarts";
import item from "./against-chart-item.vue";

const props = defineProps({
  teamData: {
    type: Array,
    required: true,
  },
  matchType: {
    type: String,
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

.button1 {
  background-color: #95e1d3;
  /* 设置第一个按钮的背景色 */
  font-size: 18px;
  margin-right: 5vw;
}

.button2 {
  background-color: #eaffd0;
  /* 设置第二个按钮的背景色 */
  font-size: 18px;
}
</style>
