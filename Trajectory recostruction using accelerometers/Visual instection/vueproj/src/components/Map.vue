<template>
  <b-overlay :show="loading">
    <svg width="100%" class="map" viewBox="0 0 730 500" preserveAspectRatio="xMidYMid meet">
      <image href="MC2-tourist.jpg" height="500" width="100%"/>
      <g class="abila" ref="abila"></g>
      <g class="routes" ref="routes"></g>
    </svg>
  </b-overlay>
</template>

<script>

import MapJS from "@/assets/MapJS";

const map = MapJS()
    .featureClass('id'); //component to handle the map

const d3 = require('d3');

export default {
  name: "Map",
  props: {
    featureCollection: {
      type: Object,
      default: () => ({
        type: 'FeatureCollection',
        features: [
          {
            type: 'Feature',
            properties: {
              color: "red"
            },
            geometry: {
              type: 'LineString',
              coordinates: [[0, 0], [1, 1]],
            },
          },
        ],
      }),
    },
  },

  data() {
    return {
      loading: true
    }
  },

  mounted() {
    const gAbila = d3.select(this.$refs.abila);
    const gRoutes = d3.select(this.$refs.routes);

    d3.json('/Abila_geo.json')
        .then((data) => {
          gAbila.datum(data)
              .call(map);
        });

    gRoutes.datum(this.featureCollection)
        .call(map);

    this.loading = false
  },

  methods: {},

  watch: {
    featureCollection(newFc) {
      this.loading = true;
      const gRoutes = d3.select(this.$refs.routes);

      gRoutes.datum(newFc).call(map);

      this.loading = false;
    }
  }
}
</script>

<style>

g.abila path {
  fill: transparent;
  stroke: rgba(204, 185, 153, .5);
}

g.routes path {
  opacity: .7;
  fill: transparent;
  stroke-width: 4;
}

svg > image {
  y: -5px;
  x: 5px;
  transform: scaleX(.984) scaleY(1.032);
}


</style>