# Push Notifications

Push notifications are small pop-up messages triggered by an application, even when the application is not open. Push notifications are an essential part of social features that a customer must provide to their end users.

## Webhook

Clients who want to have the push notifications delivered to their own servers first in order to customize before it reach their users can opt for this method.

In this solution, events are sent from Social Plus’s servers to the client’s servers via webhook. Clients can decide what to do with each event before it reaches the end user's device as a notification. Clients have the ability to edit the notifications (i.e.: translate the message), filter them (based on specific use cases or user preferences), and perform analytics before sending them to the users. With this new feature, clients can also have notifications for web apps.

For more information, go to [Webhook Events](../../../developers/beta-features/real-time-events.md) settings.

In this scenario, there's no SDK involvement needed. The whole notification process is managed on your end.

## Direct Push Notifications

With this solution, the notifications will be triggered and delivered to your users directly by Social Plus's servers. There's nothing that the iOS client has to do in order to display the notification to your users. Social Plus's servers will prepare for you a notification that can be directly displayed to the user as and when it's received.

Click for more [Network Level settings](../../../analytics-and-moderation/console/settings/push-notifications.md).&#x20;

Click to learn about different SDK [Settings](../../../analytics-and-moderation/console/settings/#push-notifications).

{% hint style="info" %}
Direct push notifications only support on iOS, Android, and Flutter SDKs.
{% endhint %}

### Push Notification Examples

As Social Plus's servers are responsible for choosing the content of the push notification, you can expect your users to receive the following notifications for different kinds of events:

* Event: A new channel has been created and the user has been added among other members. Push Notification Title: `%s` (`%s` = New Channel display name) Push Notification Body: `You're now member of %s!` (`%s` = New Channel display name)
* Event: A new user has joined a channel. Push Notification Title: `%s` (`%s` = user display name) Push Notification Body: `%1s has joined %2s` (`%1s` = user display name, `%2s` = channel display name)
* Event: A new message has been received in a channel where the user is already a member. Push Notification Title: `%1s (%2s)` (`%1s` = user display name, `%2s` = channel display name) Push Notification Body: `%s` (`%s` = message text body if text message, `Image Message` if the image message, `Special message` otherwise)

## Push Notification Triggers

A new push notification will be sent to a specific user when:

* A new message is sent in a channel of the user who is already an existing member of it.
* A new channel is created and the user is among the listed members of the channel on creation.
* A new member joins a channel of the user who is already an existing member of it.
