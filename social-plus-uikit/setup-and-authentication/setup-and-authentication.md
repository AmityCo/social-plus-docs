---
description: >-
  With Social Plus UIKit 2.3, we have introduced a new way to Authentication
  process. Just follow the guide below.
---

# iOS

## Adding required permissions

Your app may require the following permissions to work properly;

1. Camera access
2. Microphone access
3. Photo library usage access

Before submitting your application to the store, please make sure the following permissions are already granted. Here are the steps to ask for permission.

Locate the `info.plist` file and add:

1. `NSCameraUsageDescription`
2. `NSMicrophoneUsageDescription`
3. `NSPhotoLibraryUsageDescription`

## Setup API key

`Social Plus`` ``UIKit` requires an API key. You need a valid API key to begin using the UIKit. Please find your account API key in [Social Plus Console.](https://portal.amity.co/login)&#x20;

After logging in Console:

1. Click **Settings** to expand the menu.
2. Select **Security**.
3. On the **Security** page, you can find the API key in the **Keys** section.

![API key in Security page](../../../.gitbook/assets/iosConsole.png)

If you have trouble finding this, you can post in our community forum at [**community.social.plus.co**](https://community.amity.co/) so our support team can assist you.

```swift
import AmityUIKit

// in order to use AmityRegionalEndpoint enum, importing AmitySDK is required.
import AmitySDK 

AmityUIKitManager.setup(apiKey: "api-key", region: .global)
```

{% hint style="info" %}
&#x20;**AmityUIKitManager.setup** should only be called once when the app starts running. Calling the method repeatedly will create connection problems.
{% endhint %}

#### Specify Endpoints Manually (Optional)

By default, AmityClient will connect to `AmityRegion.SG`. You can specify endpoints manually via `AmityEndpoint` struct. API endpoints for each data center are different so you need to adjust the endpoint accordingly.&#x20;

```swift
let endpoint = AmityEndpoint(httpUrl: "http-endpoint",
                             rpcUrl: "rpc-endpoint",
                             mqttHost: "mqtt-host")
        
AmityUIKitManager.setup(apiKey: "api-key", endpoint: endpoint)
```

We currently support multi-data center capabilities for the following regions:

|     Region    |    Endpoint    |
| :-----------: | :------------: |
|     Europe    | AmityRegion.EU |
|   Singapore   | AmityRegion.SG |
| United States | AmityRegion.US |

## Authentication

### Register Device

To use any SDK feature, you must first register the current device with a `userId`. A device registered with an `userId` will be permanently tied to that `userId` until you explicitly unregister the device, or until the device has been inactive for more than 90 days. A device registered with a specific `userId` will receive all messages belonging to that user.

Additionally, an optional `displayName` can be provided if you wish to have this user identified in push notifications.

```swift
AmityUIKitManager.registerDevice(withUserId: "USER_ID", displayName: "Ali Connors", authToken: "AUTH_TOKEN")
```

### Register the device for push notifications

Registering your app for push notifications will require a device token as a parameter.

Social Plus's UIKit does not manage:

* User-facing requests for push notifications and authorizations
* The creation and refreshing of push notification tokens

It's up to your app to take those steps and pass the device token.

```swift
UIKitManager.registerDeviceForPushNotification("device-token") { isSuccess, error in
   // Handle completion here
}
```

## Unregister

If your user logs out, you should explicitly unregister the user from the SDK as well, to prevent the current device from receiving any unnecessary or restricted data.

```swift
AmityUIKitManager.unregisterDevice()
```

{% hint style="info" %}
Unregistering a device is a synchronous operation. Once the`unregisterDevice` method is called, the SDK disconnects from the server and wipes out user session.
{% endhint %}
