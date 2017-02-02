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
        var svg = d3.select("body").append('svg')
          .attr('width', svgDim.width)
          .attr('height', svgDim.height)
        ;

        var margin = {top: 20, right: 20, bottom: 30, left: 50};
        var width = +svg.attr("width") - margin.left - margin.right;
        var height = +svg.attr("height") - margin.top - margin.bottom;
        var g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        //develop three scales to map the incoming values onto values which can be displayed.
        var concatenatedUData = data.filter(function (v) {return v.n === parseInt(nCategory.key, 10)});
        
        var xScale = d3.scaleLinear()
          .rangeRound([0, width])
          .domain(
            d3.extent(
              concatenatedUData
              , function (d) {return d.m}
            )
          )
        ;
        
        var yScale = d3.scaleLinear()
          .rangeRound([height, 0])
          .domain(
            d3.extent(
              concatenatedUData
              , function (d) {return d.r}
            )
          )
        ;
        
        var colorScale = d3.scaleSequential(d3.interpolateRainbow)
          .domain(
            d3.extent(
              concatenatedUData
              , function (d) {return d.u}
            )
          )
        ;

        
        
        g.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(xScale))
        ;

        g.append("g")
          .call(d3.axisLeft(yScale))
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
            .x(function(d) { return xScale(d.m); })
            .y(function(d) { return yScale(d.r); })
          ;
          
          var colorString = colorScale(+uCategory.key);
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

      //when buttons are clicked, cycle through graphs
      //!!!: this only works if we assume that there are no other SVG elements in the document. The correct way to do this is to have the SVG generator enter the SVG elements into an array rather than attach them to the body, and then pass that array. But I can't figure out how to create detached D3 elements right now, so this will work in the meantime.
      var $svgs = $("svg");
      var slideshow = (function (elements) {
        function enforceTargetIndexVisibility () {
          $ul.children()
            .hide()
            .eq(targetIndex).show()
          ;
        }

        //the list containing all the elements to be shown
        var $ul = $("<ul>");
        for (element of elements)
        {
          $ul.append(element);
        }
        var targetIndex = 0;
        enforceTargetIndexVisibility();

        

        var $dOMElement = $("<div>")
          .append($ul);
        
        
        $dOMElement.on("click", function (event) {
          targetIndex = (targetIndex+1)%elements.length;
          enforceTargetIndexVisibility();

          event.preventDefault();
        })

        //return the DOM Element itself rather than the jquery object in case we stop using jquery in the future
        return $dOMElement.get(0)
      })($svgs.toArray());

      $("body").append(slideshow)
    }
  );
})();