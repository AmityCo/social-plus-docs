---
hidden: true
---

# Mark Channel as Read

### Mark Channel as Read

Clearing all unread counts in a channel is a useful feature that allows users to easily keep track of their message history. To accomplish this, the SDK provides a convenient method to mark all messages within a channel as read, effectively clearing the unread count. This method can be called by invoking the `markAsRead()` function on the `ChannelRepository` class with the appropriate `channelId` parameter.

Once called, the function will iterate through all messages in subchannels within the specified channel and mark each as read. This process will clear the unread count.

Please note that clearing unread counts in a channel only applies to the specified channel and does not affect any other channels or subchannels. Additionally, clearing unread counts does not delete any messages or modify their content in any way. It simply updates their status to reflect that they have been read by the user.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/11579eff9f17a096fc1e1533305e5119" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/8dc71eb2167423254cbb00a2448ee9b7" %}
{% endtab %}

{% tab title="TS" %}
{% embed url="https://gist.github.com/caaa923328de89d916bd260908c6737f" %}
{% endtab %}
{% endtabs %}
