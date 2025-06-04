# Heartbeat Sync

The presence heartbeat is a mechanic to signal the system whether a user is online or offline. The SDK offers two convenient methods that allow users to periodically sync or unsync their presence status with the server. When the server receives a heartbeat sync request, it records the timestamp at the time of the request, designating it as the `lastHeartbeat` timestamp for that user.

The SDK automatically manages the periodic syncing of this heartbeat once the `startHeartbeat` method is called. To cease syncing your presence with the server, the user must invoke the `stopHeartbeat` method.

## Start Heartbeat

Invoke the `startHeartbeat` method in `client.presence` to initiate the heartbeat synchronization process. This method automatically checks the user's presence settings within the network, and if enabled, begins to sync the heartbeat at specified intervals defined in the SDK. The synchronization process is handled automatically, streamlining the user's interaction with the system.

{% hint style="info" %}
The heartbeat sync interval is determined automatically by SDK. Normally you can expect the heartbeat to be synced every 20-30 seconds.
{% endhint %}

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/f8b827d21dc61ad06c334fd2d0df615b" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/1d5a051db2fafb7db00889d12c4fe035" %}
{% endtab %}
{% endtabs %}

## Stop Heartbeat

Utilize the `stopHeartbeat()` method within `client.presence` to cease the heartbeat synchronization process. To restart the sync, you must invoke the `startHeartbeat()` method again.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/29d1fb992dcc40d32c3feef458690f49" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/0cc98b67d7c16ce27a826422ba74c408" %}
{% endtab %}
{% endtabs %}

