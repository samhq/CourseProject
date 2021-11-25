import axios from "axios";
import configJson from "@/config.json";

var http = axios.create({
    baseURL: configJson.backendAPI,
})

export default http;