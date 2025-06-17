# Blocked User Page

The Blocked User Page displays a list of users blocked by the current user, the user can unblock other users from here.

<figure><img src="../../../../.gitbook/assets/b1.png" alt=""><figcaption></figcaption></figure>

### Features <a href="#features" id="features"></a>

<table data-header-hidden><thead><tr><th width="217"></th><th></th></tr></thead><tbody><tr><td>Feature</td><td>Description</td></tr><tr><td>Blocked Users</td><td>Display a list of blocked users</td></tr><tr><td>Unblock User</td><td>User can unblock other user</td></tr></tbody></table>

### Customization

<table><thead><tr><th width="306">Config ID</th><th width="122">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>blocked_users_page/*/*</code></td><td>Page</td><td>You can customize page <code>theme</code></td></tr><tr><td><code>blocked_users_page/*/back_button</code></td><td>Element</td><td>You can customize <code>image</code></td></tr><tr><td><code>blocked_users_page/*/title</code></td><td>Element</td><td>You can customize <code>text</code></td></tr><tr><td><code>blocked_users_page/*/unblock_user_button</code></td><td>Element</td><td>You can customize <code>text</code></td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../customization/) page.

### Usage <a href="#usage" id="usage"></a>

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/a2031742a254a27c542211342e17f7f8" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/b6eab4bb39ea962fb5b997833f0bc890" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/59928b755afdc9321a482d65b4edbabe" %}
{% endtab %}
{% endtabs %}

### Navigation Behavior

This page will navigate to other pages. You can override behaviors to navigate to your pages.

For more details, please refer to the [Overriding Navigation Behavior](https://docs.amity.co/amity-uikit/uikit-v4-beta/customization/overriding-navigation-behaviour) page.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/d04161282a756c2490fc2859130d3118" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/a72b9721e3c616b1b18f1f9f5aab5073" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/59928b755afdc9321a482d65b4edbabe" %}
{% endtab %}
{% endtabs %}
