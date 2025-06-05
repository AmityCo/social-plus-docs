# Live stream Post

Prior to creating a live stream post, it is crucial to create the live stream that will be included in the post data to ensure that the necessary information is accessible and can be linked to the post. This requires creating the live stream first, to obtain the data that will be used in creating the live stream post. For more information regarding live stream, please refer to [#live-stream](../../../video/#live-stream "mention")

As demonstrated in the code sample below, here's a way to create a live stream.

<Tabs>
  <Tab title="iOS">
    <Embed url="https://gist.github.com/amythee/fc657685956965e872d08a6d48d799bf#file-create_stream_repository-swift" />
    <Embed url="https://gist.github.com/amythee/ea7b8fbe83278d895f339fd2ea7282e8" />
  </Tab>
  <Tab title="Android">
    <Embed url="https://gist.github.com/amythee/777a6a7dfce5844878d78b6e10f4ae90#file-amitypostlivestreamupload-kt" />
    <Embed url="https://gist.github.com/amythee/ead4e7b79fd5fe925e8b8f2929e50004" />
  </Tab>
  <Tab title="JavaScript">
    ```javascript
    import { StreamRepository, StreamResolutions } from '@amityco/js-sdk'

    const liveObject = StreamRepository.createStream({
      title: 'title',
      thumbnailFileId: 'fileId', // use FileRepository.createFile to upload the file and get the id
      description: 'description',
      resolution: StreamResolutions.HD,
      metadata: { customField: 'customValue' },
    });

    liveObject.on('dataUpdated', (stream) => {
      console.log(stream);
    });
    ```
  </Tab>
  <Tab title="TypeScript">
    <Embed url="https://gist.github.com/amythee/75cdb3d62f3d3bb986a66eeb83b9de8e#file-createstream-ts" />
  </Tab>
</Tabs>

Upon successful completion of the live stream process, you can include the stream ID as a parameter when creating a live stream post, as demonstrated in the code sample below.

Here's an explanation of the method's parameters:

* `text`: This is a required parameter of type `String`, which represents the text content of the new post. You can pass in any text you want to include in the post, up to a maximum length of 20,000 characters.
* `streamId`: The ID of the created live stream to include in a post.
* `targetType` - Type of the target, either a particular community or a user feed.
* `tags` - Arbitrary strings that can be used for defining and querying for the posts.
* `metaData` - Additional properties to support custom fields.

<Tabs>
  <Tab title="iOS">
    You can create a livestream post via `AmityLiveStreamPostBuilder`.

    `AmityLiveStreamPostBuilder` creates a text post and attaches a stream post as a first child. This builder requires the stream object id.

    <Embed url="https://gist.github.com/amythee/90af21dfc3e6b8f4f0ec0eb671a0f0b2" />
  </Tab>
  <Tab title="Android">
    We can build the post first by using `AmityLiveStreamPostCreator.Builder`. Then, use the same `createPost` method in `AmityPostRepository` and pass the `streamId` from created `AmityStream` to create a livestream post.

    <Embed url="https://gist.github.com/amythee/de45b8efb8a6474fb7ec925615e3ccdc#file-amitypostlivestreamcreation-kt" />
  </Tab>
  <Tab title="JavaScript">
    <Embed url="https://gist.github.com/amythee/3c49499659ff169675c07dc1c418440e#file-createlivestreampost-js" />
  </Tab>
  <Tab title="TypeScript">
    <Embed url="https://gist.github.com/801819c5c196ef72af39a02d7241a4bf" />
  </Tab>
</Tabs>