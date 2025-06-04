# Chat Realtime Events

In the context of channels, subchannels, and message collections, receiving real-time events is an automatic process for **conversation and community** channels; you do not need to perform any additional actions. However, a live channel still needs to be established.

Similar to the process for social real-time events, a topic is a unique path that must be constructed for each model you wish to receive updates about in real-time. The SDK offers helper methods for creating these topics for each model type. Each topic includes an events enum that developers can select to subscribe to, based on their business context and preferences.

To receive updates from a channel or any content created within that channel, the user must hold a 'Member' status within that channel. Once the user leaves the channel, they will no longer receive real-time events.

### Subchannel Topic

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/e2942c227c355a8139073eb140c90155#file-subscribe_subchannel-swift" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/b498c3659a273eb08dc8c210c7d38f64" %}
{% endtab %}

{% tab title="JavaScript" %}
We don't support this feature in JS SDK.
{% endtab %}

{% tab title="TypeScript" %}
Version 6 and Beta(v0.0.1)

{% embed url="https://gist.github.com/amythee/7ec2e92438c22a432eceaf411a06f701#file-subscribesubchannel-ts" %}
{% endtab %}

{% tab title="Flutter" %}
The functionality isn't currently supported by this SDK.
{% endtab %}
{% endtabs %}
