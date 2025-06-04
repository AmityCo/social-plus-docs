# Edit and Delete Messages

`AmityMessageRepository` class provides APIs for you to perform actions on messages you've sent or received. These actions include editing and deleting an existing message, as well as marking a message as being read by you. You can only perform edit and delete operations on messages you've sent.&#x20;

## Edit Messages

You can only perform edit and delete operations on your own messages. When editing a message, the message's `editedAtDate` will be set to the current time. This allows you to provide UI to the user to inform the user of specific messages that have been edited, if needed. An optional completion block can be provided to notify you of operation success.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/0796cb023870756d969c672512b3c335" %}
{% endtab %}

{% tab title="Android" %}
Currently, the Chat SDK has only 2 editable data types, `TEXT` and `CUSTOM`

{% embed url="https://gist.github.com/amythee/5b7f4544988dbe9c2cd0deabfab92554" %}
{% endtab %}

{% tab title="JavaScript" %}
To edit the message, you need to pass the following parameters:

* `messageId` (`String`) - ID of the message to edit/update
* `data` (`String`) - new message

```javascript

import { MessageRepository } from '@amityco/js-sdk';
​
try {
  await MessageRepository.updateMessage({ 
    messageId: 'messageId', 
    data: { text: 'new text' },
  );
  console.log('message is updated');
} catch (error) {
  console.error('can not update message', error);
}
```
{% endtab %}

{% tab title="TypeScript" %}
Version 6

{% embed url="https://gist.github.com/amythee/f39c59f76474acf0c6f69bdfa6be05d7#file-updatemessage-ts" %}

Beta (v0.0.1)

{% embed url="https://gist.github.com/7b80ab8ac966cc7a32e35bfa5b518eac" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/b7b6661f0df6798b8ab3715ba756b2e6" %}
{% endtab %}
{% endtabs %}

## Delete Messages

The delete message functionality allows users to remove a message from a chat or messaging application. This feature provides flexibility and control, allowing users to delete messages they no longer wish to be visible to other participants in the conversation.

By utilizing the delete message function, users can remove a specific message from the chat history. This can be useful in various scenarios, such as correcting mistakes, removing sensitive or inappropriate content, or simply managing the flow of the conversation. Once the message is deleted, it may still be shown as a deleted message with timestamp which depends on the [query-and-filter-messages.md](query-and-filter-messages.md "mention") condition.

The delete message function typically requires the `messageId` as a parameter, which uniquely identifies the message to be deleted. Once the message is deleted, it will no longer be visible to other users in the chat or messaging context.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/cf8680a497657db72a5aece59a1bdd79" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/ffef0b02ec93eee8c2ce3b03669addcb" %}
{% endtab %}

{% tab title="JavaScript" %}
For deleting a message, you need to pass the ID of the message to delete.

```javascript

import { MessageRepository } from '@amityco/js-sdk';
​
try {
  await MessageRepository.deleteMessage('messageId');
  console.log('message is deleted');
} catch (error) {
  console.error('can not delete message', error);
}
```
{% endtab %}

{% tab title="TypeScript" %}
Version 6

{% embed url="https://gist.github.com/amythee/d3d50b4075afadea0666eb119d29de34#file-deletemessage-ts" %}

Beta (v0.0.1)

{% embed url="https://gist.github.com/2a809e5888a5d0f1c6221e248be0b529" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/252bf750d3803761412412d7e10f3bda" %}
{% endtab %}
{% endtabs %}
