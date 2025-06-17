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

# Community Profile Page

The Community Profile Page is the main page of a community where all announcement posts, pinned posts, regular posts, and stories created within the community are stored. This page also allows users with the necessary permissions to create posts and stories in the community.&#x20;

<div><figure><img src="../../../../../.gitbook/assets/p1.png" alt=""><figcaption></figcaption></figure> <figure><img src="../../../../../.gitbook/assets/p2.png" alt=""><figcaption></figcaption></figure></div>

### Features <a href="#features" id="features"></a>

<table data-header-hidden><thead><tr><th width="299"></th><th></th></tr></thead><tbody><tr><td>Feature</td><td>Description</td></tr><tr><td>Community Post Feed</td><td>All posts created within the community can be seen in the feed.</td></tr><tr><td>Pinned Posts</td><td>Pin  tab is the place where all pinned posts can be seen.</td></tr><tr><td>Announcement Posts</td><td>Announcement posts will be displayed on top of community post feed at the first tab.</td></tr><tr><td>Image Feed</td><td>Image tab is the one that consolidate all the image posted in the community.</td></tr><tr><td>Video Feed</td><td>Video tab will have all video posted in the community.</td></tr><tr><td>Pending Posts</td><td>User with moderator permission can review all pending posts in the community if post are needed to be reviewed.</td></tr></tbody></table>

### Customization

<table><thead><tr><th width="269">Config ID</th><th width="122">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>community_profile_page/*/*</code></td><td>Page</td><td>You can customize page <code>theme</code></td></tr><tr><td><code>community_profile_page/*/back_button</code></td><td>Element</td><td>You can customize <code>image</code></td></tr><tr><td><code>community_profile_page/*/menu_button</code></td><td>Element</td><td>You can customize <code>image</code></td></tr><tr><td><code>community_profile_page/community_pin/community_create_post_button</code></td><td>Element</td><td>You can customize <code>image</code></td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../../customization/) page.

### Usage <a href="#usage" id="usage"></a>

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/0f52668e22ddfa91960dbfe6a7b8bf65" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/f0fc02e9aa6d3800faca45dd412e7667" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/658da55e5cab8ffc2189cc5121237703" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/db38f1c0021364e0da2162d20af7924b" %}
{% endtab %}
{% endtabs %}

### Navigation Behavior

The Community Profile Page will navigate to the post composer page, story creation page, pending post page, community membership page, community setting page, and post detail page. You can override the behavior to navigate to your own pages.

For more details, please refer to the [Overriding Navigation Behavior](https://docs.amity.co/amity-uikit/uikit-v4-beta/customization/overriding-navigation-behaviour) page.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/08900b47f3aa80ef915ee71d8ef78ac0" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/a9e59a1d9cd599631ea035eb6513465b" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/db38f1c0021364e0da2162d20af7924b" %}
{% endtab %}
{% endtabs %}
