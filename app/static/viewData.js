async function getAPIData(filters) {
  const response = await fetch("/vdata/vweek?" + new URLSearchParams(filters));
  const data = await response.json();
  return data;
}

async function getScrapeData(filters) {
  const response = await fetch("/sdata?" + new URLSearchParams(filters));
  const data = await response.json();
  return data;
}
const interval = document.querySelector('#interval');

let extracted_scrape_data = {
  dates: [],
  first_dose: [],
  second_dose: [],
  locations: [],
  manufacturers: [],
};

let extrated_data = {
  dates: [],
  locations: [],
  janssenData: [],
  modernaData: [],
  pfizerData: [],
  janssen_5plus: [],
  moderna_5plus: [],
  pfizer_5plus: [],
  janssen_12plus: [],
  moderna_12plus: [],
  pfizer_12plus: [],
  janssen_18plus: [],
  moderna_18plus: [],
  pfizer_18plus: [],
  janssen_65plus: [],
  moderna_65plus: [],
  pfizer_65plus: [],
  avgsecjan: [],
  avgsecmod: [],
  avgsecpfi: [],
};

getAPIData({aggregation: interval.value}).then((data) => {
  apiData = data.entries;

  for (let i = 0; i < apiData.length; i++) {
    extrated_data.dates.push(apiData[i].date);
    extrated_data.locations.push(apiData[i].location);
    extrated_data.janssenData.push(apiData[i].avgdistjan);
    extrated_data.modernaData.push(apiData[i].avgdistmod);
    extrated_data.pfizerData.push(apiData[i].avgdistpfi);
    extrated_data.janssen_5plus.push(apiData[i].avgcomjan5);
    extrated_data.moderna_5plus.push(apiData[i].avgcommod5);
    extrated_data.pfizer_5plus.push(apiData[i].avgcompfi5);
    extrated_data.janssen_12plus.push(apiData[i].avgcomjan12);
    extrated_data.moderna_12plus.push(apiData[i].avgcommod12);
    extrated_data.pfizer_12plus.push(apiData[i].avgcompfi12);
    extrated_data.janssen_18plus.push(apiData[i].avgcomjan18);
    extrated_data.moderna_18plus.push(apiData[i].avgcommod18);
    extrated_data.pfizer_18plus.push(apiData[i].avgcompfi18);
    extrated_data.janssen_65plus.push(apiData[i].avgcomjan65);
    extrated_data.moderna_65plus.push(apiData[i].avgcommod65);
    extrated_data.pfizer_65plus.push(apiData[i].avgcompfi65);
    extrated_data.avgsecjan.push(apiData[i].avgsecjan);
    extrated_data.avgsecmod.push(apiData[i].avgsecmod);
    extrated_data.avgsecpfi.push(apiData[i].avgsecpfi);
  }

  console.log(extrated_data);

  // Create a Chart.js chart

  const chart5Data = {
    labels: extrated_data.dates,
    datasets: [
      {
        label: "Janssen",
        data: extrated_data.janssenData,
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Moderna",
        data: extrated_data.modernaData,
        borderColor: "rgba(255, 99, 132, 1)",
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        pointRadius: 0,
        borderWidth: 2,
        fill: true,
      },
      {
        label: "Pfizer",
        data: extrated_data.pfizerData,
        borderColor: "rgba(255, 206, 86, 1)",
        backgroundColor: "rgba(255, 206, 86, 0.2)",
        pointRadius: 0,
        borderWidth: 2,
        fill: true,
      },
    ],
  };

  const vaxctx = document.getElementById("vaccineChart").getContext("2d");
  const vaxChart = new Chart(vaxctx, {
    type: "line",
    data: chart5Data,
    options: {
      scales: {
        xAxes: [
          {
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 15,
              labelString: "Date",
            },
          },
        ],
        yAxes: [
          {
            beginAtZero: true,
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 14,
              labelString: "# of Doses Distributed",
            },
          },
        ],
      },
    },
  });

  // Received Booster
  const chartBoostData = {
    labels: extrated_data.dates,
    datasets: [
      {
        label: "Janssen",
        data: extrated_data.avgsecjan,
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Moderna",
        data: extrated_data.avgsecmod,
        borderColor: "rgba(255, 99, 132, 1)",
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Pfizer",
        data: extrated_data.avgsecpfi,
        borderColor: "rgba(255, 206, 86, 1)",
        backgroundColor: "rgba(255, 206, 86, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
    ],
  };

  // Create a Chart.js chart
  const boostctx = document.getElementById("boostChart").getContext("2d");
  const boostChart = new Chart(boostctx, {
    type: "line",
    data: chartBoostData,
    options: {
      scales: {
        xAxes: [
          {
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 15,
              labelString: "Date",
            },
          },
        ],
        yAxes: [
          {
            beginAtZero: true,
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 14,
              labelString: "# of Doses Administered",
            },
          },
        ],
      },
    },
  });

  // 5+ by manufacturer
  const boostData = {
    labels: extrated_data.dates,
    datasets: [
      {
        label: "Janssen (5+)",
        data: extrated_data.janssen_5plus,
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Moderna (5+)",
        data: extrated_data.moderna_5plus,
        borderColor: "rgba(255, 99, 132, 1)",
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Pfizer (5+)",
        data: extrated_data.pfizer_5plus,
        borderColor: "rgba(255, 206, 86, 1)",
        backgroundColor: "rgba(255, 206, 86, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
    ],
  };

  // Create a Chart.js chart
  const age5ctx = document.getElementById("age5Chart").getContext("2d");
  const age5Chart = new Chart(age5ctx, {
    type: "line",
    data: boostData,
    options: {
      scales: {
        xAxes: [
          {
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 15,
              labelString: "Date",
            },
          },
        ],
        yAxes: [
          {
            beginAtZero: true,
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 14,
              labelString: "# of Doses Administered",
            },
          },
        ],
      },
    },
  });

  // 12+ by manufacturer
  const chart12Data = {
    labels: extrated_data.dates,
    datasets: [
      {
        label: "Janssen (12+)",
        data: extrated_data.janssen_12plus,
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Moderna (12+)",
        data: extrated_data.moderna_12plus,
        borderColor: "rgba(255, 99, 132, 1)",
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Pfizer (12+)",
        data: extrated_data.pfizer_12plus,
        borderColor: "rgba(255, 206, 86, 1)",
        backgroundColor: "rgba(255, 206, 86, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
    ],
  };

  // Create a Chart.js chart
  const age12ctx = document.getElementById("age12Chart").getContext("2d");
  const age12Chart = new Chart(age12ctx, {
    type: "line",
    data: chart12Data,
    options: {
      scales: {
        xAxes: [
          {
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 15,
              labelString: "Date",
            },
          },
        ],
        yAxes: [
          {
            beginAtZero: true,
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 14,
              labelString: "# of Doses Administered",
            },
          },
        ],
      },
    },
  });

  // 18+ by manufacturer
  const chart18Data = {
    labels: extrated_data.dates,
    datasets: [
      {
        label: "Janssen (18+)",
        data: extrated_data.janssen_18plus,
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Moderna (18+)",
        data: extrated_data.moderna_18plus,
        borderColor: "rgba(255, 99, 132, 1)",
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Pfizer (18+)",
        data: extrated_data.pfizer_18plus,
        borderColor: "rgba(255, 206, 86, 1)",
        backgroundColor: "rgba(255, 206, 86, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
    ],
  };

  // Create a Chart.js chart
  const age18ctx = document.getElementById("age18Chart").getContext("2d");
  const age18Chart = new Chart(age18ctx, {
    type: "line",
    data: chart18Data,
    options: {
      scales: {
        xAxes: [
          {
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 15,
              labelString: "Date",
            },
          },
        ],
        yAxes: [
          {
            beginAtZero: true,
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 14,
              labelString: "# of Doses Administered",
            },
          },
        ],
      },
    },
  });

  // 65+ by manufacturer
  const chart65Data = {
    labels: extrated_data.dates,
    datasets: [
      {
        label: "Janssen (65+)",
        data: extrated_data.janssen_65plus,
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Moderna (65+)",
        data: extrated_data.moderna_65plus,
        borderColor: "rgba(255, 99, 132, 1)",
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Pfizer (65+)",
        data: extrated_data.pfizer_65plus,
        borderColor: "rgba(255, 206, 86, 1)",
        backgroundColor: "rgba(255, 206, 86, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
    ],
  };

  // Create a Chart.js chart
  const age65ctx = document.getElementById("age65Chart").getContext("2d");
  const age65Chart = new Chart(age65ctx, {
    type: "line",
    data: chart65Data,
    options: {
      scales: {
        xAxes: [
          {
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 15,
              labelString: "Date",
            },
          },
        ],
        yAxes: [
          {
            beginAtZero: true,
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 14,
              labelString: "# of Doses Administered",
            },
          },
        ],
      },
    },
  });
});

interval.addEventListener('change', function(){

let extracted_scrape_data = {
  dates: [],
  first_dose: [],
  second_dose: [],
  locations: [],
  manufacturers: [],
};

let extrated_data = {
  dates: [],
  locations: [],
  janssenData: [],
  modernaData: [],
  pfizerData: [],
  janssen_5plus: [],
  moderna_5plus: [],
  pfizer_5plus: [],
  janssen_12plus: [],
  moderna_12plus: [],
  pfizer_12plus: [],
  janssen_18plus: [],
  moderna_18plus: [],
  pfizer_18plus: [],
  janssen_65plus: [],
  moderna_65plus: [],
  pfizer_65plus: [],
  avgsecjan: [],
  avgsecmod: [],
  avgsecpfi: [],
};

getAPIData({aggregation: interval.value}).then((data) => {
  apiData = data.entries;

  for (let i = 0; i < apiData.length; i++) {
    extrated_data.dates.push(apiData[i].date);
    extrated_data.locations.push(apiData[i].location);
    extrated_data.janssenData.push(apiData[i].avgdistjan);
    extrated_data.modernaData.push(apiData[i].avgdistmod);
    extrated_data.pfizerData.push(apiData[i].avgdistpfi);
    extrated_data.janssen_5plus.push(apiData[i].avgcomjan5);
    extrated_data.moderna_5plus.push(apiData[i].avgcommod5);
    extrated_data.pfizer_5plus.push(apiData[i].avgcompfi5);
    extrated_data.janssen_12plus.push(apiData[i].avgcomjan12);
    extrated_data.moderna_12plus.push(apiData[i].avgcommod12);
    extrated_data.pfizer_12plus.push(apiData[i].avgcompfi12);
    extrated_data.janssen_18plus.push(apiData[i].avgcomjan18);
    extrated_data.moderna_18plus.push(apiData[i].avgcommod18);
    extrated_data.pfizer_18plus.push(apiData[i].avgcompfi18);
    extrated_data.janssen_65plus.push(apiData[i].avgcomjan65);
    extrated_data.moderna_65plus.push(apiData[i].avgcommod65);
    extrated_data.pfizer_65plus.push(apiData[i].avgcompfi65);
    extrated_data.avgsecjan.push(apiData[i].avgsecjan);
    extrated_data.avgsecmod.push(apiData[i].avgsecmod);
    extrated_data.avgsecpfi.push(apiData[i].avgsecpfi);
  }

  console.log(extrated_data);

  // Create a Chart.js chart

  const chart5Data = {
    labels: extrated_data.dates,
    datasets: [
      {
        label: "Janssen",
        data: extrated_data.janssenData,
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Moderna",
        data: extrated_data.modernaData,
        borderColor: "rgba(255, 99, 132, 1)",
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        pointRadius: 0,
        borderWidth: 2,
        fill: true,
      },
      {
        label: "Pfizer",
        data: extrated_data.pfizerData,
        borderColor: "rgba(255, 206, 86, 1)",
        backgroundColor: "rgba(255, 206, 86, 0.2)",
        pointRadius: 0,
        borderWidth: 2,
        fill: true,
      },
    ],
  };

  const vaxctx = document.getElementById("vaccineChart").getContext("2d");
  const vaxChart = new Chart(vaxctx, {
    type: "line",
    data: chart5Data,
    options: {
      scales: {
        xAxes: [
          {
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 15,
              labelString: "Date",
            },
          },
        ],
        yAxes: [
          {
            beginAtZero: true,
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 14,
              labelString: "# of Doses Distributed",
            },
          },
        ],
      },
    },
  });

  // Received Booster
  const chartBoostData = {
    labels: extrated_data.dates,
    datasets: [
      {
        label: "Janssen",
        data: extrated_data.avgsecjan,
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Moderna",
        data: extrated_data.avgsecmod,
        borderColor: "rgba(255, 99, 132, 1)",
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Pfizer",
        data: extrated_data.avgsecpfi,
        borderColor: "rgba(255, 206, 86, 1)",
        backgroundColor: "rgba(255, 206, 86, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
    ],
  };

  // Create a Chart.js chart
  const boostctx = document.getElementById("boostChart").getContext("2d");
  const boostChart = new Chart(boostctx, {
    type: "line",
    data: chartBoostData,
    options: {
      scales: {
        xAxes: [
          {
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 15,
              labelString: "Date",
            },
          },
        ],
        yAxes: [
          {
            beginAtZero: true,
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 14,
              labelString: "# of Doses Administered",
            },
          },
        ],
      },
    },
  });

  // 5+ by manufacturer
  const boostData = {
    labels: extrated_data.dates,
    datasets: [
      {
        label: "Janssen (5+)",
        data: extrated_data.janssen_5plus,
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Moderna (5+)",
        data: extrated_data.moderna_5plus,
        borderColor: "rgba(255, 99, 132, 1)",
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Pfizer (5+)",
        data: extrated_data.pfizer_5plus,
        borderColor: "rgba(255, 206, 86, 1)",
        backgroundColor: "rgba(255, 206, 86, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
    ],
  };

  // Create a Chart.js chart
  const age5ctx = document.getElementById("age5Chart").getContext("2d");
  const age5Chart = new Chart(age5ctx, {
    type: "line",
    data: boostData,
    options: {
      scales: {
        xAxes: [
          {
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 15,
              labelString: "Date",
            },
          },
        ],
        yAxes: [
          {
            beginAtZero: true,
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 14,
              labelString: "# of Doses Administered",
            },
          },
        ],
      },
    },
  });

  // 12+ by manufacturer
  const chart12Data = {
    labels: extrated_data.dates,
    datasets: [
      {
        label: "Janssen (12+)",
        data: extrated_data.janssen_12plus,
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Moderna (12+)",
        data: extrated_data.moderna_12plus,
        borderColor: "rgba(255, 99, 132, 1)",
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Pfizer (12+)",
        data: extrated_data.pfizer_12plus,
        borderColor: "rgba(255, 206, 86, 1)",
        backgroundColor: "rgba(255, 206, 86, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
    ],
  };

  // Create a Chart.js chart
  const age12ctx = document.getElementById("age12Chart").getContext("2d");
  const age12Chart = new Chart(age12ctx, {
    type: "line",
    data: chart12Data,
    options: {
      scales: {
        xAxes: [
          {
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 15,
              labelString: "Date",
            },
          },
        ],
        yAxes: [
          {
            beginAtZero: true,
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 14,
              labelString: "# of Doses Administered",
            },
          },
        ],
      },
    },
  });

  // 18+ by manufacturer
  const chart18Data = {
    labels: extrated_data.dates,
    datasets: [
      {
        label: "Janssen (18+)",
        data: extrated_data.janssen_18plus,
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Moderna (18+)",
        data: extrated_data.moderna_18plus,
        borderColor: "rgba(255, 99, 132, 1)",
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Pfizer (18+)",
        data: extrated_data.pfizer_18plus,
        borderColor: "rgba(255, 206, 86, 1)",
        backgroundColor: "rgba(255, 206, 86, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
    ],
  };

  // Create a Chart.js chart
  const age18ctx = document.getElementById("age18Chart").getContext("2d");
  const age18Chart = new Chart(age18ctx, {
    type: "line",
    data: chart18Data,
    options: {
      scales: {
        xAxes: [
          {
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 15,
              labelString: "Date",
            },
          },
        ],
        yAxes: [
          {
            beginAtZero: true,
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 14,
              labelString: "# of Doses Administered",
            },
          },
        ],
      },
    },
  });

  // 65+ by manufacturer
  const chart65Data = {
    labels: extrated_data.dates,
    datasets: [
      {
        label: "Janssen (65+)",
        data: extrated_data.janssen_65plus,
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Moderna (65+)",
        data: extrated_data.moderna_65plus,
        borderColor: "rgba(255, 99, 132, 1)",
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Pfizer (65+)",
        data: extrated_data.pfizer_65plus,
        borderColor: "rgba(255, 206, 86, 1)",
        backgroundColor: "rgba(255, 206, 86, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
    ],
  };

  // Create a Chart.js chart
  const age65ctx = document.getElementById("age65Chart").getContext("2d");
  const age65Chart = new Chart(age65ctx, {
    type: "line",
    data: chart65Data,
    options: {
      scales: {
        xAxes: [
          {
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 15,
              labelString: "Date",
            },
          },
        ],
        yAxes: [
          {
            beginAtZero: true,
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 14,
              labelString: "# of Doses Administered",
            },
          },
        ],
      },
    },
  });
});

});
// Get scrape data

// Get initial data
const stateSelector = document.querySelector("#state");

extracted_scrape_data = {
  dates: [],
  first_dose: [],
  second_dose: [],
  locations: [],
  manufacturers: [],
};

getScrapeData({ location: stateSelector.value }).then((data) => {
  const scrapeData = data.entries;

  for (let i = 0; i < scrapeData.length; i++) {
    extracted_scrape_data.dates.push(scrapeData[i].date);
    extracted_scrape_data.first_dose.push(scrapeData[i].first_dose);
    extracted_scrape_data.second_dose.push(scrapeData[i].second_dose);
    extracted_scrape_data.locations.push(scrapeData[i].location);
    extracted_scrape_data.manufacturers.push(scrapeData[i].manufacturer);
  }

  console.log(extracted_scrape_data);

  let janssenData = {
    first_dose: [],
    dates: [],
  };

  let pfizerData = {
    first_dose: [],
    second_dose: [],
    dates: [],
  };

  let modernaData = {
    first_dose: [],
    second_dose: [],
    dates: [],
  };

  for (let j = 0; j < scrapeData.length; j++) {
    if (extracted_scrape_data.manufacturers[j] == "Pfizer") {
      pfizerData.dates.push(extracted_scrape_data.dates[j]);
      pfizerData.first_dose.push(extracted_scrape_data.first_dose[j]);
      pfizerData.second_dose.push(extracted_scrape_data.second_dose[j]);
    } else if (extracted_scrape_data.manufacturers[j] == "Janssen") {
      janssenData.dates.push(extracted_scrape_data.dates[j]);
      janssenData.first_dose.push(extracted_scrape_data.first_dose[j]);
    } else if (extracted_scrape_data.manufacturers[j] == "Moderna") {
      modernaData.dates.push(extracted_scrape_data.dates[j]);
      modernaData.first_dose.push(extracted_scrape_data.first_dose[j]);
      modernaData.second_dose.push(extracted_scrape_data.second_dose[j]);
    }
  }
  const stateDistData = {
    labels: extracted_scrape_data.dates,
    datasets: [
      {
        label: "Janssen (First Dose)",
        data: janssenData.dates.map((x, index) => ({
          x,
          y: janssenData.first_dose[index],
        })),
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Moderna (First Dose)",
        data: modernaData.dates.map((x, index) => ({
          x,
          y: modernaData.first_dose[index],
        })),
        borderColor: "rgba(255, 99, 132, 1)",
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Moderna (Second Dose)",
        data: modernaData.dates.map((x, index) => ({
          x,
          y: modernaData.second_dose[index],
        })),
        borderColor: "rgba(227, 16, 61, 1)",
        backgroundColor: "rgba(227, 16, 61, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Pfizer (First Dose)",
        data: pfizerData.dates.map((x, index) => ({
          x,
          y: pfizerData.first_dose[index],
        })),
        borderColor: "rgba(255, 206, 86, 1)",
        backgroundColor: "rgba(255, 206, 86, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
      {
        label: "Pfizer (Second Dose)",
        data: pfizerData.dates.map((x, index) => ({
          x,
          y: pfizerData.second_dose[index],
        })),
        borderColor: "rgba(255, 176, 86, 1)",
        backgroundColor: "rgba(255, 176, 86, 0.2)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
      },
    ],
  };

  // Create a Chart.js chart
  const distCtx = document.getElementById("distChart").getContext("2d");
  const stateDistChart = new Chart(distCtx, {
    type: "line",
    data: stateDistData,
    options: {
      scales: {
        xAxes: [
          {
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 15,
              labelString: "Date",
            },
          },
        ],
        yAxes: [
          {
            beginAtZero: true,
            scaleLabel: {
              display: true,
              fontColor: "#e21011",
              fontSize: 14,
              labelString: "# of Doses Distributed",
            },
          },
        ],
      },
    },
  });
});

stateSelector.addEventListener("change", function () {
  extracted_scrape_data = {
    dates: [],
    first_dose: [],
    second_dose: [],
    locations: [],
    manufacturers: [],
  };

  getScrapeData({ location: stateSelector.value }).then((data) => {
    const scrapeData = data.entries;

    for (let i = 0; i < scrapeData.length; i++) {
      extracted_scrape_data.dates.push(scrapeData[i].date);
      extracted_scrape_data.first_dose.push(scrapeData[i].first_dose);
      extracted_scrape_data.second_dose.push(scrapeData[i].second_dose);
      extracted_scrape_data.locations.push(scrapeData[i].location);
      extracted_scrape_data.manufacturers.push(scrapeData[i].manufacturer);
    }

    let janssenData = {
      first_dose: [],
      dates: [],
    };

    let pfizerData = {
      first_dose: [],
      second_dose: [],
      dates: [],
    };

    let modernaData = {
      first_dose: [],
      second_dose: [],
      dates: [],
    };

    for (let j = 0; j < scrapeData.length; j++) {
      if (extracted_scrape_data.manufacturers[j] == "Pfizer") {
        pfizerData.dates.push(extracted_scrape_data.dates[j]);
        pfizerData.first_dose.push(extracted_scrape_data.first_dose[j]);
        pfizerData.second_dose.push(extracted_scrape_data.second_dose[j]);
      } else if (extracted_scrape_data.manufacturers[j] == "Janssen") {
        janssenData.dates.push(extracted_scrape_data.dates[j]);
        janssenData.first_dose.push(extracted_scrape_data.first_dose[j]);
      } else if (extracted_scrape_data.manufacturers[j] == "Moderna") {
        modernaData.dates.push(extracted_scrape_data.dates[j]);
        modernaData.first_dose.push(extracted_scrape_data.first_dose[j]);
        modernaData.second_dose.push(extracted_scrape_data.second_dose[j]);
      }
    }
    const stateDistData = {
      labels: extracted_scrape_data.dates,
      datasets: [
        {
          label: "Janssen (First Dose)",
          data: janssenData.dates.map((x, index) => ({
            x,
            y: janssenData.first_dose[index],
          })),
          borderColor: "rgba(75, 192, 192, 1)",
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          borderWidth: 2,
          pointRadius: 0,
          fill: true,
        },
        {
          label: "Moderna (First Dose)",
          data: modernaData.dates.map((x, index) => ({
            x,
            y: modernaData.first_dose[index],
          })),
          borderColor: "rgba(255, 99, 132, 1)",
          backgroundColor: "rgba(255, 99, 132, 0.2)",
          borderWidth: 2,
          pointRadius: 0,
          fill: true,
        },
        {
          label: "Moderna (Second Dose)",
          data: modernaData.dates.map((x, index) => ({
            x,
            y: modernaData.second_dose[index],
          })),
          borderColor: "rgba(227, 16, 61, 1)",
          backgroundColor: "rgba(227, 16, 61, 0.2)",
          borderWidth: 2,
          pointRadius: 0,
          fill: true,
        },
        {
          label: "Pfizer (First Dose)",
          data: pfizerData.dates.map((x, index) => ({
            x,
            y: pfizerData.first_dose[index],
          })),
          borderColor: "rgba(255, 206, 86, 1)",
          backgroundColor: "rgba(255, 206, 86, 0.2)",
          borderWidth: 2,
          pointRadius: 0,
          fill: true,
        },
        {
          label: "Pfizer (Second Dose)",
          data: pfizerData.dates.map((x, index) => ({
            x,
            y: pfizerData.second_dose[index],
          })),
          borderColor: "rgba(255, 176, 86, 1)",
          backgroundColor: "rgba(255, 176, 86, 0.2)",
          borderWidth: 2,
          pointRadius: 0,
          fill: true,
        },
      ],
    };

    // Create a Chart.js chart
    const distCtx = document.getElementById("distChart").getContext("2d");
    const distChart = new Chart(distCtx, {
      type: "line",
      data: stateDistData,
      options: {
        scales: {
          xAxes: [
            {
              scaleLabel: {
                display: true,
                fontColor: "#e21011",
                fontSize: 15,
                labelString: "Date",
              },
            },
          ],
          yAxes: [
            {
              beginAtZero: true,
              scaleLabel: {
                display: true,
                fontColor: "#e21011",
                fontSize: 14,
                labelString: "# of Doses Distributed",
              },
            },
          ],
        },
      },
    });
  });
});
