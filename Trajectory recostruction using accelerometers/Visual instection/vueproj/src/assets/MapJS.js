const d3 = require('d3');

export default function MapJS() {
    let projection = d3.geoEquirectangular();
    let scale = 480000;
    let center = [24.8673, 36.070512];
    let featureClass = "id";
    let colorClass = "color";
    let width = 730
    let height = 500

    function me(selection) {


        projection = d3.geoEquirectangular()
            .scale(scale)
            .center(center)
            .translate([width / 2, height / 2]);

        let path = d3.geoPath().projection(projection);

        const paths = selection.selectAll('path')
            .data(selection.datum().features);

        paths.exit().remove();

        paths.enter()
            .append('path');

        selection.selectAll('path')
            .attr('class', (d) => {
                if (d.properties[featureClass])
                    return "_" + d.properties[featureClass]
                return 'none';
            })
            .attr('stroke', (d) => {
                if (d.properties[colorClass])
                    return d.properties[colorClass]
                return 'none';
            })
            .attr('d', path);
    }

    me.projection = function (_) {
        if (!arguments.length) return projection;
        projection = _;

        return me;
    };

    me.scale = function (_) {
        if (!arguments.length) return scale;
        scale = _;
        projection.scale(scale);

        return me;
    };

    me.center = function (_) {
        if (!arguments.length) return center;
        center = _;
        projection.center(center);

        return me;
    };

    me.height = function (_) {
        if (!arguments.length) return height;
        height = _;

        return me;
    };

    me.width = function (_) {
        if (!arguments.length) return width;
        width = _;

        return me;
    };


    me.featureClass = function (_) {
        if (!arguments.length) return featureClass;
        featureClass = _;

        return me;
    };


    me.colorClass = function (_) {
        if (!arguments.length) return colorClass;
        colorClass = _;

        return me;
    };


    return me;
}