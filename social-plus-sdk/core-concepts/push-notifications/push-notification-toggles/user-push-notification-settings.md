# User Push Notification Settings

The SDK offers push notification settings per user, allowing users to configure whether to enable or disable push notifications for specific feature modules. This configuration applies universally to every device logged in as the same user.&#x20;

Configurable modules include `CHAT`, `SOCIAL`, and `LIVE_STREAM.`

## Get User Push Notification Settings

The SDK provides "`getSettings()`" function within User Notification to inspect the current settings of each feature module.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/be13df0ddc4bdea88e323a23118ae2ae" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/dfae631938e99fa631dedda46542f8a8" %}
{% endtab %}

{% tab title="Flutter" %}
The functionality isn't currently supported by this SDK.
{% endtab %}
{% endtabs %}

## Update Push Notification Settings

The SDK provides "`enable()`" function where user can specify the settings of each module and "`disableAll()`" function where user can choose to disable notifications on every module.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/378f3a1ec6337638ee7ac38ece80d4e6" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/160380953a4389c200fe950554a1ef73" %}
{% endtab %}

{% tab title="Flutter" %}
The functionality isn't currently supported by this SDK.
{% endtab %}
{% endtabs %}

