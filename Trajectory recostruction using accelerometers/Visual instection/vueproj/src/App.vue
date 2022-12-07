<template>
  <div id="app">
    <b-navbar type="dark" variant="primary" class="shadow">
      <b-navbar-brand>VAST 2014 - mc2</b-navbar-brand>
      <b-collapse id="nav-text-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-text>Cristiano Landi</b-nav-text>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>


    <b-overlay :show="loading != 0">
      <b-container style="padding-bottom: 200px" fluid="xl">
        <b-row>
          <b-col xl="8" style="text-align: center" class="xl-no-padding">
            <Map
                :featureCollection="pointCollection"
            />
          </b-col>
          <b-col xl="4" class="xl-no-padding">
            <idSelector
                :colorSet="colorbrewer_colors"
                @changeCars="updateCar($event)"/>
          </b-col>
        </b-row>
        <b-row>
          <b-col cols="12">
            <TimeControls
                @changeTime="updateDate($event)"
                :ts="ts"
                :carColors="usersColor"
            />
          </b-col>
        </b-row>
        <b-row>
          <b-col cols="12">
            <h4>Transazioni</h4>
            <MySunburst style="height: 400px"
                        :users-color="usersColor"
                        :time-controls="TimeControls"
                        :colors="colorbrewer_colors"
            ></MySunburst>
          </b-col>
        </b-row>
      </b-container>
    </b-overlay>
  </div>
</template>

<script>
import IdSelector from "@/components/idSelector";

const d3 = require('d3');

import crossfilter from 'crossfilter';
import BiMap from 'bidirectional-map'


import Map from '@/components/Map';
import TimeControls from "@/components/TimeControls";
import MySunburst from "@/components/mySunburst";

let cf; // crossfilter instance
let dID; // dimension for Id
let dTimestamp;

let id_to_car_map = new BiMap()

export default {
  name: 'App',
  components: {
    MySunburst,
    IdSelector,
    TimeControls,
    Map,
  },
  data() {
    return {
      pointCollection: {
        type: 'FeatureCollection',
        features: [
          {
            type: 'Feature',
            properties: {
              name: 'Default point',
            },
            geometry: {
              type: 'LineString',
              coordinates: [[1, 1], [1, 2]]
            },
          },
        ],
      },

      ts: [],

      colorbrewer_colors: ['#e41a1c', '#377eb8', '#4daf4a',
        '#984ea3', '#ff7f00',//'#ffff33',
        '#a65628', '#f781bf'],

      usersColor: {},

      TimeControls: {
        mapTimeStart: new Date("2014-01-06 00:00:00 GMT").getTime(),
        mapTimeStop: new Date("2014-01-06 23:59:59 GMT").getTime(),
        mapDate: new Date("2014-01-06 00:00:00 GMT").getTime(),
        playState: false
      },

      loading: 2
    }
  },

  mounted() {
    fetch('./gps.json')
        .then(data => data.json())
        .then((data) => {
          const gps = data.map((d) => {
            const r = {
              Timestamp: +new Date(d.Timestamp + " GMT").getTime(), //timestamp, lo stesso di sopra
              id: +d.id,
              lat: +d.lat,
              long: +d.long
            };
            return r;
          });

          cf = crossfilter(gps);
          dID = cf.dimension(d => d.id);
          dTimestamp = cf.dimension(d => d.Timestamp);

          dTimestamp.filterRange([parseInt(this.TimeControls.mapDate), parseInt(this.TimeControls.mapDate) + (1000 * 60 * 60 * 24)]);

          this.loading--
        });


    d3.csv("/macchine.csv").then(data => {
      data.forEach((d) => {
        id_to_car_map.set(parseInt(d.id), parseInt(d.CarID))
      })

      this.loading--
    });
  },
  methods: {
    refresh(cfDimension) {
      dTimestamp.filterRange([parseInt(this.TimeControls.mapTimeStart), parseInt(this.TimeControls.mapTimeStop)]);

      this.pointCollection = this.getGeoJsonFromReports(cfDimension.top(Infinity));
    },

    updateDate(newVal) {
      this.TimeControls.mapTimeStart = newVal.start;
      this.TimeControls.mapTimeStop = newVal.stop;
      this.TimeControls.playState = newVal.playState;
      if (newVal.day != null) {
        this.TimeControls.mapDate = newVal.day
        dTimestamp.filterRange([parseInt(this.TimeControls.mapDate), parseInt(this.TimeControls.mapDate) + (1000 * 60 * 60 * 24)]);
        this.ts = this.getTimestampList(dTimestamp.top(Infinity))
      }

      this.refresh(dTimestamp);
    },

    updateCar(newVal) {
      const carIds = newVal.map(d => id_to_car_map.get(d));

      if (carIds.includes(undefined))
        this.$bvToast.toast('Sono stati selezionati dipendenti senza auto associata, ' +
            'puoi comunque selezionare un intervallo orario per visualizzare le sue transazioni', {
          title: 'Attenzione',
          autoHideDelay: 5000,
        })

      this.updateColor(newVal);
      dID.filter(d => carIds.indexOf(d) > -1);
      this.updateDate({
        start: this.TimeControls.mapTimeStart,
        stop: this.TimeControls.mapTimeStop,
        day: this.TimeControls.mapDate
      })
      this.refresh(dID);
    },

    updateColor(ids) {
      this.usersColor = {}
      ids.forEach((d) => {
        this.usersColor[d] = this.colorbrewer_colors[d % this.colorbrewer_colors.length]
      })
    },

    getTimestampList(cf_result) {
      const ts = Array.from(d3.group(cf_result, c => c.id)).map((d) => {
        return {
          id: id_to_car_map.getKey(d[0]),
          timestamp: d[1].sort((a, b) => a.Timestamp - b.Timestamp).map(p => (p.Timestamp)),
        };
      });

      return ts;
    },

    getGeoJsonFromReports(coordinates) {
      const trs = Array.from(d3.group(coordinates, c => c.id)).map((d) => {
        return {
          id: d[0],
          trajs: d[1].sort((a, b) => a.Timestamp - b.Timestamp).map(p => ([p.long, p.lat])),
        };
      });


      const fc = {
        type: 'FeatureCollection',
        features: trs
            .map(d => ({ // for each entry
                  type: 'Feature',
                  properties: {
                    id: id_to_car_map.getKey(d.id),
                    color: this.usersColor[id_to_car_map.getKey(d.id)]
                  },
                  geometry: {
                    type: 'LineString',
                    coordinates: d.trajs,
                  }
                })
            )
      };
      return fc;
    }
  },
  watch: {},
}
</script>

<style>
nav {
  margin-bottom: 24px;
}

.row {
  margin-bottom: 16px;
}

.xl-no-padding {
  padding: 0px !important;
}

@media only screen and (max-width: 1200px) {
  .xl-no-padding {
    padding: 16px !important;
  }
}

.container-xl{
  max-width: 1200px !important; /*sfrutto al massimo lo spazio*/
}

</style>
