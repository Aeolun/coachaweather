<template>
    <div class="map" v-bind:style="{ height: windowHeight + 'px' }">
        <template v-for="(fields, index) in mapData">
            <weather-tile v-on:selected="selected" class="map-tile" v-for="value in fields" :key="value.id" :tile-data="value" :tile-height="fieldHeight" :tile-width="fieldWidth" ></weather-tile>
        </template>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import WeatherTile from "./WeatherTile.vue"

export default Vue.extend({
    props: [
        'mapData'
    ],
    data() {
        return {
            windowHeight: 0
        }
    },
    methods: {
        selected(data: object) {
            this.$emit('selected', data);
        },
    },
    computed: {
        fieldWidth(): number {
            if (typeof this.mapData[0] != 'undefined') {
                return 100 / this.mapData[0].length;
            }
            return 100;
        },
        fieldHeight(): number {
            return 100 / this.mapData.length;
        }
    },
    components: {
        WeatherTile
    },
    mounted() {
        let that = this;
        this.$nextTick(function () {
            that.windowHeight = window.innerHeight
            window.addEventListener('resize', function (e) {
                that.windowHeight = window.innerHeight
            });
        })
    },
});
</script>

<style>
    .map {
        border:1px solid grey;
    }
</style>