# Presence State

## Overview

The presence state is a vital aspect of any modern application, acting as a driving factor for engagement products by showing the user's current availability. The Social Plus SDK supports both observing and notifying the presence of users, analogous to being online and observing users' online statuses.

## Presence Setting

Social Plus SDK offers specific methods that allow the logged-in user to enable, disable, or query about presence settings. When these presence settings are enabled, the user is prepared to synchronize their presence state with the server.

Users can enable or disable their presence state feature. Disabled users will be considered offline and cannot use any presence-related functionalities. Network-level settings can also affect this feature.

{% hint style="info" %}
The presence State feature is disabled by default at both the network and user levels. Please consult with the Social Plus Team to enable this feature on the network level.
{% endhint %}

### Enable Presence Status

The SDK user can invoke the `enable()` method within `client.presence` to activate their presence status.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/c3e8f897e9fe2b9f4e59868fdc9fa3f2" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/d974935855e6cc02f40f85558ff13bcf" %}
{% endtab %}
{% endtabs %}

### Disable Presence Status

The SDK user can invoke the `disable()` method within `client.presence` to deactivate their presence status. When disabled, the user will be unable to sync both their own heartbeat and the presence of other users in the network. This action also halts any ongoing heartbeat synchronization processes.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/c249711586e2013025db540851f61444" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/3a78a68125cb848d7eb93cb232ea2861" %}
{% endtab %}
{% endtabs %}

### Query Presence Status

The SDK user can invoke the `isEnabled()` method within `client.presence` to check their presence status. This method also determines if the presence state feature is available for the app. If unavailable, `isEnabled()` returns `false`. If the feature is available, the method checks the user-level settings, which are managed through the `enable()` and `disable()` methods as previously described.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/0363c416e1676598fa3e14e90e2b972f" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/1a9bcb62fa6a8f6f9817945bbd47c6b0" %}
{% endtab %}
{% endtabs %}
