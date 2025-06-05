# Text Message

## Send a Text Message

In a chat application,  it's essential to send text messages to each other in real-time, allowing for quick and easy communication. Users can also view previous messages sent and received within the chat, allowing them to reference past conversations as needed.

The `sendTextMessage` function is a feature provided by the Social Plus chat SDK that enables users to send plain text messages in a [subchannel.md](../../channels/subchannel.md "mention"). This function requires two parameters: `text` and `subchannelId`.&#x20;

Here is a brief explanation of the function parameters:

* `text`: A string that contains the text message that the user wants to send. This parameter is mandatory as it contains the actual message content.
* `subchannelId`: An identifier for the subchannel where the message will be sent. Subchannels are subdivisions within a channel that represent individual topics or chat threads. Messages and interactions occur within subchannels, not the main channel itself.
* `metaData`: Additional properties to support custom fields.
* `tags`: Arbitrary strings that can be used for defining and querying the messages.

<Tabs>
  <Tab title="iOS">
    **Version 6**

    <Frame>
      <img src="https://gist.github.com/amythee/8caf4860ff3c6255b8c4b825e26cc089" />
    </Frame>

    **Version 5 (Maintained)**

    <Frame>
      <img src="https://gist.github.com/amythee/3abe32253b20e25ee4b710942a4f806f" />
    </Frame>
  </Tab>

  <Tab title="Android">
    **Version 6**

    <Frame>
      <img src="https://gist.github.com/amythee/284bdf467ea8fe7a136400d3b13287ea" />
    </Frame>

    **Version 5 (Maintained)**

    <Frame>
      <img src="https://gist.github.com/amythee/6bc19f3db1e24e8a31af236f1823f961" />
    </Frame>
  </Tab>

  <Tab title="JavaScript">
    ```javascript
    import { MessageRepository } from '@amityco/js-sdk';

    const liveObject = MessageRepository.createTextMessage({
      channelId: 'channel1',
      text: 'Hello World!',
    });

    liveObject.on('dataUpdate', message => {
      console.log('message is created', message);
    });
    ```

    When creating a message, we can also pass the `parentId` to make it appear under a parent.

    ```javascript
    import { MessageRepository } from '@amityco/js-sdk';

    const messageLiveObject = MessageRepository.createTextMessage({
      channelId: 'channel1',
      text: 'Hello World!',
      parentId: 'exampleParentMessageId',
      tags: ['tag1', 'tag2'],
      mentionees: [
        {
          "type": "user",
          "userIds": [
            "user1", "user2"
          ]
        }
      ]
    });
    ```
  </Tab>

  <Tab title="TypeScript">
    Version 6

    <Frame>
      <img src="https://gist.github.com/amythee/59381404ca924023929f1042c315b5ae#file-createtextmessage-ts" />
    </Frame>

    Beta (v0.0.1)

    <Frame>
      <img src="https://gist.github.com/f0ccc6a26f58792e70738a026bdfa8ad" />
    </Frame>
  </Tab>

  <Tab title="Flutter">
    <Frame>
      <img src="https://gist.github.com/amythee/cdfb7544aea37943da47bf688266ce6d#file-amitymessagetextcreate-dart" />
    </Frame>
  </Tab>
</Tabs>

<Warning>
  The limit for sending text messages is 10,000 characters per text message. Messages exceeding that limit will return an error and will not be sent.
</Warning>