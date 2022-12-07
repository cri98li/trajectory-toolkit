<template>
  <b-overlay :show="loading">
    <b-form-group>
      <h4>Seleziona una persona</h4>
      <div id="carList">
        <vue-good-table
            select-mode="multi"
            :rows="carIds"
            :columns="fields"
            @on-selected-rows-change="onRowSelected"
            class="table"
            :fixed-header="true"
            ref="ids"
            compact-mode
            :sort-options="{
            enabled: true,
            initialSortBy: {field: 'name', type: 'asc'}
          }"
            :select-options="{
            enabled: true,
            disableSelectInfo: true,
            //selectAllByGroup: true,
          }"
            :search-options="{enabled: true}"
            :group-options="{
            enabled: true,
            headerPosition: 'top'
          }"
        >
          <template slot="table-row" slot-scope="props">
          <span
              class="wrap"
              v-if="props.column.field == 'color'">
            <span>
              <!--<verte :value="props.formattedRow[props.column.field]"></verte>-->
              <div :style="{background: props.formattedRow[props.column.field]}" class="colorPicker"></div>
            </span>
          </span>
            <span v-else>
            {{ props.formattedRow[props.column.field] }}
          </span>
          </template>
        </vue-good-table>
      </div>
    </b-form-group>
  </b-overlay>
</template>

<script>

const d3 = require('d3');

export default {
  name: "idSelector",

  props: {
    colorSet: {
      type: Array,
      default: () => ["red"]
    }
  },

  data() {
    return {
      carIds: [{
        type: "Loading",
        children: [{
          value: 0,
          name: "Loading",
          title: "Loading",
          color: "red"
        }]
      }],


      loading: true,
      fields: [
        {
          label: 'Nome',
          field: 'name'
        },
        {
          label: 'Mansione',
          field: 'title'
        },
        {
          label: '',
          field: 'color',
          sortable: false,
          globalSearchDisabled: true,
        }
      ]
    }
  },

  mounted() {
    d3.csv("/nomi.csv").then(data => {
      this.carIds = [];

      let c = 0;
      let map = {};

      data.forEach((d) => {
        let id = parseInt(d.id);
        let name = d.LastName + " " + d.FirstName;
        let title = d.CurrentEmploymentTitle;
        let type = d.CurrentEmploymentType;

        if (title == "") title = "Sconosciuto"
        if (type == "") type = "Nessuna auto assegnata"
        if (d.LastName == "") {
          name = "Sconosciuto"
          title = ""
          type = "Auto noleggiate a sconosciuti"
        }

        let prop = {
          value: id,
          name: name,
          title: title,
          color: this.colorSet[id % this.colorSet.length]
        }

        if (map[type] != undefined) {
          this.carIds[map[type]].children.push(prop)
        } else {
          map[type] = c++;
          let list = [prop]
          this.carIds[map[type]] = {name: type}
          this.carIds[map[type]].children = list
        }
      })

      this.loading = false;
    });
  },

  watch: {},

  methods: {
    onRowSelected(items) {
      let selected = items.selectedRows.map(d => d.value).filter(d => d != null)

      this.$emit('changeCars', selected);
    }
  },
}
</script>

<style scoped>
.table{
  margin-top: 17px;
  max-height: 463px;
  overflow-x: auto;
}
.colorPicker {
  width: 25px;
  height: 25px;
  border-radius: 100%;
  margin: auto;
}
</style>