# Notification tray

Here's an overview of notification tray and how you can get started with integrating them into your applications

<figure><img src="../../../.gitbook/assets/Screenshot 2568-04-22 at 15.35.51.png" alt=""><figcaption></figcaption></figure>

#### **Notification Tray SDK Feature**

Enhance user engagement and connectivity within your application with the **Notification Tray SDK Feature**. This feature allows users to receive notifications based on interactions from others, ensuring they stay informed and connected to their community.

**Key Capabilities:**

* **User Post Notifications** – Instantly notify users when someone posts within their community, keeping them updated on relevant discussions.
* **Reaction Alerts** – Users receive notifications when others react to their posts, fostering engagement and interaction.
* **Comment Updates** – Notify users when someone comments on their posts, allowing timely responses and deeper conversations.
* **Reply Notifications** – Users get alerts when someone replies to their comments, ensuring they remain engaged in ongoing discussions.

Designed for seamless integration, the Notification Tray SDK ensures **real-time updates**, improved **user retention**, and a more engaging **social experience**.

### Notification Tray Item Description

<table><thead><tr><th>Name</th><th width="288.5625">DataType</th><th>Description</th></tr></thead><tbody><tr><td><code>notificationId</code></td><td><code>String</code></td><td>id of notification item</td></tr><tr><td><code>lastSeenAt</code></td><td><code>Datetime</code></td><td>Timestamp when the notification was last seen</td></tr><tr><td><code>lastOccuredAt</code></td><td><code>Datetime</code></td><td>Timestamp when the notification last occurred</td></tr><tr><td><code>actors</code></td><td><code>List&#x3C;AmityNotificationActors></code></td><td>Data of user that act on this notification item</td></tr><tr><td><code>actorCount</code></td><td><code>Int</code></td><td>Number of users that act on this notification item</td></tr><tr><td><code>actionType</code></td><td><code>String</code></td><td>Type of action that user act on this notification</td></tr><tr><td><code>trayItemCategory</code></td><td><code>String</code></td><td>Category for when action is either "mention" or "reply"</td></tr><tr><td><code>targetId</code></td><td><code>String</code></td><td>Object id of target</td></tr><tr><td><code>targetType</code></td><td><code>String</code></td><td>Type of target for this act</td></tr><tr><td><code>referenceId</code></td><td><code>String</code></td><td>Optional ObjectId of the reference</td></tr><tr><td><code>referenceType</code></td><td><code>String</code></td><td>Type of refference for this act</td></tr><tr><td><code>parentId</code></td><td><code>String</code></td><td>Optional ObjectId of parent</td></tr><tr><td><code>text</code></td><td><code>String</code></td><td>Ready to render text without any templating</td></tr><tr><td><code>templatedText</code></td><td><code>String</code></td><td>Ready to render text with templating allow client to interpret</td></tr><tr><td><code>isSeen</code></td><td><code>Boolean</code></td><td>Refference of this item is seen</td></tr><tr><td><code>isRecent</code></td><td><code>Boolean</code></td><td>Refference of this item is recent or older</td></tr><tr><td><code>users</code></td><td><code>List&#x3C;AmityUser></code></td><td>List of users that act on this notification</td></tr></tbody></table>

### Notification Tray Seen Description

| Name                | Data type  | Description                                |
| ------------------- | ---------- | ------------------------------------------ |
| `lastTraySeenAt`    | `Datetime` | Timestamp when the tray was last seen      |
| `lastTrayOccuredAt` | `Datetime` | Timestamp when the last tray item occurred |
| `isSeen`            | `Boolean`  | Refference of this Object is seen          |
