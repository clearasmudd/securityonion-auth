/*
eslint-disable no-shadow,
no-underscore-dangle,
no-unused-expressions,
implicit-arrow-linebreak,
no-param-reassign,
no-unused-vars
 */
import Vue from 'vue';
import axios from 'axios';

// Full config:  https://github.com/axios/axios#request-config
// axios.defaults.baseURL = process.env.baseURL || process.env.apiUrl || 'http://127.0.0.1:5000/auth';
// axios.defaults.headers.common.Authorization = AUTH_TOKEN;
// axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

const config = {
  baseURL: process.env.baseURL || process.env.apiUrl || 'http://localhost:5000',
  timeout: 60 * 1000, // Timeout
  // withCredentials: true, // Check cross-site Access-Control
};

const axiosInstance = axios.create(config);


/* axiosInstance.interceptors.request.use(
  (config) => {
    // Do something before request is sent
  },
  (error) => {
    // Do something with request error
    Promise.reject(error);
  },

);

// Add a response interceptor
axiosInstance.interceptors.response.use(
  response =>
    // Do something with response data
    response,
  error =>
    // Do something with response error
    Promise.reject(error),
); */

Plugin.install = (Vue, options) => {
  Vue.axios = axiosInstance;
  window.axios = axiosInstance;
  Object.defineProperties(Vue.prototype, {
    axios: {
      get() {
        return axiosInstance;
      },
    },
    $axios: {
      get() {
        return axiosInstance;
      },
    },
  });
};

Vue.use(Plugin);

export default Plugin;
