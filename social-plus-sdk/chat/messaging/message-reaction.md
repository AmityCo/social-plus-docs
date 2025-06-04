---
description: >-
  Interactions are more fun when you can express yourself! Let users react using
  emojis, stickers, or thumbs up to messages.
---

# Message Reaction

<figure><img src="../../../.gitbook/assets/image (5) (1) (1) (3).png" alt=""><figcaption></figcaption></figure>

The Social Plus SDK product also provides functionality for adding and removing reactions to messages. Users can add any number of reactions to a particular message, allowing them to engage with the content in a more expressive and nuanced way. Additionally, users can also remove reactions that they have added to a message, providing greater control and flexibility over their engagement with the content.

## Add Reaction

The `addReaction` function allows users to add a reaction to a message. The function takes the name of the reaction as a parameter, with a maximum length of 100 characters. The reaction name is case-sensitive, which means that "like" and "Like" are treated as two different reactions.

You can add reactions to a given [reference](../../social/reactions/#create-comment) through the `addReaction` method.

* `referenceId` - ID of the message.
* `reactionName` - the name of the reaction that you will remove. Reaction name is case sensitive, i.e. "like" & "Like" are two different reactions.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/1e20f8c7c11e8bc7079907f0eaed0a52" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/24cd18296df656d9a73d73bb5b0d6b98" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
try {
  const isAdded = await MessageRepository.addReaction({
    messageId: 'messageId', 
    reactionName: 'love',
  });
  
  if (isAdded) {
    console.log('reaction is added');
  }
} catch (error) {
  console.error('can not add reaction', error);
}
```

###
{% endtab %}

{% tab title="TypeScript" %}
Version 6

{% embed url="https://gist.github.com/amythee/05034754d42afde2deca9aceb465f17c#file-addreaction-ts" %}

Beta

{% embed url="https://gist.github.com/5022a25d98f47ad9a6ae98caf94e4254" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/d8881198e9354aabc189143cb84e4b28#file-amityreactionmessageadd-dart" %}
{% endtab %}
{% endtabs %}

## Remove Reaction

Similarly, the `removeReaction` function allows users to remove a previously added reaction from a [reference](../../social/reactions/#create-comment). This provides users with greater control over their engagement with the content and allows them to change their minds or update their reactions to the message over time.

You can remove a reaction from a reference by calling `removeReaction`.&#x20;

* `reactionName` - the name of the reaction that you will remove. Reaction name is case sensitive, i.e. "like" & "Like" are two different reactions.
* `referenceId` - ID of the message.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/26e1ba1e0c3eed4d60aa4745e8ebda70" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/05fc334828d93aec40d44f08025ce62b" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
try {
  const isRemoved = await MessageRepository.removeReaction({
    messageId: 'messageId', 
    reactionName: 'love',
  });
  
  if (isRemoved) {
    console.log('reaction is removed');
  }
} catch (error) {
  console.error('can not remove reaction', error);
}
```
{% endtab %}

{% tab title="TypeScript" %}
Version 6

{% embed url="https://gist.github.com/amythee/d45eddce90548d565da157666aa12f85#file-removereaction-ts" %}

Beta (v0.0.1)

{% embed url="https://gist.github.com/1afa3631156d3a1b9e03a0e078143c8a" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/33be722beb06c9fb68af44c656e2aec1#file-amityreactionmessageremove-dart" %}
{% endtab %}
{% endtabs %}

## Reaction Query

To further facilitate the management of reactions in your app, the Chat SDK product includes a `getReactions` method that allows you to retrieve information about a specific reaction or all reactions on a message.

Using this method, you can fetch detailed information about a particular reaction, including the user who made the reaction, the timestamp of the reaction, and any additional metadata associated with the reaction. This can be useful for analyzing the sentiment of the community and gaining insights into the types of content that are resonating with your users.

To query `getReactions` you'll need to simply provide `referenceType` and `referenceId` to query specific types of reactions. For further information regarding reaction reference types, please see - [#create-comment](../../social/reactions/#create-comment "mention").

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/5c1d82fe6207b2c8e17483423e33e1fa" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/9c9683cf7e37f569cec13fe17e1d2592" %}
{% endtab %}

{% tab title="JavaScript" %}
Supported ✅ (please wait while we prepare a real example!)
{% endtab %}

{% tab title="TypeScript" %}
Version 6 and Beta(v0.0.1)

{% embed url="https://gist.github.com/amythee/78ed3ecb141585261a9347a45b611a34#file-queryreactions-ts" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/d8881198e9354aabc189143cb84e4b28#file-amityreactionmessageadd-dart" %}
{% endtab %}
{% endtabs %}
