# Android Push Notifications Initialization

## Initialize Push Notification

FCM dependency:

```
implementation 'com.github.AmityCo.Amity-Social-Cloud-SDK-Android:amity-push-fcm:x.y.z'
```

Before you can start receiving push notifications, you need to obtain a FCM unique token string that identifies each FCM client app instance:

* [Retrieve the current FCM token](https://firebase.google.com/docs/cloud-messaging/android/client#retrieve-the-current-registration-token)
* [Monitor FCM token generation](https://firebase.google.com/docs/cloud-messaging/android/client#monitor-token-generation)

You can initialize the services with the obtained token. Please note that the FCM token can be changed through an application life cycle. Please make sure that the FCM token supplied to the messaging SDK is up to date. To notify the messaging SDK of the latest token, the following line of code can be called whenever necessary:

<Embed url="https://gist.github.com/850284e5274caaaf8eeaf01650525ba8"/>

### Retrieve Push Notifications

To retrieve push notifications, use a service that extends `FirebaseMessagingService`. Refer to Firebase's [messages handling](https://firebase.google.com/docs/cloud-messaging/android/receive#handling_messages) documentation for detailed information.

### Push Notification In China

Since Google Play services are banned in China, The messaging SDK provides Baidu push services as a substitute for FCM. The messaging SDK requires an api key and a secret key from Baidu:

[https://push.baidu.com/](https://push.baidu.com/)

Baidu dependency:

```
implementation 'com.github.AmityCo.Amity-Social-Cloud-SDK-Android:amity-push-baidu:x.y.z'
```

**Note: Baidu push services require a number of additional permissions. You can find** [a list of permissions here](https://push.baidu.com/doc/android/api).

Baidu API key is needed for Baidu push services initialization:

<Embed url="https://gist.github.com/amythee/05d25bc9ef2a28f9236820d383a49f08"/>

**Note: The messaging SDK always considers FCM as a primary push provider and Baidu as a secondary push provider. If the messaging SDK detects Google Play services on the device, Baidu push services won't be initialized.**