//load graphs
(function () {
  //intended size of svgs in px
  const svgDim = {width:960, height:500};

  //request the data
  d3.csv(
    "api/standard"
    , function(row) {
      //each cell is in string format, so convert to numbers
      return {
        m: +row.m,
        n: +row.n,
        u: +row.u,
        r: +row.r
      }
    }
    , function(error, data) {
      if (error) throw error;

      //in order to reduce the number of dimensions 
      var categorizedData = d3.nest()
        .key(function (d) {return d.n})
        .key(function (d) {return d.u})
        .entries(data)
      ;

      for (let nCategory of categorizedData)
      {
        $("body").append("<p>n = "+nCategory.key+"</p>");
        var svg = d3.select("body").append('svg')
          .attr('width', svgDim.width)
          .attr('height', svgDim.height)
        ;

        var margin = {top: 20, right: 20, bottom: 30, left: 50};
        var width = +svg.attr("width") - margin.left - margin.right;
        var height = +svg.attr("height") - margin.top - margin.bottom;
        var g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var x = d3.scaleLinear()
          .rangeRound([0, width])
        ;
        var y = d3.scaleLinear()
          .rangeRound([height, 0])
        ;
        var u = d3.scaleSequential(d3.interpolateRainbow);

        var concatenatedUData = data.filter(function (v) {return v.n === parseInt(nCategory.key, 10)});

        x.domain(
          [0, d3.max(
            concatenatedUData
            , function (d) {return d.m}
          )]
        );
        y.domain(
          [0, d3.max(
            concatenatedUData
            , function (d) {return d.r}
          )]
        );
        u.domain(
          d3.extent(
            concatenatedUData
            , function (d) {return d.u}
          )
        );
        
        g.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x))
        ;

        g.append("g")
          .call(d3.axisLeft(y))
          .append("text")
          .attr("fill", "#000")
          .attr("transform", "rotate(-90)")
          .attr("y", 6)
          .attr("dy", "0.71em")
          .attr("text-anchor", "end")
          .text("m")
        ;

        for (let uCategory of nCategory.values)
        {
          
          var line = d3.line()
            .x(function(d) { return x(d.m); })
            .y(function(d) { return y(d.r); })
          ;
          
          var colorString = u(+uCategory.key);
          g.append("path")
            .datum(uCategory.values)
            .attr("fill", "none")
            .attr("stroke", colorString)
            .attr("stroke-linejoin", "round")
            .attr("stroke-linecap", "round")
            .attr("stroke-width", 2)
            .attr("d", line)
          ;
        }
      }
    }
  );
})();

//when buttons are clicked, cycle through graphs
//