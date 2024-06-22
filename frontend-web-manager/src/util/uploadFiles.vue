<template>
  <el-upload
    class="upload-demo"
    action="#"
    drag
    multiple
    :accept="accept"
    :auto-upload="false"
    :limit='30'
    :file-list="submitFiles"
    :on-exceed="handleExceed"
    :on-remove="handleRemove"
    :on-change="handleChange"
    :before-upload="handleBeforeUpload"
  >
    <icon-upload-one theme="outline" size="30" fill="grey"/>
    <div class="el-upload__text">
      Drop file here or <em>click to upload</em>
    </div>
    <template #tip>
      <div class="el-upload__tip">
        支持{{accept}}格式文件；文件大小不超过{{fileSize}}M；不超过30个文件
      </div>
    </template>
  </el-upload>
</template>

<script lang="ts">
import {ElMessage} from "element-plus";
import {UploadOne as IconUploadOne} from "@icon-park/vue-next";
export default {
  name: "uploadFiles",
  components: {IconUploadOne},
  props: {
    fileType: {
      type: Array,
      default: () => ['.pdf', '.txt'],
    },
    fileSize: {
      type: Number,
      default: () => 200,
    },
    submitFiles: {
      default: []
    }
  },
  data() {
    return {
      accept: '',
    }
  },
  methods: {
    handleExceed() {
      ElMessage.warning('待上传文件数量超出限制，请分批次上传！')
    },
    handleChange(file, uploadFiles) {
      this.$emit('update:uploadFiles', uploadFiles)
    },
    handleRemove() {
      this.$emit('update:uploadFiles', '')
    },
    handleBeforeUpload(file) {
      if (this.fileType) {
        let fileExtension = "";
        if (file.name.lastIndexOf(".") > -1) {
          fileExtension = file.name.slice(file.name.lastIndexOf("."));
        }
        const isTypeOk = this.fileType.some((type) => {
          if (file.type.indexOf(type) > -1) return true;
          return fileExtension && fileExtension.indexOf(type) > -1;

        });
        if (!isTypeOk) {
          ElMessage.error(`文件格式不正确, 请上传${this.fileType.join("/")}格式文件!`);
          return false;
        }
      }
      // 校检文件大小
      if (this.fileSize) {
        const isLt = file.size / 1024 / 1024 < this.fileSize;
        if (!isLt) {
          ElMessage.error(`上传文件大小不能超过 ${this.fileSize} MB!`);
          return false;
        }
      }
      return true;
    }
  },
  created() {
    this.fileType?.forEach(el => {
      this.accept += el + ','
    })
    this.fileType?.slice(0, this.fileType?.length - 2)
  }
}
</script>

<style scoped>

</style>