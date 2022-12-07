<template>
  <b-overlay :show="loading">
    <b-form-group>
      <h4>Impostazioni temporali</h4>
      <b-row align-v="center">
        <b-col cols="2">
          <label>Seleziona un giorno:</label>
        </b-col>

        <b-col>
          <b-form-datepicker id="datepicker" v-model="pickedDate" min="2014-01-06" max="2014-01-19"
                             locale="it"></b-form-datepicker>
        </b-col>

        <b-col cols="2">
          <div>{{ datePrettyPrint(pickedDate) }}</div>
        </b-col>
      </b-row>

      <b-row align-v="center">
        <b-col cols="2">
          <label>Seleziona un intervallo orario:</label>
        </b-col>

        <b-col>
          <rangeSelector
              :curr-time="currTime"
              :timestamps="ts"
              :playState="playState"
              :carColors="carColors"
              @changeTime="updateTime($event)"
          ></rangeSelector>
        </b-col>
        <b-col cols="2">
          <div>{{ timePrettyPrint(start) }}<br>{{ timePrettyPrint(stop) }}</div>
        </b-col>
      </b-row>
      <b-row align-v="center">
        <b-col cols="2" offset="5">
          <b-button-group>
            <b-button v-on:click="slower()" variant="outline-primary">
              <b-icon icon="skip-start"></b-icon>
            </b-button>
            <b-button :pressed.sync="playState" variant="outline-primary">
              <b-icon :hidden="playState" icon="play"></b-icon>
              <b-icon :hidden="!playState" icon="stop"></b-icon>
            </b-button>
            <b-button v-on:click="faster()" variant="outline-primary">
              <b-icon icon="skip-end"></b-icon>
            </b-button>
          </b-button-group>
        </b-col>
        <b-col offset="3" cols="2">
          {{ timePrettyPrint(currTime) }} <br> x{{ playSpeed }}
        </b-col>
      </b-row>
    </b-form-group>
  </b-overlay>
</template>

<script>
import RangeSelector from "@/components/rangeSelector";

export default {
  name: "TimeControls",

  components: {RangeSelector},

  props: {
    mapTimeStart: {
      type: Number,
      default: new Date("2014-01-06 00:00:00 GMT").getTime()
    },
    mapTimeStop: {
      type: Number,
      default: new Date("2014-01-06 23:59:59 GMT").getTime()
    },

    ts: {
      type: Array,
      required: true,
      default: () => []
    },

    carColors: {
      type: Object,
      default: () => {
      }
    }
  },

  data() {
    return {
      pickedDate: "2014-01-06",

      start: new Date("2014-01-06 00:00:00 GMT").getTime(),
      stop: new Date("2014-01-06 23:59:59 GMT").getTime(),

      playSpeed: 8,

      playState: false,
      currTime: new Date("2014-01-06 00:00:00 GMT").getTime(),

      loading: true
    };
  },

  mounted() {
    this.loading = false;
  },

  computed: {},

  methods: {
    updateTime(newVal) {
      const dayTimeStamp = new Date(this.pickedDate).getTime()

      this.start = newVal.start + dayTimeStamp
      this.stop = newVal.stop + dayTimeStamp
      this.currTime = this.start
      this.playState = false

      this.$emit('changeTime', {
        start: this.start,
        stop: this.stop,
        day: null,
        playState: this.playState
      });
    },

    datePrettyPrint(YYYY_MM_DD) {
      return YYYY_MM_DD;
    },

    timePrettyPrint(timestamp) {
      let date = new Date(parseInt(timestamp));
      return date.toLocaleTimeString(['it'], {timeZone: 'GMT', hour: '2-digit', minute:'2-digit'});
    },

    animate(inizio, fine) {
      if (inizio > fine || !this.playState) {
        this.playState = false;
        this.currTime = this.start;
        return;
      }

      this.currTime = inizio + 60 * 1000; //mostra i 60 secondi successivi

      this.$emit('changeTime', {
        start: inizio,
        stop: this.currTime,
        day: null,
        playState: this.playState
      });

      setTimeout(() => {
        this.animate(inizio + 1000 * this.playSpeed, fine)
      }, 1000 / 30);
    },

    slower() {
      this.playSpeed /= 2
    },

    faster() {
      this.playSpeed *= 2
    }
  },

  watch: {
    playState: {
      handler(v) {
        if (!v)
          this.$emit('changeTime', {
            start: this.start,
            stop: this.stop,
            day: null,
            playState: this.playState
          });
        this.animate(parseInt(this.currTime), parseInt(this.stop));
      }
    },

    pickedDate: {
      handler(newVal) {
        this.start = new Date(newVal + " 00:00:00 GMT").getTime();
        this.stop = new Date(newVal + " 23:59:59 GMT").getTime();


        this.$emit('changeTime', {
          start: this.start,
          stop: this.stop,
          day: this.start,
          playState: this.playState
        });
      }
    },
  }
}
</script>

<style scoped>

</style>