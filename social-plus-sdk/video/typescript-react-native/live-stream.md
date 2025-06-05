---
description: Host your events virtually and see community interaction as it happens.
---

# Live Stream

Live streams and playback video information are stored in **`Amity.Stream`**. To start working with the stream, first, the app needs to initialize the repository. To create a new SDK instance with your API key, refer to the [Initialization](broken-reference) section.

{% hint style="warning" %}
There is a limitation for the maximum concurrent live events. Please feel free to reach out to us at [**community.social.plus.co**](https://community.amity.co/) with your use-case and we will determine if the current limit can be raised.
{% endhint %}

## Viewing a live stream

### Retrieve a stream object

Each stream object has a unique identifier. To retrieve a single stream object. The stream object contains essential data such as title, description, streamerUrl, watcherUrl, etc

{% embed url="https://gist.github.com/amythee/85740588f25afac21c52b3274bb2557e" %}

### Stream Status

The stream consists of many states. It can change from one state to another, depending on events and actions.

**`Amity.StreamStatus.<STATUS>`** represents a stream status. The following enum cases describe all the possible statuses of a stream.

* `IDLE` indicates "a stream that has generated but no actions have been taken."
* `LIVE` indicates "a stream is currently being broadcasted."
* `ENDED` indicates "a stream has ended broadcasting and is in the process of transforming to a recorded stream."
* `RECORDED` indicates "a stream has ended broadcasting and has been transformed to a recorded stream."

## Stream Moderation&#x20;

The system offers real-time automated moderation for live streams, where streams can be flagged or terminated based on customizable thresholds set via the console. The SDK provides access to information about which categories the live stream has been flagged or terminated by.

{% tabs %}
{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/2c8dbf51574b9f5bee306654db4106a6" %}
{% endtab %}
{% endtabs %}

### Retrieve a stream collection

&#x20;You can query a list of streams by calling **`queryStream`**.

{% embed url="https://gist.github.com/amythee/d74b63c788fa0782120943be4755807c" %}

## Playing a live stream

To play a live stream, please refer to [view-and-play-live-stream.md](../web/view-and-play-live-stream.md "mention").

### Play a recorded stream

To play a recorded stream, currently, FLV, MP4, and M3U8 protocols are  supported by using **`recordings`** inside the stream object.

{% embed url="https://gist.github.com/ab836532def3bbb89c4fa9805728a33f" %}

## Create a stream object

Note that the TypeScript SDK does not support broadcasting a live stream directly. Instead, it allows the creation of a stream object. You can then retrieve the streaming URL from this object and implement it with a third-party library or a streaming tool like OBS.

{% embed url="https://gist.github.com/75cdb3d62f3d3bb986a66eeb83b9de8e" %}

## Stop live stream session

To stop broadcasting a live stream, you can use the dedicated stop function provided by the SDK. This function will explicitly end the ongoing live stream and change its status to 'ENDED' Using this function is crucial for effectively managing your live streams and ensuring that they transition properly to their recorded state after broadcasting. Here's how you can use the function:

{% embed url="https://gist.github.com/5ec52719ca044545369b9964850c0c41" %}

## Delete live stream

To delete a stream, you will need the ID of the stream that you want to delete. The function will return true if successfully deleted, otherwise, it will throw an error.

{% embed url="https://gist.github.com/f80fd898ee60c0e078cb41e9843d0b80" %}
