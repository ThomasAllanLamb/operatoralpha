$(document).ready(function () {
  var svg = d3.select("svg");
  var margin = {top: 20, right: 20, bottom: 30, left: 50};
  var width = +svg.attr("width") - margin.left - margin.right;
  var height = +svg.attr("height") - margin.top - margin.bottom;
  var g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var parseTime = d3.timeParse("%d-%b-%y");

  var x = d3.scaleLinear()
      .rangeRound([0, width]);

  var y = d3.scaleLinear()
      .rangeRound([height, 0]);

  var line = d3.line()
      .x(function(d) { return x(d.u); })
      .y(function(d) { return y(d.r); });

  d3.csv(
    "standard.csv"
    , function(d) {
      //do not modify rows
      return d;
    }
    , function(error, data) {
      if (error) throw error;

      x.domain(d3.extent(data, function(d) { return d.u; }));
      y.domain(d3.extent(data, function(d) { return d.r; }));

      g.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x))
        .select(".domain")
          .remove();

      g.append("g")
          .call(d3.axisLeft(y))
        .append("text")
          .attr("fill", "#000")
          .attr("transform", "rotate(-90)")
          .attr("y", 6)
          .attr("dy", "0.71em")
          .attr("text-anchor", "end")
          .text("m");

      debugger;
      g.append("path")
          .datum(data)
          .attr("fill", "none")
          .attr("stroke", "steelblue")
          .attr("stroke-linejoin", "round")
          .attr("stroke-linecap", "round")
          .attr("stroke-width", 1.5)
          .attr("d", line);
    }
  );
});