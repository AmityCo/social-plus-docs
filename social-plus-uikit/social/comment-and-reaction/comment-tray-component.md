---
description: This component provide viewing comment, creating and editing, adding reaction.
---

# Comment Tray Component

The Comment Tray Component in Social Plus UIKit 4.0 facilitates a dynamic interaction layer for users to engage with stories or posts through comments and reactions. This customizable component is designed to foster community engagement and conversation directly within the content viewing experience.

<div data-full-width="false"><figure><img src="../../../../.gitbook/assets/image (152).png" alt=""><figcaption></figcaption></figure> <figure><img src="../../../../.gitbook/assets/image (151).png" alt=""><figcaption></figcaption></figure> <figure><img src="../../../../.gitbook/assets/image (153).png" alt=""><figcaption></figcaption></figure></div>

### Features

| View, create or edit comments | User can view, create or edit text comments or reply comments, can also add reaction to comment. |
| ----------------------------- | ------------------------------------------------------------------------------------------------ |

### Customization

<table><thead><tr><th width="355">Config ID</th><th width="124">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>*/edit_comment_component/*</code></td><td>Component</td><td>You can customize <code>theme</code> </td></tr><tr><td><code>*/edit_comment_component/cancel_button</code></td><td>Element</td><td>You can customize <code>button_text</code>, <code>icon</code> and <code>background_color</code></td></tr><tr><td><code>*/edit_comment_component/save_button</code></td><td>Element</td><td>You can customize <code>button_text</code>, <code>icon</code> and <code>background_color</code></td></tr><tr><td><code>*/comment_tray_component/*</code></td><td>Component</td><td>You can customize <code>close_icon</code></td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../customization/) page.

### Usage

{% tabs %}
{% tab title="iOS" %}
For iOS applications, integrating the Comment Tray Component involves initializing it with a reference ID (such as a story or post ID) and specifying the reference type. Here's a simple example:

{% embed url="https://gist.github.com/amythee/6dbe47b376d965f78e84462efc28fd65" %}

This snippet sets up the comment tray for a specific story, ready to be incorporated into the app’s UI through a SwiftUI hosting controller.
{% endtab %}

{% tab title="Android" %}
On Android, the Comment Tray Component is utilized within a Composable function, offering customization options such as enabling or disabling interactions and comments:

{% embed url="https://gist.github.com/426780aff8b9a7c9e2534df24100b321" %}

This code demonstrates how to integrate the component within a Compose UI, providing flexibility in configuring interaction capabilities.
{% endtab %}

{% tab title="Web (React)" %}
```
import React from 'react';
import { AmityStoryTabComponent } from '@amityco/ui-kit';

const CommunityStoriesTab = ({ communityId }) => {
  return (
    <AmityStoryTabComponent type={{ communityFeed: communityId }} />
  );
};

export default CommunityStoriesTab;
```

In this example, we define a functional component called `CommunityStoriesTab` that takes a `communityId` prop. Inside the component, we render the `AmityStoryTabComponent` and pass the `communityId` as the value for the `communityFeed` property within the `type` prop.
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/cdb423e8726992d26f011f0420a3645f" %}
{% endtab %}
{% endtabs %}
