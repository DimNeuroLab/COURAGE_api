var API_URL_PREFIX = "api/1.0/";


async function getTweetDataEN(topic, n=0) {
    var loaded_tweets = {};
    await $.ajax
    ({
        type: "POST",
        url: API_URL_PREFIX + "load_topic_data_EXP/",
        contentType: 'application/json',
        async: true,
        data: JSON.stringify({'topic': topic, 'n': n, 'lang': 'en'}),
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
        data: JSON.stringify({'user_id': user_id, 'lang': 'en'}),
        success: function (response) {
            loaded_tweets = response;
        },
        error: function (error) {
            console.log("error: " + error)
        },
    });
    return loaded_tweets;
};


async function getUserFollowingIT(user_id) {
    var user_ids = {'following': []};
    await $.ajax
    ({
        type: "POST",
        url: API_URL_PREFIX + "load_user_following_data_EXP/",
        contentType: 'application/json',
        async: true,
        data: JSON.stringify({'user_id': user_id, 'lang': 'en'}),
        success: function (response) {
            user_ids = response;
        },
        error: function (error) {
            console.log("error: " + error)
        },
    });
    return user_ids
};


function image_exists(image_url){
    var http = new XMLHttpRequest();
    http.open('HEAD', image_url, false);
    http.send();
    return http.status != 404;
}


async function create_tweets(topic='experiment') {

    var loaded_tweets = await getTweetDataEN(topic);

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
    }

    var html = document.getElementById("t_feed").innerHTML;

    var final_string = '<div id="t_feed" class="feed">' + html;

    for (let tweet of tweet_strings) {
        final_string = final_string + tweet;
    }

    document.getElementById("t_feed").innerHTML =  final_string + '</div>';

}
