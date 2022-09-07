var API_URL_PREFIX = "api/1.0/";


async function getTweetDataIT(topic, n=0) {
    var loaded_tweets = {};
    await $.ajax
    ({
        type: "POST",
        url: API_URL_PREFIX + "load_topic_data_IT/",
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
    var loaded_tweets = [];
    await $.ajax
    ({
        type: "POST",
        url: API_URL_PREFIX + "load_user_data_IT/",
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

/*
async function loadUserTweetsAnalysis(user_id) {
    await $.ajax
    ({
        type: "POST",
        url: API_URL_PREFIX + "load_user_tweets_analysis/",
        contentType: 'application/json',
        async: true,
        data: JSON.stringify({'user_id': user_id}),
        success: function (response) {
            analysis_result = response;
        },
        error: function (error) {
            console.log("error: " + error)
        },
    });
    return analysis_result;
};


async function loadTopicTweets(topic_name, n) {
    var loaded_tweets = [];
    await $.ajax
    ({
        type: "POST",
        url: API_URL_PREFIX + "load_tweets_topic/",
        contentType: 'application/json',
        async: true,
        data: JSON.stringify({'topic': topic_name, 'n': n}),
        success: function (response) {
            loaded_tweets = response['tweets'];
        },
        error: function (error) {
            console.log("error: " + error)
        },
    });
    return loaded_tweets;
};
*/

function closeAll() {
    var dolls = [];
    dolls = Array.prototype.concat.apply(dolls, document.getElementsByClassName("analysis-button"));
    for (let dol of dolls) {
        dol.classList.remove("active");
        var content = document.getElementById("analysis-" + dol['id'].split('-')[2])
        content.style.maxHeight = null;
    }

    var dolls = [];
    dolls = Array.prototype.concat.apply(dolls, document.getElementsByClassName("tweets-user-button"));
    for (let dol of dolls) {
        dol.classList.remove("active");
        var content = document.getElementById("user_tweets-" + dol['id'].split('-')[2])
        content.style.maxHeight = null;
    }

    var dolls = [];
    dolls = Array.prototype.concat.apply(dolls, document.getElementsByClassName("tweets-topic-button"));
    for (let dol of dolls) {
        dol.classList.remove("active");
        var content = document.getElementById("topic_tweets-" + dol['id'].split('-')[2])
        content.style.maxHeight = null;
    }
}


function add_collapsible() {
    var coll = [];
    coll = Array.prototype.concat.apply(coll, document.getElementsByClassName("analysis-button"));
    var i;

    for (i = 0; i < coll.length; i++) {
      coll[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var content = document.getElementById("analysis-" + this['id'].split('-')[2])
        if (content.style.maxHeight){
          content.style.maxHeight = null;
          closeAll();
        } else {
          closeAll();
          content.style.maxHeight = content.scrollHeight + "px";
        }
      });
    }

    var coll = [];
    coll = Array.prototype.concat.apply(coll, document.getElementsByClassName("tweets-user-button"));
    for (i = 0; i < coll.length; i++) {
      coll[i].addEventListener("click", function() {
        //closeAll();
        this.classList.toggle("active");
        var content = document.getElementById("user_tweets-" + this['id'].split('-')[2])
        if (content.style.maxHeight){
          content.style.maxHeight = null;
          closeAll();
        } else {
          closeAll();
          content.style.maxHeight = content.scrollHeight + "px";
        }
      });
    }

    var coll = [];
    coll = Array.prototype.concat.apply(coll, document.getElementsByClassName("tweets-topic-button"));
    for (i = 0; i < coll.length; i++) {
      coll[i].addEventListener("click", function() {
        //closeAll();
        this.classList.toggle("active");
        var content = document.getElementById("topic_tweets-" + this['id'].split('-')[2])
        if (content.style.maxHeight){
          content.style.maxHeight = null;
          closeAll();
        } else {
          closeAll();
          content.style.maxHeight = content.scrollHeight + "px";
        }
      });
    }

}

async function create_tweets(topic='covid') {

    document.getElementById("t_feed").innerHTML = `
      <div class="feed__header">
        <h2>Home</h2>
      </div>

      <div class="tweetBox">
        <form>
          <div class="tweetbox__input">
            <img
              src="https://i.pinimg.com/originals/a6/58/32/a65832155622ac173337874f02b218fb.png"
              alt=""
            />
            <input type="text" placeholder="Che c'è di nuovo?" />
          </div>
          <button class="tweetBox__tweetButton">Twitta</button>
        </form>
      </div>
    `;

    var loaded_tweets = await getTweetDataIT(topic);

    var tweet_strings = [];

    for (let tweet of loaded_tweets['tweets']) {
         s = '<div class="post">' +
            '<div class="post__avatar">' +
            '<img src=' +
            tweet['user']['profile_image_url_https'] +
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

         s = '<button type="button" id="analysis-button-' + tweet['id_str'] + '" class="analysis-button">Learn more about this post</button>'
         tweet_strings.push(s);

         s = '<button type="button" id="tweets-user-' + tweet['id_str'] + '" class="tweets-user-button">Other posts of this user</button>'
         tweet_strings.push(s);

         s = '<button type="button" id="tweets-topic-' + tweet['id_str'] + '" class="tweets-topic-button">Other opinions on that topic</button>'
         tweet_strings.push(s);

         var sent_name = tweet['id_str'] + '_sent'
         var emotion_name = tweet['id_str'] + '_emotion'
         var hate_name = tweet['id_str'] + '_hate'
         s = '<div id="analysis-' + tweet['id_str'] + '" class="analysis">' +
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

         s = '<div id="user_tweets-' + tweet['id_str'] + '" class="analysis-user-tweets">';
         tweet_strings.push(s);

         var user_tweets = await getUserDataIT(tweet['user']['id_str']);
         if (user_tweets['tweets'].length == 0) {
            tweet_strings.push("<p class='user-tweets-text'>This user hasn't posted anything else yet...</p>");
         } else {
            for (let u_tweet of user_tweets['tweets']) {
                tweet_strings.push('<p class="user-tweets-text">' + u_tweet['text'] + '</p>');
            }
            tweet_strings.push('<div class="user-post-diagram">' +
                               '<div class="user-analysis-canvas"><canvas id="user-tweets-sentiment-canvas-' +
                               tweet['id_str'] + '"></canvas></div>' +
                               '<div class="user-analysis-canvas"><canvas id="user-tweets-emotion-canvas-' +
                               tweet['id_str'] + '"></canvas></div></div>');
         }
         tweet_strings.push('</div>');

         s = '<div id="topic_tweets-' + tweet['id_str'] + '" class="analysis-topic-tweets">';
         tweet_strings.push(s);

         var topic_tweets = [];
         if (tweet['entities']['hashtags'].length > 15) {
            var topics = tweet['entities']['hashtags'].slice(0, 15);
            var topic_tweets = [];
            for (let top of topics) {
                var top_tweets = await getTweetDataIT(top, 1);
                topic_tweets.push(top_tweets['tweets']);
            }
         } else {
            var num_tweets_per_topic = ~~(15/tweet['entities']['hashtags'].length);
            var topics = tweet['entities']['hashtags'];
            var topic_tweets = [];
            for (let top of topics) {
                var top_tweets = await getTweetDataIT(top, num_tweets_per_topic);
                topic_tweets.push(top_tweets['tweets']);
            }
         }

         if (topic_tweets.length == 0) {
            tweet_strings.push("<p class='topic-tweets-text'>We couldn't find any tweets with similar topic...</p>");
         } else {
            for (let t_tweet of topic_tweets) {
                tweet_strings.push('<p class="topic-tweets-text"><b>' + t_tweet['user']['name'] + '</b><br>' +
                t_tweet['text'] + '</p>');
            }
         }
         tweet_strings.push('</div>');

    }

    var html = document.getElementById("t_feed").innerHTML;

    var final_string = '<div id="t_feed" class="feed">' + html;

    for (let tweet of tweet_strings) {
        final_string = final_string + tweet;
    }

    document.getElementById("t_feed").innerHTML =  final_string + '</div>';

    for (let tweet_idx = 0; tweet_idx < loaded_tweets['tweets'].length; tweet_idx++) {
         var sent_name = loaded_tweets['tweets'][tweet_idx]['id_str'] + '_sent'
         var ctx = document.getElementById(sent_name);
         var data_array = [];
         var labels = [];
         for (let key in loaded_tweets['analysis'][tweet_idx]['sentiment']) {
             data_array.push(parseFloat(loaded_tweets['analysis'][tweet_idx]['sentiment'][key]))
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

         var emotion_name = loaded_tweets['tweets'][tweet_idx]['id_str'] + '_emotion'
         var ctx = document.getElementById(emotion_name);
         var data_array = [];
         var labels = [];
         for (let key in loaded_tweets['analysis'][tweet_idx]['emotion']) {
             data_array.push(parseFloat(loaded_tweets['analysis'][tweet_idx]['emotion'][key]))
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
                         'rgba(0, 0, 153, 1)',
                         'rgba(39, 174, 96, 1)',
                         'rgba(0, 0, 0, 1)'
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

         var hate_name = loaded_tweets['tweets'][tweet_idx]['id_str'] + '_hate'
         var ctx = document.getElementById(hate_name);
         var data_array = [];
         var labels = [];
         for (let key in loaded_tweets['analysis'][tweet_idx]['hate_speech']) {
             data_array.push(parseFloat(loaded_tweets['analysis'][tweet_idx]['hate_speech'][key]))
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

         var user_tweets = await getUserDataIT(loaded_tweets['tweets'][tweet_idx]['user']['id_str']);
         if (user_tweets['tweets'].length > 0) {
             var user_tweets_analysis = user_tweets['analysis'][0];
             var user_tweets_sent = 'user-tweets-sentiment-canvas-' + loaded_tweets['tweets'][tweet_idx]['id_str'];
             var ctx = document.getElementById(user_tweets_sent);
             var data_array = [];
             var labels = [];
             for (let key in user_tweets_analysis['sentiment']) {
                 data_array.push(parseFloat(user_tweets_analysis['sentiment'][key]))
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
                            'rgba(39, 174, 96, 1)'
                         ]
                     }]
                 },
                 options: {
                     responsive: true,
                     //maintainAspectRatio: false,
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

             var user_tweets_emotion = 'user-tweets-emotion-canvas-' + loaded_tweets['tweets'][tweet_idx]['id_str'];
             var ctx = document.getElementById(user_tweets_emotion);
             var data_array = [];
             var labels = [];
             for (let key in user_tweets_analysis['emotion']) {
                 data_array.push(parseFloat(user_tweets_analysis['emotion'][key]))
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
                            'rgba(0, 0, 153, 1)',
                            'rgba(39, 174, 96, 1)',
                            'rgba(0, 0, 0, 1)'
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
         }
    }

    add_collapsible();
}
