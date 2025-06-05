# Subchannel

Subchannels are part of a channel. They are separate topics or chat threads inside a channel. Messages can be sent and received in subchannels. By default, a channel generates a main subchannel once it's created. You can create, update, delete, and query subchannels inside a channel. For the structure and relationship of channels and subchannels, please visit.

<Info>
Limitations:

* Sub-channel creation is supported for `Conversation` and `Community` channel types.
* Users can create up to 300 sub-channels per channel.
</Info>

### **Create Subchannel**

In the concept of channels and subchannels, a channel is a primary container that can hold multiple subchannels. Creating a subchannel will serve as a thread where users can send messages and participate in discussions related to a specific thread. The subchannel creation function requires two parameters: `channelId` and `displayName`.

* `channelId`: specifies the unique identifier of the parent channel where the subchannel will be created. This allows the SDK to link the subchannel to the correct parent channel, and organize it within the proper hierarchy.
* `displayName`: Specifies the public name or label of the subchannel that will be visible to users.

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
let channelId = "channelId"
let displayName = "displayName"

let subchannelRepository = AmitySubchannelRepository(client: client)
subchannelRepository.createSubChannel(channelId: channelId, displayName: displayName) { subchannel, error in
    if let error = error {
        // Handle error
        return
    }
    // Handle success
}
```
</CodeGroup>
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
val channelId = "channelId"
val displayName = "displayName"

val subchannelRepository = AmitySubchannelRepository(client)
subchannelRepository.createSubChannel(channelId, displayName).subscribe({ subchannel ->
    // Handle success
}, { error ->
    // Handle error
})
```
</CodeGroup>
</Tab>

<Tab title="JavaScript">
We don't support this feature in JS SDK.
</Tab>

<Tab title="TypeScript">
Version 6

<CodeGroup>
```typescript
const channelId = "channelId";
const displayName = "displayName";

const subchannelRepository = new SubchannelRepository(client);
const subchannel = await subchannelRepository.createSubchannel(channelId, displayName);
```
</CodeGroup>

Beta (v0.0.1)

<CodeGroup>
```typescript
const channelId = "channelId";
const displayName = "displayName";

const subchannelRepository = new SubchannelRepository(client);
const subchannel = await subchannelRepository.createSubchannel({
    channelId,
    displayName
});
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
<CodeGroup>
```dart
final channelId = "channelId";
final displayName = "displayName";

final subchannelRepository = AmitySubchannelRepository(client: client);
try {
    final subchannel = await subchannelRepository.createSubChannel(
        channelId: channelId,
        displayName: displayName,
    );
    // Handle success
} on AmityException catch (e) {
    // Handle error
}
```
</CodeGroup>
</Tab>
</Tabs>

### **Update Subchannel**

When you update a subchannel's properties, the changes will be reflected for all users who are members of that subchannel. Please note that the `updateSubChannel` function only updates the properties of the subchannel itself, and does not affect any messages or other content that has been sent within the subchannel.

The function requires two parameters: `subchannelId` and `displayName`.

* `subhannelId`: This is the unique identifier of the subchannel that you'd like to update.
* `displayName`: This is the updated public name or label of the subchannel that will be visible to users.

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
let subchannelId = "subchannelId"
let displayName = "displayName"

let subchannelRepository = AmitySubchannelRepository(client: client)
subchannelRepository.updateSubChannel(subchannelId: subchannelId, displayName: displayName) { subchannel, error in
    if let error = error {
        // Handle error
        return
    }
    // Handle success
}
```
</CodeGroup>
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
val subchannelId = "subchannelId"
val displayName = "displayName"

val subchannelRepository = AmitySubchannelRepository(client)
subchannelRepository.updateSubChannel(subchannelId, displayName).subscribe({ subchannel ->
    // Handle success
}, { error ->
    // Handle error
})
```
</CodeGroup>
</Tab>

<Tab title="JavaScript">
We don't support this feature in JS SDK.
</Tab>

<Tab title="TypeScript">
Version 6

<CodeGroup>
```typescript
const subchannelId = "subchannelId";
const displayName = "displayName";

const subchannelRepository = new SubchannelRepository(client);
const subchannel = await subchannelRepository.updateSubchannel(subchannelId, displayName);
```
</CodeGroup>

Beta (v0.0.1)

<CodeGroup>
```typescript
const subchannelId = "subchannelId";
const displayName = "displayName";

const subchannelRepository = new SubchannelRepository(client);
const subchannel = await subchannelRepository.updateSubchannel({
    subchannelId,
    displayName
});
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
<CodeGroup>
```dart
final subchannelId = "subchannelId";
final displayName = "displayName";

final subchannelRepository = AmitySubchannelRepository(client: client);
try {
    final subchannel = await subchannelRepository.updateSubChannel(
        subchannelId: subchannelId,
        displayName: displayName,
    );
    // Handle success
} on AmityException catch (e) {
    // Handle error
}
```
</CodeGroup>
</Tab>
</Tabs>

### **Delete Subchannel**

The `subchannelId` parameter specifies the ID of the subchannel that you'd like to delete. The `hardDelete` parameter is a boolean value that determines whether to perform a hard delete or a soft delete.

A soft delete will mark the subchannel as deleted but keep its data in the system. A hard delete will immediately and permanently delete the subchannel and all its data from the system.

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
let subchannelId = "subchannelId"
let hardDelete = true

let subchannelRepository = AmitySubchannelRepository(client: client)
subchannelRepository.deleteSubChannel(subchannelId: subchannelId, hardDelete: hardDelete) { success, error in
    if let error = error {
        // Handle error
        return
    }
    // Handle success
}
```
</CodeGroup>
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
val subchannelId = "subchannelId"
val hardDelete = true

val subchannelRepository = AmitySubchannelRepository(client)
subchannelRepository.deleteSubChannel(subchannelId, hardDelete).subscribe({
    // Handle success
}, { error ->
    // Handle error
})
```
</CodeGroup>
</Tab>

<Tab title="JavaScript">
We don't support this feature in JS SDK.
</Tab>

<Tab title="TypeScript">
Version 6

<CodeGroup>
```typescript
const subchannelId = "subchannelId";
const hardDelete = true;

const subchannelRepository = new SubchannelRepository(client);
await subchannelRepository.deleteSubchannel(subchannelId, hardDelete);
```
</CodeGroup>

Beta (v0.0.1)

<CodeGroup>
```typescript
const subchannelId = "subchannelId";
const hardDelete = true;

const subchannelRepository = new SubchannelRepository(client);
await subchannelRepository.deleteSubchannel({
    subchannelId,
    hardDelete
});
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
<CodeGroup>
```dart
final subchannelId = "subchannelId";
final hardDelete = true;

final subchannelRepository = AmitySubchannelRepository(client: client);
try {
    await subchannelRepository.deleteSubChannel(
        subchannelId: subchannelId,
        hardDelete: hardDelete,
    );
    // Handle success
} on AmityException catch (e) {
    // Handle error
}
```
</CodeGroup>
</Tab>
</Tabs>

### **Get Subchannel**

To get a subchannel, you can use the `getSubchannel` method provided by the `SubchannelRepository`. This method accepts a `subchannelId` parameter and returns a [#live-object](../../core-concepts/live-objects-collections/#live-object "mention") of the `AmitySubchannel` class.

The `AmitySubchannel` class represents a subchannel in a channel. It contains information about the subchannel, such as its ID, display name, avatar, creation time, and more.

By using a [#live-object](../../core-concepts/live-objects-collections/#live-object "mention") combines with [#real-time-events](subchannel.md#real-time-events "mention"), you can observe any changes made to the subchannel in real-time. This is particularly useful in cases where multiple users may be interacting with the same subchannel and you need to keep the UI up-to-date with the latest data.

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
let subchannelId = "subchannelId"

let subchannelRepository = AmitySubchannelRepository(client: client)
let subchannel = subchannelRepository.getSubChannel(subchannelId)
```
</CodeGroup>
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
val subchannelId = "subchannelId"

val subchannelRepository = AmitySubchannelRepository(client)
val subchannel = subchannelRepository.getSubChannel(subchannelId)
```
</CodeGroup>
</Tab>

<Tab title="JavaScript">
We don't support this feature in JS SDK.
</Tab>

<Tab title="TypeScript">
Version 6 and Beta(v0.0.1)

<CodeGroup>
```typescript
const subchannelId = "subchannelId";

const subchannelRepository = new SubchannelRepository(client);
const subchannel = await subchannelRepository.getSubchannel(subchannelId);
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
<CodeGroup>
```dart
final subchannelId = "subchannelId";

final subchannelRepository = AmitySubchannelRepository(client: client);
try {
    final subchannel = await subchannelRepository.getSubChannel(
        subchannelId: subchannelId,
    );
    // Handle success
} on AmityException catch (e) {
    // Handle error
}
```
</CodeGroup>
</Tab>
</Tabs>

### **Query Subchannels**

The `getSubChannels` function allows you to retrieve a list of subchannels within a specific channel. It accepts the `channelId` parameter to specify which channel to retrieve subchannels from.

The function returns a [#live-collection](../../core-concepts/live-objects-collections/#live-collection "mention"), which allows you to observe changes to the collection in real-time.

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
let channelId = "channelId"

let subchannelRepository = AmitySubchannelRepository(client: client)
let collection = subchannelRepository.getSubChannels(channelId: channelId)
```
</CodeGroup>
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
val channelId = "channelId"

val subchannelRepository = AmitySubchannelRepository(client)
val collection = subchannelRepository.getSubChannels(channelId)
```
</CodeGroup>
</Tab>

<Tab title="JavaScript">
We don't support this feature in JS SDK.
</Tab>

<Tab title="TypeScript">
Version 6 and Beta(v0.0.1)

<CodeGroup>
```typescript
const channelId = "channelId";

const subchannelRepository = new SubchannelRepository(client);
const subchannels = await subchannelRepository.getSubchannels(channelId);
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
<CodeGroup>
```dart
final channelId = "channelId";

final subchannelRepository = AmitySubchannelRepository(client: client);
try {
    final subchannels = await subchannelRepository.getSubChannels(
        channelId: channelId,
    );
    // Handle success
} on AmityException catch (e) {
    // Handle error
}
```
</CodeGroup>
</Tab>
</Tabs>