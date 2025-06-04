# Get Channels

SDK now supports querying channels based on provided channel IDs. The `ChannelRepository` class includes a `getChannels` method that takes an array of channel IDs as input and returns a live collection of channels. This live collection will contain all the channels that are being queried in the first page. This live collection will not support pagination.

Any update to the channels present in this live collection will be automatically notified to the user. Furthermore,

* This live collection will only contain valid channels. In case of invalid channels (such as user gets banned etc.) the list may exclude those channels.
* If any channel id is invalid, live collection will throw error.

{% hint style="info" %}
💡 The maximum number of channel that can be queried is 100.
{% endhint %}

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/d1e815829343ff614437fc381d3ab56c" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/c91b1fb9681e4d9706ace0ec2278478e" %}
{% endtab %}
{% endtabs %}

**Limitations:**

If the channel is not public and user leaves the channel, the channel will still remain in the live collection until user refresh or resets the live collection.
