---
description: Host your events virtually and see community interaction as it happens.
---

# View & Play Live Stream

Live streams and playback videos information are stored in **`AmityStream`**. This stream objects reside in **`AmityStreamRepository`**. To start working with stream, first the app need to intialize the repository.

{% tabs %}
{% tab title="Swift" %}
```swift
// `client` is AmityClient that has been initiated during the setup 
streamRepository = AmityStreamRepository(client: client)
```
{% endtab %}
{% endtabs %}

**\*Note :** There is a limitation for the maximum concurrent live events. Please feel free to reach out to us at [**community.amity.co**](https://community.amity.co/) with your use-case and we will determine if the current limit can be raised.

## Retrieve a stream object

Each stream object has a unique identifier. To retrieve a single stream object, call

* **`repository.getStreamById(_:)`**

This function returns a Live Object of **`AmityStream`**. The stream object contains essential data, for example, title and description.

```swift
let streamProxy = streamRepository.getStreamById(streamId)

getStreamToken = streamProxy.observe { (proxy, error) in
	// We have a stream object here.
	let stream = proxy.object
	print("Title: \(stream.title)")
	print("Description: \(stream.streamDescription)")
}
```

## Stream Status

Stream consists of many states. It can change from one state to another, depending on events and actions.

**`AmityStreamStatus`** represents a stream status. The following enum cases describe all the possible status of a stream.

* **`.idle`** indicates "a stream that has generated but no actions have been taken."
* **`.live`** indicates "a stream is currently being broadcasted."
* **`.ended`** indicates "a stream has ended broadcasting and in the progress of transforming to a recorded stream."
* **`.recorded`** indicates "a stream has ended broadcasting and has been transformed to a recorded stream."

You can check the status of a stream by calling **`.status`**.

```swift
// Print out the current status of a stream.
print(stream.status)
```

## Stream Moderation&#x20;

The system offers real-time automated moderation for live streams, where streams can be flagged or terminated based on customizable thresholds set via the console. The SDK provides access to information about which categories the live stream has been flagged or terminated by.

{% tabs %}
{% tab title="iOS" %}
<Embed url="https://gist.github.com/amythee/82c7c4f0cb8a18a523b1c9985888811e"/>
{% endtab %}
{% endtabs %}

## Retrieve streams collection

To query stream collection, first, you need to create a **`AmityStreamCollectionQuery`**.

```swift
// Create query object.
let query = AmityStreamCollectionQuery()
// Specify statuses to include in the streams collection.
query.includeStatus(.live)
```

Then call **`.getStreamsCollection(from:)`** with the query object that you've created.

* **`.getStreamsCollection(from: query)`**

This function returns the live collection of stream objects.

```swift
// Here we get AmityCollection<AmityStream>
streamsCollection = streamRepository.getStreamsCollection(from: query)

// An example of streams collection usage,
// to observe the changes and update UI.
token = streamsCollection.observe { [weak self] collection, change, error in
	// Any update will be notified here.
	self?.updateUI(from: collection)
}
```

If your app needs stream collections in many parts of the app. We recommend maintaining only one collection for each query, in an application scope. And use it as a single source of truth.

```swift
App.liveStreamsCollections = streamRepository.getStreamsCollection(from: liveStreamQuery)
App.liveStreamsToken = App.liveStreamsCollection.observe { collection, change, error in
	// Any update will be notified here.
	App.updateDataSource(from: collection)
	App.notifyLiveStreamsUpdate()
}
```

## Play a live stream

{% tabs %}
{% tab title="v6.19.0 and above" %}
Use AmityVideoPlayer to play a live stream.

<Embed url="https://gist.github.com/amythee/8d0f4f0da7500573cd67be5fe3d1bd2c"/>
{% endtab %}

{% tab title="Deprecated" %}
To play a live stream, currently only RTMP protocol is supported, call&#x20;

* **`stream.watcherUrl`**

**`AmityLiveStreamURLInfo`** contains a full RTMP url, which most of RTMP players support. For some players that does not support the full url, this object contains enough data for custom RTMP url formatting.

```swift
if let urlInfo = stream.watcherUrl {

	// play with the full ur
	rtmpPlayer.play(urlInfo.url)

	// or for some players that require custom RTMP url formatting
	customRtmpPlayer.setHost("\(urlInfo.origin)/\(urlInfo.appName)?\(urlInfo.query)")
	customRtmpPlayer.play(urlInfo.streamName)

}
```

**`AmityStream`** has **`isLive`** propert&#x79;**.**

* When there is an update of live object, use **`isLive`** property to check.
* When there is an update of live stream collections:
  * The streams that are not live, will disappear from the collection.
  * The streams that are just live, will appear in the collection.

```swift
if (stream.isLive) {
	print("The stream is live now.")
}
```

## Recommended RTMP players

RTMP is a low-latency video streaming protocol, that iOS does not support in its native video player. Therefore when working with RTMP, here are some open-source players that we recommend:

* [MobileVLCKit](https://code.videolan.org/videolan/VLCKit)
* [SGPlayer](https://github.com/libobjc/SGPlayer)
* [HaishinKit](https://github.com/shogo4405/HaishinKit.swift)
{% endtab %}
{% endtabs %}

## Play recorded videos

Live streams are recorded and saved as files after the session ends. It would take some time to prepare recorded videos to be ready. You can observe the collection of streams that have recorded videos available.

<Embed url="https://gist.github.com/amythee/e15d9925faef67ed6d3fad56d494831e"/>

{% tabs %}
{% tab title="v6.19.0 and above" %}
Use AmityRecordedStreamPlayer to play recorded videos. If the live stream session contains multiple recorded videos, the player will play one video after another.

<Embed url="https://gist.github.com/amythee/120b94f06260532184215670be0522fe"/>
{% endtab %}

{% tab title="Deprecated" %}
Each live stream session can contain multiple recorded videos. You can retrieve the array of **`AmityLiveVideoRecordingData`** that store all recording data, by calling

* **`stream.recordingData`**

To get the actual url, you need to specify the file format by calling on a recorded item.

* **`recordingItem.url(for: AmityLiveVideoRecordingFileFormat)`**

The following code shows an example of getting all the mp4 url of a stream instance.

```swift
// Print out all mp4 url for all recorded videos of `stream`.
//
for (index, dataItem) in stream.recordingData.enumerated() {
	// Specify .MP4, to get the actual url in mp4 format.
	if let url = dataItem.url(for: .MP4) {
		print("Video \(index): \(url)")
	} else {
		print("Video \(index): url not found")
	}
}
```

{% hint style="info" %}
In contrast with RTMP live videos, you don't need 3rd party video players for the recorded videos. iOS native players already support playing mp4 file from the URL given by API.

_See also_ [_AVFoundation_](https://developer.apple.com/documentation/avfoundation) _and_ [_AVKit_](https://developer.apple.com/documentation/avkit/)_._
{% endhint %}
{% endtab %}
{% endtabs %}

## Social Plus Video Player <a href="#ios-upstra-video-player" id="ios-upstra-video-player"></a>

Social Plus Video SDK includes `AmityVideoPlayerKit.framework`, a basic RTMP player to support live video functionality.

This framework requires `MobileVLCKit.framework` as a dependency. You can download the framework from the link provided in the [Installation Steps](https://docs.amity.co/installation-and-authentication/install-ios-sdk#additional-steps-for-amity-video).

## Social Plus Recorded Stream Player <a href="#ios-upstra-video-player" id="ios-upstra-video-player"></a>

This player is part of the Social Plus Video SDK, built as a subclass of AVPlayer for playing recorded livestream videos. It works seamlessly with AVPlayerViewController.
