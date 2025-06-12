# Mark Message as Read

Marking a message as read is a crucial functionality to update the read count and provide an accurate representation of the user's interaction with messages. The SDK provides a method to manually mark a specific message as read.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
```swift
let messageID = "message_id"
SendbirdChat.markAsRead(channelURL: channelURL, messageID: messageID) { error in
    guard error == nil else {
        // Handle error
        return
    }
    // Message marked as read successfully
}
```
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
```kotlin
val messageId = "message_id"
SendbirdChat.markAsRead(channelUrl, messageId) { error ->
    if (error != null) {
        // Handle error
        return@markAsRead
    }
    // Message marked as read successfully
}
```
    </CodeGroup>
  </Tab>
  <Tab title="TS">
    <CodeGroup>
```typescript
const messageId = "message_id";
await SendbirdChat.markAsRead(channelUrl, messageId);
```
    </CodeGroup>
  </Tab>
</Tabs>

This action should be taken when entering the chat room or a new message appears in the chatroom UI, and the user has viewed the message.

To maintain accuracy in the read count, it is recommended to mark only the latest message as read. This ensures that the counts reflect the user's most recent interaction with the chat.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
```swift
channel.getMessages { messages, error in
    guard error == nil else {
        // Handle error
        return
    }
    
    if let latestMessage = messages?.first {
        SendbirdChat.markAsRead(channelURL: channel.channelURL, messageID: latestMessage.messageId)
    }
}
```
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
```kotlin
channel.getMessages { messages, error ->
    if (error != null) {
        // Handle error
        return@getMessages
    }
    
    messages?.firstOrNull()?.let { latestMessage ->
        SendbirdChat.markAsRead(channel.url, latestMessage.messageId)
    }
}
```
    </CodeGroup>
  </Tab>
  <Tab title="TS">
    <CodeGroup>
```typescript
const messages = await channel.getMessages();
if (messages.length > 0) {
    await SendbirdChat.markAsRead(channel.url, messages[0].messageId);
}
```
    </CodeGroup>
  </Tab>
</Tabs>