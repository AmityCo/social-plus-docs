# Register and Unregister Push Notifications on a Device

## Client Registration

Registering your app for push notifications will require a registered `AmityClient` instance (necessary to know which user is associated with this device) and a push notification token.

Social Plus's Development Kit does not manage:

* user-facing requests for push notifications and authorizations
* the creation and refreshing of push notification tokens

It's up to your app to take those steps and pass the notification token to the SDK.

<Tabs>
<Tab title="Swift">
<CodeGroup>
```swift
// assume the client has been initialized with a valid API key
// assume we have a valid push notification token
client.registerDeviceForPushNotification(withDeviceToken: deviceToken) { [weak self] success, error in
    ...
}
```
</CodeGroup>
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
// assume the client has been initialized with a valid API key
// assume we have a valid push notification token
client.registerDeviceForPushNotification(deviceToken, object: AmityCallback<Unit> {
    override fun onSuccess(result: Unit) {
        // handle success
    }
    override fun onError(error: AmityException) {
        // handle error
    }
})
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
<CodeGroup>
```dart
// assume the client has been initialized with a valid API key
// assume we have a valid push notification token
await AmityCoreClient.registerDeviceNotification(deviceToken);
```
</CodeGroup>
</Tab>
</Tabs>

We recommend observing the completion block outcome to ensure a successful registration.

> _If the device was previously registered with this or another user, the previous registration is invalidated as soon as this new request is received, which means that the device will always receive notifications of up to one user._

## Client Unregistration

Unlike the registration, unregistering for push does not require the `AmityClient` instance to be associated with any user, therefore you can unregister the device from receiving push notifications as soon as the `AmityClient` has been initialized with a valid API key.

#### The userId Parameter

The unregistration allows one to pass an optional `userId`:

* if a valid `userId` is passed, Social Plus's backend will stop sending push notifications to this device only if the currently active push notification associated with this device is also associated with that user. No action is taken otherwise.
* if no `userId` is passed, Social Plus's backend will stop sending push notifications to this device.

<Tabs>
<Tab title="Swift">
<CodeGroup>
```swift
// assume the client has been initialized with a valid API key
// unregister from receiving push notifications for the user with id `userId`
client.unregisterDeviceForPushNotification(forUserId: userId) { [weak self] _, success, error in
  ...
}

// unregister from receiving push notifications for this device
client.unregisterDeviceForPushNotification(forUserId: nil) { [weak self] _, success, error in
  ...
}
```
</CodeGroup>
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
// assume the client has been initialized with a valid API key
// unregister from receiving push notifications for the user with id `userId`
client.unregisterDeviceForPushNotification(userId, object: AmityCallback<Unit> {
    override fun onSuccess(result: Unit) {
        // handle success
    }
    override fun onError(error: AmityException) {
        // handle error
    }
})
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
<CodeGroup>
```dart
// assume the client has been initialized with a valid API key
// unregister from receiving push notifications
await AmityCoreClient.unregisterDeviceNotification();
```
</CodeGroup>
</Tab>
</Tabs>

You can register and unregister as many times as you'd like, however, please remember that we use the "Last write wins" strategy.