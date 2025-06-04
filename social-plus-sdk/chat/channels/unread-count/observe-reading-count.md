# Observe reading count

The SDK provides the startMessageReceiptSync() function to enable the observation of reading/delivered status within the chatroom. It is essential to initiate this functionality to receive real-time updates on message read/delivered counts. If the client doesn't start observing, it won't receive any updates regarding the read/delivered count.

Note: Observing reading status consumes real-time event topics. Therefore, it is recommended to stop observing when the user exits the chatroom using stopMessageReceiptSync().

### Starting Observation

To start observing reading status, call the startMessageReceiptSync() function:

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/98825a7acd668f8019b2810d8a96bd44" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/255c7a568c5e14c68dd7f64f99a617f1" %}
{% endtab %}
{% endtabs %}

This action ensures that the client receives real-time updates on the reading/delivered status of messages in the chatroom.

### Stopping Observation

When the user exits the chatroom or when observation is no longer required, it is crucial to stop observing reading status to conserve resources and prevent unnecessary real-time event consumption. Use the stopMessageReceiptSync() function for this purpose:

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/c0a81b61c644bd69780fe44d7663b0bf" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/eb9b376fde7fe9fe1a974180e0071aa9" %}
{% endtab %}
{% endtabs %}

Stopping observation ensures that the client no longer receives real-time updates on message read/delivered counts.

### Best Practices

* Lifecycle Management: Start observing reading status when the user enters the chatroom and stop observing when the user exits to optimize resource usage.
* Real-time Event Topics: Be mindful that observing reading status consumes real-time event topics, and unnecessary observation can lead to reaching the limit quota to receive real-time events in the SDK.
* Resource Optimization: Stop observation when it is no longer required to conserve resources and improve overall performance.
