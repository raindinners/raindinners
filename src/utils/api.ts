import axios from "axios";

export const axiosClient = axios.create({
  baseURL: "http://localhost:8081",
  timeout: 4000
});

axiosClient.interceptors.request.use(
  function (config) {
    config.headers.Accept = "application/json";
    return config;
  },
  function (error) {
    // Do something with request error
    return Promise.reject(error);
  }
);
