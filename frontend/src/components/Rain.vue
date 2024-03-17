<template>
  <div class="background-container">
    <canvas id="c"></canvas>
  </div>
</template>

<script lang="ts">


export default {
  data() {
    return {
      canvas: null,
      ctx: null,
      chinese: "010110",
      font_size: 10,
      columns: 0,
      drops: [],
    };
  },
  mounted() {
    this.canvas = document.getElementById("c");
    this.ctx = this.canvas.getContext("2d");
    this.initCanvas();
    this.initDrops();
    setInterval(this.draw, 50);
  },
  methods: {
    initCanvas() {
      this.canvas.height = window.innerHeight;
      this.canvas.width = window.innerWidth;
      this.columns = this.canvas.width / this.font_size;
    },
    initDrops() {
      for (let x = 0; x < this.columns; x++) {
        this.drops[x] = 1;
      }
    },
    draw() {
      this.ctx.fillStyle = "rgba(0,0,0,0.05)";
      this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

      this.ctx.fillStyle = "#0F0";
      this.ctx.font = this.font_size + "px arial";

      for (let i = 0; i < this.drops.length; i++) {
        const text = this.chinese[Math.floor(Math.random() * this.chinese.length)];

        this.ctx.fillText(text, i * this.font_size, this.drops[i] * this.font_size);

        if (this.drops[i] * this.font_size > this.canvas.height && Math.random() > 0.975) {
          this.drops[i] = 0;
        }
        this.drops[i]++;
      }
    },
  },
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
}
.background-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

canvas {
  display: block;
  width: 100%; /* 设置canvas宽度为100% */
  height: 100%; /* 设置canvas高度为100% */
  z-index: -1;
}
</style>