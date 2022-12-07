<template>
  <sunburst
      :data="data"
      :colorScale="colorScale"
      class="sunburst">

    <myBreadcrumbTrail slot="legend"
                       slot-scope="{ nodes, colorGetter, width }"
                       :current="nodes.mouseOver"
                       :root="nodes.root"
                       :colorGetter="colorGetter"
                       :from="nodes.clicked"
                       :width="width"
                       :itemWidth="150"/>

    <template slot-scope="{ on, actions }">
      <highlightOnHover v-bind="{ on, actions }"/>
      <zoomOnClick v-bind="{ on, actions }"/>
    </template>

  </sunburst>
</template>

<script>
import {
  highlightOnHover,
  sunburst,
  zoomOnClick
} from 'vue-d3-sunburst'
import crossfilter from 'crossfilter';
import myBreadcrumbTrail from "@/components/vue-d3-sunburst/myBreadcrumbTrail";
import BiMap from 'bidirectional-map'

const d3 = require('d3');

let id_FristLastName = new BiMap()

let cf; // crossfilter instance
let dID; // dimension for Id
let dDate;
let dTime;

export default {
  name: "mySunburst",

  components: {
    myBreadcrumbTrail,
    highlightOnHover,
    sunburst,
    zoomOnClick
  },

  props: {
    usersColor: {
      type: Object,
      default: () => {
      }
    },
    TimeControls: {
      type: Object,
      default: () => {
        return {
          mapTimeStart: new Date("2014-01-06 00:00:00 GMT").getTime(),
          mapTimeStop: new Date("2014-01-06 00:01:00 GMT").getTime(),
          mapDate: new Date("2014-01-06 00:00:00 GMT").getTime(),
          playState: false
        }
      }
    },

    scaler: {
      type: Function,
      default: d3.scaleLinear()

    },

    colors: {
      required: true,
      default: () => ["red"]
    }
  },

  mounted() {
    d3.csv("/transazioni.csv", (row) => {
      let time = null;

      if (row.time != "")
        time = new Date(row.timestamp + " " + row.time + " UTC").getTime()

      return {
        id: row.id,
        date: new Date(row.timestamp + " GMT").getTime(),
        location: row.location,
        price: parseFloat(row.price),
        time: time,
        credit_card: row.credit_card == "True",
        loyalty_card: row.loyalty_card == "True"
      }
    }).then((data) => {
      cf = crossfilter(data)
      dID = cf.dimension(d => d.id);
      dDate = cf.dimension(d => d.date);
      dTime = cf.dimension(d => d.time);

      dID.filter(d => Object.keys(this.usersColor).indexOf(d) > -1);
      dDate.filter(d => d == this.TimeControls.mapDate)

      d3.csv("/nomi.csv").then(data => {
        data.forEach((d) => {
          id_FristLastName.set(d.id, d.LastName + " " + d.FirstName)
        })

        this.colorScale = d3.scaleOrdinal(this.mappaPersoneColori(), this.colors)

        this.loading = false;
      });

      this.updateData()
    });
  },

  methods: {
    updateData() {
      let res = dID.top(Infinity)

      const hierarchy = this.list_to_tree(res, ["id", "location"]);

      this.data = hierarchy;
    },

    list_to_tree(data, levels) {
      let newData = {name: "Totale", children: []};

      data.forEach(function (d) {
        var depthCursor = newData.children;
        levels.forEach(function (property, depth) {
          var index;
          depthCursor.forEach(function (child, i) {
            if (d[property] == child.name || (property == "id" && id_FristLastName.get(d[property]) == child.name))
              index = i;
          });

          if (isNaN(index)) {
            if (property == "id") {
              depthCursor.push({name: id_FristLastName.get(d[property]), children: []});
            } else
              depthCursor.push({name: d[property], children: []});

            index = depthCursor.length - 1;
          }

          depthCursor = depthCursor[index].children;

          if (depth === levels.length - 1) {
            let name = ""
            const ore = new Date(d.time).getUTCHours();
            const minuti = new Date(d.time).getUTCMinutes()

            if (d.time != null) {
              if (ore < 10)
                name += "0" + ore
              else
                name += ore
              if (minuti < 10)
                name += ":0" + minuti
              else
                name += ":" + minuti

            } else
              name = "Solo C. Fedeltà"

            depthCursor.push({size: d.price, name: name, loyalty_card: d.loyalty_card, credit_card: d.credit_card});
          }
        });
      });

      return newData;
    },

    mappaPersoneColori() {
      let tmp = []
      for (let i = 0; i < 59; i++)
        tmp[i] = id_FristLastName.get(i.toString())
      return tmp
    }
  },

  watch: {
    usersColor: {
      handler(nv) {
        dID.filter(d => Object.keys(nv).indexOf(d) > -1);

        this.updateData()
      }
    },

    TimeControls: {
      handler(nv) {
        if (nv.playState == true) return;

        dDate.filter(d => {
          return d == nv.mapDate
        });

        dTime.filter(d => {
          if (d == null)
            return true;

          return d > nv.mapTimeStart && d < nv.mapTimeStop

        });

        this.updateData()
      },
      deep: true
    }
  },

  data() {
    return {
      data: {
        "name": "flare",
        "children": [
          {
            "name": "analytics",
            "children": [
              {
                "name": "cluster",
                "children": [
                  {"name": "AgglomerativeCluster", "size": 3938}
                ]
              },
              {
                "name": "optimization",
                "children": [
                  {"name": "AspectRatioBanker", "size": 7074}
                ]
              }
            ]
          }
        ]
      },

      colorScale: d3.scaleOrdinal()
    }
  },
}

</script>

<style>

.sunburst .viewport {
  height: 100%;
}

.sunburst text {
  fill: white;
}

</style>