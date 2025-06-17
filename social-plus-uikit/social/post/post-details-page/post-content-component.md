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

# Post Content Component

The Post Content Component displays information about a post, including its content and engagements.

<figure><img src="../../../../../.gitbook/assets/Screenshot 2024-07-17 at 11.34.27 AM.png" alt="" width="375"><figcaption></figcaption></figure>

### Customization

<table><thead><tr><th width="213">Config ID</th><th width="122">Type</th><th>Description</th></tr></thead><tbody><tr><td>*/post_content/*</td><td>Theme</td><td>User can customize component theme.</td></tr><tr><td>*/post_content/moderator_badge</td><td>Element</td><td>User can change icon and wording of Moderator Badge.</td></tr><tr><td>*/post_content/timestamp</td><td>Element</td><td>User can hide timestamp.</td></tr><tr><td>*/post_content/menu_button</td><td>Element</td><td>User can change icon of menu button.</td></tr><tr><td>*/post_content/reaction_button</td><td>Element</td><td>User can change reaction button icon and wording.</td></tr><tr><td>*/post_content/comment_button</td><td>Element</td><td>User can change comment button icon and wording.</td></tr><tr><td>*/post_content/share_button</td><td>Element</td><td>User can change share button icon and wording.</td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../../customization/) page.

### Usage <a href="#usage" id="usage"></a>

The Post Content Component can be used in the app if you already have an AmityPost object from Social Plus SDK.&#x20;

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/65e5a7dde7deee76e93a7e2624e242a9" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/9d3a0a0eba4bb6d39171ee6b98e7ddbe" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/b2935b60715e01825c9a58a636322f0a" %}
{% endtab %}

{% tab title="React Native" %}
{% embed url="https://gist.github.com/amythee/1f58d75e6a2c28030889829970748307" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/31f09b1d3ba8c82c390070e4364c4e82" %}
{% endtab %}
{% endtabs %}

### Navigation Behavior

Custom navigation behavior can be implemented to enhance or modify the interaction flow on the AmityPostContentComponent.

For more details, please refer to the [Overriding Navigation Behavior](https://docs.amity.co/amity-uikit/uikit-v4-beta/customization/overriding-navigation-behaviour) page.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/d3cfa869a3eaa49806b73e44957ade4c" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/e7c75e6dde0532689ec176d00767cfef" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/b2935b60715e01825c9a58a636322f0a" %}
{% endtab %}

{% tab title="React Native" %}
{% embed url="https://gist.github.com/e7c75e6dde0532689ec176d00767cfef" %}
{% endtab %}
{% endtabs %}
