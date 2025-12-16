<script setup lang="ts">
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  CategoryScale
} from 'chart.js'
import { Line } from 'vue-chartjs'
import { computed } from 'vue'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  CategoryScale
)

const props = defineProps({
  data: {
    type: Array as () => number[],
    default: () => [40, 39, 10, 40, 39, 80, 40]
  },
  labels: {
    type: Array as () => string[],
    default: () => ['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom']
  },
  label: {
    type: String,
    default: 'Data'
  },
  color: {
    type: String,
    default: '#0071e3' // Apple Blue
  }
})

const chartData = computed(() => ({
  labels: props.labels,
  datasets: [
    {
      label: props.label,
      backgroundColor: 'transparent',
      borderColor: props.color,
      borderWidth: 2,
      pointRadius: 0, // Minimalist: no points by default
      pointHoverRadius: 4,
      data: props.data,
      tension: 0.4 // Smooth curves
    }
  ]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false // Minimalist: no legend inside chart
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      titleFont: { family: 'Inter', size: 13 },
      bodyFont: { family: 'Inter', size: 13 },
      padding: 10,
      cornerRadius: 8,
      displayColors: false
    }
  },
  scales: {
    x: {
      grid: {
        display: false // No vertical grid lines
      },
      ticks: {
        font: { family: 'Inter', size: 11 },
        color: '#9ca3af'
      },
      border: {
        display: false
      }
    },
    y: {
      grid: {
        color: '#f3f4f6', // Very subtle horizontal lines
        drawBorder: false
      },
      ticks: {
        font: { family: 'Inter', size: 11 },
        color: '#9ca3af',
        maxTicksLimit: 5
      },
      border: {
        display: false
      }
    }
  },
  interaction: {
    intersect: false,
    mode: 'index'
  }
}
</script>

<template>
  <div class="h-64 w-full">
    <Line :data="chartData" :options="chartOptions as any" />
  </div>
</template>
