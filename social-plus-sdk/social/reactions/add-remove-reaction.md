# Add / Remove Reaction

The Social Plus SDK product also provides functionality for adding and removing reactions on posts. Users can add any number of reactions to a particular post, allowing them to engage with the content more expressive and nuancedly. Additionally, users can also remove reactions that they have added to a post, providing greater control and flexibility over their engagement with the content.

## Add Reaction

The `addReaction` function allows users to add a reaction to a post. The function takes the name of the reaction as a parameter, with a maximum length of 100 characters. The reaction name is case-sensitive, which means that "like" and "Like" are treated as two different reactions.

You can add reactions to a given [reference](./#create-comment) through the `addReaction` method.

* `referenceId` - ID of the post or comment respectively.
* `reactionName` - The name of the reaction that you will remove. Reaction names are case sensitive, i.e. "like" & "Like" are two different reactions.

The `referenceType` parameter specifies where the reaction is applied. Supported values are:

* **`post`**: Adds the reaction to a post.
* **`story`**: Adds the reaction to a story.
* **`content`**: Adds the reaction to other supported content types.

To add a reaction, use the `addReaction` method:

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/67bfd56d56e268c9a23dd8374386e623#file-add_reaction-swift" %}
{% endtab %}

{% tab title="Android" %}
**Add Reaction from Post and Story**

{% embed url="https://gist.github.com/amythee/cc36e27db1f1c1c8882e18476581e9bf" %}

#### Add Reaction from Comment

{% embed url="https://gist.github.com/amythee/9d5ff06a616be7ad0d299e6a38100559" %}
{% endtab %}

{% tab title="JavaScript" %}
The method returns a promise. If the reaction is successfully removed, the method will return `true`. Otherwise, it will return `false` or an error.

{% embed url="https://gist.github.com/amythee/e91fb91a874f1aadff43ab05d6fac48d#file-addreaction-js" %}
{% endtab %}

{% tab title="TypeScript" %}
Version 6

{% embed url="https://gist.github.com/83229aba19155404b9eb064fbf6825fc" %}

Beta (v0.0.1)

{% embed url="https://gist.github.com/9d81fb5be7625d760764d3406809f182" %}
{% endtab %}

{% tab title="Flutter" %}
#### Add Reaction from Post

{% embed url="https://gist.github.com/amythee/b4f039f00725992ecceebe638b208762" %}

#### Add Reaction from Comment

{% embed url="https://gist.github.com/amythee/b16e7e14f5bceb07b115ac420d43a826#file-amityreactioncommentadd-dart" %}
{% endtab %}
{% endtabs %}

## Remove Reaction

Similarly, the `removeReaction` function allows users to remove a previously added reaction from a [reference](./#create-comment). This provides users with greater control over their engagement with the content and allows them to change their minds or update their reactions to the post or comment over time.

You can remove a reaction from a reference by calling `removeReaction`.&#x20;

* `reactionName` - The name of the reaction that you will remove. Reaction names are case sensitive, i.e. "like" & "Like" are two different reactions.
* `referenceId` - ID of the post or comment respectively.

The `referenceType` parameter works similarly here, depending on where the reaction is removed. Supported values are:

* **`post`**: Removes the reaction from a post.
* **`story`**: Removes the reaction from a story.
* **`comment`**: Removes the reaction from a comment.
* **`message`**: Removes the reaction from a message.

To remove a reaction, use the `removeReaction` method:

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/4c0ecfa60b8b2139e7853c05d1b2b3e3#file-remove_reaction-swift" %}
{% endtab %}

{% tab title="Android" %}
#### Remove Reaction from Post and Story

{% embed url="https://gist.github.com/amythee/a38d9429a7de4f3f319dc19888f77ad6" %}

#### Remove Reaction from Comment

{% embed url="https://gist.github.com/amythee/028a6ef0331341363f43f28b0acab6ee" %}
{% endtab %}

{% tab title="JavaScript" %}
The method returns a promise. If the reaction is successfully removed, the method will return `true`. Otherwise, it will return `false` or an error.

{% embed url="https://gist.github.com/amythee/76e0022838d87228405d25891de0ed94#file-removereaction-js" %}
{% endtab %}

{% tab title="TypeScript" %}
Version 6

{% embed url="https://gist.github.com/9a898b74d7fa47b3123bb34c23a50ac7" %}

Beta (v0.0.1)

{% embed url="https://gist.github.com/825b74fcbaeb80539efbafa5c4288c38" %}
{% endtab %}

{% tab title="Flutter" %}
#### Remove Reaction from Post

{% embed url="https://gist.github.com/amythee/3aad1618c44aab5a74519e43292e98a3#file-amityreactionpostremove-dart" %}

#### Remove Reaction from Comment

{% embed url="https://gist.github.com/amythee/3a72bcc5cdbebe27ffb2c01033ef3362#file-amityreactioncommentremove-dart" %}
{% endtab %}
{% endtabs %}
