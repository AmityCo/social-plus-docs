# Trending and Recommended Communities

By presenting users with a list of trending communities, and recommending communities, the SDK can help to promote a more dynamic and engaging user experience within your app. This can help to foster greater engagement, collaboration, and communication among members, promoting a more supportive and inclusive community atmosphere.

## **Trending Communities**&#x20;

The `getTrendingCommunities` method works by identifying communities that are currently having high levels of members where the user may or may not be part of.&#x20;

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/0df898a7df9c14a2bc0081570b646262#file-query-trending-communities-swift" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/c078c63367a196111b239c3abaab7121#file-amitycommunitytrendingquery-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/8519accd97d6dd55fd18440064424a85#file-gettoptrendingcommunities-js" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/280a812f127a74775b60b60cc7ead451#file-gettoptrendingcommunities-ts" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/1ce677c13dde96bb336dfd41a3063499#file-amitycommunitytrending-dart" %}
{% endtab %}
{% endtabs %}

## **Recommended Communities**

The `getRecommendedCommunities` method works by identifying communities that are currently having high levels of members where the user is not be part of.&#x20;

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/af16b1f87d66fc09817d98683de87769#file-query-recommended-communities-swift" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/c96d7b059984874c7ba138432385c472#file-amitycommunityrecommendedquery-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/056b896a8066e9136fbe40437856f21d#file-getrecommendedcommunities-js" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/95e40871492c5dc56cad1b7d2eccd170#file-getrecommendedcommunities-ts" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/37faa26a2ca713e4d3aadf30a7cf9fb6#file-amitycommunityrecommended-dart" %}
{% endtab %}
{% endtabs %}

{% hint style="info" %}
_**Note**: You can fetch a maximum of 15 items from the trending and recommendation communities at once._
{% endhint %}
