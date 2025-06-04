# Mention in Comment

Mentions allow users to tag other users in comments. It's a powerful tool for fostering engagement and collaboration within your social application. With mentions, users can easily notify specific individuals or groups to new content or important updates. In the SDK, mentions can be implemented in a range of ways, depending on your application's needs and user experience. For more information about mentions, please refer to [mentions.md](../../core-concepts/mentions.md "mention").

## **Create Comment with Mentions**

You can easily mention users when creating a comment by including their user IDs in the mention user parameter as well as defining metadata for mention rendering. For further explanation, please refer to [#mention-users](../../core-concepts/mentions.md#mention-users "mention").

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/19d2ef314ff3dc862372c45a9a9e9c48" %}

{% embed url="https://gist.github.com/amythee/462ab10479cb6fca4d6df05d3317c8c0" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/5a761f4f5273556ada9e4f9d11a15511" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/04e63c4ad13ee0dfdf174c7157ac8d5d#file-createcomment-js" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/4dd325324015b0e8b2b7fc4338054616" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/8ba20704ecf3a127497a54c4db57a3e7" %}
{% endtab %}
{% endtabs %}

## **Update Comment with Mentions**

We provide developers with an efficient method for updating comments with mentions of specific users, you can easily add mentions to their post updates and but it will not notify the relevant users.&#x20;

To remove mentions you can provide an empty JSON object for the metadata parameter, and an empty list for the mention users parameter. By doing so, You can easily remove mentions from the post content, while ensuring that the overall structure of the post remains intact.:

{% tabs %}
{% tab title="iOS" %}
To update a comment/reply with mentions, this is the method in `AmityCommentEditor`:

{% embed url="https://gist.github.com/amythee/6fdb78fe358e762befe92c49e4205fe1#file-edit_comment_with_mention_api-swift" %}

{% embed url="https://gist.github.com/amythee/ddd40c78a450b7a63ed73a91056f78b5" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/35278b96395fb7d2eabf36e1a11a74a9" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/b769f4661499b4a76a60a9f0a4a59eb1#file-createcomment-js" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/b6892e44c9b68bef93cd5a371708d20e" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/94844f30c4d620f7d432969e83aff13e" %}
{% endtab %}
{% endtabs %}

## Render Mentions

To render mentions in a supported feature, please refer to [#render-mentions](../../core-concepts/mentions.md#render-mentions "mention"), specifically the section on handling mentions. This documentation provides detailed information on how to represent mentions in your application, including information on metadata structure, custom mention objects, and rendering support.
