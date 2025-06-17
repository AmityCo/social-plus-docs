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

# Post Composer Page

The Post Composer Page enables users to create and edit post by inputting text content and attaching media and files. It uses [AmityMediaAttachmentComponent](https://app.gitbook.com/o/-LC7aYJfVrBgEkQp-YT8/s/-MX0mOAVWkotGme0iRzu/~/changes/3277/amity-uikit/uikit-v4-beta/social/post-composer-page/media-attachment-component) and [AmityDetailedMediaAttachmentComponent](https://app.gitbook.com/o/-LC7aYJfVrBgEkQp-YT8/s/-MX0mOAVWkotGme0iRzu/~/changes/3277/amity-uikit/uikit-v4-beta/social/post-composer-page/detailed-media-attachment-component) to attach media and files.

<figure><img src="../../../../../.gitbook/assets/Screenshot 2024-07-17 at 3.04.03 PM.png" alt="" width="340"><figcaption></figcaption></figure>

### Features <a href="#features" id="features"></a>

| Feature          | Description                                                                           |
| ---------------- | ------------------------------------------------------------------------------------- |
| Post Composition | User can create a post with text content, images, videos and files by attaching them. |
| Post Editing     | User can edit a existing post by using this page in edit mode.                        |

### Customization

<table><thead><tr><th width="261">Config ID</th><th width="122">Type</th><th>Description</th></tr></thead><tbody><tr><td>post_composer_page/*/*</td><td>Theme</td><td>User can customize page theme.</td></tr><tr><td>post_composer_page/*/close_button</td><td>Element</td><td>User can update close button icon.</td></tr><tr><td>post_composer_page/*/community_display_name</td><td>Element</td><td>User can hide community name on navigation bar.</td></tr><tr><td>post_composer_page/*/create_new_post_button</td><td>Element</td><td>User can change wording of post button on navigation bar.</td></tr><tr><td>post_composer_page/*/edit_post_button</td><td>Element</td><td>User can change wording of save button on navigation bar if this page is used as edit mode for editing post.</td></tr><tr><td>post_composer_page/*/edit_post_title</td><td>Element</td><td>User can change navigation title appeared in the edit mode.</td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../../customization/) page.

### Usage <a href="#usage" id="usage"></a>

The Post Composer page can be used in two modes, creation mode to create a new post and editing mode to edit the existing post.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/52e882fb9cc731aa5f8ecdbdcc102409" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/080eabe5d6f6e1ad23b2f8eb185795da" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/06b6518371f112ae762f6cd5fed70577" %}
{% endtab %}

{% tab title="React Native" %}
{% embed url="https://gist.github.com/amythee/b3efac9e475a0ffd382607b6b5184ae1" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/69181da436dc63192ba0ea9bc888ca17" %}
{% endtab %}
{% endtabs %}

### Navigation Behavior

Custom navigation behavior can be implemented to enhance or modify the interaction flow on the AmityPostComposerPage.

For more details, please refer to the [Overriding Navigation Behavior](https://docs.amity.co/amity-uikit/uikit-v4-beta/customization/overriding-navigation-behaviour) page.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/eb7d4f19377622ab6e30df8bf2169cb5" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/be70698b41419f55e06688d95242af4e" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/06b6518371f112ae762f6cd5fed70577" %}
{% endtab %}

{% tab title="React Native" %}
{% embed url="https://gist.github.com/amythee/b3efac9e475a0ffd382607b6b5184ae1" %}
{% endtab %}
{% endtabs %}
