function buildMetadata(sample) {

  // @TODO: Complete the following function that builds the metadata panel

  // Use `d3.json` to fetch the metadata for a sample
  d3.json("/metadata/"+sample).then(function(data){
    // Use d3 to select the panel with id of `#sample-metadata`
    // Use `.html("") to clear any existing metadata
    d3.select("#sample-metadata").html("")
    // Use `Object.entries` to add each key and value pair to the panel
    // Hint: Inside the loop, you will need to use d3 to append new
    // tags for each key-value in the metadata.
    Object.entries(data).forEach(([key, value]) => {
      var cell = d3.select("#sample-metadata").append("p");
      cell.text(key + ": " +value);
    });
    // this will return each row of grape, need to groupby grape
   
  }


  )
    
}

function buildCharts(sample) {

  // @TODO: Use `d3.json` to fetch the sample data for the plots
  d3.json("/samples/"+sample).then(function(sampleInput){
    // parse points to be integer
    sampleInput.forEach(function(data) {
      data.points = +data.points;
    });

    var pointsArr = [];
    var countryArr = [];
    var provinceArr = [];
    var priceArr =[];

    for (i = 0; i < 100; i++){
      if(typeof sampleInput[i] !== "undefined"){
        pointsArr.push(sampleInput[i].points)
        // console.log(sampleInput[i].points)
        countryArr.push(sampleInput[i].country)
        // console.log(sampleInput[i].country)
        provinceArr.push(sampleInput[i].province)
        // console.log(sampleInput[i].province)
        priceArr.push(sampleInput[i].price)
        // console.log(sampleInput[i].price)
      }


    };
    // console.log(pointsArr);
    // console.log(countryArr);
    // console.log(provinceArr);
    // console.log(priceArr);

    // @TODO: Build a Bubble Chart using the sample data
    var trace1 = {
      x: pointsArr,
      y: priceArr,
      mode: 'markers',
      marker: {
        size: priceArr,
        color: countryArr
      },
      text:provinceArr
    };
    
    var dataBubble = [trace1];
    
    var layoutBubble = {
      title: {
        text:'Price vs. Points'
      },
      xaxis: {
        title: {
          text: 'Points (Out of 100)'
        },
      },
      yaxis: {
        title: {
          text: 'Price in USD'
        },
      },
    };
    
    Plotly.newPlot('bubble', dataBubble,layoutBubble);
    // @TODO: Build a Pie Chart
    
      
    var data = [{
      values: pointsArr,
      labels: countryArr,
      hoverinfo:provinceArr,
      type: 'pie'
    }];
    
    var layout = {
      title: {
        text:'% of Country'
      },
    };
    
    Plotly.newPlot('pie', data,layout);

  }
  )
}





function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/variety").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[1];
    buildCharts(firstSample);
    buildMetadata(firstSample);
    // include buildWordCloud
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();




