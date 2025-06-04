# Query and Filter Messages

## Querying Messages

The `getMessages` function is a powerful feature of the chat or messaging SDK that allows users to retrieve messages from a specific subchannel based on various criteria. This function provides flexibility in fetching messages that meet specific requirements. This function returns a [#live-collection](../../core-concepts/live-objects-collections/#live-collection "mention") of messages.

**Filter parameters**

* `subChannelId`: This parameter specifies the ID of the subchannel from which you want to retrieve messages.
* `includingTags[]` (optional): This parameter allows you to filter messages based on specific tags. You can provide an array of tags, and the function will return only the messages that have at least one of the specified tags.
* `excludingTags[]` (optional): Conversely, this parameter allows you to exclude messages that have certain tags. You can specify an array of tags, and the function will exclude messages with any of the specified tags from the result.
* `includeDeleted` (optional): This parameter determines whether to include deleted messages in the result. If set to `true`, the function will include both active and deleted messages. If set to `false`, only active messages will be returned.
* &#x20;`type` (optional): You can filter messages according to their type
  * if no `type` is passed, any message will match
  * if an `AmityMessage.DataType` is passed, query for all messages with the specific type
    * `AmityMessage.DataType.TEXT` for text messages
    * `AmityMessage.DataType.IMAGE` for image messages
    * `AmityMessage.DataType.FILE` for file messages
    * `AmityMessage.DataType.AUDIO` for audio messages
    * `AmityMessage.DataType.VIDEO` for video messages
    * `AmityMessage.DataType.CUSTOM` for custom messages

**Sorting**

In the `getMessages` function, the sorting option allows you to specify how the returned messages should be ordered. There are two available sorting options:

1. `firstCreated`: When you set the sorting option to `firstCreated`, the messages will be ordered in ascending order based on their creation time. This means that the oldest messages will appear first in the returned collection, while the newest messages will be at the end.
2. `lastCreated`: On the other hand, when you choose the `lastCreated` sorting option, the messages will be ordered in descending order based on their creation time. This means that the newest messages will appear first in the returned collection, while the oldest messages will be at the end.

By utilizing the `getMessages` function with these parameters and sorting option, you can retrieve messages from a specific subchannel while applying additional filters based on tags and including or excluding deleted messages. This provides a flexible and efficient way to fetch and manage messages within your chat or messaging application.

{% tabs %}
{% tab title="iOS" %}
**Version 6**

{% embed url="https://gist.github.com/amythee/040057c97b76df7df8f43cc514452a1f" %}

{% embed url="https://gist.github.com/amythee/a6d01874bc38381af94b414f684555ca" %}

**Version 5 (Maintained)**

{% embed url="https://gist.github.com/amythee/87fecde0c5b6ff286262bcc6bb2fd59d" %}

{% embed url="https://gist.github.com/amythee/e15a3dcee35961ffd09ce5d3d1cc475d#file-get_threaded_messages-swift" %}
{% endtab %}

{% tab title="Android" %}
**Version 6**

{% embed url="https://gist.github.com/amythee/f0ec8d303589c528e974133b12c51cd2" %}

**Version 5 (Maintained)**

{% embed url="https://gist.github.com/amythee/4b9ef4177741d376743906589f5a1b06#file-amitymessagefilterquery-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
import { MessageRepository } from '@amityco/js-sdk';
​
const liveCollection = MessageRepository.queryMessages({
  channelId: 'channelId',
  parentId: parentIdValue,
  filterByParentId: true,
  tags: ['summer2021']
  excludeTags: ['awful_hotel']
});
```
{% endtab %}

{% tab title="TypeScript" %}
Version 6&#x20;

{% embed url="https://gist.github.com/amythee/dab8384f3d0cee39775e89d7155d010b#file-querymessages-ts" %}

Beta (v0.0.1)

{% embed url="https://gist.github.com/amythee/2e3f1612ad5f731fe95e3eb342d70a25#file-livemessages-ts" %}

.


{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/5ce897888da3296f244106a25ca8ef1a" %}
{% endtab %}
{% endtabs %}

### Threaded Messages

Querying threaded messages allows users to retrieve the replied (children) messages associated with a specific message thread. When a message serves as the root of a thread, you can use the `parentId` parameter in a message query to fetch its child messages.

To query threaded messages, you can add the following parameters to your message query:

* `parentId`: This parameter specifies the ID of the parent message. By providing the `parentId`, you are indicating that you want to retrieve the child messages associated with that specific parent message.
* `filterByParentId`: This flag enables the filtering of messages based on their parent ID. By setting this flag, the query will only return messages that have the specified `parentId`.

By including the `parentId` parameter and setting the `filterByParentId` flag in your message query, you can retrieve the child messages of a particular message thread. This functionality allows for structured and organized conversations within your chat or messaging application, enabling users to navigate and explore threaded discussions with ease.

{% tabs %}
{% tab title="iOS" %}
**Version 6**

{% embed url="https://gist.github.com/amythee/0cf6ef5a8f974f1bb4ce924cebfca490" %}

**Version 5 (Maintained)**

{% embed url="https://gist.github.com/amythee/e15a3dcee35961ffd09ce5d3d1cc475d#file-get_threaded_messages-swift" %}
{% endtab %}

{% tab title="Android" %}
**Version 6**

{% embed url="https://gist.github.com/amythee/52ec722528d6b13e73f95e07e88a5ea7" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
import { MessageRepository } from '@amityco/js-sdk';

const liveCollection = MessageRepository.queryMessages({
  channelId: 'channel1',
  parentId: 'exampleParentMessageId',
  filterByParentId: true,
});
```
{% endtab %}

{% tab title="TypeScript" %}
Version 6 and Beta (v0.0.1)

{% embed url="https://gist.github.com/amythee/6c39832f2b2fac3f3ec039f6f51e923f#file-querythreadmessages-ts" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/5ce897888da3296f244106a25ca8ef1a" %}
{% endtab %}
{% endtabs %}

### Navigating(Jump) to a specific message

To locate a specific message within a chatroom, you can use the index of the message in the collection if known. However, there may be cases where the desired message, such as a reply to a much older message, is not in the current collection. In such instances, it's essential to perform a message query. The SDK offers an additional parameter for message queries called `aroundMessageId`, which retrieves the target message along with its preceding and following messages.

Using a message query with `aroundMessageId` generates a new live collection. The application's decision to perform data swapping depends on the query's result. Typically, data swapping should not be executed in case of a business error, such as using an invalid target `messageId` or a `messageId` associated with a deleted message for `aroundMessageId`. Upon a successful query, the application can proceed with the source swap, locate the index of the target message, and scroll to that specific position.

In cases where there is a business error but no existing source (e.g., entering a chatroom via push notification), the application can recover by querying for the latest message using a message query without `aroundMessageId`.

After swapping the source, most, if not all, of the messages from the previous source will likely no longer be available in the new one. To enable users to navigate back to the message they jumped from, they can scroll through the pages manually. However, the application can also facilitate this by caching  `messageId` the message they jumped from and offering a floating button as a shortcut to navigate back. This functionality can be achieved by leveraging a message query and using the cached `messageId` as the value for `aroundMessageId`.

{% hint style="info" %}
This feature is available exclusively from version 6.18.0 onwards
{% endhint %}

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/5ab5a320f4d50ce91843482e0d068f7e" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/8d8f5dca7af3955fd1c5eb473782f764" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/5ef6e41037c3d447457c5b7ab6e682fe" %}
{% endtab %}
{% endtabs %}
