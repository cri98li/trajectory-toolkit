<template>
  <svg width="100%" height="70px" class="rangeSelector" ref="rangeSelector">
    <!-- non uso viewport anche qui perchè altrimenti non scala bene l'asse delle x -->
  </svg>
</template>

<script>
import RangeSelector from "@/assets/rangeSelectorJS";

const rs = RangeSelector();
const d3 = require('d3')

export default {
  name: "rangeSelector",

  //Per ridisegnare il componente se la pagina viene ridimensioata
  created() {
    window.addEventListener("resize", this.pageResize);
  },
  destroyed() {
    window.removeEventListener("resize", this.pageResize);
  },

  props: {
    timestamps: {
      type: Array,
      default: () => []
    },
    currTime: {
      type: Number,
      default: () => 0
    },
    playState: {
      type: Boolean,
      default: () => false
    },
    carColors: {
      type: Object,
      default: () => {
        return {1: 'red', 2: 'blue'}
      }
    }
  },

  data() {
    return {
      min: 0,
      max: 86400000,
      step: 60 * 1000 * 10
    }
  },

  mounted() {
    d3.select(this.$refs.rangeSelector)
        .datum(this.makeConfig())
        .call(rs);

    rs.on("interval", (d) => {
      this.$emit('changeTime', {
        start: d[0],
        stop: d[1]
      });
    })
  },

  methods: {
    makeConfig() {
      return {
        values: this.timestamps.map((a) => {
          return {
            id: a.id,
            ts: a.timestamp.map((d) => d % this.max)
          }
        }),
        min: this.min,
        max: this.max,
        step: this.step, //intervalli di 1 s
        colors: this.carColors
      }
    },

    pageResize() {
      d3.select(this.$refs.rangeSelector)
          .call(rs);
    }
  },

  watch: {
    timestamps: {
      handler() {
        d3.select(this.$refs.rangeSelector)
            .datum(this.makeConfig())
            .call(rs);

        rs.clearBrush()
      }
    },
    currTime: {
      handler(newVal) {
        if (this.playState)
          rs.updateCircle(newVal % this.max)
        else rs.updateCircle(null)
      }
    }
  },
}
</script>

<style scoped>
.rangeSelector {
}
</style>