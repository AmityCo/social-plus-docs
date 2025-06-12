---
description: Host your events virtually and see community interaction as it happens.
---

# Broadcast Live Stream

### Setup & Configuration

To use `AmityVideoBroadcaster` , please follow this setup step in your react native project.&#x20;

Install peer dependencies

```sh
yarn add \
@amityco/ts-sdk-react-native \
@api.video/react-native-livestream
```

After peer dependencies installed, follow these following steps depends on your Platform

#### IOS

1. Install pod&#x20;

```sh
cd ios && pod install
```

2. Add permission in your `info.split` file

```xml
<key>NSCameraUsageDescription</key>
<string>Your own description of the purpose</string>

<key>NSMicrophoneUsageDescription</key>
<string>Your own description of the purpose</string>
```

#### Android

1. config `kotlinVersion` and `compileSdkVersion` in `android/build.gradle`, add kotlinVersion above 1.7.0 and compileSdkVersion above 34 in buildscript > ext

```gradle
buildscript {
    ext {
        ...
        compileSdkVersion = 34
        kotlinVersion = "1.9.22"
        ...
    }
    ....
}
```

2. Add following permissions to `AndroidManifest.xml` file

```xml
<manifest>
    <uses-feature android:name="android.hardware.camera" android:required="true" />
    <uses-feature android:name="android.hardware.camera.autofocus" android:required="false" />
</manifest>
```

### Broadcast a stream&#x20;

To create a stream, use `StreamRepository.createStream()`  This will return a `LiveObject` instance of the created `AmityStream`. After `AmityStream` created successfully, `StreamId` will be used to publish the stream.&#x20;

We provide `AmityVideoBroadcaster` component. This component can be used to preview your preview your video. You can adjust your own resolution and bitrate as followed.

```typescript
import {AmityVideoBroadcaster} from '@amityco/video-broadcaster-react-native';
import {StreamRepository} from '@amityco/ts-sdk-react-native';
import {useRef} from 'react';

const Component = () => {
  const ref = useRef();

  const startPublish = () => {
   // Create Amity.Stream to get streamId
    const params = {
      title: 'stream title',
      thumbnailFileId: 'fileId',
      description: 'this is my live stream',
      isSecure: false,
    };
  
    const { data: newStream } = await StreamRepository.createStream(params);
    ref?.current.startPublish(newStream.streamId);
  };

  const stopPublish = () => {
    ref?.current.stopPublish();
  };

  const switchCamera = () => {
   ref?.current.switchCamera();
  };

  const onBroadcastStateChange = (state: AmityStreamBroadcasterState) => {
   ...
  }

  return (
    <View>
      <AmityVideoBroadcaster
        onBroadcastStateChange={onBroadcastStateChange}
        resolution={{
          width: 1280,
          height: 720,
        }}
        ref={ref}
        bitrate={2 * 1024 * 1024}
      />
      <YourOtherComponents>
    </View>
  );
};

export default Components;
```

### **Observe a broadcasting state**

To observe the status of a broadcast, you can pass onBroadcastStateChange to observe broadcaster's stage change. This function will be invoke and accept `AmityStreamBroadcasterState` as an input. The possible statuses are :&#x20;

* `idle` a status of stream in an idle state.
* `connecting`indicates a status of stream that it's connecting to a rtmp server.
* `connected`indicates a status of stream that it's connected to a rtmp server.
* `disconnected`indicates a status of stream that it's disconnected to a rtmp server. We also provide error information through an exception.

```jsx
import {AmityStreamBroadcasterState} from '@amityco/video-broadcaster-react-native';

const Component = () => {
  ...
  const onBroadcastStateChange = (state: AmityStreamBroadcasterState) => {
     console.log('state', state);
  }
  
  return (
    <View>
      <AmityVideoBroadcaster
        onBroadcastStateChange={onBroadcastStateChange}
        ...
      />
      ...
    </View>
  );
};

export default Components;
```
