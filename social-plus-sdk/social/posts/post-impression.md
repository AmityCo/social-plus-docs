# Post Impression

The Post Impression feature in our Social Plus SDK is a tool designed to collect valuable data regarding post interactions for analytics and reporting purposes. This feature empowers users to gain insights into how their content is performing and who is actively engaging with it. With this feature, users can mark specific posts as viewed and access information about impressions, reach, and the list of users who have viewed each post.

{% hint style="info" %}
Impressions represent the number of users who viewed the post, while reach represents the number of unique users who viewed the post. Please keep in mind that post-impression data won't be updated in real-time but rather almost in real-time.
{% endhint %}

### Marking a post as viewed

The SDK provides an ability to mark any post as viewed by invoking `markAsViewed()` method within `post.analytics`, which will increase the impression and reach count of specific posts. Additionally, users can easily access the `impression` and `reach` counts directly from the `post` object within the SDK.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/00da1e1106f8472175e6e04eed7e3b78" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/031b390b430831aacd6d396fe455a11f" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/0f593be58130e0bfa4ab657dacc4c245" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/1a5bc855b84b8ad9070b1f331ed37ea0" %}
{% endtab %}
{% endtabs %}

### Query posts reached users

The '`queryReachedUsers`()' function within `UserRepository` provides the ability to query a list of unique users who have viewed the specific story.

This function requires two parameters: viewedType, and viewedId.

Here's an explanation of the function parameters:

* **viewedType**: Represents the type of content that has reached the users. In this case, it is type ‘POST’.
* **viewedId**: Corresponds to the ID of the viewed content. In this case, it is a post.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/9326242f676a678acc01d7b83c2df6ed" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/d1f07175850f656a1fdd48e58200409f" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/5b3dd19991b7fb35871277cf2d5b056e" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/2a7c28bd3c4032cfeeb5c3f7a7075922" %}
{% endtab %}
{% endtabs %}
