
dataForAnalysis = {};

function makeVolumeChart(id, labels, series) {

  var data = {
    labels: labels,
    series: [series]
  };

  var options = {
    fullWidth: true,
    axisX: {showLabel: false,},
    axisY: {showLabel: false,},
    chartPadding: { left: -35 },
    showArea: true
  };

  var chart = new Chartist.Line(id, data, options);

  chart.on('draw', function(data) {
    if (data.type === 'point') {
      var circle = new Chartist.Svg('circle', {
        cx: [data.x],
        cy: [data.y],
        r: [0],
      }, 'ct-circle');
      data.element.replace(circle);
    }})
}

function makeSentimentChart(id, labels, series) {
  var chart = new Chartist.Line(id, {
    labels: labels,
    series: [series]
  }, {
    showArea: true,
    fullWidth: true,
    chartPadding: {
      left: -20,
      bottom: -20,
    },
    width: '100%',
    axisY: {
      showLabel: false,
    },
    axisX: {showLabel: false,},
    plugins: [
      Chartist.plugins.ctThreshold({
        threshold: .5
      })
      ]
  });
}

function makeNarrativesChart(id, labels, series) {

  new Chartist.Line(id, {
    labels: labels,
    series: series
  }, {
    showPoint: false,
    fullWidth: true,
    axisX: {
      showLabel: false,
      showGrid: false
    },
    axisY: {
      showLabel: false,
      showGrid: false
    },
    chartPadding: {
      left: -20,
      bottom: -20
    },
  });
}

function makeNarrativesTableLabel(headerData, percentageData) {

  const headerRow = document.getElementById('header-row');
  headerRow.innerHTML = '';

  for (let i = 0; i < headerData.length; i++) {

    const cell = document.createElement('div');
    cell.className = 'cell';
    cell.id = "cell" + (i+1).toString();
    cell.innerHTML = "<H3>"+ percentageData[i] +"%</H3>" + "<H5>" + headerData[i] + "</H5>";
    headerRow.appendChild(cell);
  }
}

var id = Math.random().toString(36).slice(2, 7)

fetch("https://www.infegy.com/hubfs/Insight%20Briefs/RankingNarratives/siteData.json?randomID=" + id).then(response => {return response.json();}).then(data => {

  dataForAnalysis = data;
  makeVolumeChart(".tiktok-chart1", data['tiktok']['volume']['1 day ago']['dates'], data['tiktok']['volume']['1 day ago']['data']);
  makeSentimentChart(".tiktok-chart3", data['tiktok']['sentiment']['1 day ago']['dates'], data['tiktok']['sentiment']['1 day ago']['data']);

  makeVolumeChart(".twitter-chart1", data['twitter']['volume']['1 day ago']['dates'], data['twitter']['volume']['1 day ago']['data']);
  makeSentimentChart(".twitter-chart3", data['twitter']['sentiment']['1 day ago']['dates'], data['twitter']['sentiment']['1 day ago']['data']);

  makeVolumeChart(".instagram-chart1", data['instagram']['volume']['1 day ago']['dates'], data['instagram']['volume']['1 day ago']['data']);
  makeSentimentChart(".instagram-chart3", data['instagram']['sentiment']['1 day ago']['dates'], data['instagram']['sentiment']['1 day ago']['data']);

  makeNarrativesChart(".narrativesChart", data['tiktok']['entities']['1 day ago']['entities'], data['tiktok']['entities']['1 day ago']['timelines']);
  makeNarrativesTableLabel(data['tiktok']['entities']['1 day ago']['entities'], data['tiktok']['entities']['1 day ago']['growth']);

})
.catch(function(error) {
  console.log(error);
});

const platformButtons = document.querySelectorAll('.platform-button');
const timeframeButtons = document.querySelectorAll('.timeframe-button');

function deselectAllButtons(buttons) {
  buttons.forEach(button => {
    button.classList.remove('selected');
  });
}

function findSelectedButtons(buttons) {

  var buttonID;

  for (let i = 0; i < buttons.length; i++) {

    if (buttons[i].classList.contains('selected')) {
      buttonID = buttons[i].id;
    }

  }

  return buttonID;
}


function handlePlatformButtonClick(event) {

  var dataSource;
  var timeFrame;

  var button = findSelectedButtons(timeframeButtons);

  if (button == "48h-button") {
    timeFrame = '1 day ago';
  }

  if (button == "7d-button") {
    timeFrame = '1 week ago';
  }

  if (button == "30d-button") {
    timeFrame = '1 month ago';
  }

  deselectAllButtons(platformButtons);
  event.target.classList.add('selected');

  if (event.target.id == "twitter-button") {
    dataSource = 'twitter';
  }

  if (event.target.id == "instagram-button") {
    dataSource = 'instagram';    
  }

  if (event.target.id == "tiktok-button") {
    dataSource = "tiktok";
  }

  makeNarrativesChart(".narrativesChart", dataForAnalysis[dataSource]['entities'][timeFrame]['entities'], dataForAnalysis[dataSource]['entities'][timeFrame]['timelines']);
  makeNarrativesTableLabel(dataForAnalysis[dataSource]['entities'][timeFrame]['entities'], dataForAnalysis[dataSource]['entities'][timeFrame]['growth']);

}

function handleTimeframeButtonClick(event) {

  var dataSource;
  var timeFrame;

  var button = findSelectedButtons(platformButtons);

  if (button == "twitter-button") {
    dataSource = 'twitter';
  }

  if (button == "instagram-button") {
    dataSource = 'instagram';
  }

  if (button == "tiktok-button") {
    dataSource = 'tiktok';
  }

  deselectAllButtons(timeframeButtons);
  event.target.classList.add('selected');

  if (event.target.id == "48h-button") {
    timeFrame = '1 day ago';
  }

  if (event.target.id == "7d-button") {
    timeFrame = '1 week ago';    
  }

  if (event.target.id == "30d-button") {
    timeFrame = "1 month ago";
  }

  makeVolumeChart(".tiktok-chart1", dataForAnalysis['tiktok']['volume'][timeFrame]['dates'], dataForAnalysis['tiktok']['volume'][timeFrame]['data']);
  makeSentimentChart(".tiktok-chart3", dataForAnalysis['tiktok']['sentiment'][timeFrame]['dates'], dataForAnalysis['tiktok']['sentiment'][timeFrame]['data']);

  makeVolumeChart(".twitter-chart1", dataForAnalysis['twitter']['volume'][timeFrame]['dates'], dataForAnalysis['twitter']['volume'][timeFrame]['data']);
  makeSentimentChart(".twitter-chart3", dataForAnalysis['twitter']['sentiment'][timeFrame]['dates'], dataForAnalysis['twitter']['sentiment'][timeFrame]['data']);

  makeVolumeChart(".instagram-chart1", dataForAnalysis['instagram']['volume'][timeFrame]['dates'], dataForAnalysis['instagram']['volume'][timeFrame]['data']);
  makeSentimentChart(".instagram-chart3", dataForAnalysis['instagram']['sentiment'][timeFrame]['dates'], dataForAnalysis['instagram']['sentiment'][timeFrame]['data']);

  makeNarrativesChart(".narrativesChart", dataForAnalysis[dataSource]['entities'][timeFrame]['entities'], dataForAnalysis[dataSource]['entities'][timeFrame]['timelines']);
  makeNarrativesTableLabel(dataForAnalysis[dataSource]['entities'][timeFrame]['entities'], dataForAnalysis[dataSource]['entities'][timeFrame]['growth']);

}

platformButtons.forEach(button => {
  button.addEventListener('click', handlePlatformButtonClick);
});

timeframeButtons.forEach(button => {
  button.addEventListener('click', handleTimeframeButtonClick);
});

document.getElementById("tiktok-button").classList.add('selected');
document.getElementById("48h-button").classList.add('selected');


