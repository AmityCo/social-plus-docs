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

# Post Details Page

The Post Details Page displays detailed information about a post, including its content, engagements, and comments, using a combination of the [SocialPlusPostContentComponent](https://app.gitbook.com/o/-LC7aYJfVrBgEkQp-YT8/s/r5Wd8I2hK89ISloMqJTq/) and the [SocialPlusCommentTrayComponent](../../comment-and-reaction/comment-tray-component.md).

<figure><img src="../../../../../.gitbook/assets/Screenshot 2024-07-16 at 2.41.41 PM.png" alt="" width="366"><figcaption></figcaption></figure>

### Features <a href="#features" id="features"></a>

| Feature            | Description                                                              |
| ------------------ | ------------------------------------------------------------------------ |
| Engagement Options | Users can like, comment, and interact with post directly from this page. |

### Customization



<table><thead><tr><th width="213">Config ID</th><th width="122">Type</th><th>Description</th></tr></thead><tbody><tr><td>post_detail_page/*/*</td><td>Theme</td><td>User can customize page theme</td></tr><tr><td>post_detail_page/*/back_button</td><td>Element</td><td>User can update back button icon</td></tr><tr><td>post_detail_page/*/menu_button</td><td>Element</td><td>User can update menu button icon</td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../../customization/) page.

### Usage <a href="#usage" id="usage"></a>

The Post Details Page can be used in the app if you already have an AmityPost object from Social Plus SDK. The postId from the AmityPost object is needed to initialize it.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/b2c450e21ee90c124b5fd7c6c18223e5" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/3b8d784369e0bd41fdbd20f370bec422" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/050536a42ab2ebfbc5b6bc243f306f49" %}


{% endtab %}

{% tab title="React Native" %}
{% embed url="https://gist.github.com/amythee/54dc7a4a9622fc95b747022a18e11e77" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/20e5f285ed7f4a80b2762b676539207a" %}
{% endtab %}
{% endtabs %}

### Navigation Behavior

Custom navigation behavior can be implemented to enhance or modify the interaction flow on the AmityPostDetailPage.

For more details, please refer to the [Overriding Navigation Behavior](https://docs.amity.co/amity-uikit/uikit-v4-beta/customization/overriding-navigation-behaviour) page.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/2b8d8fe58f98a4b9e839b31e348050cd" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/fd252cb9f594a8b584bef6c187dfc0ef" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/3845ebf577ac745aaba6d0b3d8f3a5c0" %}
{% endtab %}

{% tab title="React Native" %}
{% embed url="https://gist.github.com/amythee/54dc7a4a9622fc95b747022a18e11e77" %}
{% endtab %}
{% endtabs %}
