---
description: >-
  This page provides a list of joined communities that user can create a poll
  post on
---

# Poll Target Selection Page

The Poll Target Selection Page is a crucial component designed to streamline the process of selecting the target audience or community for polling within the Amity UIKit 4.0. This feature allows users to specify where their poll post will be visible, whether it's a particular community, or to all followers, enhancing the user experience by providing control and flexibility over their content's visibility.

<figure><img src="../../../../.gitbook/assets/ptsp.png" alt=""><figcaption></figcaption></figure>

### Features <a href="#features" id="features"></a>

<table data-header-hidden><thead><tr><th width="217"></th><th></th></tr></thead><tbody><tr><td>Feature</td><td>Description</td></tr><tr><td>Post creation</td><td>Select a community or my timeline to create a poll post with the selected target.</td></tr></tbody></table>

### Customization

<table><thead><tr><th width="269">Config ID</th><th width="122">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>select_poll_target_page/*/*</code></td><td>Page</td><td>You can customize page <code>theme</code></td></tr><tr><td><code>select_poll_target_page/*/close_button</code></td><td>Element</td><td>You can customize <code>image</code></td></tr><tr><td><code>select_poll_target_page/*/title</code></td><td>Element</td><td>You can customize <code>text</code></td></tr><tr><td><code>select_poll_target_page/*/my_timeline_text</code></td><td>Element</td><td>You can customize <code>text</code></td></tr></tbody></table>

For more details customization, please refer to [Customization](../../customization/) page.

### Usage <a href="#usage" id="usage"></a>

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/62845311ae958743dd05098f32cd75f6" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/51d5391108df17b1d7993f63d92cd090" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/5a6bc756858f82ea05ef59df9330f2af" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/09d7f94cf648d8ac650f72c8b682d667" %}
{% endtab %}
{% endtabs %}

### Navigation Behavior

Poll Target Selection Page will navigate to poll post composer you can override the behavior to navigate to your own pages.

For more details, please refer to [Overriding Navigation Behavior](https://docs.amity.co/amity-uikit/uikit-v4-beta/customization/overriding-navigation-behaviour) page.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/238aa212aa00c6c377e1d68ef946a5bc" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/a182e7789d08684af5355ad3696363b8" %}
{% endtab %}

{% tab title="Flutter" %}
Will be available soon
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/09d7f94cf648d8ac650f72c8b682d667" %}
{% endtab %}
{% endtabs %}

