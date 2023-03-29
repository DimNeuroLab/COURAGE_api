var API_URL_PREFIX = "api/1.0/";


async function getTweetDataIT(topic, n=0) {
    var loaded_tweets = {};
    await $.ajax
    ({
        type: "POST",
        url: API_URL_PREFIX + "load_topic_data_EXP/",
        contentType: 'application/json',
        async: true,
        data: JSON.stringify({'topic': topic, 'n': n}),
        success: function (response) {
            loaded_tweets = response;
        },
        error: function (error) {
            console.log("error: " + error)
        },
    });
    return loaded_tweets;
};


async function getUserDataIT(user_id) {
    var loaded_tweets = {'tweets': []};
    await $.ajax
    ({
        type: "POST",
        url: API_URL_PREFIX + "load_user_data_EXP/",
        contentType: 'application/json',
        async: true,
        data: JSON.stringify({'user_id': user_id}),
        success: function (response) {
            loaded_tweets = response;
        },
        error: function (error) {
            console.log("error: " + error)
        },
    });
    return loaded_tweets;
};


function image_exists(image_url){
    var http = new XMLHttpRequest();
    http.open('HEAD', image_url, false);
    http.send();
    return http.status != 404;
}


async function create_tweets(topic='covid') {
    var loaded_tweets = await getTweetDataIT(topic);

    var tweet_strings = [];

    for (let tweet of loaded_tweets['tweets']) {
         var img_src = "https://i.pinimg.com/originals/a6/58/32/a65832155622ac173337874f02b218fb.png";
         if(image_exists(tweet['user']['profile_image_url_https'])) {
            img_src = tweet['user']['profile_image_url_https'];
         }
         s = '<div class="post">' +
            '<div class="post__avatar">' +
            '<img src=' +
            img_src +
            ' alt="" />' +
            '</div>' +
            '<div class="post__body">' +
            '<div class="post__header">' +
            '<div class="post__headerText">' +
            '<h3>' +
            tweet['user']['name'] +
            '<span class="post__headerSpecial">';
         tweet_strings.push(s);

         if (tweet['user']['verified'] == true)
         {
            s = '<span class="material-icons post__badge"> verified </span>';
            tweet_strings.push(s);
         }

         s = ' @' +
             tweet['user']['screen_name'] +
             '</span>' +
             '</h3>' +
             '</div>' +
             '<div class="post__headerDescription">' +
             '<p>' + tweet['text'] + '</p>' +
             '</div>' +
             '</div>';
         tweet_strings.push(s);

         try {
            if (typeof(tweet['extended_entities']['media']) != "undefined")
             {
                for (let i = 0; i < tweet['extended_entities']['media'].length; i++) {
                    if (tweet['extended_entities']['media'][i]['type'] == "photo")
                    {
                        s = '<img src=' +
                            tweet['extended_entities']['media'][i]['media_url_https'] +
                            ' alt=""/>';
                            tweet_strings.push(s);
                    }
                }
             }
         }
         catch(err) {
            console.log(err.message);
         }

         s = '<div class="post__footer">' +
             '<span class="material-icons"> repeat </span>' +
             '<span class="material-icons"> favorite_border </span>' +
             '<span class="material-icons"> publish </span>' +
             '</div>' +
             '</div>' +
             '</div>';
         tweet_strings.push(s);

         var sent_name = tweet['id_str'] + '_sent'
         var emotion_name = tweet['id_str'] + '_emotion'
         var hate_name = tweet['id_str'] + '_hate'
         s = '<div id="analysis-' + tweet['id_str'] + '" class="analysis">' +
             '<div class="post-diagram">' +
             //'<p class="analysis-text">Analisi del sentimento di questo post:</p>' +
             '<div class="post-analysis-canvas">' +
             '<canvas class="analysis-canvas" id=' + sent_name + '></canvas>' +
             '</div>' +
             '<div class="post-analysis-canvas">' +
             //'<p class="analysis-text">Analisi delle emozioni di questo post:</p>' +
             '<canvas class="analysis-canvas" id=' + emotion_name + '></canvas>' +
             '</div>' +
             '<div class="post-analysis-canvas">' +
             //'<p class="analysis-text">Classificazione di questo post odioso:</p>' +
             '<canvas class="analysis-canvas" id=' + hate_name + '></canvas>' +
             '</div>' +
             '</div>' +
             '</div>';
         tweet_strings.push(s);

    }

    var html = document.getElementById("t_feed").innerHTML;

    var final_string = '<div id="t_feed" class="feed">' + html;

    for (let tweet of tweet_strings) {
        final_string = final_string + tweet;
    }

    document.getElementById("t_feed").innerHTML =  final_string + '</div>';

    for (let tweet_idx = 0; tweet_idx < loaded_tweets['tweets'].length; tweet_idx++) {

         if (loaded_tweets['analysis'][tweet_idx]['topics'].length > 0) {
            var sentiment_label = ['neg', 'pos'].at([loaded_tweets['analysis'][tweet_idx]['sentiment']['negative'],
            loaded_tweets['analysis'][tweet_idx]['sentiment']['positive']].indexOf(Math.max(loaded_tweets['analysis'][tweet_idx]['sentiment']['negative'],
            loaded_tweets['analysis'][tweet_idx]['sentiment']['positive'])));
         }

         var sent_name = loaded_tweets['tweets'][tweet_idx]['id_str'] + '_sent'
         var ctx = document.getElementById(sent_name);
         var data_array = [];
         var labels = ['negativo', 'positivo'];
         for (let key in loaded_tweets['analysis'][tweet_idx]['sentiment']) {
             data_array.push(Math.round((parseFloat(loaded_tweets['analysis'][tweet_idx]['sentiment'][key]) + Number.EPSILON) * 100));
             // labels.push(key)
         }
         var myChart = new Chart(ctx, {
             type: 'pie',
             data: {
                 labels: labels,
                 datasets: [{
                     label: 'sentiment',
                     data: data_array,
                     backgroundColor: [
                         'rgba(203, 67, 53, 1)',
                         'rgba(39, 174, 96, 1)'
                     ]
                 }]
             },
             options: {
                 aspectRatio: 1,
                 cutoutPercentage: 20,
                 responsive: true,
                 // maintainAspectRatio: false,
                 title: {
                    display: true,
                    text: 'sentimento'
                 },
                 legend: {
                     display: false,
                     position: 'right',
                     labels: {
                         fontColor: 'rgb(0,0,0)'
                     },
                     onClick: (e) => e.stopPropagation(),
                 }
             }
         });

         var emotion_name = loaded_tweets['tweets'][tweet_idx]['id_str'] + '_emotion'
         var ctx = document.getElementById(emotion_name);
         var data_array = [];
         var labels = ['rabbia', 'paura', 'gioia', 'tristezza'];
         for (let key in loaded_tweets['analysis'][tweet_idx]['emotion']) {
             data_array.push(Math.round((parseFloat(loaded_tweets['analysis'][tweet_idx]['emotion'][key]) + Number.EPSILON) * 100));
             // labels.push(key)
         }
         var myChart = new Chart(ctx, {
             type: 'pie',
             data: {
                 labels: labels,
                 datasets: [{
                     label: 'emotion',
                     data: data_array,
                     backgroundColor: [
                         'rgba(203, 67, 53, 1)',
                         'rgba(0, 0, 153, 1)',
                         'rgba(39, 174, 96, 1)',
                         'rgba(0, 0, 0, 1)'
                     ]
                 }]
             },
             options: {
                 aspectRatio: 1,
                 cutoutPercentage: 20,
                 responsive: true,
                 // maintainAspectRatio: false,
                 title: {
                    display: true,
                    text: 'emozioni'
                 },
                 legend: {
                     display: false,
                     position: 'right',
                     labels: {
                         fontColor: 'rgb(0,0,0)'
                     },
                     onClick: (e) => e.stopPropagation(),
                 }
             }
         });

         var hate_name = loaded_tweets['tweets'][tweet_idx]['id_str'] + '_hate'
         var ctx = document.getElementById(hate_name);
         var data_array = [];
         var labels = ['odio', 'nessun odio'];
         data_array.push(Math.round((parseFloat(loaded_tweets['analysis'][tweet_idx]['hate_speech'][1]) + Number.EPSILON) * 100));
         data_array.push(Math.round((parseFloat(1 - loaded_tweets['analysis'][tweet_idx]['hate_speech'][1]) + Number.EPSILON) * 100));

         var myChart = new Chart(ctx, {
             type: 'pie',
             data: {
                 labels: labels,
                 datasets: [{
                     label: 'incitamento all\'odio',
                     data: data_array,
                     backgroundColor: [
                         'rgba(203, 67, 53, 1)',
                         'rgba(39, 174, 96, 1)'
                     ]
                 }]
             },
             options: {
                 aspectRatio: 1,
                 cutoutPercentage: 20,
                 responsive: true,
                 // maintainAspectRatio: false,
                 title: {
                    display: true,
                    text: 'incitamento all\'odio'
                 },
                 legend: {
                     display: false,
                     position: 'right',
                     labels: {
                         fontColor: 'rgb(0,0,0)'
                     },
                     onClick: (e) => e.stopPropagation(),
                 },
             }
         });

    }

}
