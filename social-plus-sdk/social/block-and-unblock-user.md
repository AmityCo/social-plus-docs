# Block and Unblock User

This feature allows users to block and unblock other users, manage their list of blocked users, and interact with the users accordingly. The block and unblock features play an important roles in user experience and maintaining a safe, positive environment within a platform or community.

* **User safety and privacy:** The block feature allows users to protect themselves from unwanted interactions, harassment, or cyberbullying. By blocking another user, they can prevent the blocked user from viewing their content and engaging with them on the platform.
* **Control over personal space:** Users can maintain control over their online environment by choosing who they interact with and whose content they want to see. Blocking helps users curate their experience on the platform to match their preferences and comfort levels.
* **Reducing spam and inappropriate content:** Blocking enables users to filter out spam or content that they find offensive or irrelevant. This helps maintain a more pleasant experience for the user and reduces the negative impact that spam or inappropriate content can have on the platform's overall quality.

## Product Behavior for Blocked and Unblocked Users

#### When a user is blocked:

* Blocked users content in global feed, community feed, or user feed will be hidden
* Search user functionality will function normally, blocked users will still be visible.
* Some interactions will be disabled such as:
  * create a post on a blocker's user feed
  * create a comment on a blocker's user posts* (please read limitations in the last section)
  * add or remove reactions on a blocker's posts
* The [connection status](follow-unfollow/get-connection-status-and-connection-counter.md#connection-status) on the blocked user will become `none` and the blocker will not be able to follow the blocked user.

#### When a user is unblocked:

* Blocked users content in global feed, community feed, or user feed content will be visible
* All prohibited Interactions will be enabled as mentioned above.
* The connection status on the blocked user will retain `none` regardless of the previous connection, and the blocker will be able to follow the unblocked user again.

## Block User

Users can block other users with the following constraints:

* Only users can be blocked, not Console Admins or communities.
* Community moderators or custom roles can be blocked, regardless of their roles.

When Alice blocks Bob:

* Alice can block Bob regardless of their connection status.
* Alice will see Bob's [connection status](follow-unfollow/get-connection-status-and-connection-counter.md#connection-status) as `blocked`.
* Bob will see Alice's [connection status](follow-unfollow/get-connection-status-and-connection-counter.md#connection-status) as `none`.
* Bob won't be notified of the block and can still block Alice.
* Bob's roles and community memberships remain unchanged.

Here's the explanation of the parameter:

* `userId`: This is a required parameter of type `String` that represents the unique identifier of the user you want to block.

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
amity.blockUser(userId: "userID") { success, error in
    if success {
        // Handle success
    } else {
        // Handle error
    }
}
```
</CodeGroup>
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
amity.blockUser("userID").subscribe({ 
    // Handle success
}, { error -> 
    // Handle error
})
```
</CodeGroup>
</Tab>

<Tab title="TS">
<CodeGroup>
```typescript
await amity.blockUser("userID");
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
<CodeGroup>
```dart
try {
  await amity.blockUser("userID");
  // Handle success
} catch (error) {
  // Handle error
}
```
</CodeGroup>
</Tab>
</Tabs>

## Unblock User

Users can also unblock blocked users with the following constraints: 

* Their connection status will not return to the state before the block if they were connected. The connection status will always be `none`.
* If Alice was following Bob, they'll need to reconnect with Bob after unblocking.
* If Alice and Bob were not connected, the connection status will remain `none` upon unblocking.

Here's the explanation of the parameter:

* `userId`: This is a required parameter of type `String` that represents the unique identifier of the user you want to unblock.

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
amity.unblockUser(userId: "userID") { success, error in
    if success {
        // Handle success
    } else {
        // Handle error
    }
}
```
</CodeGroup>
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
amity.unblockUser("userID").subscribe({ 
    // Handle success
}, { error -> 
    // Handle error
})
```
</CodeGroup>
</Tab>

<Tab title="TS">
<CodeGroup>
```typescript
await amity.unblockUser("userID");
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
<CodeGroup>
```dart
try {
  await amity.unblockUser("userID");
  // Handle success
} catch (error) {
  // Handle error
}
```
</CodeGroup>
</Tab>
</Tabs>

## Blocked Users List

Users can view and manage a list of users they've blocked. The list will display:

* User ID
* Display Name
* Avatar
* Other relevant user information

Blocked users that are inactive or deleted will not be shown in the list. Users can only view users they've blocked and not the users that have blocked them.

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
amity.getBlockedUsers { blockedUsers, error in
    if let users = blockedUsers {
        // Handle blocked users list
    } else {
        // Handle error
    }
}
```
</CodeGroup>
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
amity.getBlockedUsers().subscribe({ blockedUsers -> 
    // Handle blocked users list
}, { error -> 
    // Handle error
})
```
</CodeGroup>
</Tab>

<Tab title="TS">
<CodeGroup>
```typescript
const blockedUsers = await amity.getBlockedUsers();
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
<CodeGroup>
```dart
try {
  final blockedUsers = await amity.getBlockedUsers();
  // Handle blocked users list
} catch (error) {
  // Handle error
}
```
</CodeGroup>
</Tab>
</Tabs>

## Limitations

While the block and unblock features offer several benefits, there are limitations to their capabilities:

**Interaction with Content**

Blocking does not completely restrict interactions with the blocked user's content in the following scenarios:

* If Alice blocks Bob, and either of them knows the other's post ID, they can still comment on or react to each other's posts.

**Content Notifications**

Blocking does not affect notifications related to blocked users:

* If Alice or Bob creates a post in a community they are both members of, they will still receive notifications about the post created by the other person.
* No user-blocking related real-time events are provided to the SDK.
* Filtering blocked users' RTE is not supported. For example, if Alice and Bob subscribe to the same community feed and one of them creates a post, the other will still receive the post-created event.