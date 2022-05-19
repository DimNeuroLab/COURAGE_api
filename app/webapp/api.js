var API_URL_PREFIX = "api/1.0/";

function createChart(analysis_result, algo_type) {
    var ctx = document.getElementById("output-chart");
    var data_array = [];
    var labels = [];
    for (let key in analysis_result) {
        data_array.push(parseFloat(analysis_result[key]))
        labels.push(key)
    }
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: algo_type,
                data: data_array
                /*,
                backgroundColor: [
                    'rgba(39, 174, 96, 1)',
                    'rgba(244, 208, 63, 1)',
                    'rgba(203, 67, 53, 1)'
                ]
                */
            }]
        },
        options: {
            responsive: true,
            legend: {
                display: true,
                position: 'right',
                labels: {
                    fontColor: 'rgb(0,0,0)'
                },
                onClick: (e) => e.stopPropagation(),
            },
            scales: {
                    yAxes: [{
                            display: true,
                            ticks: {
                                beginAtZero: true,
                                max: 1
                            }
                        }]
                }
        }
    });
}

function resetAnalysisOutput() {
    switchSendInput();
    /*
    var chart_div_pro = document.getElementById('chart-div-pro');
    var chartProgress = document.getElementById('chartProgress');
    chart_div_pro.removeChild(chartProgress);
    chart_div_pro.insertAdjacentHTML('afterbegin', '<canvas id="chartProgress"></canvas>');
    */
    var chart_div_nut = document.getElementById('chart-div-nut');
    var old_canvas = document.getElementById('output-chart');
    chart_div_nut.removeChild(old_canvas);
    chart_div_nut.insertAdjacentHTML('afterbegin', '<canvas id="output-chart"></canvas>');
    document.getElementById('results').innerHTML = ""
}

function resetInput() {
    document.getElementById("inputText").value = "";
}

function sendApiRequest() {
    let input_text = document.getElementById("inputText").value
    if (input_text == "") {
        document.getElementById('no-input-alert').hidden = false
        return
    } else {
        document.getElementById('no-input-alert').hidden = true
    }
    resetAnalysisOutput();
    let language = document.getElementById("language").value;
    let algorithm = document.getElementById("algo").value;
    if (language == "EN" && algorithm == "hate") {
        algorithm = "hate_speech_semeval19"
    }
    $.ajax
    ({
        type: "POST",
        url: API_URL_PREFIX + language + "/" + algorithm + "/",
        contentType: 'application/json',
        async: true,
        data: JSON.stringify({'text': input_text}),
        success: function (response) {
            switchInputResult();
            console.log(response)
            var data = JSON.parse(response);
            console.log(data)
            createChart(data, algorithm)
        },
        error: function (error) {
            console.log("error: " + error)
            switchInputResult();
            document.getElementById("results").innerHTML = "This algorithm is not yet available for the selected language."
        },
    });
}

function switchInputResult() {
    if (document.getElementById("output").hidden) {
        document.getElementById("output").hidden = false
    }
    document.getElementById("spinner").hidden = !document.getElementById("spinner").hidden
}

function switchSendInput() {
    document.getElementById("spinner").hidden = !document.getElementById("spinner").hidden
}
