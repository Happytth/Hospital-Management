<template>
  <div class="chart-container">
  <canvas ref="canvas"></canvas>
  </div>
</template>

<script>
export default {
  props: {
    genderData: {
      type: Object,
      required: true
    }
  },
  mounted() {
    this.renderChart()
  },
  watch: {
    genderData: {
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
        type: 'pie',
        data: {
          labels: ['Male', 'Female', 'Other'],
          datasets: [{
            label: 'Patient Count',
            data: [
              this.genderData.male || 0,
              this.genderData.female || 0,
              this.genderData.other || 0
            ],
            backgroundColor: ['#5494ef', '#e75480', '#ccc']
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { position: 'top' },
            title: { display: true, text: 'Gender Distribution' }
          },
          animation: {
            duration: 1500,
            easing: 'easeOutBounce'
          }
        }
      })
    },

    updateChart() {
      if (this._chart) {
        this._chart.data.datasets[0].data = [
          this.genderData.male || 0,
          this.genderData.female || 0,
          this.genderData.other || 0
        ]
        this._chart.update()
      }
    }
  },
  beforeUnmount() {
    if (this._chart) {
      this._chart.destroy()
    }
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
