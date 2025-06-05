# Reply to a Message

In addition to creating top-level messages, Social Plus Chat SDK also allows you to reply to existing messages. To reply to a message, you'll need to specify the parent messages `parentMessageId` as one of the parameters. This allows the SDK to associate the new message as a reply to the parent comment.

Similar to creating a top-level message, you can use the SDK's optimistic creation feature to create a reply message.

<Tabs>
  <Tab title="iOS">
    **Version 6**

    <Embed url="https://gist.github.com/amythee/5a24fec8ae07856463201f3e7b1a1b00" />

    **Version 5 (Maintained)**

    <Embed url="https://gist.github.com/amythee/2b2db3ab91f252f723e942ccf2d6482a" />
  </Tab>

  <Tab title="Android">
    **Version 6**

    <Embed url="https://gist.github.com/amythee/7197d3c152436d5c00893771c5ad85cf" />

    **Version 5 (Maintained)**

    <Embed url="https://gist.github.com/amythee/14df5d319f9c9b999d7cab6e04198def#file-amitymessagereply-kt" />
  </Tab>

  <Tab title="JavaScript">
    ```javascript
    import { MessageRepository } from '@amityco/js-sdk'

    const message = { ... };

    MessageRepository.createTextMessage({
      channelId: 'channelId',
      text: 'reply message',
      parentId: message.messageId
    });
    ```
  </Tab>

  <Tab title="TypeScript">
    Version 6

    <Embed url="https://gist.github.com/amythee/7a980b5ca8225838ab3b51507a36f26c#file-replymessage-ts" />

    Beta (v0.0.1)

    <Embed url="https://gist.github.com/7737ac58ff0479b7eb0dc60199b3b74a" />
  </Tab>

  <Tab title="Flutter">
    <Embed url="https://gist.github.com/amythee/15d2f575d9e3a9badf6a2c63bec0c901" />
  </Tab>
</Tabs>