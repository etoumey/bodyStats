var svg = d3.select("body").append("svg")
      .attr("width", 960)
      .attr("height", 300)

var margin = {left:30, right:30, top: 10, bottom: 20}
var width = svg.attr("width") - margin.left - margin.right;
var height = svg.attr("height") - margin.bottom - margin.top;
    
   
var data = [
		   {"date":"2019-06-01", "RHR": 50},
		   {"date":"2019-06-02", "RHR": 51},
           {"date":"2019-06-03", "RHR": 49},
           {"date":"2019-06-04", "RHR": 58},
           {"date":"2019-06-05", "RHR": 57},
           {"date":"2019-06-06", "RHR": 55},
	       {"date":"2019-06-07", "RHR": 48},
           {"date":"2019-06-08", "RHR": 48},
           {"date":"2019-06-09", "RHR": 50},
   					
		   ]

var x = d3.scaleTime()
	.rangeRound([0, width]);
var x_axis = d3.axisBottom(x);

var y = d3.scaleLinear()
	.rangeRound([height, 0]);
var y_axis = d3.axisBottom(y);
var xFormat = "%m-%d-%Y";;
var parseTime = d3.timeParse("%Y-%m-%d");

x.domain(d3.extent(data, function(d) { return parseTime(d.date); }));
	y.domain([d3.min(data, function(d) {return 0.9*d3.min([d.RHR])}), 
          d3.max(data, function(d) { 
            return 1.1*d3.max([d.RHR, d.b, d.c, d.d]);
          })]);

//var RHR = function(d) {return d.RHR};

var multiline = function(category) {
  var line = d3.line()
              .x(function(d) { return x(parseTime(d.date)); })
              .y(function(d) { return y(d[category]); });
 return line;
}



var categories = ['RHR'];
var color = d3.scaleOrdinal(d3.schemeCategory10);

var g = svg.append("g")
    .attr("transform",
      "translate(" + margin.left + "," + margin.top + ")");

var lineFunction = multiline(categories);
  g.append("path")
    .datum(data) 
    .attr("class", "line")
    .style("stroke", color)
    .attr("d", lineFunction);

  // Add the X Axis
	  g.append("g")
  .attr("transform", "translate(0," + height + ")")
  .call(d3.axisBottom(x).tickFormat(d3.timeFormat(xFormat)));

  // Add the Y Axis
		g.append("g")
  .call(d3.axisLeft(y));
