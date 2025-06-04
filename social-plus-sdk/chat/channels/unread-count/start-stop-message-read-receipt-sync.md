# Start / stop message read receipt sync

To ensure that the message read count is up to date for a channel, users need to start reading the channel. When a user opens a channel, the chat system updates the read count for all messages in that channel, based on the user's reading status. This feature is designed to provide accurate read counts for channels, ensuring that users have a clear understanding of which messages have been read and which are still unread

### Start message read receipt sync

Active syncing read receipt of a channel and letting the chat system know that reading status can update the message read count in that channel. The system will update the read count for all messages in the channel that the user has not yet read.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/98825a7acd668f8019b2810d8a96bd44" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/255c7a568c5e14c68dd7f64f99a617f1" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/f66867f52e9fc76c73c41475149522b0" %}
{% endtab %}
{% endtabs %}

### Stop message read receipt sync

To optimize performance and reduce unnecessary memory consumption, it's important to stop syncing message read receipts before exiting the chatroom page. By halting the read receipt synchronization process, the application can avoid continuing to observe message read statuses when they're no longer relevant. This ensures that system resources are not wasted on monitoring activities that have ceased to be useful, thus enhancing application efficiency and ensuring smoother operation for the user.

{% hint style="info" %}
`stopReading` will be called automatically if the internet connection drops or is disconnected. It lasts for one minute. This means that if an internet connection drops after one minute, `stopReading` will be automatically called, and after it is re-established, `startReading` will be called again.
{% endhint %}

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/c0a81b61c644bd69780fe44d7663b0bf" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/eb9b376fde7fe9fe1a974180e0071aa9" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/5871e8f179132be03a70d9398438efc4" %}
{% endtab %}
{% endtabs %}
