<template>
  <div class="chart-container">
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script>
export default {
  props: {
    appointment_data: {
      type: Object,
      required: true
    }
  },
  mounted() {
    this.renderChart()
  },
  watch: {
    appointment_data: {
      handler() {
        this.updateChart()
      },
      deep: true
    }
  },
  methods: {
    renderChart() {
      const ctx = this.$refs.canvas.getContext('2d')
      this._chart = new window.Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ['Booked', 'Completed', 'Cancelled'],
          datasets: [{
            label: 'Appointment Status',
            data: [
              this.appointment_data.booked || 0,
              this.appointment_data.completed || 0,
              this.appointment_data.cancelled || 0
            ],
            backgroundColor: ['#5494ef', '#e75480', '#ccc'],
            borderWidth: 2,
            hoverOffset: 10
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '60%', // controls hole size — smaller = thicker ring
          plugins: {
            legend: {
              position: 'bottom',
              labels: { boxWidth: 14, font: { size: 12 } }
            },
            title: {
              display: true,
              text: 'Appointment Status',
              font: { size: 14 }
            }
          },
          animation: {
            duration: 1200,
            easing: 'easeOutCubic'
          }
        }
      })
    },

    updateChart() {
      if (this._chart) {
        this._chart.data.datasets[0].data = [
          this.appointment_data.booked || 0,
          this.appointment_data.completed || 0,
          this.appointment_data.cancelled || 0
        ]
        this._chart.update()
      }
    }
  },
  beforeUnmount() {
    if (this._chart) this._chart.destroy()
  }
}
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 350px; /* smaller height for a compact fit */
  padding: 0.5rem;
}

canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>
