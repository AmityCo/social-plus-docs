# Social Home Page

The Social Home Page is the gateway to various social interactions within the application. This page integrates multiple components such as AmityGlobalFeedNavigationComponent, AmityEmptyNewsfeedComponent, AmityNewsfeedComponent, and AmityMyCommunitiesComponent, providing a comprehensive view of the social features available to the user.

<figure><img src="../../../../../.gitbook/assets/Screenshot 2567-07-14 at 13.10.30.png" alt=""><figcaption></figcaption></figure>



### Features <a href="#features" id="features"></a>

| Feature                | Description                                                                                                              |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Global Feed Navigation | Enables users to navigate through different segments of the social platform like newsfeed, explore, my communities, etc. |
| Newsfeed Viewing       | Displays recent posts, updates, and activities from connections and followed communities.                                |
| Community Access       | Quick access to communities the user is part of, with a view to join more.                                               |
| Engagement Options     | Users can like, comment, and interact with posts directly from this page.                                                |

### Customization

<table><thead><tr><th width="320">Config ID</th><th width="122">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>social_home_page/*/*</code></td><td>Page</td><td>You can customize page <code>theme</code></td></tr><tr><td><code>social_home_page/*/newsfeed_button</code></td><td>Element</td><td>You can customize <code>text</code></td></tr><tr><td><code>social_home_page/*/explore_button</code></td><td>Element</td><td>You can customize <code>text</code></td></tr><tr><td><code>social_home_page/*/my_communities_button</code></td><td>Element</td><td>You can customize <code>text</code></td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../../customization/) page.

### Usage <a href="#usage" id="usage"></a>

The AmitySocialHomePage can be implemented in any application to serve as the entry point to social features. Incorporate the AmitySocialHomePage within your app’s UI composition to ensure it is the first component loaded when accessing the social features.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/bd437e0a1ec41eccc76cd58dae751a57" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/8ff2b1bbde1ba699e8f78d77c5fb2e7a" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/d70b8b63bb26958f88ec6eb5857f0623" %}


{% endtab %}

{% tab title="React Native" %}
{% embed url="https://gist.github.com/amythee/8ca969055c904f77851cac166d8c98f2" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/3631a44e305a312fcacace1fec64891d" %}
{% endtab %}
{% endtabs %}

### Navigation Behavior

Custom navigation behavior can be implemented to enhance or modify the interaction flow on the AmitySocialHomePage. This includes overriding default actions to navigate to specific pages like global search or community search based on user interactions.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/904f4ce49f42661f1b59921de7582878" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/62a245b88d792703fa10c2ea3780ab73" %}
{% endtab %}

{% tab title="Web" %}
{% embed url="https://gist.github.com/amythee/abd8cfcd6c0c3b899d3ced73c50428bc" %}


{% endtab %}

{% tab title="React Native" %}
{% embed url="https://gist.github.com/amythee/8ca969055c904f77851cac166d8c98f2" %}
{% endtab %}
{% endtabs %}
