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

# Pending Post Page

The pending post page will have the list of posts needed to be reviewed. Moderator of the community can review the pending posts.

<figure><img src="../../../../../.gitbook/assets/p1 (1).png" alt=""><figcaption></figcaption></figure>

### Features <a href="#features" id="features"></a>

<table data-header-hidden><thead><tr><th width="217"></th><th></th></tr></thead><tbody><tr><td>Feature</td><td>Description</td></tr><tr><td>Pending Posts</td><td>Moderator can review the pending posts to accept or decline. If the user is not a moderator, the list will be the user's own posts needed to be reviewed. </td></tr></tbody></table>

### Customization

<table><thead><tr><th width="269">Config ID</th><th width="122">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>pending_posts_page/*/*</code></td><td>Page</td><td>You can customize page <code>theme</code></td></tr><tr><td><code>pending_posts_page/*/back_button</code></td><td>Element</td><td>You can customize <code>image</code></td></tr><tr><td><code>pending_posts_page/*/title</code></td><td>Element</td><td>You can customize <code>text</code></td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../../customization/) page.

### Usage <a href="#usage" id="usage"></a>

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/3ff85f84e9e7861f7ac446c7a2ed6bbe" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/eda118afcd18feff46bc8be25c01967d" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/a744aa6b07f01d784bff6841da6c28b7" %}
{% endtab %}
{% endtabs %}
