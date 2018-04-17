<template>
    <div class="weather-tile" v-on:click="click" v-on:mouseover="mouseOver" v-on:mouseout="mouseOut" data-toggle="tooltip" v-bind:title="JSON.stringify(tileData)" v-bind:style="{
        width: tileWidth + '%',
        height: tileHeight + '%',
        border: (hovered ? '1px solid red' : '')
    }" >
        <div class="tile tile-surface" v-bind:style="{
            backgroundColor: backgroundColor,
            backgroundImage: backgroundImage,
        }"></div>
        <div class="tile tile-ice" v-bind:style="{
            opacity: this.tileData.current_ice / 100
        }"></div>
        <div class="tile tile-water" v-bind:style="{
            opacity: this.tileData.current_water / 100
        }"></div>
        <div class="tile tile-rain" v-bind:style="{
            opacity: this.tileData.current_rain / 100
        }"></div>
        <div class="tile tile-low-clouds" v-bind:style="{
            opacity: this.tileData.current_low_clouds / 100
        }"></div>
        <div class="tile tile-high-clouds" v-bind:style="{
            opacity: this.tileData.current_high_clouds / 100
        }"></div>
    </div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
    props: [
        'tileData',
        'tileHeight',
        'tileWidth'
    ],
    data() {
        return {
            hovered: false
        }
    },
    methods: {
        click() {
            this.$emit('selected', this.tileData);
        },
        mouseOver() {
            this.hovered = true;
        },
        mouseOut() {
            this.hovered = false;
        },
    },
    computed: {
        backgroundColor() {
            const componentToHex = (c: number) => {
                const hex = Math.round(c).toString(16);
                return hex.length == 1 ? "0" + hex : hex;
            };
            const rgbToHex = (r:number, g:number, b:number) => {
                return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
            };


            if (this.tileData.elevation <= 10) {
                const one: number = ((this.tileData.elevation) / 10 * 20);
                const two: number = ((this.tileData.elevation) / 10 * 50);
                const three: number = (100+(this.tileData.elevation / 10 * 150));
                return rgbToHex(one, two, three);
            } else if (this.tileData.elevation <= 30) {
                const one: number = (20 + (this.tileData.elevation - 10) / 30 * 70);
                const two: number = (50 + (this.tileData.elevation - 10) / 30 * 10);
                return rgbToHex(one, two, 0);
            } else if (this.tileData.elevation > 70) {
                const one: number = (150 + (this.tileData.elevation - 70) / 30 * 100);
                return rgbToHex(one, one, one);
            } else if (this.tileData.elevation > 30) {
                const one: number = (90 + (this.tileData.elevation - 30) / 40 * 60);
                const two: number = (60 + (this.tileData.elevation - 30) / 40 * 90);
                const three: number = (this.tileData.elevation - 30) / 40 * 150;
                return rgbToHex(one, two, three);
            }
            return '#ff00ff';
        },
        backgroundImage() {
            return ''
        }
    },
    components: {

    }
});
</script>

<style>
    .tile {
        width:100%;
        height:100%;
        position:absolute;
        top:0;
        left:0;
    }
    .weather-tile {
        display:block;
        float:left;
        position:relative;
    }
    .tile-ice {
        background:url(/static/images/ice.png)
    }
    .tile-water {
        background:url(/static/images/water.png)
    }
    .tile-low-clouds {
        background:url(/static/images/lowcloud.png)
    }
    .tile-high-clouds {
        background:url(/static/images/highcloud.png)
    }
    .tile-rain {
        background:url(/static/images/rain.png)
    }
</style>