<template>
    <div>
        <!-- 给 div 元素设置一个 id 来引用 -->
        <div id="heatmap" style="width: 61vh; height: 61vh;"></div>
    </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, PropType, nextTick } from "vue";
import * as echarts from "echarts";

export default defineComponent({
    name: "Heatmap",
    props: {
        teamNames: {
            type: Array as PropType<string[]>,
            required: true,
        },
        data: {
            type: Array as PropType<[number, number, number | "-"][]>,
            required: true,
        },
        title: {
            type: String,
            default: "Heatmap",
        },
    },
    setup(props) {
        // 使用 `onMounted` 或 `nextTick` 确保 DOM 渲染完成后再初始化 ECharts
        onMounted(() => {
            nextTick(() => {
                // 获取 DOM 元素，使用 id 获取 DOM 元素
                const heatmapElement = document.getElementById("heatmap");

                // 确保元素存在后再初始化 ECharts
                if (heatmapElement) {
                    const chart = echarts.init(heatmapElement);

                    // ECharts 配置项
                    const option = {
                        title: {
                            text: props.title,
                            left: "center",
                        },
                        tooltip: {
                            position: "top",
                            formatter: (params: { value: [number, number, number | "-"] }) => {
                                const value = params.value[2];
                                return value === "-" ? "N/A" : `胜率：${value}%`;
                            },
                        },
                        grid: {
                            height: "70%",
                            top: "10%",
                            left: "10%", // 增加左侧留白
                            right: "10%", // 增加右侧留白
                        },
                        xAxis: {
                            type: "category",
                            data: props.teamNames,
                            splitArea: { show: true },
                            axisLabel: {
                                rotate: 45, // 将 X 轴标签旋转 45 度，避免重叠
                                interval: 0, // 确保每个标签都显示
                            },
                        },
                        yAxis: {
                            type: "category",
                            data: props.teamNames,
                            splitArea: { show: true },
                        },
                        visualMap: {
                            min: 0,
                            max: 100,
                            calculable: true,
                            orient: "horizontal",
                            left: "center",
                            bottom: "5%",
                            // inRange: {
                            //     color: ["#d4e157", "#ffee58", "#f57f17"],
                            // },
                        },
                        series: [
                            {
                                name: "胜率",
                                type: "heatmap",
                                data: props.data, // 使用生成的数据
                                label: {
                                    show: true,
                                },
                                emphasis: {
                                    itemStyle: {
                                        shadowBlur: 10, // 设置阴影的模糊度
                                        shadowColor: 'rgba(0, 0, 0, 0.5)', // 设置阴影的颜色
                                    },
                                },
                            },
                        ],
                    };

                    // 设置图表选项
                    chart.setOption(option);

                    // // 监听窗口大小变化
                    // window.addEventListener("resize", chart.resize);
                } else {
                    console.error("DOM element for heatmap not found!");
                }
            });
        });

        return {};
    },
});
</script>

<style scoped></style>