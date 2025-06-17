# User Profile Header Component

The User Profile Header component will display user information, follow relationship, following and followers count, and accept or decline follow requests.

<div><figure><img src="../../../../../.gitbook/assets/h1.png" alt="" width="369"><figcaption></figcaption></figure> <figure><img src="../../../../../.gitbook/assets/h2.png" alt=""><figcaption></figcaption></figure></div>

### Features <a href="#features" id="features"></a>

| **Feature**      | **Description**                                              |
| ---------------- | ------------------------------------------------------------ |
| User Information | Display user name, description, following and follower count |
| Follow Request   | User can accept or decline follow request from other users   |

### Customization

<table><thead><tr><th width="273">Config ID</th><th width="122">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>user_profile_page/user_profile_header/*</code></td><td>Component</td><td>You can customize component <code>theme</code></td></tr><tr><td><code>user_profile_page/user_profile_header/follow_user_button</code></td><td>Element</td><td>You can customize <code>text</code> and <code>image</code></td></tr><tr><td><code>user_profile_page/user_profile_header/following_user_button</code></td><td>Element</td><td>You can customize <code>text</code> and <code>image</code></td></tr><tr><td><code>user_profile_page/user_profile_header/following_user_button</code></td><td>Element</td><td>You can customize <code>text</code> and <code>image</code></td></tr><tr><td><code>user_profile_page/user_profile_header/unblock_user_button</code></td><td>Element</td><td>You can customize <code>text</code> and <code>image</code></td></tr><tr><td><code>user_profile_page/user_profile_header/user_following</code></td><td>Element</td><td>You can customize <code>text</code> </td></tr><tr><td><code>user_profile_page/user_profile_header/user_follower</code></td><td>Element</td><td>You can customize <code>text</code> </td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../../customization/) page.

### Usage <a href="#usage" id="usage"></a>

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/e303a34ae645dcf85a59feed242ec33b" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/77ffa2cc77de60ce311391b60e01ea79" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/59925f991871ce04cf82d8b5353b9bbe" %}


{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/4deb89db7d7f81f2b1ae157df929413e" %}
{% endtab %}
{% endtabs %}

### Navigation Behavior

This component will navigate to other pages. You can override behaviors to navigate to your pages.&#x20;

For more details, please refer to the [Overriding Navigation Behavior](https://docs.amity.co/amity-uikit/uikit-v4-beta/customization/overriding-navigation-behaviour) page.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/b015a330d9769e9043e721f2f213a942" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/2d9f10820a29608fe7af65beb06568b9" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/4deb89db7d7f81f2b1ae157df929413e" %}
{% endtab %}
{% endtabs %}
