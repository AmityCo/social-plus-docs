---
layout:
  title:
    visible: true
  description:
    visible: false
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
---

# Community Notification Setting Page

The Community Notification Setting Page is the main page to change the notification settings within the community.

<div><figure><img src="../../../../../../.gitbook/assets/Notifications copy.png" alt=""><figcaption></figcaption></figure> <figure><img src="../../../../../../.gitbook/assets/Notifications.png" alt=""><figcaption></figcaption></figure></div>

### Features <a href="#features" id="features"></a>

<table data-header-hidden><thead><tr><th width="217"></th><th></th></tr></thead><tbody><tr><td>Feature</td><td>Description</td></tr><tr><td>Allow notification</td><td>User can turn the community notification on and off. </td></tr></tbody></table>

### Customization

<table><thead><tr><th width="269">Config ID</th><th width="122">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>community_notification_page/*/*</code></td><td>Page</td><td>You can customize page <code>theme</code></td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../../../customization/) page.

### Usage <a href="#usage" id="usage"></a>

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/fdeaf93b84a1610b9089e32632b57f7a" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/cf8480190c9a0f3e3c4fc4048f4aae49" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/a17fa631d76fd991264a5a242f7feb47" %}


{% endtab %}
{% endtabs %}

### Navigation Behavior

This page will navigate to dedicated notification setting pages of posts, comments, and stories. You can override the behaviors to navigate to your own pages.

For more details, please refer to the [Overriding Navigation Behavior](https://docs.amity.co/amity-uikit/uikit-v4-beta/customization/overriding-navigation-behaviour) page.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/da78e68988412f468487c5d5c6c5f2f4" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/160dc511427e388763b07ae6d4082274" %}
{% endtab %}
{% endtabs %}
