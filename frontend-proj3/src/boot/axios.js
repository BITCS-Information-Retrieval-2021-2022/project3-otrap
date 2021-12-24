import Vue from 'vue'
import axios from 'axios'

const axiosInstance = axios.create({
    // baseURL:process.env.API,
    timeout: 10000
});

// 在Vue文件中通过this.$axios来使用
Vue.prototype.$axios = axiosInstance;

export { axiosInstance };
