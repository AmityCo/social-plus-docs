# Live Objects/Collections

Live Objects and Live Collections are observable data holders. The observer gets updated when there is a change of data in the local cache.

There are two main sources that can make changes to the object and collection:

* When an object gets updated by an action from the current device.
* Real-time events of the subscribed objects from the server.

Refer to the platform-specific subpages in this section for an in-depth explanation of how your SDK handles live objects and live collections.

{% hint style="info" %}
By subscribing to a specific topic in the [Real-time event](../realtime-events/) system, users can ensure that they are receiving the most up-to-date information and notifications related to the observed object across devices.
{% endhint %}

## Live Object

Live Object allows users to observe the states of a single object within the app, such as a post, message, or channel. With Live Object, users can automatically receive notifications of any data updates related to the observed object, whether from the network or locally.

Live Object also provides additional states, such as `isLoading` and `error`, which can help understand the status of the observed object and any potential issues that may arise.

Live Object API is designed around the observer design pattern, allowing users to subscribe to an object, receive notifications of any data updates, and unsubscribe when necessary. These updates are delivered via Snapshot, a captured state that is frozen and cannot be changed. Users can own and access these snapshots to stay up-to-date with the latest data within the app.

It's worth noting that while data updates may occur internally within the SDK, these updates will not affect previous snapshots. The only way for users to see the latest data is by getting new snapshots delivered via Live Object updates.

<figure><img src="../../../.gitbook/assets/image (4) (4).png" alt=""><figcaption></figcaption></figure>

## Live Collection

Live Collection allows users to observe changes to an entire collection of data within their app in real-time. Live Collection works similarly to Live Object, with the main difference being that Live Collection notifies changes related to the entire collection rather than just a single object.

To use Live Collection, users can observe changes in a specific collection within the SDK. The collection handler then receives a snapshot of changes since the last result, which includes three possible events:&#x20;

* the indices of the objects that were deleted
* the indices of the objects that were inserted
* the indices of the objects that were modified.

By subscribing to changes on a specific collection using Live Collection, users can stay up-to-date with the latest changes and updates to important collections within the app. This can be particularly helpful for managing large amounts of data or monitoring changes to frequently updated collections, such as messages or posts.

<figure><img src="../../../.gitbook/assets/image (2) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>
