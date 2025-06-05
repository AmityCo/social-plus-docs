# Add / Remove Reaction

The Social Plus SDK product also provides functionality for adding and removing reactions on posts. Users can add any number of reactions to a particular post, allowing them to engage with the content more expressive and nuancedly. Additionally, users can also remove reactions that they have added to a post, providing greater control and flexibility over their engagement with the content.

## Add Reaction

The `addReaction` function allows users to add a reaction to a post. The function takes the name of the reaction as a parameter, with a maximum length of 100 characters. The reaction name is case-sensitive, which means that "like" and "Like" are treated as two different reactions.

You can add reactions to a given [reference](./#create-comment) through the `addReaction` method.

* `referenceId` - ID of the post or comment respectively.
* `reactionName` - The name of the reaction that you will remove. Reaction names are case sensitive, i.e. "like" & "Like" are two different reactions.

The `referenceType` parameter specifies where the reaction is applied. Supported values are:

* **`post`**: Adds the reaction to a post.
* **`story`**: Adds the reaction to a story.
* **`content`**: Adds the reaction to other supported content types.

To add a reaction, use the `addReaction` method:

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
// Add reaction from Post and Story
AmityReactionRepository()
    .addReaction("like", referenceType: .post, referenceId: postId) { success, error in
    // handle success/error
}
```
</CodeGroup>
</Tab>

<Tab title="Android">
Add Reaction from Post and Story

<CodeGroup>
```kotlin
val reactionRepository = AmityReactionRepository(client)
reactionRepository.addReaction("like", AmityReactionReferenceType.POST, postId)
    .subscribe()
```
</CodeGroup>

Add Reaction from Comment

<CodeGroup>
```kotlin
val reactionRepository = AmityReactionRepository(client)
reactionRepository.addReaction("like", AmityReactionReferenceType.COMMENT, commentId)
    .subscribe()
```
</CodeGroup>
</Tab>

<Tab title="JavaScript">
The method returns a promise. If the reaction is successfully removed, the method will return `true`. Otherwise, it will return `false` or an error.

<CodeGroup>
```javascript
const response = await client.addReaction('like', 'post', postId);
```
</CodeGroup>
</Tab>

<Tab title="TypeScript">
Version 6

<CodeGroup>
```typescript
const response = await client.addReaction('like', 'post', postId);
```
</CodeGroup>

Beta (v0.0.1)

<CodeGroup>
```typescript
const response = await client.addReaction('like', 'post', postId);
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
Add Reaction from Post

<CodeGroup>
```dart
AmityReaction.postReaction(postId: postId, reactionName: "like");
```
</CodeGroup>

Add Reaction from Comment

<CodeGroup>
```dart
AmityReaction.commentReaction(commentId: commentId, reactionName: "like");
```
</CodeGroup>
</Tab>
</Tabs>

## Remove Reaction

Similarly, the `removeReaction` function allows users to remove a previously added reaction from a [reference](./#create-comment). This provides users with greater control over their engagement with the content and allows them to change their minds or update their reactions to the post or comment over time.

You can remove a reaction from a reference by calling `removeReaction`.

* `reactionName` - The name of the reaction that you will remove. Reaction names are case sensitive, i.e. "like" & "Like" are two different reactions.
* `referenceId` - ID of the post or comment respectively.

The `referenceType` parameter works similarly here, depending on where the reaction is removed. Supported values are:

* **`post`**: Removes the reaction from a post.
* **`story`**: Removes the reaction from a story.
* **`comment`**: Removes the reaction from a comment.
* **`message`**: Removes the reaction from a message.

To remove a reaction, use the `removeReaction` method:

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
AmityReactionRepository()
    .removeReaction("like", referenceType: .post, referenceId: postId) { success, error in
    // handle success/error
}
```
</CodeGroup>
</Tab>

<Tab title="Android">
Remove Reaction from Post and Story

<CodeGroup>
```kotlin
val reactionRepository = AmityReactionRepository(client)
reactionRepository.removeReaction("like", AmityReactionReferenceType.POST, postId)
    .subscribe()
```
</CodeGroup>

Remove Reaction from Comment

<CodeGroup>
```kotlin
val reactionRepository = AmityReactionRepository(client)
reactionRepository.removeReaction("like", AmityReactionReferenceType.COMMENT, commentId)
    .subscribe()
```
</CodeGroup>
</Tab>

<Tab title="JavaScript">
The method returns a promise. If the reaction is successfully removed, the method will return `true`. Otherwise, it will return `false` or an error.

<CodeGroup>
```javascript
const response = await client.removeReaction('like', 'post', postId);
```
</CodeGroup>
</Tab>

<Tab title="TypeScript">
Version 6

<CodeGroup>
```typescript
const response = await client.removeReaction('like', 'post', postId);
```
</CodeGroup>

Beta (v0.0.1)

<CodeGroup>
```typescript
const response = await client.removeReaction('like', 'post', postId);
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
Remove Reaction from Post

<CodeGroup>
```dart
AmityReaction.removePostReaction(postId: postId, reactionName: "like");
```
</CodeGroup>

Remove Reaction from Comment

<CodeGroup>
```dart
AmityReaction.removeCommentReaction(commentId: commentId, reactionName: "like");
```
</CodeGroup>
</Tab>
</Tabs>