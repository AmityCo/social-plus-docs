---
description: Editing and changing post details and content
---

# Edit Post

Social Plus SDK supports the editing of the following post types:

* Text post
* Image post
* File post
* Video post

## Edit a Post

Social Plus SDK provides a post-editing functionality that fosters accountability and user awareness within your application. This feature enables users to edit their posts exclusively. Users can only edit their posts, except if you're an admin or a moderator of a particular community. The functionality encourages responsible interactions and maintains accountability. Upon completing an edit operation, the SDK updates the `editedAt` property to the current time, reflecting the changes made by the user. You can then leverage the updated `editedAt` timestamp to create a user interface that informs users of edited posts, fostering transparency. You can edit a post by following this sample code.

{% tabs %}
{% tab title="iOS" %}
You can edit a post using a pattern similar to creating a post. Follow these steps:

1. Choose the appropriate post builder type and structure your post.
2. Make the API call for post-editing.

Note: If you intend to update files, images, or videos in a post, you must upload them first. Once you have the data, you can use it with the corresponding post type. Ensure that the builder type matches the original post type.

For further details on uploading, refer to [#upload-images](../../core-concepts/files-images-and-videos/image-handling.md#upload-images "mention") [#upload-files](../../core-concepts/files-images-and-videos/file.md#upload-files "mention")[#upload-videos](../../core-concepts/files-images-and-videos/video-handling.md#upload-videos "mention").&#x20;

### Update Text Post

To edit a text post, utilize the `editPost` method in a post repository using `AmityTextPostBuilder` class to compose a new text as demonstrated in the provided code snippet.&#x20;

{% embed url="https://gist.github.com/amythee/889a5149744bd8210bec8e69341ed611" %}

### Update File Post

To edit a file post, utilize the `editPost` method in a post repository using `AmityFilePostBuilder` class to compose a set of new files as demonstrated in the provided code snippet. The `files` parameter should include both the current files (if required) and any newly uploaded files you wish to append to the post.

{% embed url="https://gist.github.com/amythee/2e6ffc849db32aba7cf14f6a657028bb" %}

### Update Image Post

To edit an image post, utilize the `editPost` method in a post repository using `AmityImagePostBuilder` class to compose a set of new images as demonstrated in the provided code snippet. The `images` parameter should include both the current images (if required) and any newly uploaded images you wish to append to the post.

{% embed url="https://gist.github.com/amythee/5fab45554188aea27860fb67159b09bf" %}

### Update Video Post

To edit a video post, utilize the `editPost` method in a post repository using `AmityVideoPostBuilder` class to compose a set of new videos as demonstrated in the provided code snippet. The `videos` parameter should include both the current videos (if required) and any newly uploaded videos you wish to append to the post.

{% embed url="https://gist.github.com/amythee/c5ae979c36d7d1f43e309c86d1a74599" %}
{% endtab %}

{% tab title="Android" %}
If you want to edit a file/image/video post to add more files, the files/images to be added must be uploaded first. The `AmityFileRepository` class handles the uploading and downloading of files. The repository has an `uploadFile` method which takes the file's  `Uri` and returns an array of `AmityUploadResult` for successful or failed uploads.&#x20;

`AmityUploadResult` will return four possible types of data:

* &#x20;`AmityUploadResult.PROGRESS` - uploading is in progress. It returns `AmityUploadInfo` which can be used to track the progress of the upload.
* `AmityUploadResult.COMPLETE` - the upload completed successfully.  It returns `AmityFile` that can then be attached to the post.
* `AmityUploadResult.ERROR(exception)`  - the upload failed. It returns an `Exception`.
* `AmityUploadResult.CANCELLED` - uploading is canceled.

For further details on uploading, refer to [#upload-images](../../core-concepts/files-images-and-videos/image-handling.md#upload-images "mention") [#upload-files](../../core-concepts/files-images-and-videos/file.md#upload-files "mention")[#upload-videos](../../core-concepts/files-images-and-videos/video-handling.md#upload-videos "mention").

#### Update Text Post

{% embed url="https://gist.github.com/amythee/04e109e2774146f5ab7f3c8a4e0bcf27#file-amityposttextupdate-kt" %}

#### Update File Post

{% embed url="https://gist.github.com/amythee/699e8e2058f8962342e14f4713915e7d" %}

To edit a file post, use the `edit` method as shown in the sample code below. The `attachments` should contain the uploaded files that you want to add to the post which are stored in `existingFiles` and `newFiles` respectively.

{% embed url="https://gist.github.com/amythee/5dd0c0868843ef59fdcf35865f8e478e" %}

#### Update Image Post

{% embed url="https://gist.github.com/amythee/24cc8b78b5e4269f1f29263b6bb9695a" %}

To edit an image post, use the `edit` method as shown in the sample code below. The `attachments` should contain the existing images and the uploaded images that you want to add to the post which are stored in `existingImages` and `newImages` respectively.

{% embed url="https://gist.github.com/amythee/1a291007f1e02e50d760fd372759948b" %}

{% hint style="info" %}
You can remove existing images from the post by excluding them from the `attachments` list. You can also change the order of the images in the list.
{% endhint %}



#### Update Video Post

{% embed url="https://gist.github.com/amythee/3aeb5fe489319c2c72c45ad4a378b6e0" %}

To edit a video post, use the `edit` method as shown in the sample code below. The `attachments` should contain the existing videos and the uploaded videos that you want to add to the post which are stored in `existingVideos` and `newVideos` respectively.

{% embed url="https://gist.github.com/amythee/f3cd61f2b5ad8005fcfb45e3f2f00c06" %}
{% endtab %}

{% tab title="JavaScript" %}
This method requires the following parameters:

* `postId (String)` - ID of the post to update
* `data (Object)` - data object of the post

Other optional parameters are:

* `metadata (Object)` - the metadata object of the post
* `tags (Array.<String>)` - strings used to query the post. Up to five tags can be added and each tag can be up to 24 characters long.

{% hint style="info" %}
In JavaScript SDK, the following are not yet supported:

1. Adding videos to a non-video post (e.g. text post, image post)
2. Adding different media types (e.g. image, custom files) in a single post
{% endhint %}



{% embed url="https://gist.github.com/amythee/9243e4d6f493f24ddd26ea29982680f7#file-updatepost-js" %}

The `updatePost` method returns a `Promise<boolean>` - `true` if the post is successfully updated. Otherwise, it will throw an error.

#### Update Video Post

You can add new videos or remove existing ones from a video post. In adding new videos, you must first upload the videos that you will add to the post. Refer to Upload Video for the details on how to upload a video.

When updating a video post, provide the file ID of the video and the type `FileType.Video`  in the `attachments` parameter.  Modifying `attachments` array will overwrite the existing videos so it’s recommended to include original attachments if you want to retain the original videos in the post. Leave the `attachments` array empty to remove all videos.

```javascript
import { PostRepository, FileType } from '@amityco/js-sdk';

const post = PostRepository.updatePost({
    postId: 'post123',
    tags: ['a','b'], //optional, max no. tags = 5, max length per tag = 24 chars
    data: { text: 'hello!'},
    mentionees: [
    {
      "type": "user",
      "userIds": [
        "user1", “user2”
      ]
    },
    attachments: [
      { fileId: ‘yourFileId’, type: FileType.Video },
      …
    ]
  ]
});
```
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/0e287e6a5b90dc4a5e108a7780a65036#file-updatepost-ts" %}
{% endtab %}

{% tab title="Flutter" %}
When updating a post, you can update its text content. However, you cannot add or remove the post's attachments (i.e. image, video, and file).

You can update the post using the `update` method. This method requires the following parameters:

* `postId (String)` - ID of the post to update
* `text (String)` -  text data of the post

{% embed url="https://gist.github.com/amythee/7bbfcfd4bbffaff62e857b7162001e31#file-amitypostupdate-dart" %}
{% endtab %}
{% endtabs %}

{% hint style="info" %}
You can upload a maximum of ten images/files in a single post.
{% endhint %}
