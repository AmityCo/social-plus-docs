# Custom Message

## Send a Custom Message

If you'd like to display content on your app that cannot be represented by the available text, image, video, and file message types, you can create your own custom message type. Custom message type allows you to include the necessary data for rendering, such as additional metadata and custom data formatting. This is useful if you want to present specific types of content to your users.&#x20;

Here is a brief explanation of the function parameters:

* `data`: A free-form JSON object that can be customized based on your use cases.
* `subchannelId`: An identifier for the subchannel where the message will be sent. Subchannels are subdivisions within a channel that represent individual topics or chat threads. Messages and interactions occur within subchannels, not the main channel itself.
* `tags` - Arbitrary strings that can be used for defining and querying for the messages.

{% tabs %}
{% tab title="iOS" %}
**Version 6**

{% embed url="https://gist.github.com/amythee/03798ae631b17d41f625175ba6a5f6da" %}

**Version 5 (Maintained)**

{% embed url="https://gist.github.com/amythee/dfffa4ca5ec7de1a32d230422bac497b" %}
{% endtab %}

{% tab title="Android" %}
**Version 6**

{% embed url="https://gist.github.com/amythee/4bab7cfc226e8e10d6541beb090e6041" %}

**Version 5**

{% embed url="https://gist.github.com/amythee/0b30d9457a2b8648349faf6889155d3d#file-amitymessagecustomcreation-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
{% code overflow="wrap" %}
```javascript
import { MessageRepository, MessageType } from '@amityco/js-sdk';

const messageLiveObject = MessageRepository.createMessage({
  channelId: 'channel1',
  type: MessageType.Custom,
  data: {
    customField1: 'customValue1',
    customField2: 'customValue2',
  }
  tags: ['tag1', 'tag2'],
  mentionees: [{type: 'user', userIds: ['user1', 'user2']}],
});
Previous
Audio Message
Next
Viewing Mesages
```
{% endcode %}
{% endtab %}

{% tab title="TypeScript" %}
Version 6

{% embed url="https://gist.github.com/amythee/e7ead8cff10b8ce354a86db59bb8c4d8#file-createcustommessage-ts" %}

Beta (v0.0.1)

{% embed url="https://gist.github.com/1205276223b81a8cb5aa6b6f13b3eb1d" %}
{% endtab %}
{% endtabs %}
