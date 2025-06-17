---
description: >-
  This page provides a list of feeds where users can create posts based on their
  selected story target.
---

# Story Target Selection Page

The Target Selection Page is a crucial component designed to streamline the process of selecting the target audience or community for story and post sharing within the Social Plus UIKit 4.0. This feature allows users to specify where their story will be visible, whether it's a particular community, or to all followers, enhancing the user experience by providing control and flexibility over their content's visibility.

![](<../../../../.gitbook/assets/image (1) (1) (1) (1) (1) (1).png>)

## Features

| Feature                          | Description                                                                                       |
| -------------------------------- | ------------------------------------------------------------------------------------------------- |
| Story creation on community feed | When a user selects a community, UIKit will open Story Creation page with the selected community. |

### Customization

<table><thead><tr><th width="213">Config ID</th><th width="102">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>select_story_target_page/*/*</code></td><td>Page</td><td>You can customize <code>theme</code> </td></tr><tr><td><code>select_story_target_page/*/close_button</code></td><td>Element</td><td>You can customize <code>image</code></td></tr><tr><td><code>select_story_target_page/*/title</code></td><td>Element</td><td>You can customize <code>text</code></td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../customization/) page.

## Usage

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/262a6a86106c23923f8b7ca8df1f70a2" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/6c935d3ba9364ed4495867ef9a8f7385" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/6e77af27da86bc11092aa2949d33572a" %}
{% endtab %}
{% endtabs %}

### Navigation Behavior

The target Selection Page will navigate to other pages based on the user's actions, you can override the behavior to navigate to your own pages.

For more details, please refer to the [Overriding Navigation Behavior](https://docs.amity.co/amity-uikit/uikit-v4-beta/customization/overriding-navigation-behaviour) page.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/6ad347bcb8604eaeb098e5e0eb9aeda6" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/c578dc8dc6bac6c9c637c3e6dce14ad1" %}
{% endtab %}
{% endtabs %}
