var API_URL_PREFIX = "api/1.0/";


async function getData() {
    var loaded_tweets = [];
    await $.ajax
    ({
        type: "GET",
        url: API_URL_PREFIX  + "load_twitter_data/",
        contentType: 'application/json',
        success: function (response) {
            loaded_tweets = response['tweets'];
        },
        error: function (error) {
            console.log("error: " + error)
        },
    });
    return loaded_tweets;
};


function add_collapsible() {
    var coll = document.getElementsByClassName("analysis-button");
    var i;

    for (i = 0; i < coll.length; i++) {
      coll[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.maxHeight){
          content.style.maxHeight = null;
        } else {
          content.style.maxHeight = content.scrollHeight + "px";
        }
      });
    }
}

async function create_tweets() {

    var loaded_tweets = await getData();

    var tweet_strings = [];

    for (let tweet of loaded_tweets) {
         s = '<div class="post">' +
            '<div class="post__avatar">' +
            '<img src=' +
            tweet[0]['user']['profile_image_url_https'] +
            ' alt="" />' +
            '</div>' +
            '<div class="post__body">' +
            '<div class="post__header">' +
            '<div class="post__headerText">' +
            '<h3>' +
            tweet[0]['user']['name'] +
            '<span class="post__headerSpecial">';
         tweet_strings.push(s);

         if (tweet[0]['user']['verified'] == true)
         {
            s = '<span class="material-icons post__badge"> verified </span>';
            tweet_strings.push(s);
         }

         s = ' @' +
             tweet[0]['user']['screen_name'] +
             '</span>' +
             '</h3>' +
             '</div>' +
             '<div class="post__headerDescription">' +
             '<p>' + tweet[0]['text'] + '</p>' +
             '</div>' +
             '</div>';
         tweet_strings.push(s);

         try {
            if (typeof(tweet[0]['extended_entities']['media']) != "undefined")
             {
                for (let i = 0; i < tweet[0]['extended_entities']['media'].length; i++) {
                    if (tweet[0]['extended_entities']['media'][i]['type'] == "photo")
                    {
                        s = '<img src=' +
                            tweet[0]['extended_entities']['media'][i]['media_url_https'] +
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

         s = '<button type="button" class="analysis-button">Learn more about this post</button>'
         tweet_strings.push(s);

         var sent_name = tweet[0]['id_str'] + '_sent'
         var emotion_name = tweet[0]['id_str'] + '_emotion'
         var hate_name = tweet[0]['id_str'] + '_hate'
         s = '<div class="analysis">' +
             // '<div style="height: 200px">' +
             '<p class="analysis-text">Sentiment analysis of this post:</p>' +
             '<canvas class="analysis-canvas" id=' + sent_name + '></canvas>' +
             // '</div>' +
             // '<div style="height: 200px">' +
             '<p class="analysis-text">Emotion analysis of this post:</p>' +
             '<canvas class="analysis-canvas" id=' + emotion_name + '></canvas>' +
             // '</div>' +
             // '<div style="height: 200px">' +
             '<p class="analysis-text">Probability of this post being aggressive, hateful and targeted:</p>' +
             '<canvas class="analysis-canvas" id=' + hate_name + '></canvas>' +
             // '</div>' +
             '</div>';
         tweet_strings.push(s);

    }

    var html = document.getElementById("t_feed").innerHTML;

    var final_string = '<div id="t_feed" class="feed">' + html;

    for (let tweet of tweet_strings) {
        final_string = final_string + tweet;
    }

    document.getElementById("t_feed").innerHTML =  final_string + '</div>';

    for (let tweet of loaded_tweets) {
         var sent_name = tweet[0]['id_str'] + '_sent'
         var ctx = document.getElementById(sent_name);
         var data_array = [];
         var labels = [];
         for (let key in tweet[1]['sentiment']) {
             data_array.push(parseFloat(tweet[1]['sentiment'][key]))
             labels.push(key)
         }
         var myChart = new Chart(ctx, {
             type: 'doughnut',
             data: {
                 labels: labels,
                 datasets: [{
                     label: 'sentiment',
                     data: data_array,
                     backgroundColor: [
                         'rgba(203, 67, 53, 1)',
                         'rgba(244, 208, 63, 1)',
                         'rgba(39, 174, 96, 1)'
                     ]
                 }]
             },
             options: {
                 responsive: true,
                 // maintainAspectRatio: false,
                 legend: {
                     display: true,
                     position: 'right',
                     labels: {
                         fontColor: 'rgb(0,0,0)'
                     },
                     onClick: (e) => e.stopPropagation(),
                 }
             }
         });

         var emotion_name = tweet[0]['id_str'] + '_emotion'
         var ctx = document.getElementById(emotion_name);
         var data_array = [];
         var labels = [];
         for (let key in tweet[1]['emotion']) {
             data_array.push(parseFloat(tweet[1]['emotion'][key]))
             labels.push(key)
         }
         var myChart = new Chart(ctx, {
             type: 'doughnut',
             data: {
                 labels: labels,
                 datasets: [{
                     label: 'emotion',
                     data: data_array,
                     backgroundColor: [
                         'rgba(203, 67, 53, 1)',
                         'rgba(39, 174, 96, 1)',
                         'rgba(52, 152, 219, 1)',
                         'rgba(44, 62, 80, 1)'
                     ]
                 }]
             },
             options: {
                 responsive: true,
                 // maintainAspectRatio: false,
                 legend: {
                     display: true,
                     position: 'right',
                     labels: {
                         fontColor: 'rgb(0,0,0)'
                     },
                     onClick: (e) => e.stopPropagation(),
                 }
             }
         });

         var hate_name = tweet[0]['id_str'] + '_hate'
         var ctx = document.getElementById(hate_name);
         var data_array = [];
         var labels = [];
         for (let key in tweet[1]['hate_speech']) {
             data_array.push(parseFloat(tweet[1]['hate_speech'][key]))
             labels.push(key)
         }
         var myChart = new Chart(ctx, {
             type: 'bar',
             data: {
                 labels: labels,
                 datasets: [{
                     label: 'hate speech',
                     data: data_array,
                     backgroundColor: [
                         'rgba(203, 67, 53, 1)',
                         'rgba(203, 67, 53, 1)',
                         'rgba(203, 67, 53, 1)'
                     ]
                 }]
             },
             options: {
                 responsive: true,
                 // maintainAspectRatio: false,
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

    add_collapsible();
}
