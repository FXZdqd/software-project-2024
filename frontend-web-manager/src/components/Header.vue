<template>
  <div class="logo">
    <img src="@/assets/bz.svg" alt="Logo" />
    <h1
      style="font-family: &quot;优设标题&quot;; font-size: 20px; margin-top: 3%"
    >
      智能校园 <br />问答平台
    </h1>
  </div>
</template>

<script>
export default {};
</script>

<style>
.logo {
  margin-top: 4%;
  display: flex; /* 启用Flexbox布局 */
  align-items: center; /* 垂直居中对齐 */
  gap: 10px; /* 图片和文字之间的间隙 */
  height: fit-content;
}

.logo img {
  width: 20%; /* 图片大小，可以根据需要调整 */
}
</style>
