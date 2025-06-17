# React Native (Beta)

### Minimum Requirement

* iOS
  * Minimum iOS Target >= 13.4
* Android
  * buildToolVersion >= "34.0.0"
  * kotlinVersion >= 1.7.0
  * minSdkVersion >= 24
  * compileSdkVersion >= 34
  * ndkVersion >= "25.1.8937393"
* ENV
  * React >= v16
  * NodeJS >= v18
  * NPM >= v6
  * yarn >= v1.22.15
  * JDK >= 17.0.10
  * ruby >= 3.2.0
  * XCode >= 15

### Installation

## <mark style="color:green;">Open-source Installation</mark>

With open-source, developers have more flexibility and greater customization options, allowing you to have complete control over the visual style. Open sourcing allows for more transparency and visibility and enables contributions from a greater developer community in terms of good design, implementation, code improvement, and fixes, translating into a better product and typical development.

1.  Clone the Social Plus UI Kit open-source repository from GitHub:

    ```
    git clone https://github.com/AmityCo/Amity-Social-UIKit-React-Native-CLI-OpenSource.git
    ```
2.  Navigate to the cloned repository directory:

    ```
    cd Amity-Social-Cloud-UIKit-React-Native-OpenSource
    ```
3.  Install the dependencies:

    ```
    yarn install
    ```
4.  Build the UI Kit:&#x20;

    ```
    npm run prepack
    npm pack
    ```

## <mark style="color:green;">Package Installation</mark>

This step will build the app and return amity-react-native-social-ui-kit-x.x.x.tgz file in inside the folder

1. Copy tgz file to your project folder where you need to use ui-kit:
2. Install built UI Kit  tgz file: The command to install the ui-kit package depends on the package manager used in your project.
   *   Yarn

       <pre><code><strong>yarn add ./amity-react-native-social-ui-kit-x.x.x.tgz
       </strong></code></pre>
   *   NPM

       ```
       npm install./amity-react-native-social-ui-kit-x.x.x.tgz
       ```
   *   PNPM

       <pre><code><strong>pnpm install ./amity-react-native-social-ui-kit-x.x.x.tgz
       </strong></code></pre>
3. Install peer dependencies: The command to install the ui-kit package depends on the package manager used in your project.
   *   Yarn

       <pre><code><strong>yarn add \
       </strong><strong>react-native-safe-area-context@^4.7.2 \
       </strong><strong>react-native-image-picker@^7.0.0 \
       </strong><strong>@react-native-async-storage/async-storage@^1.19.3 \
       </strong><strong>react-native-svg@^14.1.0 \
       </strong><strong>react-native-gesture-handler@^2.15.0 \
       </strong><strong>react-native-screens@^3.25.0 \
       </strong><strong>react-native-video@6.0.0-beta.6 \
       </strong><strong>react-native-create-thumbnail@^2.0.0 \
       </strong><strong>@react-native-community/netinfo@^11.3.1 \
       </strong><strong>@react-navigation/native@^6.1.17 \
       </strong><strong>@react-navigation/native-stack@^6.9.26 \
       </strong><strong>@react-navigation/stack@^6.3.29 \
       </strong><strong>react-native-vision-camera@^3.9.2 \
       </strong><strong>react-native-push-notification^8.1.1 \
       </strong><strong>@api.video/react-native-livestream@2.0.0 \
       </strong><strong>react-native-get-random-values@^1.11.0 \
       </strong><strong>react-native-rsa-native@^2.0.5 \
       </strong><strong>react-native-vlc-media-player@^1.0.67 \
       </strong><strong>react-native-fs@2.20.0 \
       </strong></code></pre>
   *   NPM

       <pre><code><strong>npm install \
       </strong>react-native-safe-area-context@^4.7.2 \
       react-native-image-picker@^7.0.0 \
       @react-native-async-storage/async-storage@^1.19.3 \
       react-native-svg@^14.1.0 \
       react-native-gesture-handler@^2.15.0 \
       react-native-screens@^3.25.0 \
       react-native-video@6.0.0-beta.6 \
       react-native-create-thumbnail@^2.0.0 \
       @react-native-community/netinfo@^11.3.1 \
       @react-navigation/native@^6.1.17 \
       @react-navigation/native-stack@^6.9.26 \
       @react-navigation/stack@^6.3.29 \
       react-native-vision-camera@^3.9.2 \
       react-native-push-notification^8.1.1 \
       @api.video/react-native-livestream@2.0.0 \
       react-native-get-random-values@^1.11.0 \
       react-native-rsa-native@^2.0.5 \
       react-native-vlc-media-player@^1.0.67 \
       react-native-fs@2.20.0 \
       </code></pre>
   *   PNPM

       <pre><code><strong>pnpm install \
       </strong>react-native-safe-area-context@^4.7.2 \
       react-native-image-picker@^7.0.0 \
       @react-native-async-storage/async-storage@^1.19.3 \
       react-native-svg@^14.1.0 \
       react-native-gesture-handler@^2.15.0 \
       react-native-screens@^3.25.0 \
       react-native-video@6.0.0-beta.6 \
       react-native-create-thumbnail@^2.0.0 \
       @react-native-community/netinfo@^11.3.1 \
       @react-navigation/native@^6.1.17 \
       @react-navigation/native-stack@^6.9.26 \
       @react-navigation/stack@^6.3.29 \
       react-native-vision-camera@^3.9.2 \
       react-native-push-notification^8.1.1 \
       @api.video/react-native-livestream@2.0.0 \
       react-native-get-random-values@^1.11.0 \
       react-native-rsa-native@^2.0.5 \
       react-native-vlc-media-player@^1.0.67 \
       react-native-fs@2.20.0 \
       </code></pre>

### iOS Configuration

In Pod file, add these lines under your target,

```
  pod 'SPTPersistentCache', :modular_headers => true
  pod 'DVAssetLoaderDelegate', :modular_headers => true
  $RNVideoUseVideoCaching = true  
```

<figure><img src="../../../.gitbook/assets/Screenshot 2567-06-10 at 10.57.11.png" alt=""><figcaption></figcaption></figure>

In XCode,

Set `Minimum Deployments at least iOS 12.0`

<figure><img src="../../../.gitbook/assets/Screenshot 2567-06-10 at 10.59.15.png" alt=""><figcaption></figcaption></figure>

```
cd ios
pod install
```

### iOS Permissions

Add following permissions to `info.plist` file (ios/{YourAppName}/Info.plist)

```markup
 <key>NSCameraUsageDescription</key>
 <string>App needs access to the camera to take photos.</string>
 <key>NSMicrophoneUsageDescription</key>
 <string>App needs access to the microphone to record audio.</string>
 <key>NSPhotoLibraryUsageDescription</key>
 <string>App needs access to the gallery to select photos.</string>
```

### iOS Setup Background downloading

Add this method in `AppDelegate.mm` file (ios/{YourAppName}/AppDelegate.mm)

````objectivec
```
#import <RNFSManager.h>
...
- (void)application:(UIApplication *)application handleEventsForBackgroundURLSession:(NSString *)identifier completionHandler:(void (^)())completionHandler
{
  [RNFSManager setCompletionHandlerForIdentifier:identifier completionHandler:completionHandler];
}
```
````

### Android Configuration

Build project gradle with your Android Studio

In android/build.gradle, add below in in buildscript > ext

kotlinVersion = 1.7.0 and above, compileSdkVersion = 34, buildToolsVersion = "34.0.0"

<figure><img src="../../../.gitbook/assets/Screenshot 2567-06-14 at 19.01.13 (1).png" alt=""><figcaption></figcaption></figure>

### Android Permissions

Add the following permissions to `AndroidManifest.xml` file (android/app/src/main/AndroidManifest.xml)

```markup
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
```

### Usage

```
import * as React from 'react';

import {
  AmityUiKitSocial,
  AmityUiKitProvider,
} from 'amity-react-native-social-ui-kit';

export default function App() {
  return (
    <AmityUiKitProvider
      apiKey="API_KEY"
      apiRegion="API_REGION"
      userId="userId"
      displayName="displayName"
      apiEndpoint="https://api.{API_REGION}.amity.co"
    >
      <AmityUiKitSocial />
    </AmityUiKitProvider>
  );
}
```

### Customization

Our UIKit v4 supports customization in a single place by modifying a `uikit.config.json` file in related UIKit repository. This configuration file includes all the necessary data to customize the appearance of each pages, components, and elements that we allow to do customization. Note: uikit.config.json file should be in your project. Please kindly check the example project.

```typescript
import * as React from 'react';
import {
  AmityUiKitSocial,
  AmityUiKitProvider,
} from 'amity-react-native-social-ui-kit';
import config from './uikit.config.json'; 

export default function App() {
  return (
    <AmityUiKitProvider
      configs={config} //put your customized config json object
      apiKey="API_KEY"
      apiRegion="API_REGION"
      userId="userId"
      displayName="displayName"
      apiEndpoint="https://api.{API_REGION}.amity.co"
    >
      <AmityUiKitSocial />
    </AmityUiKitProvider>
  );
}
```

### Using Theme

**Using the default theme**

Social Plus UIKit uses the default theme as part of the design language.

**Theme customization**

Without customization, the UIKit already looks good. However, if you wish to customize the theme, you can declare changes to color variables by passing your own color codes to our `uikit.config.json`. Here is the code usage of how to customize the theme.

```json
"preferred_theme": "default",
  "theme": {
    "light": {
      "primary_color": "#1054DE",
      "secondary_color": "#292B32",
      "base_color": "#292b32",
      "base_shade1_color": "#636878",
      "base_shade2_color": "#898e9e",
      "base_shade3_color": "#a5a9b5",
      "base_shade4_color": "#ebecef",
      "alert_color": "#FA4D30",
      "background_color": "#FFFFFF",
      "background_shade1_color": "#f6f7f8"
    },
    "dark": {
      "primary_color": "#1054DE",
      "secondary_color": "#292B32",
      "base_color": "#ebecef",
      "base_shade1_color": "#a5a9b5",
      "base_shade2_color": "#6e7487",
      "base_shade3_color": "#40434e",
      "base_shade4_color": "#292b32",
      "alert_color": "#FA4D30",
      "background_color": "#191919",
      "background_shade1_color": "#40434e"
    }
  },
```

**Dark Mode**

The Dark Mode feature in our UIKit enhances user experience by providing an alternative visual style that is particularly beneficial in low-light environments. It's designed to reduce eye strain, improve readability, and offer a more visually comfortable interface. You can enable dark mode by just changing `preferred_theme: "default"` to the `preferred_theme: "dark"` in `uikit.config.json`

```json
"preferred_theme": "dark" // change it to dark || light || default,
```

### Push Notification

Since v4.0.0-beta.7, UIKit supports push notifications by registering `fcm token` for android and `apn token` for ios. To enable push notifications in UIKit, please follow the instructions on the [React Native Push Notifications Initialization](../../../social-plus-sdk/core-concepts/push-notifications/react-native-push-notifications-initialization.md) page.&#x20;
