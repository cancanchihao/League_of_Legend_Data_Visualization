<template>
    <div>
        <!-- 给 div 元素设置一个 id 来引用 -->
        <div id="heatmap" style="width: 100%; height: 45vh;margin-top: -4vh;"></div>
    </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, PropType, nextTick } from "vue";
import * as echarts from "echarts";
import { tr } from "element-plus/es/locale";

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
    setup(props, { emit }) {
        // 使用 `onMounted` 或 `nextTick` 确保 DOM 渲染完成后再初始化 ECharts
        onMounted(() => {
            nextTick(() => {
                // 获取 DOM 元素，使用 id 获取 DOM 元素
                const heatmapElement = document.getElementById("heatmap");

                // 确保元素存在后再初始化 ECharts
                if (heatmapElement) {
                    const chart = echarts.init(heatmapElement, 'dark');

                    // ECharts 配置项
                    const option = {
                        backgroundColor: '',
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
                            formatter: (value) => {
                                return value.toFixed(1); // 保留一位小数
                            }
                        },
                        series: [
                            {
                                name: "胜率",
                                type: "heatmap",
                                data: props.data, // 使用生成的数据
                                label: {
                                    show: true,
                                    fontSize: 10, // 调整字体大小
                                    color: 'white', // 设置字体颜色为白色
                                    formatter: (params) => {
                                        const value = params.value[2];
                                        if (value === "-") {
                                            return "N/A";
                                        }
                                        return Number.isInteger(value) 
                                            ? `${value}` 
                                            : `${value.toFixed(1)}`;
                                    },
                                },
                                itemStyle: {
                                    opacity: 0.8, // 设置单元格透明度
                                    shadowBlur: 10, // 设置阴影的模糊度
                                    shadowColor: 'rgba(0, 0, 0, 0.5)', // 设置阴影的颜色
                                    color: 'rgba(255, 255, 255, 0.1)', // 调整颜色的透明度和色调
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

                    // 监听点击事件
                    chart.on('click', (params) => {
                        if (params && params.data) {
                            const xIndex = params.data[0]; // 获取点击点的 X 轴索引
                            const yIndex = params.data[1]; // 获取点击点的 Y 轴索引

                            // 根据 xIndex 和 yIndex 获取对应的战队名称
                            const team1 = props.teamNames[xIndex];
                            const team2 = props.teamNames[yIndex];

                            emit('wordClick', team1, team2);
                            console.log(`点击的战队是: ${team1} 和 ${team2}`);
                        }
                    });

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