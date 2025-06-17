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

# Community Membership Page

The Community Membership Page will provide the complete user-related information in a community.\
Adding a new user into the community, removing a user, or updating the roles of the users can be done on this page.

<div><figure><img src="../../../../.gitbook/assets/m1.png" alt=""><figcaption></figcaption></figure> <figure><img src="../../../../.gitbook/assets/m2.png" alt=""><figcaption></figcaption></figure> <figure><img src="../../../../.gitbook/assets/m3.png" alt=""><figcaption></figcaption></figure></div>

### Features <a href="#features" id="features"></a>

<table data-header-hidden><thead><tr><th width="217"></th><th></th></tr></thead><tbody><tr><td>Feature</td><td>Description</td></tr><tr><td>Adding new members</td><td>New members can be added into the community.</td></tr><tr><td>Removing existing members</td><td>Existing members can be removed from the community.</td></tr><tr><td>Updating user roles</td><td>Roles of the users within the community can be updated.</td></tr><tr><td>Reporting the user</td><td>Report other community members.</td></tr></tbody></table>

### Customization

<table><thead><tr><th width="269">Config ID</th><th width="122">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>community_membership_page/*/*</code></td><td>Page</td><td>You can customize page <code>theme</code></td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../customization/) page.

### Usage <a href="#usage" id="usage"></a>

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/14ece6636cd9bf745e763a8f87f1969a" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/8328c322ed56661f1d11195e3f1b6bce" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/1f62c3c99c0abfdd7eb22cf602f8cfee" %}


{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/6a2c4c5a70d475151ed7ff920df4dcb7" %}
{% endtab %}
{% endtabs %}

### Navigation Behavior

a This page will navigate to add a user page and user profile page. You can override behaviors to navigate to your own pages.

For more details, please refer to the [Overriding Navigation Behavior](https://docs.amity.co/amity-uikit/uikit-v4-beta/customization/overriding-navigation-behaviour) page.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/a1edec673350438a1e4d47fb0c31e6fd" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/3a9de57a320cc1fdda8ce5b2611f9441" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/6a2c4c5a70d475151ed7ff920df4dcb7" %}
{% endtab %}
{% endtabs %}
