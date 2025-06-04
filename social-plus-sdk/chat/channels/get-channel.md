# Get Channel

## Get a Channel

The function allows users to retrieve information about a specific channel using the `channelId` parameter. This function returns a [#live-object](../../core-concepts/live-objects-collections/#live-object "mention") of the `AmityChannel` class, which contains information such as the channel's display name, tags, avatar, and other metadata.

This function is useful for a variety of purposes, such as displaying information about a channel to users or retrieving channel details before joining the channel.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/72ca9286e31921fe3dc55233279b2c0f#file-get_a_channel-swift" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/ba91336c32a8c63fbcf705d7c4cf5c3b" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
const liveChannel = ChannelRepository.getChannel('channel3');

liveChannel.once('dataUpdated', data => {
  ...
});
```
{% endtab %}

{% tab title="TypeScript" %}
Version 6 and Beta (v0.0.1)

{% embed url="https://gist.github.com/amythee/a59af04a9616edc6da341671972a0453#file-getchannel-ts" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/358169d6acb5e4def7ee6b6c1d3ba5df#file-amitychannelview-dart" %}
{% endtab %}
{% endtabs %}
