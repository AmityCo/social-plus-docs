# Create Post Menu Component

The `AmityCreatePostMenuComponent` provides users with options to create posts or stories, enhancing user engagement by facilitating content creation on community feeds or my timeline. It acts as a gateway for users to navigate to specific content creation flows.



### Features

| Feature      | Description                                                                                                                |
| ------------ | -------------------------------------------------------------------------------------------------------------------------- |
| Create Post  | Allows users to create a new post directly from the component, navigating to a post target selection page.                 |
| Create Story | Enables story creation, directing users to a story target selection page to customize their story’s audience and settings. |

### Customization

<table><thead><tr><th width="320">Config ID</th><th width="122">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>social_home_page/create_post_menu/*</code></td><td>Component</td><td>You can customize component <code>theme</code></td></tr><tr><td><code>social_home_page/create_post_menu/create_post_button</code></td><td>Element</td><td>You can customize <code>text</code> and <code>image</code></td></tr><tr><td><code>social_home_page/create_post_menu/create_story_button</code></td><td>Element</td><td>You can customize <code>text</code> and <code>image</code></td></tr><tr><td><code>social_home_page/create_post_menu/create_poll_button</code></td><td>Element</td><td>You can customize <code>text</code> and <code>image</code></td></tr><tr><td><code>social_home_page/create_post_menu/create_livestream_button</code></td><td>Element</td><td>You can customize <code>text</code> and <code>image</code></td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../../customization/) page.

### Usage <a href="#usage" id="usage"></a>

The AmityCreatePostMenuComponent is designed for straightforward integration into any part of your application that requires user interaction with content creation options. This component is highly versatile, supporting various development scenarios.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/0e56bc4f693fd3beb19da666b03e24b5" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/4449850a598a5ce60f9470a7e5deef75" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/0a764c3486802c810d6515c45ff754c8" %}
{% endtab %}

{% tab title="React Native" %}
{% embed url="https://gist.github.com/amythee/a5976a141516a6fe6e561344a8656286" %}
{% endtab %}

{% tab title="Flutter" %}

{% endtab %}
{% endtabs %}

### Navigation Behavior

The behavior of the AmityCreatePostMenuComponent can be customized to manage how the application navigates upon user actions related to post and story creation. Here’s how you can override the default behavior to ensure that navigation aligns with your application’s specific user flow and business logic:

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/526e258e55d2316e50aa339e2ccb5411" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/9dd421495daa1981003bf950037e7c8c" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/0a764c3486802c810d6515c45ff754c8" %}
{% endtab %}

{% tab title="React Native" %}
{% embed url="https://gist.github.com/amythee/a5976a141516a6fe6e561344a8656286" %}
{% endtab %}
{% endtabs %}
