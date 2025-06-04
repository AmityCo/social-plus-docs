---
description: Host your events virtually and see community interaction as it happens.
---

# View & Play Live Stream

Live streams and playback videos information are stored in **`AmityStream`**. These stream objects reside in **`AmityStreamRepository`**. To start working with stream, first, the app needs to initialize the repository.

```kotlin
val streamRepository = AmityVideoClient.newStreamRepository()
```

**Note :** There is a limitation for the maximum number of concurrent live events. Reach out to us at [**community.amity.co**](https://community.amity.co/) with your use-case and we will determine if the current limit can be raised.

## Retrieve a stream object

Each stream object has a unique identifier. To retrieve a single stream object.

This function returns a flowable of **`AmityStream`**. The stream object contains essential data, for example, title and description.

```
streamRepository
       .getStream(streamId)
       .subscribe( {doOnNext} )
```

## Stream Status

Stream consists of many states. It can change from one state to another, depending on events and actions.

`Amitystream.Status` represents a stream status. The following enum cases describe all the possible statuses of a stream.

* `.IDLE` indicates "a stream that has generated but no actions have been taken."
* `.LIVE` indicates "a stream is currently being broadcasted."
* `.ENDED` indicates "a stream has ended broadcasting and in the process of transforming to a recorded stream."
* `.RECORDED` indicates "a stream has ended broadcasting and has been transformed to a recorded stream."

You can check the status of a stream by calling `stream.getStatus()`.

## Stream Moderation&#x20;

The system offers real-time automated moderation for live streams, where streams can be flagged or terminated based on customizable thresholds set via the console. The SDK provides access to information about which categories the live stream has been flagged or terminated by.

{% tabs %}
{% tab title="Android" %}
{% embed url="https://gist.github.com/3c1acb7679c2be88319284616187e58f" %}
{% endtab %}
{% endtabs %}

## Retrieve a stream collection

AmityStreamRepository provides a convenient method `getStreams`and also call `setStatus(statuses: Array<Amitystream.Status>)` to query live streams. We provide enums of stream status as `AmityStream.Status`

&#x20;You can observe changes in a collection as per the defined statuses.

```go
  AmityVideoClient.newStreamRepository()
         .getStreams()
         .setStatus(arrayOf(AmityStream.Status.LIVE, AmityStream.Status.RECORDED))
         .build()
         .query()
         .doOnNext { 
            // PagingData<AmityStream>    
          }
          .doOnError {
            // Exception
          }
         .subscribe()
```

## Play a live stream

#### Setup&#x20;

You simply need to include this dependency to your project in `build.gradle` in the application l

```
 implementation 'com.github.AmityCo.Amity-Social-Cloud-SDK-Android:amity-video-player:x.y.z'
```

Inside your Application class, in the application initialization process, you need to register the video player SDK to the core SDK by calling.

```kotlin
  @Override
  open fun onCreate() {
        super.onCreate()
        AmityStreamPlayerClient.setup(AmityCoreClient.getConfiguration())
    }
  
```

SDK provides AmityVideoPlayer with a capability to play a Live stream based on `streamId`

{% hint style="info" %}
From SDK version 6.19.0 onwards, AmityVideoPlayer plays a Live stream with `streamId`
{% endhint %}

{% tabs %}
{% tab title="6.19.0 and above" %}
{% embed url="https://gist.github.com/amythee/84fd476998b8d9fcab087fc28c978c2f" %}
{% endtab %}

{% tab title="Deprecated" %}
To play a live stream, currently FLV, RTMP and HLS protocol are supported by calling `getWatcherData.getUrl()` inside the stream object. The parameter accepts streamId and enum of AmityWatcherData.Format.

```kotlin
  AmityVideoClient.newStreamRepository()
                .getStreamById(streamId)
                .subscribe { stream -> 
                    val url = stream.getWatcherData()?.getUrl(AmityWatcherData.Format.FLV)
                    url?.let {
                        amityVideoPlayer.play(stream.getStreamId(), it)
                    }
                }
```

This function provides request/response API. The callback of this function returns a URL string.This object contains a full FLV, RTMP or HLS URL.
{% endtab %}
{% endtabs %}

## Play a recorded stream

{% hint style="info" %}
From SDK version 6.19.0 onwards, recorded stream can only be played with AmityVideoPlayer.
{% endhint %}

{% tabs %}
{% tab title="6.19.0 and above" %}
SDK provides AmityVideoPlayer with a capability to play a recorded stream based on `streamId`&#x20;

{% embed url="https://gist.github.com/amythee/7e8b11c7f9e0b32e510388d983608ba0" %}
{% endtab %}

{% tab title="Deprecated" %}
To play a recorded stream, currently FLV, MP4 and M3U8 protocol are supported by calling `getRecordings()[index]` inside the stream object. The parameter accepts streamId and enum of AmityWatcherData.Format.

```kotlin
  AmityVideoClient.newStreamRepository()
                .getStreamById(streamId)
                .subscribe { stream -> 
                    startStreaming(stream.getRecordings()[index]?
                            .getUrl(AmityRecordingData.Format.FLV))
                }
```

This function provides request/response API. The callback of this function returns a URL string.This object contains a full FLV, MP4 or M3U8 URL.



## Recommended video player&#x20;

We recommend using [ExoPlayer](https://exoplayer.dev) from Google.  ExoPlayer supports features not currently supported by Android’s MediaPlayer API, including DASH and SmoothStreaming adaptive playbacks. Unlike the MediaPlayer API, ExoPlayer is easy to customize and extend.

For FLV we highly recommend using the `DefaultDataSourceFactory`.

<pre class="language-kotlin"><code class="lang-kotlin"><strong>val dataSourceFactory = DefaultDataSourceFactory(this,  Util.getUserAgent(this, "Upstra"))
</strong>val videoSource = ProgressiveMediaSource.Factory(dataSourceFactory, DefaultExtractorsFactory())
                .createMediaSource(Uri.parse(videoUrl))
                
exoplayer?.prepare(videoSource)
</code></pre>

For RTMP we highly recommend using the `RtmpDataSourceFactory`.

```kotlin
val dataSourceFactory = RtmpDataSourceFactory()
val videoSource = ProgressiveMediaSource.Factory(dataSourceFactory, DefaultExtractorsFactory())
                .createMediaSource(Uri.parse(videoUrl))
                
exoplayer?.prepare(videoSource)
```
{% endtab %}
{% endtabs %}

## Playing stream in Jetpack Compose

By inflating `AmityVideoPlayer` as AndroidView in Compose, it can seamlessly play live or recorded stream video within the Composable function.

{% embed url="https://gist.github.com/amythee/193a6de1d10f4a4153822adb10f77728" %}
