# Mention in Messages

Mentions allow users to tag other users in messages. It's a powerful tool for fostering engagement and collaboration within your social application. With mentions, users can easily notify specific individuals or groups to new content or important updates. In the SDK, mentions can be implemented in a range of ways, depending on your application's needs and user experience. For more information about mentions, please refer to [mentions.md](../../core-concepts/mentions.md "mention"). We only support the ability to mention in only these channel types:

* Community
* Live&#x20;

## **Create Message with Mentions**

You can easily mention users when creating a message by including their user IDs in the mention user parameter as well as defining metadata for mention rendering. For further explanation, please refer to [#mention-users](../../core-concepts/mentions.md#mention-users "mention"). We offer two types of mentions that can be included in a message:

#### Mention Users

When using this type of mention, up to 30 channel members can be notified through push notifications. Each individual member mentioned in the message will receive a notification.

{% tabs %}
{% tab title="iOS" %}
**Version 6**

{% embed url="https://gist.github.com/amythee/f1aebacfa41a3f6f49968d3b78ec320f" %}

**Version 5 (Maintained)**

{% embed url="https://gist.github.com/amythee/832b9ffeb5c513c010adfd009258b522" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/744ac24bf0756c6919fdd6d1027bef40" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
import { MentionType, MessageRepository, MessageTools } from '@amityco/js-sdk';

MessageRepository.createTextMessage({
  channelId: 'channelId',
  text: 'hi @user1 @user2',
  mentionees: [{ type: MentionType.User, userIds: ['userId1', 'userId2'] }],
  metadata: MessageTools.createMentionMetadata([
    { type: MentionType.User, userId: 'userId1', index: 3, length: 5 },
    { type: MentionType.User, userId: 'userId2', index: 10, length: 5 },
  ]),
});
```
{% endtab %}

{% tab title="TypeScript" %}
Version 6

{% embed url="https://gist.github.com/amythee/0352041d897e661b38ee2fc245ffe0fe#file-createusermention-ts" %}

Beta (v0.0.1)

{% embed url="https://gist.github.com/a0a26122193ce6fd920790480e1760e5" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/a352eb30e135b9ad51f3207ce39d7197#file-amitymessagementionuser-dart" %}
{% endtab %}
{% endtabs %}

#### Mention Channel

By specifying the channel ID in the mention channel parameter when creating a message, push notifications will be sent to all members of that channel when this type of mention is used.

{% tabs %}
{% tab title="iOS" %}
**Version 6**

{% embed url="https://gist.github.com/amythee/43a86c6923fb53fca458831e3f2aff62" %}

**Version 5 (Maintained)**

{% embed url="https://gist.github.com/amythee/e4602df2faab2bb096ecdf64b3665638" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/07b21ddcaa0736bdee673edba41b3b70" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
import { MentionType, MessageRepository, MessageTools } from '@amityco/js-sdk';

MessageRepository.createTextMessage({
  channelId: 'channelId',
  text: 'hi @all',
  mentionees: [{ type: MentionType.Channel }],
  metadata: MessageTools.createMentionMetadata([
    { type: MentionType.Channel, index: 3, length: 3 },
  ]),
});
```
{% endtab %}

{% tab title="TypeScript" %}
Version 6

{% embed url="https://gist.github.com/amythee/d824dff0704ab400c3b01b13c3536f22#file-createallchannelusersmention-ts" %}

Beta (v0.0.1)

{% embed url="https://gist.github.com/e16b55e20d3ce68a02cf4b52b58b8dac" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/1ad6da7f00c2899359014cdcd8ad7582#file-amitymessagementionchannel-dart" %}
{% endtab %}
{% endtabs %}

## **Update Message with Mentions**

We provide developers with an efficient method for updating messages with mentions of specific users, you can easily add mentions to their post updates and but it will not notify the relevant users.&#x20;

To remove mentions you can provide an empty JSON object for the metadata parameter, and an empty list for the mention users parameter. By doing so, You can easily remove mentions from the post content, while ensuring that the overall structure of the post remains intact.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/600a61a557c747b8ce68f47df59b7a4e" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/d3315ddba88f5e15edc6db4e865d0531" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
import { MentionType, MessageRepository, MessageTools } from '@amityco/js-sdk';

MessageRepository.updateMessage({
  messageId: 'messageId',
  data: { text: 'hi @user3' },
  mentionees: [{ type: MentionType.User, userIds: ['userId3'] }],
  metadata: MessageTools.createMentionMetadata([{ type: MentionType.User, userId: 'userId3', index: 3, length: 5 }]),
});
```
{% endtab %}

{% tab title="TypeScript" %}
Version 6

{% embed url="https://gist.github.com/amythee/6c0254f66beed155f2372bc5da36c75e#file-updatemention-ts" %}

Beta (v0.0.1)

{% embed url="https://gist.github.com/f38031e5af7302c90949008b79124d53" %}
{% endtab %}

{% tab title="Flutter" %}
The functionality isn't currently supported by this SDK.
{% endtab %}
{% endtabs %}

## Render Mentions

To render mentions in a supported feature, please refer to [#render-mentions](../../core-concepts/mentions.md#render-mentions "mention"), specifically the section on handling mentions. This documentation provides detailed information on how to represent mentions in your application, including information on metadata structure, custom mention objects, and rendering support.

## **Unread Mention Count**

When a member is mentioned(mention type could be channel as well) in a text message and the message is not rea&#x64;**,** then `hasMention` property is "true" in `Channel` class. Every time the `hasMention` property is true, this means that the member has an unread message with mention(message could be created or updated as well).
