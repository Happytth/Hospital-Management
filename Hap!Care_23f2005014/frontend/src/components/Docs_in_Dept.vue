<template>
  <div class="chart-container">
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script>
export default {
  props: {
    Docs_in_Dept: {
      type: Array,
      required: true
    }
  },
  mounted() {
    this.renderChart()
  },
  watch: {
    Docs_in_Dept: {
      handler() {
        this.updateChart()
      },
      deep: true
    }
  },
  methods: {
    renderChart() {
      const ctx = this.$refs.canvas.getContext('2d')
      const labels = this.Docs_in_Dept.map(dep => dep.dept_name)
      const values = this.Docs_in_Dept.map(dep => dep.doctor_count)

      this._chart = new window.Chart(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [{
            label: 'Doctors per Department',
            data: values,
            backgroundColor: this.generateColors(labels.length),
            borderRadius: 4,
            barThickness: 'flex' // adaptive thickness
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'top', labels: { boxWidth: 15 } },
            title: { display: true, text: 'Doctors by Department', font: { size: 14 } }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: { stepSize: 1, font: { size: 11 } },
              title: { display: true, text: 'Doctors', font: { size: 12 } },
              grid: { display: false }
            },
            x: {
              ticks: { font: { size: 11 } },
              title: { display: true, text: 'Departments', font: { size: 12 } },
              grid: { display: false }
            }
          },
          animation: {
            duration: 1200,
            easing: 'easeOutCubic'
          },
          layout: {
            padding: { top: 5, bottom: 5, left: 5, right: 5 }
          }
        }
      })
    },

    updateChart() {
      if (this._chart) {
        this._chart.data.labels = this.Docs_in_Dept.map(dep => dep.dept_name)
        this._chart.data.datasets[0].data = this.Docs_in_Dept.map(dep => dep.doctor_count)
        this._chart.data.datasets[0].backgroundColor = this.generateColors(this._chart.data.labels.length)
        this._chart.update()
      }
    },

    generateColors(count) {
      const colors = []
      for (let i = 0; i < count; i++) {
        const hue = Math.floor(Math.random() * 360)
        colors.push(`hsl(${hue}, 65%, 70%)`)
      }
      return colors
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
  height: 290px; /* reduced height for better fit */
  padding: 0.5rem;
}
canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>
