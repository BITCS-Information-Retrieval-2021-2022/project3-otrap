import Vue from 'vue'
import axios from 'axios'

const axiosInstance = axios.create({
    // baseURL:process.env.API,
    timeout: 1500 * 5
});

// 在Vue文件中通过this.$axios来使用
Vue.prototype.$axios = axiosInstance;

//在main.js设置全局的请求次数，请求的间隙
axiosInstance.defaults.retry = 6;
axiosInstance.defaults.retryDelay = 1400;

axiosInstance.interceptors.response.use(undefined, function axiosRetryInterceptor(err) {
    var config = err.config;
    // If config does not exist or the retry option is not set, reject
    if (!config || !config.retry) return Promise.reject(err);

    // Set the variable for keeping track of the retry count
    config.__retryCount = config.__retryCount || 0;

    // Check if we've maxed out the total number of retries
    if (config.__retryCount >= config.retry) {
        // Reject with the error
        return Promise.reject(err);
    }

    // Increase the retry count
    config.__retryCount += 1;

    // Create new promise to handle exponential backoff
    var backoff = new Promise(function (resolve) {
        setTimeout(function () {
            resolve();
        }, config.retryDelay || 1);
    });

    // Return the promise in which recalls axios to retry the request
    return backoff.then(function () {
        return axios(config);
    });
});



export { axiosInstance };
