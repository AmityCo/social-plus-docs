---
description: This component displays a list of filtered communities.
---

# Community Search Result Component

The Community Search Result Component is an essential element of the Global Search Page, providing a clear and organized display of communities that match your search keywords. Once you enter a keyword into the Top Search Bar, this component dynamically updates to show a list of relevant communities, complete with brief descriptions and key details. Each community in the search results is presented in an easy-to-read format, allowing you to quickly assess and decide which groups you want to explore further. This component is designed to enhance your search experience by making it simple to find and join communities that align with your interests and goals.

<div align="center" data-full-width="false"><figure><img src="../../../../../.gitbook/assets/image (1).png" alt="" width="375"><figcaption></figcaption></figure></div>



### Features <a href="#features" id="features"></a>

<table data-header-hidden><thead><tr><th width="217"></th><th></th></tr></thead><tbody><tr><td>Feature</td><td>Description</td></tr><tr><td>Communities list</td><td>A list of communities matching to search keyword</td></tr></tbody></table>

### Customization

<table><thead><tr><th width="308">Config ID</th><th width="121">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>social_global_search_page/community_search_result/*</code></td><td>Component</td><td>You can customize component <code>theme</code></td></tr><tr><td><code>social_global_search_page/community_search_result/community_private_badge</code></td><td>Element</td><td>You can customize <code>icon</code>.</td></tr><tr><td><code>social_global_search_page/community_search_result/community_official_badge</code></td><td>Element</td><td>You can customize <code>icon</code>.</td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../../customization/) page.

### Usage <a href="#usage" id="usage"></a>

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/e5160d215b5a26be5d91cbb1d6281e88" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/3772b820749808df479b52f0da340018" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/86c94ccd3f084540c3224bf881da6c94" %}
{% endtab %}

{% tab title="React Native" %}
{% embed url="https://gist.github.com/amythee/1c885a98ffdc94f5f3336e477ffce9d6" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/54af818483558c55afe6ca3f3499bc18" %}
{% endtab %}
{% endtabs %}

### Navigation Behavior

When a user clicks on a community in the search results, they are seamlessly navigated to the community's profile page. This page provides detailed information about the community, including posts, members, and activities. This intuitive navigation ensures that users can quickly and effortlessly explore and engage with the communities they are interested in.

For more details, please refer to the [Overriding Navigation Behavior](https://docs.amity.co/amity-uikit/uikit-v4-beta/customization/overriding-navigation-behaviour) page.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/9b3e9e0722521459082a9eab8cebc280" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/a0f2074468cb26d8189e59b08a0cc903" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/86c94ccd3f084540c3224bf881da6c94" %}
{% endtab %}

{% tab title="React Native" %}
{% embed url="https://gist.github.com/amythee/1c885a98ffdc94f5f3336e477ffce9d6" %}
{% endtab %}
{% endtabs %}
