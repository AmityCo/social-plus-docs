# React Native Push Notifications Initialization

In order to send or receive push notifications using our UIKit v4.0.0-beta.7, you would need to register the FCM token for Android and the APN token for iOS.&#x20;

Follow the steps below to enable push notifications in your project:

### **1. Setup and Install Firebase and FCM:**

Refer to the official documentation to set up and install Firebase and Firebase Cloud Messaging (FCM):

* [Firebase Setup](https://rnfirebase.io/)
* [Firebase Cloud Messaging Usage](https://rnfirebase.io/messaging/usage)

### **2. Setup Push Notification Certificates in Console**:

#### **Android**

1. Follow the [FCM Legacy API Migration Guide](https://docs.amity.co/developers/migration-guides/fcm-legacy-api-migration-guide) to get the FCM service account JSON file.
2. Open the Social Plus Console.
3. Navigate to **Settings → Push Notifications**.
4. Upload the FCM service account JSON file.

<div align="left">
<figure>
<img src="https://docs.amity.co/~gitbook/image?url=https%3A%2F%2F2352509137-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252F-MX0mOAVWkotGme0iRzu%252Fuploads%252FyQx9uOJgaMZX0x56hHEd%252FScreenshot%25202567-06-10%2520at%252009.43.29.png%3Falt%3Dmedia%26token%3D76e2a909-cfea-430c-bf47-71639c4ee16c&#x26;width=300&#x26;dpr=4&#x26;quality=100&#x26;sign=26c549f&#x26;sv=1" alt="" width="375" />
<figcaption></figcaption>
</figure>
</div>

#### **iOS**

1. Follow the [iOS Push Notification Certificate Setup Guide](https://docs.amity.co/amity-sdk/core-concepts/push-notifications/ios-push-notification-certificate-setup) to get the iOS keychain file with a `.p12` extension.
2. Open the Social Plus Console.
3. Navigate to **Settings → Push Notifications**.
4. Upload the `.p12` file.

<div align="left">
<figure>
<img src="https://docs.amity.co/~gitbook/image?url=https%3A%2F%2F2352509137-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252F-MX0mOAVWkotGme0iRzu%252Fuploads%252FwLgHn5gldylHoWkyxKqZ%252FScreenshot%25202567-06-10%2520at%252010.08.40.png%3Falt%3Dmedia%26token%3De302837e-a6d6-433a-a191-fe1038fa9cd2&#x26;width=300&#x26;dpr=4&#x26;quality=100&#x26;sign=2f4752fd&#x26;sv=1" alt="" width="375" />
<figcaption></figcaption>
</figure>
</div>

### 3. Passing FCM Token or APN Token to UIKit

Integrate the following code into your React Native app to pass the FCM or APN token to the Social Plus UIKit:

```tsx
import React, {useState, useEffect} from 'react';
import messaging from '@react-native-firebase/messaging';
import { AmityUiKitProvider, AmityUiKitSocial } from '@amityco/asc-react-native-ui-kit';
import { Platform } from 'react-native';

const App = () => {
  const [fcmToken, setFcmToken] = useState<string | null | undefined>(null);

  useEffect(() => {
    messaging()
      .registerDeviceForRemoteMessages()
      .then(() => 
        Platform.select({
          ios: messaging().getAPNSToken(),
          android: messaging().getToken(),
        })
      )
      .then(token => {
        setFcmToken(token);
      })
      .catch(error => {
        console.log(error);
      });
  }, []);

  const configs = { /* your configs here */ };
  const apiKey = 'your-api-key';
  const apiRegion = 'your-api-region';
  const userId = 'your-user-id';
  const displayName = 'your-display-name';
  const endpoint = 'your-api-endpoint';

  return (
    <AmityUiKitProvider
      configs={configs}
      apiKey={apiKey}
      apiRegion={apiRegion}
      userId={userId}
      displayName={displayName}
      apiEndpoint={endpoint}
      fcmToken={fcmToken} // FCM/APN token
    >
      <AmityUiKitSocial />
    </AmityUiKitProvider>
  );
};

export default App;
```