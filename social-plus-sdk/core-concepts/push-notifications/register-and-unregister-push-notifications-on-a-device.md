# Register and Unregister Push Notifications on a Device

## Client Registration&#x20;

Registering your app for push notifications will require a registered `AmityClient` instance (necessary to know which user is associated with this device) and a push notification token.

Social Plus's Development Kit does not manage:

* user-facing requests for push notifications and authorizations
* the creation and refreshing of push notification tokens

It's up to your app to take those steps and pass the notification token to the SDK.

{% tabs %}
{% tab title="Swift" %}
{% embed url="https://gist.github.com/amythee/807aecce37cff79890c8d90ce046667d" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/3f7ae2f46c181d0890d773aad1fe51a0" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/f3ff0205f7d7c9e94747cf13ea14028b#file-amitynotificationregister-dart" %}
{% endtab %}
{% endtabs %}

We recommend observing the completion block outcome to ensure a successful registration.

> _If the device was previously registered with this or another user, the previous registration is invalidated as soon as this new request is received, which means that the device will always receive notifications of up to one user._

## Client Unregistration

Unlike the registration, unregistering for push does not require the `AmityClient` instance to be associated with any user, therefore you can unregister the device from receiving push notifications as soon as the `AmityClient` has been initialized with a valid API key.

#### The userId Parameter&#x20;

The unregistration allows one to pass an optional `userId`:

* if a valid `userId` is passed, Social Plus's backend will stop sending push notifications to this device only if the currently active push notification associated with this device is also associated with that user. No action is taken otherwise.
* if no `userId` is passed, Social Plus's backend will stop sending push notifications to this device.

{% tabs %}
{% tab title="Swift" %}
{% code overflow="wrap" %}
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
{% endcode %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/3e9646b99e65932349a9b3fca7f901ee" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/849f272d0c6133887ae19fc1200f261f#file-amitynotificationunregister-dart" %}
{% endtab %}
{% endtabs %}

You can register and unregister as many times as you'd like, however, please remember that we use the "Last write wins" strategy.
