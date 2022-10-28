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


async function loadCfMatrix(file_name) {
    var table = [];
    await $.ajax
    ({
        type: "POST",
        url: API_URL_PREFIX  + "load_algorithm_results/",
        contentType: "application/json",
        data: JSON.stringify({"file_name": file_name}),
        success: function (response) {
            cf_data = JSON.parse(response)['predictions'];
        },
        error: function (error) {
            console.log("error: " + error)
        },
    });

    var labels = cf_data[0];
    var cf_data = cf_data.slice(1);

    table.push('<table><tr><td></td>');
    for (let label of labels) {
        table.push('<th>' + label + '</th>');
    }
    table.push('</tr>');

    for (var i = 0; i < cf_data.length; i++) {
        var cf_row = cf_data[i];
        var s = '<tr><th>' + labels[i] + '</th>';
        table.push(s);
        for (let value of cf_row) {
            table.push('<td>' + value + '</td>');
        }
        table.push('</tr>');
    }
    table.push('</table>');
    var final_table = "";
    for (let table_line of table) {
        final_table = final_table + table_line;
    }
    return final_table;
};


async function load_algorithm_samples() {
    // load sentiment info
    var en_sentiment_out = await getData('EN_sentiment_out.tsv');
    var en_sentiment_strings = [];
    var s = '<p><a href="https://huggingface.co/finiteautomata/bertweet-base-sentiment-analysis">[MODEL]</a>';
    en_sentiment_strings.push(s);
    var s = '<a href="https://www.dropbox.com/s/byzr8yoda6bua1b/2017_English_final.zip?file_subpath=%2F2017_English_final%2FGOLD">[DATASET]</a></p>';
    en_sentiment_strings.push(s);

    var en_sentiment_cf = await loadCfMatrix('EN_sentiment_cf.tsv');
    en_sentiment_strings.push(en_sentiment_cf);
    en_sentiment_strings.push('<br>');

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
    var s = '<p><a href="https://huggingface.co/cardiffnlp/twitter-roberta-base-emotion">[MODEL]</a>';
    en_emotion_strings.push(s);
    var s = '<a href="https://github.com/cardiffnlp/tweeteval">[DATASET]</a></p>';
    en_emotion_strings.push(s);

    var en_emotion_cf = await loadCfMatrix('EN_emotion_cf.tsv');
    en_emotion_strings.push(en_emotion_cf);
    en_emotion_strings.push('<br>');

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

    // load hate speech info
    var en_hate_out = await getData('EN_hate_speech_out.tsv');
    var en_hate_speech_strings = [];
    var s = '<p><a href="https://huggingface.co/pysentimiento/bertweet-hate-speech">[MODEL]</a>';
    en_hate_speech_strings.push(s);
    var s = '<a href="https://aclanthology.org/S19-2007.pdf">[DATASET]</a></p>';
    en_hate_speech_strings.push(s);

    en_hate_speech_strings.push('<h3>Confusion Matrix Hate</h3>');
    var en_hate_cf = await loadCfMatrix('EN_hate_cf.tsv');
    en_hate_speech_strings.push(en_hate_cf);
    en_hate_speech_strings.push('<br>');
    en_hate_speech_strings.push('<h3>Confusion Matrix Targeted</h3>');
    var en_targeted_cf = await loadCfMatrix('EN_targeted_cf.tsv');
    en_hate_speech_strings.push(en_targeted_cf);
    en_hate_speech_strings.push('<br>');
    en_hate_speech_strings.push('<h3>Confusion Matrix Aggressive</h3>');
    var en_aggressive_cf = await loadCfMatrix('EN_aggressive_cf.tsv');
    en_hate_speech_strings.push(en_aggressive_cf);
    en_hate_speech_strings.push('<br>');

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

    // load sentiment info IT
    var it_sentiment_out = await getData('IT_sentiment_out.tsv');
    var it_sentiment_strings = [];
    var s = '<p><a href="https://huggingface.co/MilaNLProc/feel-it-italian-sentiment">[MODEL]</a>';
    it_sentiment_strings.push(s);
    var s = '<a href="https://aclanthology.org/2021.wassa-1.8/">[DATASET]</a></p>';
    it_sentiment_strings.push(s);

    var it_sentiment_cf = await loadCfMatrix('IT_sentiment_cf.tsv');
    it_sentiment_strings.push(it_sentiment_cf);
    it_sentiment_strings.push('<br>');

    var s = '<table><tr><th>Campione</th><th>Predizione</th><th>Corretto</th></tr>';
    it_sentiment_strings.push(s);
    for (let prediction of it_sentiment_out) {
        if (prediction[1] == prediction[2]) {
            s = '<tr><td>' + prediction[0] + '</td><td style="color: green;">' + prediction[1] + '</td><td style="color: green;">' +
             prediction[2] + '</td></tr>';
        } else {
            s = '<tr><td>' + prediction[0] + '</td><td style="color: red;">' + prediction[1] + '</td><td style="color: red;">' +
             prediction[2] + '</td></tr>';
        }
        it_sentiment_strings.push(s);
    }
    var s = '</table>';
    it_sentiment_strings.push(s);
    var final_string = "";
    for (let table_line of it_sentiment_strings) {
        final_string = final_string + table_line;
    }
    document.getElementById("IT_sentiment_output").innerHTML = final_string;

    // load emotion info IT
    var it_emotion_out = await getData('IT_emotion_out.tsv');
    var it_emotion_strings = [];
    var s = '<p><a href="https://huggingface.co/MilaNLProc/feel-it-italian-emotion">[MODEL]</a>';
    it_emotion_strings.push(s);
    var s = '<a href="https://aclanthology.org/2021.wassa-1.8/">[DATASET]</a></p>';
    it_emotion_strings.push(s);

    var it_emotion_cf = await loadCfMatrix('IT_emotion_cf.tsv');
    it_emotion_strings.push(it_emotion_cf);
    it_emotion_strings.push('<br>');

    var s = '<table><tr><th>Campione</th><th>Predizione</th><th>Corretto</th></tr>';
    it_emotion_strings.push(s);
    for (let prediction of it_emotion_out) {
        if (prediction[1] == prediction[2]) {
            s = '<tr><td>' + prediction[0] + '</td><td style="color: green;">' + prediction[1] + '</td><td style="color: green;">' +
             prediction[2] + '</td></tr>';
        } else {
            s = '<tr><td>' + prediction[0] + '</td><td style="color: red;">' + prediction[1] + '</td><td style="color: red;">' +
             prediction[2] + '</td></tr>';
        }
        it_emotion_strings.push(s);
    }
    var s = '</table>';
    it_emotion_strings.push(s);
    var final_string = "";
    for (let table_line of it_emotion_strings) {
        final_string = final_string + table_line;
    }
    document.getElementById("IT_emotion_output").innerHTML = final_string;

    // load hate speech info IT
    var it_hate_out = await getData('IT_hate_speech_out.tsv');
    var it_hate_speech_strings = [];
    // var s = '<p><a href="https://huggingface.co/pysentimiento/bertweet-hate-speech">[MODEL]</a>';
    // en_hate_speech_strings.push(s);
    // var s = '<a href="https://aclanthology.org/S19-2007.pdf">[DATASET]</a></p>';
    // en_hate_speech_strings.push(s);

    var it_hate_cf = await loadCfMatrix('IT_hate_speech_cf.tsv');
    it_hate_speech_strings.push(it_hate_cf);
    it_hate_speech_strings.push('<br>');

    var s = '<table><tr><th>Campione</th><th>Predizione</th><th>Corretto</th></tr>';
    it_hate_speech_strings.push(s);
    var label_dict = {0: 'false', 1: 'true'};
    for (let prediction of it_hate_out) {
        s = '<tr><td>' + prediction[0] + '</td>';
        it_hate_speech_strings.push(s);

        if (label_dict[prediction[1]] == label_dict[prediction[2]]) {
            s = '<td style="color: green;">' + label_dict[prediction[1]] + '</td><td style="color: green;">' + label_dict[prediction[2]] +'</td>';
        } else {
            s = '<td style="color: red;">' + label_dict[prediction[1]] + '</td><td style="color: red;">' + label_dict[prediction[2]] +'</td>';
        }
        it_hate_speech_strings.push(s);
        s= '</tr>';
        it_hate_speech_strings.push(s);
    }
    var s = '</table>';
    it_hate_speech_strings.push(s);
    var final_string = "";
    for (let table_line of it_hate_speech_strings) {
        final_string = final_string + table_line;
    }
    document.getElementById("IT_hate_speech_output").innerHTML = final_string;
}
