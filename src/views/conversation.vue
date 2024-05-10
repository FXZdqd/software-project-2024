<template>
  <div class="chat">
    <el-scrollbar>
      <div v-for="(message, index) in history" :key="index" style="margin-bottom: 2vh">
        <div v-if="message.role==='user'" style="position: relative; display: flex; align-items: center;">
          <div style="position: absolute; top: 0; left: 0; width: 30px; height: 30px; padding: 5px 5px 5px 5px; background-color: #f2c867; border-radius: 10px">
            <icon-user size="20" fill="#fff"/>
          </div>
          <div v-html="md.render(message.content)"
               style="margin-left: 40px; background-color: #f1f2f5; padding: 10px 10px 0 10px; border-radius: 10px"></div>
        </div>
        <div v-else style="position: relative; display: flex; align-items: center;">
          <div style="position: absolute; top: 0; left: 0; width: 35px; height: 35px; border-radius: 10px">
            <el-image src="/src/assets/logo.png"/>
          </div>
          <div style="margin-left: 40px; padding: 10px 10px 0 10px; border-radius: 10px">
            <div v-html="md.render(message.content)"></div>
            <div v-if="message.docs !== ''"  style="border: 1px solid gray; padding: 10px; border-radius: 10px">
              <p style="font-weight: bold">知识库匹配结果</p>
              <div v-html="md.render(message.docs)"/>
            </div>
          </div>
        </div>
      </div>
    </el-scrollbar>

    <div class="message-box">
      <el-input @keydown.enter.native="keyDown" v-model="input" placeholder="请输入对话内容" type="textarea" size="large"/>
      <el-button style="height: 50px" @click="goChat" color="#4e2fd1" plain>
        <icon-send-one size="30"/>
      </el-button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {onMounted, ref} from "vue";
import {md} from "@/util/markdown";
import eventBus from "@/util/mitt";
import {SendOne as IconSendOne, User as IconUser} from "@icon-park/vue-next";
interface Message {
  docs: string;
  content: string;
  role: string;
}

const input = ref<string>('');
const history = ref<Message[]>([]);
const temperature = ref(0)
const runningModel = ref('')
const kbName = ref('')

const insertMessage = (first: boolean, content: string, role: string, docs: string) => {
  if (!Array.isArray(history.value)) {
    console.error('history value is not an array:', history.value);
    console.error(typeof(history))
  }
  if (first) {
    history.value.push({ content, role, docs});
  } else {
    const lastMessage = history.value[history.value.length - 1];
    if (lastMessage && lastMessage.role === role) {
      lastMessage.content += content;
      lastMessage.docs += docs;
    } else {
      history.value.push({ content, role, docs});
    }
  }
};
const Real_Chat = async (query:string) => {
  if (kbName.value == '') {
    try {
      // 我只需要history的role和content
      const his = history.value.map((item) => {
        return {role: item.role, content: item.content}
      })
      const params = {
        query: query,
        history: his,
        stream: true,
        model_name: runningModel.value,
        temperature: temperature.value,
        prompt_name: 'default'
      }
      const response = await fetch("http://192.168.1.101:7861/chat/chat", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json;charset=UTF-8',
        },
        body: JSON.stringify(params)
      });

      if (response.body) {

        const reader = response.body.getReader();
        let firstChunk = true;
        while (true) {
          const { value, done } = await reader.read();
          if (done) break;
          const chunkValue = new TextDecoder().decode(value);
          console.log(chunkValue.slice(6).trim().replace(/[\x00-\x1F\x7F-\x9F]/g, ''))
          const js = JSON.parse(chunkValue.slice(6).trim().replace(/[\x00-\x1F\x7F-\x9F]/g, ''))
          insertMessage(firstChunk, js.text, 'assistant', '');
          firstChunk = false;
        }
        reader.releaseLock();
      }
    } catch (error) {
      console.error('Failed to read chat bot reply:', error);
    }
  }
  else {
    try {
      const his = history.value.map((item) => {
        return {role: item.role, content: item.content}
      })
      const params = {
        query: query,
        knowledge_base_name: kbName.value,
        top_k: 3,
        score_threshold: 0.5,
        history: his,
        stream: true,
        model_name: runningModel.value,
        temperature: temperature.value,
        prompt_name: 'default'
      }
      const response = await fetch("http://192.168.1.101:7861/chat/knowledge_base_chat", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json;charset=UTF-8',
        },
        body: JSON.stringify(params)
      });
      if (response.body) {
        const reader = response.body.getReader();
        let firstChunk = true;
        while (true) {
          const { value, done } = await reader.read();
          if (done) break;
          const chunkValue = new TextDecoder().decode(value);
          const regex = /data:\s*(\{(?:"answer":\s*".*?"|(?:"docs":\s*\[.*?\]))\})/g;
          const matches = chunkValue.match(regex);
          const jsonArray = matches.map((match) => {
            // 移除每个匹配字符串前的"data:"和可能的空格
            const jsonPart = match.replace(/data:\s*/, '');
            // 将字符串转换为JSON对象
            return JSON.parse(jsonPart);
          });
          for (let js of jsonArray){
            if('answer' in js ) {
              insertMessage(firstChunk,js.answer,'assistant','')
            }
            else{
              js.docs.forEach((doc) => {
                insertMessage(firstChunk,'','assistant',doc+'\n')
              })
            }
          }
          firstChunk = false;
        }
        reader.releaseLock();
      }
    } catch(error) {
      console.error('Failed to read chat bot reply:', error);
    }
  }
};
const goChat = async () => {
  if (!input.value) return;
  insertMessage(true, input.value, 'user', '');
  let inputText = input.value;
  input.value = ''
  await Real_Chat(inputText)
};
const keyDown = (e: KeyboardEvent) => {
  if(e.ctrlKey && e.keyCode==13) {   //用户点击了ctrl+enter触发
    input.value += '\n';
  }else { //用户点击了enter触发
    e.preventDefault();
    goChat();
  }
};
onMounted(() => {
  eventBus.on('clear', (value: boolean) => {
    if (value == true)
      history.value = [];
  })
  eventBus.on('runningModel', (value: string) => {
    runningModel.value = value
  })
  eventBus.on('kbName', (value: string) => {
    kbName.value = value
  })
  eventBus.on('temperature', (value: number) => {
    temperature.value = value
  })
})

</script>

<style scoped>
.chat {
  padding-top: 8vh;
  width: 800px;
  display: flex;
  flex-direction: column;
  height: 100%;
}
@media screen and (max-width: 1100px) {
  .chat {
    width: 100%;
  }
}

.chat-title {
  border-bottom: 1px solid #eee;
  padding: 12px;
  text-align: center;
  font-size: 20px;
}

.ms {
  flex-grow: 1;
  overflow: auto;
  display: flex;
  flex-direction: column;
}

.message {
  padding: 1rem;
  margin: 1rem;
  border-radius: 0.5rem;
  background: #fff;
}

.user {
  background-color: #f8f8fa;
  align-self: flex-end;
}
.assistant{
  align-self: flex-start;
  background-color: #f1f1f0;
  color: #000;
}

.message-box {
  display: flex;
  flex-shrink: 0;
  padding: 8px;
}

.message-box textarea {
  flex-grow: 1;
  border: 1px solid #eee;
  padding: 8px;
  border-radius: 4px;
  font-size: 14px;
}

/*.message-box button {*/
/*  padding: 0 16px;*/
/*  border: none;*/
/*  border-radius: 4px;*/
/*  background: black;*/
/*  color: #fff;*/
/*}*/
html,body,div,h1,p,textarea,button,pre {
  margin: 0;
  box-sizing: border-box;
}
</style>