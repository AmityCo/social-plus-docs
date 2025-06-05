# Edit Comment

Social Plus SDK provides a comment editing functionality that fosters accountability and user awareness within your application. This feature enables users to edit their own comments exclusively. Users can only edit their comments, which encourages responsible interactions and maintains accountability. Upon completing an edit operation, the SDK updates the `editedAt` property to the current time, reflecting the changes made by the user. You can then leverage the updated `editedAt` timestamp to create a user interface that informs users of edited comments, fostering transparency.

<Tabs>
  <Tab title="iOS">
For any editing operation - either update or delete a comment, you can use APIs from `AmityCommentRepository`.

<CodeGroup>
  ```swift accbe118986f0d48154823ce7dbe22b1#file-create_comment_editor-swift
  let commentRepository = AmityCommentRepository(client: client)
  commentRepository.updateComment(withId: commentId, text: "Updated comment") { (comment, error) in
      // Handle the result
  }
  ```
</CodeGroup>

<CodeGroup>
  ```swift 5f887f00905b9853bbd49ea00e991473
  let commentRepository = AmityCommentRepository(client: client)
  commentRepository.deleteComment(withId: commentId) { (success, error) in
      // Handle the result
  }
  ```
</CodeGroup>
  </Tab>

  <Tab title="Android">
<CodeGroup>
  ```java 20c83eb8977b65f8fdcd38be81a19322
  AmityCommentRepository commentRepository = new AmityCommentRepository(client);
  commentRepository.updateComment(commentId, "Updated comment")
      .subscribe(new SingleObserver<AmityComment>() {
          @Override
          public void onSuccess(AmityComment comment) {
              // Handle success
          }

          @Override
          public void onError(Throwable e) {
              // Handle error
          }
      });
  ```
</CodeGroup>
  </Tab>

  <Tab title="JavaScript">
<CodeGroup>
  ```javascript 149aae5bf5e44d76ae22ae8f06d1fd41#file-editcomment-js
  const commentRepository = new AmityCommentRepository(client);
  commentRepository.updateComment(commentId, "Updated comment")
    .then(comment => {
      // Handle success
    })
    .catch(error => {
      // Handle error
    });
  ```
</CodeGroup>
  </Tab>

  <Tab title="TypeScript">
<CodeGroup>
  ```typescript cc3c9d5b5a130bd81d3c3ff9ac3d6c25
  const commentRepository = new AmityCommentRepository(client);
  commentRepository.updateComment(commentId, "Updated comment")
    .then((comment: AmityComment) => {
      // Handle success
    })
    .catch((error: Error) => {
      // Handle error
    });
  ```
</CodeGroup>
  </Tab>

  <Tab title="Flutter">
<CodeGroup>
  ```dart 893357a8ae37f04677e5704bfacec50d#file-amitycommentupdate-dart
  final commentRepository = AmityCommentRepository(client);
  try {
    final comment = await commentRepository.updateComment(
      commentId: commentId,
      text: "Updated comment",
    );
    // Handle success
  } catch (error) {
    // Handle error
  }
  ```
</CodeGroup>
  </Tab>
</Tabs>

## Edit Comment with Image

Social Plus SDK extends its comment editing functionality to include images, allowing users to update their comments with images. This feature enables users to modify not only the text but also the images associated with their comments, providing a richer and more engaging experience for your app's audience.

Before editing images in comments, it is crucial to upload the images that will be included in the comment data to ensure that the necessary information is accessible and can be linked to the comment. This requires uploading the file first, to obtain the file data that will be used in creating the file post. To upload a file, please refer to [#upload-images](../../core-concepts/files-images-and-videos/image-handling.md#upload-images "mention").

Upon successful completion of the file upload process, you can include the image data as a parameter when updating comments as demonstrated in the code sample below.

<Tabs>
  <Tab title="iOS">
<CodeGroup>
  ```swift c1ed70332e7451310b6686a90346be27
  let commentRepository = AmityCommentRepository(client: client)
  let fileIds = ["fileId1", "fileId2"]
  commentRepository.updateComment(withId: commentId, text: "Updated comment with images", fileIds: fileIds) { (comment, error) in
      // Handle the result
  }
  ```
</CodeGroup>
  </Tab>

  <Tab title="Android">
<CodeGroup>
  ```java 3f4df12e211bf3163568295218e6faa9
  AmityCommentRepository commentRepository = new AmityCommentRepository(client);
  List<String> fileIds = Arrays.asList("fileId1", "fileId2");
  commentRepository.updateComment(commentId, "Updated comment with images", fileIds)
      .subscribe(new SingleObserver<AmityComment>() {
          @Override
          public void onSuccess(AmityComment comment) {
              // Handle success
          }

          @Override
          public void onError(Throwable e) {
              // Handle error
          }
      });
  ```
</CodeGroup>
  </Tab>

  <Tab title="TypeScript">
<CodeGroup>
  ```typescript 5d91a603eb45bd9c6184e637b31f780a
  const commentRepository = new AmityCommentRepository(client);
  const fileIds = ["fileId1", "fileId2"];
  commentRepository.updateComment(commentId, "Updated comment with images", fileIds)
    .then((comment: AmityComment) => {
      // Handle success
    })
    .catch((error: Error) => {
      // Handle error
    });
  ```
</CodeGroup>
  </Tab>

  <Tab title="Flutter">
The functionality isn't currently supported by this SDK.
  </Tab>
</Tabs>

_Refer to the following_ [_Limitations_](create-comment.md#limitations) _on the use of images in comments._