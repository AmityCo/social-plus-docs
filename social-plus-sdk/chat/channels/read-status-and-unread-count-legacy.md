---
description: >-
  For Android, iOS, JS SDK version 6.5.0 and below and TS SDK version
  v0.0.1-beta.42.3
---

# Read Status & Unread Count (Legacy)

### Reading Status and Unread Count <a href="#reading-status-and-unread-count" id="reading-status-and-unread-count"></a>

The `ChannelRepository` object exposes a `totalUnreadCount` property that reflects the number of messages that the current user has yet to read. This count is the sum of all the `unreadCount` channels properties where the user is already a member.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/f1babe34b2f2ed5e4d53fe3773594b10#file-get_unread_count-swift" %}
{% endtab %}

{% tab title="Android" %}
**Version 6**

The `ChannelRepository` provides `getTotalDefaultSubChannelUnreadCount()` method.&#x20;



{% embed url="https://gist.github.com/amythee/b222e54eccc30843c13768116dd95a20" %}

#### Version 5 (Maintained)&#x20;

The `ChannelRepository` provides `getTotalUnreadCount()` method. It's giving the flowable of the number of messages that the current user has yet to read. This count is the sum of all the `unreadCount` channels properties where the user is a member of.

{% embed url="https://gist.github.com/amythee/d8e16d14f7361e9a13794fb1d51539d9#file-amitychannelunreadget-kt" %}



#### Unread Mention

To check whether the current user has been mentioned on one of the unread messages:



#### Version 6

{% embed url="https://gist.github.com/amythee/c953f7b8e4380a6d5892f947eb92535c" %}

#### Version 5 (Maintained)

{% embed url="https://gist.github.com/amythee/a15d8d5680dc345f3ea4258635419d71#file-amitychannelunreadmentionget-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
const liveObject = ChannelRepository.getChannel('channelId');

liveObject.on('dataUpdated', channel => {
  // the number of unread messages
  console.log(channel.unreadCount);
});
```
{% endtab %}

{% tab title="TypeScript" %}
Version 6

The `Channel` object exposes a `unreadCount` property that reflects the number of messages that the current user has yet to read. This count is the sum of all the `unreadCount` channels properties where the user is already a member. It also provides hasMention which is a boolean presenting having a mention for current user in channel.

{% embed url="https://gist.github.com/amythee/a59af04a9616edc6da341671972a0453#file-getchannel-ts" %}
{% endtab %}
{% endtabs %}

The `startReading()` and `stopReading()` methods let the server know that the current user is reading a channel. After the `startReading()`and `stopReading()` methods are called, the `unreadCount` is reset to 0.

You can call both methods as much as you'd like, the SDK takes care of multi-device management: therefore a user can read multiple channels, from one or multiple devices at the same time. In case of an abrupt disconnection (whether because the app was killed, or the internet went down, etc.), the SDK backend will automatically call the `stopReading` on the user's behalf.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/2d1c40e7019d59be978696070fc5eb9e#file-start_and_stop_reading-swift" %}
{% endtab %}

{% tab title="Android" %}
#### Version 6

{% embed url="https://gist.github.com/amythee/b30c00c179a9b70ba07fb2cfb334933a" %}

#### Version 5 (Maintained)

{% embed url="https://gist.github.com/amythee/4bb70caf1169354401f5ce570a9ad7b5#file-amitychannelstartstopreading-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
// start reading a channel
await ChannelRepository.startReading({ channelId: 'channel1' });

// stop reading a channel
await ChannelRepository.stopReading({ channelId: 'channel1' }); 
```
{% endtab %}

{% tab title="TypeScript" %}
Beta (v0.0.1)

This is the legacy feature, for version 6.0.0 and above, please visit [unread-count](unread-count/ "mention").

{% embed url="https://gist.github.com/amythee/48a98ca12b26a939ae524b93e97d8d4e#file-startreading-ts" %}

{% embed url="https://gist.github.com/amythee/844ab8c5c6ec41e2771640db62abb35e#file-stopreading-ts" %}
{% endtab %}
{% endtabs %}

