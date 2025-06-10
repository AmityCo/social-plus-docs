---
description: >-
  Here's an overview of how you can start integrating comments into your
  applications
---

# Create Comment

Social Plus SDK's comment creation is designed to handle comments efficiently and reliably across your application. Each comment is assigned a unique, immutable `commentId`, and the SDK includes an optimistic update feature to enhance user experience.

To work with comments, you'll need to use the `CommentRepository`.

With the SDK's optimistic creation feature, you don't need to manually create a `commentId`. Instead, the SDK generates one automatically. However, you must provide the `referenceId` and `referenceType` parameters. This feature enables the app to display the comment immediately while assuming it will be successfully added, reducing perceived latency for users.

The `referenceType` parameter specifies the type of content the comment is associated with. Supported values are:

* `post`: Create a comment on a post.
* `story`: Create a comment on a story.
* `content`: Create a comment on other content types.

<Info>
A comment should not exceed 20,000 characters in length.
</Info>

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
https://gist.github.com/amythee/e1c3ad53511f589105776e2b32265b40
```
</CodeGroup>

The `AmityNotificationToken` returned by the `observeOnceWithBlock:` is saved in `self.token`, a strongly referenced property. This is needed to prevent the observed block from being released.

The `parentId` parameter in `createComment:` is optional.

The `referenceId` parameter in `createComment:` is mandatory and will only support `AmityPost` identifier.
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
https://gist.github.com/amythee/8b3044e1449499522f3259828e7b22f2#file-amitycommentcreate-kt
```
</CodeGroup>
</Tab>

<Tab title="JavaScript">
<CodeGroup>
```javascript
https://gist.github.com/amythee/73a5a476abada38f33bf0ba6613b8a6c#file-createcomment-js
```
</CodeGroup>
</Tab>

<Tab title="TypeScript">
<Embed url="https://gist.github.com/2e38f085497fa8cec7177976edb8b549" />
</Tab>

<Tab title="Flutter">
<Embed url="https://gist.github.com/amythee/99d02516b7f851d06100cfcfe9e3e177#file-amityposttextcreation-dart" />
</Tab>
</Tabs>

## Create a Comment with an Image

Social Plus SDK also allows you to create comments with images. This feature works seamlessly with the SDK's optimistic creation mechanism, ensuring the same fast and responsive user experience as with text comments.

The `referenceType` parameter determines the content type the image comment is associated with. Supported values are:

* `post`: Create a comment on a post.
* `story`: Create a comment on a story.
* `content`: Create a comment on other content types.

To create an image comment, you'll need to:

1. Upload the image to obtain a `fileId`.
2. Provide the `fileId` in the `attachments` parameter along with the required `referenceId` and `referenceType`.

The SDK automatically generates a unique `commentId` for the image comment and handles the creation process optimistically.

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
https://gist.github.com/amythee/19486c590680aa6df4240b32af143248
```
</CodeGroup>
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
https://gist.github.com/amythee/b00f8ce59d581ac05a9b0ab17a1916e3
```
</CodeGroup>
</Tab>

<Tab title="TypeScript">
<CodeGroup>
```typescript
https://gist.github.com/fc5ad48dcad539ec59fe6d33223564bf
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
The functionality isn't currently supported by this SDK.
</Tab>
</Tabs>

<Info>
#### Limitations:

1. Users can use a maximum of 10 images per comment.
2. The supported file types with the image moderation feature is enabled are jpg/jpeg + png.
3. The supported file types when the image moderation feature is not enabled are jpg/jpeg + webp
4. The maximum file size per image is 1 GB.
</Info>

## Reply to a Comment

In addition to creating top-level comments, Social Plus SDK enables you to reply to existing comments in addition to creating top-level comments.

To reply to a comment, you must:

1. Specify the **parent comment's** `commentId` using the `parentId` parameter.
2. Provide the `referenceId`, `referenceType`, and the reply's text content.

The `referenceType` parameter also supports replies to comments on stories. To reply to a story comment:

* Set `referenceType` to `.story`.
* Provide the corresponding `referenceId` for the story.

Similar to top-level comments, replies leverage the SDK's optimistic creation feature. You don't need to provide a unique `commentId` for the reply, the SDK generates it automatically while associating it with the parent comment.

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
https://gist.github.com/amythee/72615abf8c6bc53d1f4fc307ea630f5c
```
</CodeGroup>
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
https://gist.github.com/amythee/106136159a8fb36a811782b22ddbc7cb
```
</CodeGroup>
</Tab>

<Tab title="TypeScript">
<CodeGroup>
```typescript
https://gist.github.com/48391c1ec8f9055a9da508c76476a111
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
<CodeGroup>
```dart
https://gist.github.com/amythee/99d02516b7f851d06100cfcfe9e3e177#file-amityposttextcreation-dart
```
</CodeGroup>
</Tab>
</Tabs>

### Reply to Comments with an Image

<Tabs>
<Tab title="iOS">
<Embed url="https://gist.github.com/amythee/b6a4f1f190552246334f228cc856e339" />
</Tab>

<Tab title="Android">
<Embed url="https://gist.github.com/amythee/1ad226283e7c5e1b4cf36e41b531a029" />
</Tab>

<Tab title="TypeScript">
<Embed url="https://gist.github.com/93ae3275f1133d3580d00b9ae0110f3d" />
</Tab>

<Tab title="Flutter">
The functionality isn't currently supported by this SDK.
</Tab>
</Tabs>