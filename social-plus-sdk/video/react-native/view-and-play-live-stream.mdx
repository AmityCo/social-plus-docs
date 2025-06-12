---
description: Host your events virtually and see community interaction as it happens.
---

# View & Play Live Stream

In order to play a live stream or recorded live stream using React Native app, we provided **`AmityStreamPlayer`** component. This player allows developers to easily incorporate video playback functionality into their applications. To utilize this feature, developers can refer to the example code provided below, which demonstrates how to play the desired video with simplicity and efficiency.

### Setup & Configuration

To use `AmityStreamPlayer` , please follow this setup step in your react native project.&#x20;

Install peer dependencies

```sh
yarn add \
@amityco/ts-sdk-react-native \
react-native-video \
react-native-vlc-media-player \
react-native-get-random-values \
react-native-rsa-native
```

After peer dependencies are installed, follow the following steps depending on your Platform.

#### IOS

Install pods

```sh
cd ios && pod install
```

#### Android

config `kotlinVersion` and `compileSdkVersion` in `android/build.gradle`, add kotlinVersion above 1.7.0 and compileSdkVersion above 34 in buildscript > ext

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

### Play a live stream and playback video

To initialize the player, call `setupAmityVideoPlayer()` after login

```jsx
import {Client} from '@amityco/ts-sdk-react-native';
import {setupAmityVideoPlayer} from '@amityco/video-player-react-native';

const response = await Client.login(loginParam, sessionHandler);
setupAmityVideoPlayer();
```

Get `Amity.Stream` object using `StreamRepository.getStreamById`

```typescript
import {StreamRepository} from '@amityco/ts-sdk-react-native';

const getStreamById = (streamId: string) => {
    const unsubscriber = StreamRepository.getStreamById(({data, loading, error}) => {
        if (data) {
            console.log(data.streamId)
        }
    });
    unsubscriber();
};
```

On your live-stream video player page, use `AmityStreamPlayer` component and pass `Amity.Stream` .&#x20;

```typescript
import {AmityStreamPlayer} from '@amityco/video-player-react-native';
import {useRef} from 'react';

const Component = ({livestream}: {livestream:Amity.Stream}) => {
  const ref = useRef();

  // You can implement your own media control and use ref to pause and play the livestream
  const onStopPlayer = () => {
    ref.current && ref.current.pause();
  };

  const onStartPlayer = () => {
    ref.current && ref.current.play();
  };

  return (
    <View>
      {/* Pass Amity.Stream object as stream prop to AmtiyStreamPlayer */}
      <AmityStreamPlayer ref={ref} stream={livestream} status={livestream.status} />
      {/* You can add your media control compoent here. Since for the live video, AmitStreamPlayer does not provide the media control */}
      <ControlComponent />
    </View>
  );
};

export default Components;
```
