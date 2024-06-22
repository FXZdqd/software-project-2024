<template>
  <div class="background-container">
    <canvas id="c"></canvas>
  </div>
</template>

<script lang="ts">
import {onMounted, ref } from 'vue';

export default {
  name:"Rain",
  setup(_props) {
    const canvas = ref<HTMLCanvasElement | null>(null);
    const ctx = ref<CanvasRenderingContext2D | null>(null);
    const chinese = '010110';
    const font_size = 10;
    let columns = 0;
    const drops: number[] = [];

    const initCanvas = () => {
      if (canvas.value) {
        canvas.value.height = window.innerHeight;
        canvas.value.width = window.innerWidth;
        columns = canvas.value.width / font_size;
      }
    };

    const initDrops = () => {
      for (let x = 0; x < columns; x++) {
        drops[x] = 1;
      }
    };

    const draw = () => {
      if (ctx.value) {
        ctx.value.fillStyle = 'rgba(0,0,0,0.05)';
        ctx.value.fillRect(0, 0, canvas.value!.width, canvas.value!.height);

        ctx.value.fillStyle = '#0F0';
        ctx.value.font = `${font_size}px arial`;

        for (let i = 0; i < drops.length; i++) {
          const text = chinese[Math.floor(Math.random() * chinese.length)];
          ctx.value.fillText(text, i * font_size, drops[i] * font_size);

          if (drops[i] * font_size > canvas.value!.height && Math.random() > 0.975) {
            drops[i] = 0;
          }
          drops[i]++;
        }
      }
    };

    onMounted(() => {
      canvas.value = document.getElementById('c') as HTMLCanvasElement;
      ctx.value = canvas.value.getContext('2d');
      initCanvas();
      initDrops();
      setTimeout(() => {
        setInterval(draw, 50);
      }, 5000); // 5000毫秒后启动动画，即5秒
    });

    return {
      canvas,
      ctx,
      chinese,
      font_size,
      columns,
      drops,
    };
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
  width: 100%;
  height: 100%;
  z-index: -1;
}
</style>
