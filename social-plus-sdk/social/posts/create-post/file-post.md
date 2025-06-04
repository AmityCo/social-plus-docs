# File Post

Prior to creating a file post, it is crucial to upload the files that will be included in the post data to ensure that the necessary information is accessible and can be linked to the post. This requires uploading the file first, to obtain the file data that will be used in creating the file post. To upload a file, please refer to [#upload-files](../../../core-concepts/files-images-and-videos/file.md#upload-files "mention")

Upon successful completion of the file upload process, you can include the file data as a parameter when creating a file post, as demonstrated in the code sample below.

Here's an explanation of the method's parameters:

* `text`: This is a required parameter of type `String`, which represents the text content of the new post. You can pass in any text you want to include in the post, up to a maximum length of 20,000 characters.
* `files`: Which represents an array of files uploaded by the user on Android, iOS and Flutter and `fileIds` for Typescript and Javascript to include in the new post. You can pass up to 10 files in a post.
* `targetType` - Type of the target, either a particular community or a user feed.
* `tags` - Arbitrary strings that can be used for defining and querying for the posts (Except Flutter).
* `metaData` - Additional properties to support custom fields.

**Requirements for File**

* The maximum file size limit is up to 1 GB.

{% tabs %}
{% tab title="iOS" %}
We can build the post first by using `AmityFilePostBuilder`. Then use the `createFilePost` method in `AmityPostRepository` to create a file post.

{% embed url="https://gist.github.com/amythee/36c78812a3c17917f15c99e0b0c014e6" %}
{% endtab %}

{% tab title="Android" %}
We can build the post first by using `AmityFilePostCreator.Builder`. Then use the same `createPost` method in `AmityPostRepository` to create an image post.

{% embed url="https://gist.github.com/amythee/14b4c1493117c6b55e4018dbb17efe1b#file-amitypostfilecreation-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/073b1f78add7b0ab5890148f87a93c01#file-createimagepost-js" %}
{% endtab %}

{% tab title="TypeScript" %}
Version 6

{% embed url="https://gist.github.com/ee133f379abcf710624f9466fd78a76b" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/bd5a3d58f619c5fc89438b5a3ce33618#file-amitypostfilecreation-dart" %}

{% hint style="info" %}
* Updating files in a file post is not yet supported.
* Refer to [Post target type](../#post-description) for a more detailed explanation of the `targetType` parameter.
{% endhint %}
{% endtab %}
{% endtabs %}

{% hint style="info" %}
A post can have a maximum of ten files.
{% endhint %}
