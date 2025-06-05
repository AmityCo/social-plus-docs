# Community Push Notification Settings

The SDK offers push notification settings per community, allowing users to configure which notification events should be enabled on the community. This configuration applies universally to every device logged in as the same user.

Configurable events include `POST_CREATED`, `POST_REACTED`, `COMMENT_CREATED`, `COMMENT_REACTED`, `COMMENT_REPLIED`, `STORY_CREATED`, `STORY_REACTED`, `STORY_COMMENT_CREATED`, LIVESTREAM`_START`

## Get Community Push Notification Settings

The SDK provides "`getSettings()`" function within Community Notification to inspect which notification events are enabled on the community.

{% tabs %}
{% tab title="iOS" %}
<Embed url="https://gist.github.com/amythee/925c4470c6ecf110b7de4a7f7ab1d508"/>
{% endtab %}

{% tab title="Android" %}
<Embed url="https://gist.github.com/amythee/73a153e9d84d32e6739d19299797a9cc"/>
{% endtab %}

{% tab title="Flutter" %}
The functionality isn't currently supported by this SDK.
{% endtab %}
{% endtabs %}

## Update Community Push Notification Settings

The SDK provides "`enable()`" function where user can choose which notification events to be enabled on the community and "`disable()`" function to disable all notification events on the community.

{% tabs %}
{% tab title="iOS" %}
<Embed url="https://gist.github.com/amythee/88ef088d70bfa97c5c9a807ed47f1678"/>
{% endtab %}

{% tab title="Android" %}
<Embed url="https://gist.github.com/amythee/7838f75ff18921274834c1e12e446d62"/>
{% endtab %}

{% tab title="Flutter" %}
The functionality isn't currently supported by this SDK.
{% endtab %}
{% endtabs %}

