# Story Impressions

The Story Impressions feature is a tool designed to collect valuable data regarding story interactions for analytics and reporting purposes. This feature empowers users to gain insights into how their content is performing and who is actively engaging with it. With this feature, users can mark specific stories as seen and access information about impressions, reach, and the list of users who have viewed each story.

{% hint style="info" %}
Impressions represent the number of users who viewed the story, while reach represents the number of unique users who viewed the story. Please keep in mind that story impression data won't be updated in real-time but rather almost in real-time.
{% endhint %}

## Mark Seen

The '`markAsSeen()`' function in the Social Plus SDK serves to increase the impression and reach count of specific stories while promptly updating the 'isSeen' state of the story.

{% hint style="info" %}
Info: In order to mark a story as seen, that story must be in sync state "SYNCED".
{% endhint %}

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/d52f430b549d5964d7a812982983368e" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/e3e713c0700176c6e59544d905d70c33" %}
{% endtab %}

{% tab title="TS" %}
{% embed url="https://gist.github.com/amythee/9322005527105af8aea5b9cf0367ca7c" %}
{% endtab %}
{% endtabs %}

## Mark Link Clicked

The '`markLinkAsClicked()`' function in the AmitySDK serves to increase the CTR of specific stories.

{% hint style="info" %}
Info: In order to mark a story as seen, that story must be in sync state "SYNCED".
{% endhint %}

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/25a703e8166237e0f38ec51ac5123c4b" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/5f433318dfbdb2e2a6cc7f5bee5617b2" %}
{% endtab %}

{% tab title="TS" %}
{% embed url="https://gist.github.com/amythee/1bc335a8f4d1ab2325c2e4d79314744c" %}
{% endtab %}
{% endtabs %}

## Query Story Reached Users

The '`queryReachedUsers`()' function within `UserRepository` provides the ability to query a list of unique users who have viewed the specific story.

This function requires two parameters: viewedType, and viewedId.

Here's an explanation of the function parameters:

* **viewedType**: Represents the type of content that has reached the users. In this case, it is type ‘STORY’.
* **viewedId**: Corresponds to the ID of the viewed content. In this case, it is storyId.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/b811aee488970afda8d217bcfe3ebef3" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/438f44bec769b0f3cf7ff78a1d11ce19" %}
{% endtab %}

{% tab title="TS" %}
{% embed url="https://gist.github.com/amythee/c4434d34b259ccb5bef94c569088618f" %}
{% endtab %}
{% endtabs %}
