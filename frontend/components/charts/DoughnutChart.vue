<template>
  <Doughnut :data="chartData" :options="chartOptions" />
</template>

<script setup>
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js'
import { Doughnut } from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps({
  chartData: { type: Object, required: true },
  chartOptions: { type: Object, default: () => ({ responsive: true }) }
})
</script>
