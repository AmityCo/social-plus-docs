# Video Post

Prior creating a video post, it is crucial to upload the videos that will be included in the post data to ensure that the necessary information is accessible and can be linked to the post. This requires uploading the video first, to obtain the video data that will be used in creating the video post. To upload a video, please refer to [#upload-videos](../../../core-concepts/files-images-and-videos/video-handling.md#upload-videos "mention")

Upon successful completion of the video upload process, you can include the video data as a parameter when creating a video post, as demonstrated in the code sample below.

Here's an explanation of the method's parameters:

* `text`: This is a required parameter of type `String`, which represents the text content of the new post. You can pass in any text you want to include in the post, up to a maximum length of 20,000 characters.
* `videos`: Which represents an array of videos uploaded by the user on Android, iOS and Flutter and `videoIds` for Typescript and Javascript to include in the new post. You can pass up to 10 videos in a post.
* `targetType` - Type of the target, either a particular community or a user feed.
* `tags` - Arbitrary strings that can be used for defining and querying for the posts (Except Flutter).
* `metaData` - Additional properties to support custom fields.

**Requirements for Video**

* Supported video types are `3gp`**,** `avi`**,** `f4v`**,** `flv`**,** `m4v`**,** `mov`**,** `mp4`**,** `ogv`**,** `3g2`, `wmv`, `vob`, `webm`, `mkv`
* The maximum file size limit is up to 2 GB.
* The maximum duration of the video is 2 hours

{% tabs %}
{% tab title="iOS" %}
We can build the post first by using `AmityVideoPostBuilder`. Then use the `createVideoPost` method in `AmityPostRepository` to create a video post.

{% embed url="https://gist.github.com/amythee/7bdb11b98fbc0c80b945e1c1205b4847" %}
{% endtab %}

{% tab title="Android" %}
We can build the post first by using `AmityFilePostCreator.Builder`. Then use the same `createPost` method in `AmityPostRepository` to create an image post.

{% embed url="https://gist.github.com/amythee/84582804ce6477c42aa1a86f1acd7e69#file-amitypostvideocreation-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/6f013397c66891decacb08b0df14bc6c#file-createvideopost-js" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/306f1d249a52cbe9fa26c2e417650211" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/4da70fc3109fff7e3f457b1eb1564f07#file-amitypostvideocreation-dart" %}
{% endtab %}
{% endtabs %}

{% hint style="info" %}
* A post can have a maximum of ten videos.
* Uploading HDR video format is not supported on iOS.
{% endhint %}
