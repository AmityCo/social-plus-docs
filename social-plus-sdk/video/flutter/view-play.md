---
description: Host your events virtually and see community interaction as it happens.
---

# View & Play Live Stream

Live streams and playback videos information are stored in **`AmityStream`**. These stream objects reside in **`AmityStreamRepository`**. To start working with stream, first, the app needs to initialize the repository.

{% embed url="https://gist.github.com/amythee/e12e14f386a7111e91c7bb4078e212b1" %}

**Note :** There is a limitation for the maximum number of concurrent live events. Reach out to us at [**community.amity.co**](https://community.amity.co/) with your use-case and we will determine if the current limit can be raised.

## Retrieve a stream object

Each stream object has a unique identifier. To retrieve a single stream object.

This function returns a flowable of **`AmityStream`**. The stream object contains essential data, for example, title and description.

{% embed url="https://gist.github.com/amythee/b7f2b94499697b80e1908409faefc44f" %}

## Stream Status

The stream consists of many states. It can change from one state to another, depending on events and actions.

`Amitystream.Status` represents a stream status. The following enum cases describe all the possible statuses of a stream.

* `.IDLE` indicates "a stream that has generated but no actions have been taken."
* `.LIVE` indicates "a stream is currently being broadcasted."
* `.ENDED` indicates "a stream has ended broadcasting and is in the process of transforming to a recorded stream."
* `.RECORDED` indicates "a stream has ended broadcasting and has been transformed to a recorded stream."

You can check the status of a stream by calling `stream.getStatus()`.

## Retrieve a stream collection

AmityStreamRepository provides a convenient method `getStreams`and also call `setStatus(statuses: Array<Amitystream.Status>)` to query live streams. We provide enums of stream status as `AmityStream.Status`

&#x20;You can observe changes in a collection as per the defined statuses.

{% embed url="https://gist.github.com/amythee/e4c92d47b09c7d3ed3e4c8c5f59b00df" %}

## Play a live stream and a recorded live stream

#### Setup&#x20;

Run this command:

With Flutter:

```shell
 $ flutter pub add amity_video_player
```

This will add a line like this to your package's pubspec.yaml (and run an implicit `flutter pub get`):

```yaml
dependencies:
  amity_video_player: ^0.0.1
```

Alternatively, your editor might support `flutter pub get`. Check the docs for your editor to learn more.

#### Import it

Now in your Dart code, you can use:

```dart
import 'package:amity_video_player/amity_video_player.dart';
```

#### Configuration

To begin with, you will need to setup the AmityVideoPlayerClient at the application level.&#x20;

{% embed url="https://gist.github.com/amythee/5bc06de28dc0bcf043096bc6c854e251" %}

SDK provides AmityVideoPlayer with the capability to play a live stream or a recorded live stream by providing a `streamId` in `AmityVideoContoller`.

{% embed url="https://gist.github.com/amythee/4be4a38a2aa2b35710ce9fc38682b6aa" %}
