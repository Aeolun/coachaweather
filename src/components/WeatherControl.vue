<template>
    <div class="container">
        <div class="row">
            <div class="col-md-3">
                <h2>Weather Control</h2>
                <div class="btn-group d-flex">
                    <a class="btn btn-secondary w-100" v-on:click="load()">Reset</a>
                </div>
                <a class="btn btn-primary btn-block mt-1" v-on:click="update()">Compute Next Day</a>
                <div class="counter"><i class="wi wi-strong-wind"></i> {{windSpeed}} <i class="fa fa-arrow-up" v-bind:style="{ transform: 'rotate(' + (windDirection % 8 * 45) + 'deg)' }"></i></div>
                <div class="row">
                    <div class="col-3">
                        <a class="btn btn-danger btn-block" v-on:click="windSpeed--">-</a>
                    </div>
                    <div class="col-6 text-center p-1">
                        Wind Speed
                    </div>
                    <div class="col-3">
                        <a class="btn btn-success btn-block" v-on:click="windSpeed++">+</a>
                    </div>
                </div>
                <div class="row mt-1">
                    <div class="col-3">
                        <a class="btn btn-danger btn-block" v-on:click="windDirection--">-</a>
                    </div>
                    <div class="col-6 text-center p-1">
                        Wind Direction
                    </div>
                    <div class="col-3">
                        <a class="btn btn-success btn-block" v-on:click="windDirection++">+</a>
                    </div>
                </div>
                <div class="counter"><i class="fa fa-thermometer-half"></i> {{temperature}}</div>
                <div class="row">
                    <div class="col-3">
                        <a class="btn btn-danger btn-block" v-on:click="temperature--">-</a>
                    </div>
                    <div class="col-6 text-center p-1">
                        Temperature
                    </div>
                    <div class="col-3">
                        <a class="btn btn-success btn-block" v-on:click="temperature++">+</a>
                    </div>
                </div>
                <a class="btn btn-secondary btn-block mt-1" v-on:click="advancedVisible = !advancedVisible">Toggle Advanced</a>
                <div id="advanced" class="mt-1" v-if="advancedVisible">
                    <a class="btn btn-secondary btn-block" v-on:click="create()">Create New Base</a>
                    <p class="text-small">This creates a new map of the chosen size, allowing you to save it as a new base.</p>
                    <a class="btn btn-secondary btn-block" v-on:click="save()">Save As Base</a>
                    <p class="text-small">This saves the current status of the map as the base map that's loaded after a reset.</p>
                </div>
            </div>
            <div class="col-md-6">
                <weather-map v-on:selected="selected" :map-data="tiles"></weather-map>
            </div>
            <div class="col-md-3">
                <div v-if="selectedTile">
                    <h3>Tile Information</h3>
                    <div class="row">
                        <div class="col-md-3">X</div>
                        <div class="col-md-3"><strong>{{selectedTile.x}}</strong></div>
                        <div class="col-md-3">Y</div>
                        <div class="col-md-3"><strong>{{selectedTile.y}}</strong></div>
                    </div>
                    <div class="mt-2">Elevation</div>
                    <vue-slider v-model="selectedTile.elevation" max="100" step="1"></vue-slider>
                    <div>Water</div>
                    <vue-slider v-model="selectedTile.current_water" max="100" step="1"></vue-slider>
                    <div>Ice</div>
                    <vue-slider v-model="selectedTile.current_ice" max="100" step="1"></vue-slider>
                    <div>Clouds (Low)</div>
                    <vue-slider v-model="selectedTile.current_low_clouds" max="100" step="1"></vue-slider>
                    <div>Clouds (High)</div>
                    <vue-slider v-model="selectedTile.current_high_clouds" max="100" step="1"></vue-slider>
                    <div>Rain</div>
                    <vue-slider v-model="selectedTile.current_rain" max="100" step="1"></vue-slider>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import VueSlider from 'vue-slider-component';

import WeatherMap from "./WeatherMap.vue"


let basetile: object = {
    x: null,
    y: null,
    elevation: 0,
    current_low_clouds: 0,
    current_high_clouds: 0,
    current_water: 0,
    current_ice: 0,
    current_rain: 0,
};

export default Vue.extend({
    props: [],
    data() : {
        map: any,
        tiles: object[][],
        temperature: number,
        windSpeed: number,
        windDirection: number,
        selectedTile: object|null,
        advancedVisible: boolean
    } {
        return {
            map: {},
            tiles: [],
            temperature: 20,
            windSpeed: 1,
            windDirection: 0,
            selectedTile: null,
            advancedVisible: false
        }
    },
    methods: {
        update() {
            if (typeof this.map.id == 'undefined') {
                alert('Cannot update the map without resetting first.')
            }

            const weatherControl = this;
            $.post('/api/map/'+weatherControl.map.id+'/step', {
                temperature: this.temperature,
                wind_direction: this.windDirection % 8,
                wind_speed: this.windSpeed
            }, (data) => {
                //new tile status is returned after step
                weatherControl.tiles = data;
            });
        },
        create() {
            const width: any = prompt("What would you like the width of the new map to be?");
            const height: any = prompt("What would you like the height of the new map to be?");

            if (width == null || height == null) return;

            let newtiles = [];
            for(let i = 0; i < height; i++) {
                let row = [];
                for(let j = 0; j < width; j++) {
                    let base = JSON.parse(JSON.stringify(basetile));
                    base.x = i;
                    base.y = j;
                    row.push(base);
                }
                newtiles.push(row);
            }

            this.tiles = newtiles;
        },
        save() {
            $.post('/api/basemap', {
                data: JSON.stringify(this.tiles)
            }, (data) => {

            });
        },
        load() {
            const weatherControl = this;
            $.post('/api/map', {}, (data) => {
                //new map is created from base
                weatherControl.map = data;
                $.get('/api/map/'+data.id+'/tiles', {}, (data) => {
                    //new map data retrieved
                    weatherControl.tiles = data;
                });
            });
        },
        selected(data: any) {
            this.selectedTile = this.tiles[data.x][data.y];
        }
    },
    computed: {

    },
    components: {
        WeatherMap,
        VueSlider,
    }
});
</script>

<style>
    .vue-slider-component {
        padding: 2.7em 0.8em 0.5em 0.8em !important;
        border: 1px solid #00000020;
        border-radius: 3px;
    }
    .text-small {
        font-size:70%;
    }
    .counter {
        width:100%;
        text-align:center;
        font-size:2em;
        border:1px solid black;
        border-radius:3px;
        margin:0.3em 0;
    }
</style>