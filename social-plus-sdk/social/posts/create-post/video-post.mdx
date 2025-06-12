# Video Post

Prior creating a video post, it is crucial to upload the videos that will be included in the post data to ensure that the necessary information is accessible and can be linked to the post. This requires uploading the video first, to obtain the video data that will be used in creating the video post. To upload a video, please refer to [#upload-videos](../../../core-concepts/files-images-and-videos/video-handling.md#upload-videos "mention")

Upon successful completion of the video upload process, you can include the video data as a parameter when creating a video post, as demonstrated in the code sample below.

Here's an explanation of the method's parameters:

* `text`: This is a required parameter of type `String`, which represents the text content of the new post. You can pass in any text you want to include in the post, up to a maximum length of 20,000 characters.
* `videos`: Which represents an array of videos uploaded by the user on Android, iOS and Flutter and `videoIds` for Typescript and Javascript to include in the new post. You can pass up to 10 videos in a post.
* `targetType`: Type of the target, either a particular community or a user feed.
* `tags`: Arbitrary strings that can be used for defining and querying for the posts (Except Flutter).
* `metaData`: Additional properties to support custom fields.

**Requirements for Video**

* Supported video types are `3gp`, `avi`, `f4v`, `flv`, `m4v`, `mov`, `mp4`, `ogv`, `3g2`, `wmv`, `vob`, `webm`, `mkv`
* The maximum file size limit is up to 2 GB.
* The maximum duration of the video is 2 hours

<Tabs>
<Tab title="iOS">
We can build the post first by using `AmityVideoPostBuilder`. Then use the `createVideoPost` method in `AmityPostRepository` to create a video post.

<CodeGroup>
```swift
let repository = AmityPostRepository(client: client)
let builder = AmityVideoPostBuilder()
builder.setText("Hello World")
builder.setVideos([videoData1, videoData2])
builder.setMetadata(["key": "value"])
builder.setTags(["tag1", "tag2"])
builder.setTargetCommunity(communityId)

repository.createPost(builder) { (post, error) in
    // handle result
}
```
</CodeGroup>
</Tab>

<Tab title="Android">
We can build the post first by using `AmityFilePostCreator.Builder`. Then use the same `createPost` method in `AmityPostRepository` to create an image post.

<CodeGroup>
```kotlin
val repository = AmityPostRepository(client)
val builder = AmityFilePostCreator.Builder()
    .setText("Hello World")
    .setVideos(listOf(videoData1, videoData2))
    .setMetadata(mapOf("key" to "value"))
    .setTags(listOf("tag1", "tag2"))
    .setTargetCommunity(communityId)
    .build()

repository.createPost(builder).observe { post ->
    // handle result
}
```
</CodeGroup>
</Tab>

<Tab title="JavaScript">
<CodeGroup>
```javascript
const repository = new AmityPostRepository(client);
const post = await repository.createPost({
    text: "Hello World",
    videoIds: ["videoId1", "videoId2"],
    metadata: { key: "value" },
    tags: ["tag1", "tag2"],
    targetCommunity: communityId
});
```
</CodeGroup>
</Tab>

<Tab title="TypeScript">
<CodeGroup>
```typescript
const repository = new AmityPostRepository(client);
const post = await repository.createPost({
    text: "Hello World",
    videoIds: ["videoId1", "videoId2"],
    metadata: { key: "value" },
    tags: ["tag1", "tag2"],
    targetCommunity: communityId
});
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
<CodeGroup>
```dart
final repository = AmityPostRepository(client);
final post = await repository.createPost(
    text: "Hello World",
    videos: [videoData1, videoData2],
    metadata: {"key": "value"},
    targetCommunity: communityId,
);
```
</CodeGroup>
</Tab>
</Tabs>

<Note>
* A post can have a maximum of ten videos.
* Uploading HDR video format is not supported on iOS.
</Note>