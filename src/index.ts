import Vue from "vue";
import WeatherControl from "./components/WeatherControl.vue";

let v = new Vue({
    el: "#app",
    template: `<weather-control></weather-control>`,
    components: {
        WeatherControl
    }
});