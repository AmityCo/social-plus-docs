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

# Reaction List Component

The Reaction List Component displays detailed information about users who have reacted to your post and the specific reactions they have used.

<figure><img src="../../../../.gitbook/assets/Screenshot 2024-07-17 at 1.30.33 PM.png" alt="" width="315"><figcaption></figcaption></figure>

### Features

| Feature       | Description                                              |
| ------------- | -------------------------------------------------------- |
| Reaction List | Users can view the list of user who reacted on the post. |

### Customization

<table><thead><tr><th width="213">Config ID</th><th width="122">Type</th><th>Description</th></tr></thead><tbody><tr><td>*/reaction_list/*</td><td>Theme</td><td>User can customize component theme.</td></tr><tr><td>*/reaction_list/user_avatar_view</td><td>Element</td><td>User can hide avatar image view.</td></tr><tr><td>*/reaction_list/user_display_name</td><td>Element</td><td>User can hide display name.</td></tr><tr><td>*/reaction_list/reaction_image_view</td><td>Element</td><td>User can hide reaction icon.</td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../customization/) page.

### Usage <a href="#usage" id="usage"></a>

The Reaction List Component can be used in the app if you already have an AmityPost object from Social Plus SDK. postId from AmityPost object will be used to initialize the component.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/1d10b0242319018a91440b47af75b38f" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/95bb12b0e79a0fb35593c8ed629c9193" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/17677dcceea5c443f71ee3d3f4dbe9f7" %}
{% endtab %}

{% tab title="React Native" %}
{% embed url="https://gist.github.com/amythee/28f83760eb562da4c163d614a2efa269" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/987bad25e718a10263f1cde3e2e62353" %}
{% endtab %}
{% endtabs %}
