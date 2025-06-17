# Global Feed Component

The `AmityGlobalFeedComponent` is a central component within the Social Plus platform, designed to aggregate and display a diverse array of posts from the user community. It utilizes the `AmityPostContentComponent` to render individual posts, creating an engaging newsfeed experience. This component not only enhances user interaction by providing a seamless scroll through various types of posts but also serves as a reflection of the community’s activity, showing everything from user updates to broader community announcements.&#x20;



### Features

| Feature            | Description                                                                               |
| ------------------ | ----------------------------------------------------------------------------------------- |
| Post List          | Displays recent posts, updates, and activities from connections and followed communities. |
| Engagement Options | Users can like, comment, and interact with posts directly from this page.                 |

### Customization

<table><thead><tr><th width="320">Config ID</th><th width="122">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>social_home_page/global_feed_component/*</code></td><td>Component</td><td>You can customize component <code>theme</code></td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../../customization/) page.

### Usage <a href="#usage" id="usage"></a>

The AmityGlobalFeedComponent is designed for easy integration across various platforms, enabling a consistent user experience by displaying a global feed of posts.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/c365ef4c6563ebdb5c33a68726617edd" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/056368d1a2ffa2ff4541dd672144e632" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/e0a7d7e7556c1be449ef98324fe36975" %}
{% endtab %}

{% tab title="React Native" %}
{% embed url="https://gist.github.com/amythee/3ec04da66a931c826f471ef50a90c7b9" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/f4358451f4e7cbc8b80b15b4b118dd03" %}
{% endtab %}
{% endtabs %}

### Navigation Behavior

The behavior of the AmityGlobalFeedComponent can be customized to handle navigation to the post detail page differently. Here’s how you can override the default behavior:

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/7fa90748f75d364802e691962698c1d8" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/b90b3cee1c80fcb51d7b2e6ce51e3aaa" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/e0a7d7e7556c1be449ef98324fe36975" %}
{% endtab %}

{% tab title="React Native" %}
{% embed url="https://gist.github.com/amythee/3ec04da66a931c826f471ef50a90c7b9" %}
{% endtab %}
{% endtabs %}
