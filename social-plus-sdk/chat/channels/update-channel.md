# Update Channel

## Update a Channel

The `updateChannel` function allows users to modify the properties of a channel. This function is useful in cases where a channel's details need to be updated, such as changing the channel's display name or avatar.

The function takes a `channelId` parameter as a required input, which specifies the channel to be modified. Additionally, users can pass in any number of optional parameters to update the channel's properties. These optional parameters include:

* `displayName`: The new display name for the channel.
* `avatarFileId`: A new avatar image for the channel - Used to store ID of image file that represents avatar of the channel. To obtain file ID to set as channel avatar please see [#upload-images](../../core-concepts/files-images-and-videos/image-handling.md#upload-images "mention") section
* `tags`: Arbitrary strings that can be used for define and query for the channels
* `metadata`: Additional metadata to be associated with the channel.

<Info>
`metadata` is implemented with _last writer wins_ semantics: multiple mutations by independent users to the metadata object will result in a single stored value. No locking, merging, or other coordination is performed across multiple writes on the data.
</Info>

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
AmityChannelRepository().updateChannel(channelId, displayName: channelName, avatarFileId: fileId, tags: ["tag1", "tag2"], metadata: ["hello": "world"]) { channel, error in
    // Handle success/error
}
```

```swift
AmityChannelRepository().updateChannel(channelId, displayName: channelName) { channel, error in
    // Handle success/error
}
```
</CodeGroup>
</Tab>

<Tab title="Android">
```kotlin
val channelRepository = AmityChannelRepository(client)
channelRepository.updateChannel(channelId)
    .displayName(channelName)
    .avatarFileId(fileId)
    .tags(listOf("tag1", "tag2"))
    .metadata(mapOf("hello" to "world"))
    .build()
    .submit()
    .observe { channel ->
        // Handle success
    }
```
</Tab>

<Tab title="JavaScript">
```javascript
await ChannelRepository.updateChannel({ 
    channelId: 'channelId', 
    displayName: channelName,
    avatarFileId: fileId,
    tags: ['tag1', 'tag2'],
    metadata: { hello: 'world' }
 })
```
</Tab>

<Tab title="TypeScript">
Version 6

```typescript
await channelRepository.updateChannel({
    channelId: "channelId",
    displayName: "New Channel Name",
    tags: ["tag1", "tag2"]
});
```

Beta (v0.0.1)

```typescript
const channelRepository = new ChannelRepository();
await channelRepository.updateChannel("channelId", {
    displayName: "New Channel Name",
    tags: ["tag1", "tag2"]
});
```
</Tab>

<Tab title="Flutter">
```dart
final channelRepository = AmityChannelRepository();
await channelRepository.updateChannel(
    channelId: channelId,
    displayName: channelName,
    avatarFileId: fileId,
    tags: ['tag1', 'tag2'],
    metadata: {'hello': 'world'},
);
```
</Tab>
</Tabs>