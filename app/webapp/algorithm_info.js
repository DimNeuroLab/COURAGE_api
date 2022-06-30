var API_URL_PREFIX = "api/1.0/";


async function getData(file_name) {
    var loaded_predictions = [];
    await $.ajax
    ({
        type: "POST",
        url: API_URL_PREFIX  + "load_algorithm_results/",
        contentType: "application/json",
        data: JSON.stringify({"file_name": file_name}),
        success: function (response) {
            loaded_predictions = JSON.parse(response)['predictions'];
        },
        error: function (error) {
            console.log("error: " + error)
        },
    });
    return loaded_predictions;
};


async function load_algorithm_samples() {
    // load sentiment info
    var en_sentiment_out = await getData('EN_sentiment_out.tsv');
    var en_sentiment_strings = [];
    var s = '<table><tr><th>Sample</th><th>Prediction</th><th>True</th></tr>';
    en_sentiment_strings.push(s);
    for (let prediction of en_sentiment_out) {
        if (prediction[1] == prediction[2]) {
            s = '<tr><td>' + prediction[0] + '</td><td style="color: green;">' + prediction[1] + '</td><td style="color: green;">' +
             prediction[2] + '</td></tr>';
        } else {
            s = '<tr><td>' + prediction[0] + '</td><td style="color: red;">' + prediction[1] + '</td><td style="color: red;">' +
             prediction[2] + '</td></tr>';
        }
        en_sentiment_strings.push(s);
    }
    var s = '</table>';
    en_sentiment_strings.push(s);
    var final_string = "";
    for (let table_line of en_sentiment_strings) {
        final_string = final_string + table_line;
    }
    document.getElementById("EN_sentiment_output").innerHTML = final_string;

    // load emotion info
    var en_emotion_out = await getData('EN_emotion_out.tsv');
    var en_emotion_strings = [];
    var s = '<table><tr><th>Sample</th><th>Prediction</th><th>True</th></tr>';
    en_emotion_strings.push(s);
    for (let prediction of en_emotion_out) {
        if (prediction[1] == prediction[2]) {
            s = '<tr><td>' + prediction[0] + '</td><td style="color: green;">' + prediction[1] + '</td><td style="color: green;">' +
             prediction[2] + '</td></tr>';
        } else {
            s = '<tr><td>' + prediction[0] + '</td><td style="color: red;">' + prediction[1] + '</td><td style="color: red;">' +
             prediction[2] + '</td></tr>';
        }
        en_emotion_strings.push(s);
    }
    var s = '</table>';
    en_emotion_strings.push(s);
    var final_string = "";
    for (let table_line of en_emotion_strings) {
        final_string = final_string + table_line;
    }
    document.getElementById("EN_emotion_output").innerHTML = final_string;

    // prediction hate speech out
    var en_hate_out = await getData('EN_hate_speech_out.tsv');
    var en_hate_speech_strings = [];
    var s = '<table><tr><th>Sample</th><th>Prediction Hate Speech</th><th>True Hate Speech</th>' +
            '<th>Prediction Targeted</th><th>True Targeted</th>' +
            '<th>Prediction Aggressive</th><th>True Aggressive</th></tr>';
    en_hate_speech_strings.push(s);
    var label_dict = {0: 'false', 1: 'true'};
    for (let prediction of en_hate_out) {
        s = '<tr><td>' + prediction[0] + '</td>';
        en_hate_speech_strings.push(s);

        if (label_dict[prediction[1]] == label_dict[prediction[2]]) {
            s = '<td style="color: green;">' + label_dict[prediction[1]] + '</td><td style="color: green;">' + label_dict[prediction[2]] +'</td>';
        } else {
            s = '<td style="color: red;">' + label_dict[prediction[1]] + '</td><td style="color: red;">' + label_dict[prediction[2]] +'</td>';
        }
        en_hate_speech_strings.push(s);
        if (label_dict[prediction[3]] == label_dict[prediction[4]]) {
            s = '<td style="color: green;">' + label_dict[prediction[3]] + '</td><td style="color: green;">' + label_dict[prediction[4]] +'</td>';
        } else {
            s = '<td style="color: red;">' + label_dict[prediction[3]] + '</td><td style="color: red;">' + label_dict[prediction[4]] +'</td>';
        }
        en_hate_speech_strings.push(s);
        if (label_dict[prediction[5]] == label_dict[prediction[6]]) {
            s = '<td style="color: green;">' + label_dict[prediction[5]] + '</td><td style="color: green;">' + label_dict[prediction[6]] +'</td>';
        } else {
            s = '<td style="color: red;">' + label_dict[prediction[5]] + '</td><td style="color: red;">' + label_dict[prediction[6]] +'</td>';
        }
        en_hate_speech_strings.push(s);
        s= '</tr>';
        en_hate_speech_strings.push(s);
    }
    var s = '</table>';
    en_hate_speech_strings.push(s);
    var final_string = "";
    for (let table_line of en_hate_speech_strings) {
        final_string = final_string + table_line;
    }
    document.getElementById("EN_hate_speech_output").innerHTML = final_string;
}
