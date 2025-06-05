# Mute/Unmute a List of Channel Members

Moderators can mute and unmute users. When a user is muted, they cannot send messages in a channel. However, muted users will still be allowed to observe messages in a channel. The status of being muted is indefinite but is only applied at the channel level. The mute and unmute operations can be done via `Channel` object.

## Muting Channel Members

When a user is muted, they cannot send messages in a channel and all the messages sent by that user to that channel will be rejected. This method is useful for preventing certain members from sending inappropriate messages, but still allowing them to participate in the conversation in a read-only manner. The timeout property allows you to make the timeout temporary, or permanent until unset by passing in `-1`.

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
channel.muteMembers(userIds: ["userId1", "userId2"], period: 600) { success, error in
    // Handle the result
}
```
</CodeGroup>
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
channel.muteMembers(
    userIds = listOf("userId1", "userId2"),
    period = 600
).doOnComplete {
    // Handle success
}.doOnError { 
    // Handle error
}.subscribe()
```
</CodeGroup>
</Tab>

<Tab title="JavaScript">
```javascript
repository.muteMembers({
  userIds: ['user1'],
  period: 600,
}).catch(error => {
  ...
});
```
</Tab>

<Tab title="TypeScript">
<CodeGroup>
```typescript
repository.muteMembers({
  userIds: ['user1'],
  period: 600,
}).catch(error => {
  // Handle error
});
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
<CodeGroup>
```dart
try {
  await channel.muteMembers(
    userIds: ['userId1', 'userId2'],
    period: 600,
  );
} on AmityException catch (error) {
  // Handle error
}
```
</CodeGroup>
</Tab>
</Tabs>

## Unmuting Channel Members

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
channel.unmuteMembers(userIds: ["userId1", "userId2"]) { success, error in
    // Handle the result
}
```
</CodeGroup>
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
channel.unmuteMembers(
    userIds = listOf("userId1", "userId2")
).doOnComplete {
    // Handle success
}.doOnError { 
    // Handle error
}.subscribe()
```
</CodeGroup>
</Tab>

<Tab title="JavaScript">
```javascript
repository.unmuteMembers({
  userIds: ['user1'],
}).catch(error => {
  ...
});
```
</Tab>

<Tab title="TypeScript">
<CodeGroup>
```typescript
repository.unmuteMembers({
  userIds: ['user1'],
}).catch(error => {
  // Handle error
});
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
<CodeGroup>
```dart
try {
  await channel.unmuteMembers(
    userIds: ['userId1', 'userId2'],
  );
} on AmityException catch (error) {
  // Handle error
}
```
</CodeGroup>
</Tab>
</Tabs>

<Info>
This feature is not applicable in `Broadcast` and `Conversation` channel. Calling `muteMembers()` or `unmuteMembers()` on these channels will result in an error.
</Info>