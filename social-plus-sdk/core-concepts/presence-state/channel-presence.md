# Channel Presence

The SDK also provides a way to query & sync the presence of members of the conversation channel. This allows you to create a UI that displays the presence status of other members in the conversation channel. Example: A green dot to indicate whether another user is online or offline in the conversation channel.

In SDK, channel presence is represented by `AmityChannelPresence` object. This object contains 3 properties.

| Property          | Remarks                                                                   |
| ----------------- | ------------------------------------------------------------------------- |
| channelId         | Id of the Channel                                                         |
| userPresences     | AmityUserPresence object for members whose presence state has been synced |
| isAnyMemberOnline | If any user's (except you) lastHeartbeat has been within last 60 seconds  |

## Sync & Unsync Channel Presence

The SDK also offers the functionality to query and synchronize the presence of members within a conversation channel. This enables the creation of a user interface that displays the presence status of other members in the channel, such as using a green dot to indicate whether a user is online or offline within a specific conversation. In the SDK, channel presence is represented by the `AmityChannelPresence` object, which contains three properties.

### Sync Channel Presence

The SDK includes the `syncChannelPresence(id,viewId)` method in the `AmityChannelPresenceRepository` class to synchronize the presence of members within a conversation channel. This method adds the specified ID to the list of channel IDs whose members' presence will be synced, and this process occurs periodically at a predetermined interval. To observe the results of this syncing process, use the `getSyncingChannelPresence()` method. When the presence information for the currently syncing channel members is obtained, it is published through the observer returned by the `getSyncingChannelPresence()` method. More details can be found in the [#observe-channel-presence](channel-presence.md#observe-channel-presence "mention") section.

When displaying a list of conversation channels, it is advisable to use this method. The observer offers a class named `AmityChannelPresence` that holds the presence information for the channel's members. Likewise, the `unsyncChannelPresence(id, viewId)` method should be used to stop syncing the presence state when a list item is no longer visible, ensuring that the maximum sync limit is never reached.

{% hint style="info" %}
Only syncing of the Conversation channel type is supported! The maximum number of channel IDs that can be synced at a time is 20. If the count exceeds this limit, the SDK will log an error message to the console. To remove a channel ID from the list, use the `unsyncChannelPresence(id, viewId`) method.
{% endhint %}

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/ef9b3d3e66a4db062271a84d7709be8c" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/15297b8e41ca4a05b90a09434be8b599" %}
{% endtab %}
{% endtabs %}

This `syncChannelPresence(id, viewId)` method also provides an optional `viewId` parameter. `viewId` is the unique id of the view that this user id is tied to. In most cases, you do not need to specify any value to this parameter. `viewId` is useful if you want to bind the same channel id to multiple views on the same screen. In that case, When you unsync channel presence in one view, it won't affect presence syncing for the same channel id in another view.

{% hint style="info" %}
SDK will log a message in the console in case of any error that occurs during the syncing process.
{% endhint %}

### Unsync Channel Presence

The SDK offers the `unsyncChannelPresence(id, viewId)` method to cease syncing the presence of a particular conversation channel. If the channel ID is unsynced, the SDK will remove it from the list of channel IDs whose members are currently being synced. Consequently, the observer returned by the `getSyncingChannelPresence()` method will no longer contain information about this channel. This method includes an optional `viewId` parameter and operates similarly to the `syncChannelPresence(id, viewId)` method.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/c3a308c34ff1a4ceeb878413dd0e17bc" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/a7afb802d25fa7e963b8aa078e3bc07b" %}
{% endtab %}
{% endtabs %}

The SDK includes a convenient method, `unsyncAllChannelPresence()`, to stop syncing all channels that are currently being monitored. This feature is particularly useful when the application no longer requires information about the channels being synced. For example, this method can be called when a user navigates to a different screen that has no dependence on the previously synced channels, allowing for an efficient transition between different parts of the application.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/9c7ce6d1254940c24bf4bdb6eb78b99d" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/965450fe5f8c6f42be5cb0f06060bb32" %}
{% endtab %}
{% endtabs %}

## Observe Channel Presence

After adding the channels to sync, the next step is observing the user presence. The SDK provides an observer through the `getSyncingChannelPresence()` method. Whenever presence information is fetched for channels synced through the `syncChannelPresence(id, viewId)` method, that information is published through this observer.

**Accessing Channel Presence:**

* The observer returned from `getSyncingChannelPresence()`

Whenever presence information is updated, the observer will provide an array of `[AmityChannelPresence]` for the channels that are being synced. Users must map `AmityChannelPresence` from this array to the view where this information is to be displayed

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/82d3c8d44cf89fc3cd4c5f9def54449a" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/8f6789b0fc5fc522ff90f7c8edb94de0" %}
{% endtab %}
{% endtabs %}
