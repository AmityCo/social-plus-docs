# User Profile Page

The user profile page will display user information, follow relationship, following and followers count, managing blocked user, editing user profile, accept or decline follow request, created post feed and post creation action.

<div><figure><img src="../../../../../.gitbook/assets/p1 (2).png" alt=""><figcaption></figcaption></figure> <figure><img src="../../../../../.gitbook/assets/p2 (1).png" alt=""><figcaption></figcaption></figure> <figure><img src="../../../../../.gitbook/assets/p3.png" alt=""><figcaption></figcaption></figure> <figure><img src="../../../../../.gitbook/assets/p4.png" alt=""><figcaption></figcaption></figure></div>



### Features <a href="#features" id="features"></a>

| **Feature**            | **Description**                                                          |
| ---------------------- | ------------------------------------------------------------------------ |
| User Information       | Display user name, description, following and follower count             |
| Follow Request         | User can accept or decline follow request from other users               |
| User Feed              | Display post, image and video feed posts created by the user             |
| Post Creation          | Allow user to create a post on own timeline                              |
| Other User Information | User can view other user profile and can follow/unfollow/block that user |

### Customization

<table><thead><tr><th width="284">Config ID</th><th width="122">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>user_profile_page/*/*</code></td><td>Page</td><td>You can customize page <code>theme</code></td></tr><tr><td><code>user_profile_page/*/back_button</code></td><td>Element</td><td>You can customize <code>image</code></td></tr><tr><td><code>user_profile_page/*/menu_button</code></td><td>Element</td><td>You can customize <code>image</code></td></tr><tr><td><code>user_profile_page/*/user_feed_tab_button</code></td><td>Element</td><td>You can customize <code>image</code></td></tr><tr><td><code>user_profile_page/*/user_image_feed_tab_button</code></td><td>Element</td><td>You can customize <code>image</code></td></tr><tr><td><code>user_profile_page/*/user_video_feed_tab_button</code></td><td>Element</td><td>You can customize <code>image</code></td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../../customization/) page.

### Usage <a href="#usage" id="usage"></a>

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/8ba539d7f5114d36b413f51aeb73b9e4" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/3afd3a8dbf6c4123aad19e452e1db448" %}


{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/f88dc336226b2f51f5da67045ee8cb29" %}


{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/80609ac73ac07676c6efce16667d6bb3" %}
{% endtab %}
{% endtabs %}

### Navigation Behavior

This page will navigate to other pages. You can override behaviors to navigate to your own pages.

For more details, please refer to the [Overriding Navigation Behavior](https://docs.amity.co/amity-uikit/uikit-v4-beta/customization/overriding-navigation-behaviour) page.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/7080f86b855b7a6c01eb669538a296c1" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/c5bc8c14eb6930d53afdbeacfbdd37d2" %}


{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/80609ac73ac07676c6efce16667d6bb3" %}
{% endtab %}
{% endtabs %}
