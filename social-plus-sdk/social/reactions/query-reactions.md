# Query Reactions

To further facilitate the management of reactions in your app, the Social Plus SDK product includes a `getReactions` method that allows you to retrieve information about a specific reaction or all reactions on a comment and post.

Using this method, you can fetch detailed information about:

* The user who made the reaction.
* The timestamp of the reaction.
* Any additional metadata associated with the reaction.

This feature helps analyze community sentiment and gain insights into the types of content that resonate with the users.

To query `getReactions` you'll need to simply provide `referenceType` and `referenceId` to query specific types of reactions. For further information regarding reaction reference types, please see - [#create-comment](./#create-comment "mention").

The `referenceType` parameter determines the type of reference for which reactions are queried. Supported values are:

* **`post`**: Retrieves reactions for a post.
* **`story`**: Retrieves reactions for a story.
* **`comment`**: Retrieves reactions for a comment.
* **`message`**: Retrieves reactions to a message.

To query reactions, provide both the `referenceType` and `referenceId`. If you'd like to filter by a specific reaction type, provide the `reactionName` as well.

To query all reactions for a post:

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/1bef06f426a2111b1e813070641b8ca1#file-create_reaction_repository-swift" %}

{% embed url="https://gist.github.com/amythee/2faed56b67b193f21f03cad198e3e775#file-query_reactions-swift" %}
{% endtab %}

{% tab title="Android" %}
#### Query Reaction from Post and Story

{% embed url="https://gist.github.com/amythee/7eb599535699cb59293a0526dfc78565" %}

#### Query Reaction from Comment

{% embed url="https://gist.github.com/amythee/98aaa981f3a49c414b7fc1e12bb2158f" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/6352b136da223bef701a2ad8edb1b708#file-queryreactions-js" %}

Each post, comment, message has a set of fields providing detailed info about reactions.&#x20;

* `reactionsCount` - how many reactions the post has
* `myReactions` - list of reactions you added to the post
* `reactions` - map that tells how many reactions of a certain type a post has

{% embed url="https://gist.github.com/amythee/96d0a5a3ebe596045ce8929da1c9233e#file-reactiondata-js" %}
{% endtab %}

{% tab title="TypeScript" %}
Version 6

{% embed url="https://gist.github.com/amythee/9aaf99dcbd8a409b0d4ee6385194093b#file-livereactions-ts" %}

Beta(v0.0.1)

{% embed url="https://gist.github.com/amythee/4c6f28231439a60d290d6c9495ef2715#file-queryreactions-ts" %}
{% endtab %}

{% tab title="Flutter" %}
#### Query Reaction from Post

{% embed url="https://gist.github.com/amythee/4952a13a22bdb16b2adb9e289123aab6#file-amityreactionpostquery-dart" %}

#### Query Reaction from Comment

{% embed url="https://gist.github.com/amythee/960394ce8afa5c8436a18ac58dd9eaa2#file-amityreactioncommentquery-dart" %}
{% endtab %}
{% endtabs %}
