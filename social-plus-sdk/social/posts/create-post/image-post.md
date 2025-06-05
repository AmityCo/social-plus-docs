# Image Post

Prior to creating an image post, it is crucial to upload the images that will be included in the post data to ensure that the necessary information is accessible and can be linked to the post. This requires uploading the image first, to obtain the image data that will be used in creating the image post. To upload an image, please refer to [#upload-images](../../../core-concepts/files-images-and-videos/image-handling.md#upload-images "mention").

Upon successful completion of the image upload process, you can include the image data as a parameter when creating an image post, as demonstrated in the code sample below.

Here's an explanation of the method's parameters:

* `text`: This is a required parameter of type `String`, which represents the text content of the new post. You can pass in any text you want to include in the post, up to a maximum length of 20,000 characters.
* `images`: Which represents an array of images uploaded by the user on Android, iOS and Flutter and `imageIds` for Typescript and Javascript to include in the new post. You can pass up to 10 images in a post.
* `targetType` - Type of the target, either a particular community or a user feed.
* `tags` - Arbitrary strings that can be used for defining and querying for the posts (Except Flutter).
* `metaData` - Additional properties to support custom fields.

**Requirements for Image**

* The maximum file size limit is up to 1 GB.

<Tabs>
<Tab title="iOS">
We can build the post first by using `AmityImagePostBuilder`. Then use the `createImagePost` method in `AmityPostRepository` to create image post.

<Embed url="https://gist.github.com/amythee/59b5728fedb04b7802613b36eca55213" />
</Tab>

<Tab title="Android">
We can build the post first by using `AmityImagePostCreator.Builder`. Then use the same `createPost` method in `AmityPostRepository` to create an image post.

<Embed url="https://gist.github.com/amythee/38f66cbf0bcec9a2b6e27dfb01329f04#file-amitypostimagecreation-kt" />
</Tab>

<Tab title="JavaScript">
<Embed url="https://gist.github.com/amythee/b29244f0cf72e26e29d2da04f20ceebe#file-createimagepost-js" />

An image post data structure is:

```javascript
normalPostStructure + {
  dataType: "image",
  data: { imageId: File["fileId"] }
}
```

<Warning>
Updating image post in JS SDK is not yet supported.
</Warning>
</Tab>

<Tab title="TypeScript">
<Embed url="https://gist.github.com/213b708c6f722fd05f3b01e72afa2e50" />
</Tab>

<Tab title="Flutter">
<Embed url="https://gist.github.com/amythee/53e67894a1e6baa80c99ef4681a50ea4#file-amitypostimagecreation-dart" />

<Info>
* Updating images in image post is not yet supported.
* Refer to Post target type for  a more detailed explanation of the `targetType` parameter.
</Info>
</Tab>
</Tabs>

<Info>
A post can have a maximum of ten images.
</Info>