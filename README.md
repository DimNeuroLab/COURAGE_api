# COURAGE_api
Collection of all COURAGE algorithms and its API

## Endpoints and routes
There are several endpoints:

## General

| Endpoint | HTTP method | Requires auth? | Description                            | Returned data                                                       | Requested data format | 
|----------|-------------|----------------|----------------------------------------|---------------------------------------------------------------------|-----------------------|
| /info/   | GET         | no             | Info on API when it is live and online | **200 OK** `{'COURAGE': 'api', 'version': '1.0'}` if up and running | none                  |


## Images

| Endpoint         | HTTP method | Requires auth? | Description                                                                                        | Returned data                                                                                                                                                                                                                                                                                                                                                    | Requested data format                            | 
|------------------|-------------|----------------|----------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------|
| /predict_bmi/    | POST        | no             | BMI prediction based on an image. Returns predicted BMI and class label on success, else sends 444 | **200 OK** `{'bmi': <bmi>, 'label': <label>}` on success, where `<bmi>` contains the BMI as float and `<label>` the body class as string. <br /> **400 Missing Arg** if no image is passed to the endpoint. <br /> **444 Bad Request** else                                                                                                                      | `{image: <image>}` as utf-8 encoded bytes string |
| /predict_gender/ | POST        | no             | Gender prediction based on image. Returns predicted gender label on success, else sends 444        | **200 OK** `{'gender': <gender> }` on success, where `<gender>` contains gender class label as string. <br /> **400 Missing Arg** if no image is passed to the endpoint. <br /> **444 Bad Request** else                                                                                                                                                         | `{image: <image>}` as utf-8 encoded bytes string |
| /detect_objects/ | POST        | no             | Object detection in image. Returns predicted object labels on success, else sends 444              | **200 OK** `{'objects': [{'label': <label>, 'x': <x>, 'y': <y>, 'w': <w>, 'h': <h>}*n]}` on success, where `<label>` is the name of one detected object, `<x>` is its x coordinate in the image, `<y>` its y coordinate, `<w>` its width and `<h>` its height. <br /> **400 Missing Arg** if no image is passed to the endpoint. <br /> **444 Bad Request** else | `{image: <image>}` as utf-8 encoded bytes string |

## Text

### Overview

| Method      | EN  | IT | ES  | DE  |
|-------------|:---:|:--:|:---:|:---:|
| Sentiment   | `X` | `X` | `X` | `X` |
| Emotion     | `X` | `X` | `X` | `-` |
| Hate Speech | `X` | `X` | `-` | `P` |
| Fake News   | `P` | `-` | `-` | `-` |
| Toxicity    | `-` | `-` | `-` | `X` |

`X` = available; `P` = in progress; `-` not available or in progress

### Italian

| Endpoint         | HTTP method | Requires auth? | Description                                                                                                          | Returned data                                                                                                                                                                                                                                                                                                | Requested data format        | 
|------------------|-------------|----------------|----------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------|
| /IT/sentiment/   | POST        | no             | Sentiment prediction based on an Italian text. Returns positve/negative sentiment scores on success, else 444        | **200 OK** `{'negative': <neg>, 'positive': <pos>}` on success, where `<neg>` is the probability (float) of negative sentiment and `<pos>` the probability of positive sentiment, `<neg> + <pos> = 1`. <br /> **400 Missing Arg** if no text is passed to the endpoint. <br /> **444 Bad Request** else      | `{'text': <text>}` as string |
| /IT/emotion/     | POST        | no             | Emotion prediction based on an Italian text. Returns emotion types and confidence scores on success, else 444        | **200 OK** `{'label': <confidence>, ...}` on success, where `<label>` is a emotion type as string and `<confidence>` the probability of this emotion (multiple key-value pairs). <br /> **400 Missing Arg** if no text is passed to the endpoint. <br /> **444 Bad Request** else                            | `{'text': <text>}` as string |
| /IT/hate_speech/ | POST        | no             | Prediction whether an Italian text is hate speech or not. Returns hate speech/not hate speech class labels, else 444 | **200 OK** `{'not hate': <n_hate>, 'hate': <hate>}` on success, where `<n_hate>` is 1 if the text is not hate speech (`<hate>` = 0 then) or `<hate>` is 1 if the text is hate speech (`<n_hate>` = 0 then). <br /> **400 Missing Arg** if no text is passed to the endpoint. <br /> **444 Bad Request** else | `{'text': <text>}` as string |

### English

| Endpoint                   | HTTP method | Requires auth? | Description                                                                                                                                  | Returned data                                                                                                                                                                                                                                                                                                                                                                                                              | Requested data format        | 
|----------------------------|-------------|----------------|----------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------|
| /EN/sentiment/             | POST        | no             | Sentiment prediction based on an English text. Returns positive/neutral/negative sentiment scores on success, else 444                       | **200 OK** `{'negative': <neg>, 'neutral': <neu>, 'positive': <pos>}` on success, where `<neg>` is the probability (float) of negative sentiment, `<neu>` the probability of neutral sentiment and `<pos>` the probability of positive sentiment, `<neg> + <neu> + <pos> = 1`. <br /> **400 Missing Arg** if no text is passed to the endpoint. <br /> **444 Bad Request** else                                            | `{'text': <text>}` as string |
| /EN/hate_speech_semeval19/ | POST        | no             | Predicts Hate Speech related characteristics based on an English text. Returns Hate Speech types and probability scores on success, else 444 | **200 OK** `{'hateful': <hate>, 'targeted': <targ>, 'aggressive': <agg>}` on success, where `<hate>` is the probability (float) of the text being Hate Speech, and `<targ>` the probability (float) of the text being targeted to a specific individual and `<agg>` the probability (float) of the text being aggressive. <br /> **400 Missing Arg** if no text is passed to the endpoint. <br /> **444 Bad Request** else | `{'text': <text>}` as string |
| /EN/emotion/               | POST        | no             | Emotion prediction based on an English text. Returns emotion types and confidence scores on success, else 444                                | **200 OK** `{'label': <confidence>, ...}` on success, where `<label>` is a emotion type as string and `<confidence>` the probability of this emotion (multiple key-value pairs). <br /> **400 Missing Arg** if no text is passed to the endpoint. <br /> **444 Bad Request** else                                                                                                                                                                    | `{'text': <text>}` as string |

### Spanish

| Endpoint       | HTTP method | Requires auth? | Description                                                                                                           | Returned data                                                                                                                                                                                                                                                                                                                                                                   | Requested data format        | 
|----------------|-------------|----------------|-----------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------|
| /ES/sentiment/ | POST        | no             | Sentiment prediction based on a Spanish text. Returns positive/neutral/negative sentiment scores on success, else 444 | **200 OK** `{'negative': <neg>, 'neutral': <neu>, 'positive': <pos>}` on success, where `<neg>` is the probability (float) of negative sentiment, `<neu>` the probability of neutral sentiment and `<pos>` the probability of positive sentiment, `<neg> + <neu> + <pos> = 1`. <br /> **400 Missing Arg** if no text is passed to the endpoint. <br /> **444 Bad Request** else | `{'text': <text>}` as string |
| /ES/emotion/   | POST        | no             | Emotion prediction based on a Spanish text. Returns emotion types and confidence scores on success, else 444          | **200 OK** `{'label': <confidence>, ...}` on success, where `<label>` is a emotion type as string and `<confidence>` the probability of this emotion (multiple key-value pairs). <br /> **400 Missing Arg** if no text is passed to the endpoint. <br /> **444 Bad Request** else                                                                                                                         | `{'text': <text>}` as string |

### German

| Endpoint       | HTTP method | Requires auth? | Description                                                                                                        | Returned data                                                                                                                                                                                                                                                                                                                                                                   | Requested data format        | 
|----------------|-------------|----------------|--------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------|
| /DE/sentiment/ | POST        | no             | Sentiment prediction based on a German text. Returns positive/neutral/negative sentiment scores on success, else 444 | **200 OK** `{'negative': <neg>, 'neutral': <neu>, 'positive': <pos>}` on success, where `<neg>` is the probability (float) of negative sentiment, `<neu>` the probability of neutral sentiment and `<pos>` the probability of positive sentiment, `<neg> + <neu> + <pos> = 1`. <br /> **400 Missing Arg** if no text is passed to the endpoint. <br /> **444 Bad Request** else | `{'text': <text>}` as string |
| /DE/toxic/     | POST        | no             | Prediction whether a German text is toxic or not. Returns toxic/not toxic class labels, else 444                   | **200 OK** `{'not toxic': <n_tox>, 'toxic': <tox>}` on success, where `<n_tox>` is 1 if the text is not toxic (`<tox>` = 0 then) or `<tox>` is 1 if the text is toxic (`<n_tox>` = 0 then). <br /> **400 Missing Arg** if no text is passed to the endpoint. <br /> **444 Bad Request** else                                                                                    | `{'text': <text>}` as string |
