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

# Community Setting Page

The Community Settings Page is the gateway for changing various settings within the community and updating its profile information. User can leave the community or close the entire community from this page.

<figure><img src="../../../../../.gitbook/assets/Settings.png" alt=""><figcaption></figcaption></figure>

### Features <a href="#features" id="features"></a>

<table data-header-hidden><thead><tr><th width="217"></th><th></th></tr></thead><tbody><tr><td>Feature</td><td>Description</td></tr><tr><td>Editing Profile</td><td>Community profile can be updated through this setting.</td></tr><tr><td>Updating Members</td><td>Adding new members or removing existing members can be done from this setting. It also has the functionality to change role of users within the community.</td></tr><tr><td>Notification Setting</td><td>All notification settings related to a community can be changed here.</td></tr><tr><td>Post Permissions</td><td>Post related permissions can be changed here.</td></tr><tr><td>Story comments</td><td>Story comment permissions can be changed here.</td></tr><tr><td>Leave community</td><td>User can leave the community.</td></tr><tr><td>Close community</td><td>Moderator user can close the entire community. </td></tr></tbody></table>

### Customization

<table><thead><tr><th width="269">Config ID</th><th width="122">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>community_setting_page/*/*</code></td><td>Page</td><td>You can customize page <code>theme</code></td></tr><tr><td><code>community_setting_page/*/edit_profile</code></td><td>Element</td><td>You can customize <code>text</code></td></tr><tr><td><code>community_setting_page/*/members</code></td><td>Element</td><td>You can customize <code>text</code></td></tr><tr><td><code>community_setting_page/*/notifications</code></td><td>Element</td><td>You can customize <code>text</code></td></tr><tr><td><code>community_setting_page/*/post_permission</code></td><td>Element</td><td>You can customize <code>text</code></td></tr><tr><td><code>community_setting_page/*/story_setting</code></td><td>Element</td><td>You can customize <code>text</code></td></tr><tr><td><code>community_setting_page/*/leave_community</code></td><td>Element</td><td>You can customize <code>text</code></td></tr><tr><td><code>community_setting_page/*/close_community</code></td><td>Element</td><td>You can customize <code>text</code></td></tr><tr><td><code>community_setting_page/*/close_community_description</code></td><td>Element</td><td>You can customize <code>text</code></td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../../customization/) page.

### Usage <a href="#usage" id="usage"></a>

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/0c3b39595578b7c2f45e95044f3abfd1" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/4a0f361450ada243fad81a07815b77ce" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/0773526dad2223fdb2bbf615a4f39722" %}


{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/739aaeeda534db84880a41299e7aec65" %}
{% endtab %}
{% endtabs %}

### Navigation Behavior

The Community Profile Page will navigate to each page related to the setting. You can override these behaviors to navigate to your own pages.

For more details, please refer to the [Overriding Navigation Behavior](https://docs.amity.co/amity-uikit/uikit-v4-beta/customization/overriding-navigation-behaviour) page.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/589eaa6e87b216f3efd40f4e7ad17f71" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/569b38bb05415f0e6ae810817534f8fd" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/739aaeeda534db84880a41299e7aec65" %}
{% endtab %}
{% endtabs %}
