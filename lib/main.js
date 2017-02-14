var d3 = require('d3');

//load graphs
(function () {
  //intended size of svgs in px
  const svgDim = {width:960, height:500};

  //request the data
  d3.csv(
    "api/standard"
    , function(row) {
      //each cell is in string format, so convert to numbers. Javascript converts numbers which are too high or too low to infinity. Discard those rows because D3 can't plot them.
      var formattedRow = {};
      var columns = ["m","n","u","r"];
      for (var i = 0; i <= columns.length-1; i++)
      {
        var column = columns[i];
        var formattedValue = +row[column];

        //if the value can't be plotted...
        if (!Number.isSafeInteger(formattedValue))
        {
          //...discard this row
          return undefined;
        }

        //the value is valid, so add it to the row
        formattedRow[column] = formattedValue;
      }

      //all values in this row are valid numbers.
      return formattedRow;
    }
    , function(error, data) {
      if (error) throw error;

      //in order to reduce the number of dimensions 
      var categorizedData = d3.nest()
        .key(function (d) {return d.n})
        .key(function (d) {return d.u})
        .entries(data)
      ;

      var svg = d3.select(document.createElementNS(d3.namespaces.svg, 'svg'))
          .attr('width', svgDim.width)
          .attr('height', svgDim.height)
        ;
      //!!!:temporarily attach to document to see it while we work on creating a graph
      
      document.getElementById("chart").appendChild(svg.node());

      var margin = {top: 20, right: 20, bottom: 50, left: 75};
      var width = +svg.attr("width") - margin.left - margin.right;
      var height = +svg.attr("height") - margin.top - margin.bottom;
      var g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      var xScale = d3.scaleLinear()
        .rangeRound([0, width])
      ;
      
      var yScale = d3.scaleLinear()
        .rangeRound([height, 0])
      ;
      
      var colorScale = d3.scaleSequential(d3.interpolateRainbow)
      ;

      var line = d3.line()
        .x(function(d) { return xScale(d.m); })
        .y(function(d) { return yScale(d.r); })
      ;

      var xAxis = g.append("g")
        .attr("transform", "translate(0," + height + ")");
      xAxis
        .append("text")
        .attr("fill", "#000")
        .attr("x", width/2)
        .attr("y", 25)
        .attr("dy", "0.71em")
        .attr("text-anchor", "end")
        .text("M")
        .attr("style","font-size:16px")
      ;
      var yAxis = g.append("g");
      yAxis
        .append("text")
        .attr("fill", "#000")
        .attr("y", height/2)
        .attr("x", -40)
        .attr("dy", "0.71em")
        .attr("text-anchor", "end")
        .text("R")
        .attr("style","font-size:16px")
      ;

      //indicate which n slice this is. Position is arbitrary
      var nTitle = g.append("text")
        .attr("x", width/2)
        .attr("dx", "-2em")
        .attr("y", 40)
        .attr("style", ""
          +"font-family:monospace;"
          +"font-size:50px;"
          +"fill:#BBBBBB;"
        )
      ;

      var lineGroup = g.append("g");

      //prepare the legend
      var legendGroup = g.append("g");
      legendGroup
        .attr("transform", "translate(40, 15)")
      ;
      legendGroup.append("text")
        .text("U")
        .attr("style", "text-decoration:underline")
        .attr("x", 8)
        .attr("dy","0.7em")
      ;

      function update (nCategory) {
        //update scale
        //!!!: currently draws new axes each time. does not remove. refactor
        var concatenatedUData = data.filter(function (v) {
            return v.n === parseInt(nCategory.key, 10)
        });

        xScale.domain(
            d3.extent(
              concatenatedUData
              , function (d) {return d.m}
            )
          )
        ;
        
        yScale.domain(
            d3.extent(
              concatenatedUData
              , function (d) {return d.r}
            )
          )
        ;
        
        //extend the domain to prevent the appearance of the top and bottom values being identical. The buffer is arbitrarily chosen to be 15%
        var uExtent = d3.extent(
          concatenatedUData
          , function (d) {return d.u}
        );
        uExtent[1] = uExtent[1]+0.15*(uExtent[1]-uExtent[0])
        colorScale.domain(uExtent);

        //draw x axis
        xAxis.call(d3.axisBottom(xScale));

        //draw y axis
        yAxis.call(d3.axisLeft(yScale));

        nTitle.text("n = "+nCategory.key)

        var legendBulletSelection = legendGroup.selectAll("g")
          .data(nCategory.values, function (uCategory) {
            return uCategory.key
          })
          .enter()
          .append("g")
          .attr("transform", function (d, i) {return "translate(0,"+(20+i*15)+")";})
        ;
        legendBulletSelection
          .append("rect")
          .attr("width", 12)
          .attr("height", 12)
          .attr("fill", function (d) {return colorScale(d.key)})
        ;
        legendBulletSelection
          .append("text")
          .attr("x", 16)
          .attr("y", 0)
          .attr("dy", "0.8em")
          .text(function (d) {return d.key})
        ;
        
        var pathSelection = lineGroup.selectAll("path").data(
          nCategory.values
        , function (uCategory) {
            return uCategory.key
          }
        );

        pathSelection.exit().remove();

        pathSelection.transition()
          .attr("d", function(uCategory) {return line(uCategory.values)})
        ;

        pathSelection.enter()
          .append("path")
          .attr("fill", "none")
          .attr("stroke", function (uCategory) {return colorScale(+uCategory.key)})
          .attr("stroke-linejoin", "round")
          .attr("stroke-linecap", "round")
          .attr("stroke-width", 2)
          .attr("d", function (uCategory) {return line(uCategory.values)})
        ;
      }

      var nCategoryIndex = 0;
      enforceNCategoryIndex();
      function enforceNCategoryIndex () {
        var nCategory = categorizedData[nCategoryIndex];
        
        update(nCategory);
      }

      document.documentElement.addEventListener(
        "click", 
        function(event) {
          nCategoryIndex = (nCategoryIndex+1)%categorizedData.length;
          enforceNCategoryIndex();
        },
        false
      );
    }
  );

  

})();