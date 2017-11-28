/* Generate lists of researchers and projects from the data. */

$(document).ready(function () {

  //drawMap();

  queue()
    //.defer(d3.json, "processed_data/media_by_city.json")
    //.defer(d3.json, "processed_data/code_to_city.json")
    .defer(d3.json, "data/media_by_city.json")
    .defer(d3.json, "data/code_to_city.json")
    .await(formatData);


});

function formatData(error, tweetCounts, codeToCity) {

  if (error) throw error;

  console.log(codeToCity)

  for (let key of Object.keys(tweetCounts)) {

    // console.log(key)

    console.log(codeToCity[key])

    if(codeToCity[key] === "beijing" || codeToCity[key] === "shanghai") {
      console.log(codeToCity[key])
    } 

  }


}


function drawMap() {

  var margin = {top: 0, right: 0, bottom: 0, left: 0},
      width = 960 - margin.left - margin.right,
      height = 800 - margin.top - margin.bottom;

  var svg = d3.select(".map")
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .append('g')
      .attr('class', 'map');

  var path = d3.geoPath();

  d3.json("all_city_china.json", function(error, china) {
    if (error) throw error;

    var proj = d3.geoMercator().center([105, 38]).scale(750).translate([width/2, height/2]);
    var path = d3.geoPath().projection(proj);

    svg.append("g")
      .attr("transform","translate(0,0)")
      .attr("class", "counties")
      .selectAll("path")
      .data(china.features)
      .enter()
      .append("path")
      .style("fill","#ddd")
      .style("stroke","white")
      .attr("d", path)


  });

}