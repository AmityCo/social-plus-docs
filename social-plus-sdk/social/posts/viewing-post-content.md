# Viewing Post Content

## Post Structure

In Social Plus's social SDK, posts with images, files, or videos follow a Parent-Child relationship, where each uploaded image/file is represented as a separate child post. When creating an image/file post, any text that is set will act as the Parent post. The Parent post contains a child posts property, which provides an array of Social Plus Post instances for each child post. For more information about post structure, please refer to - [#post-structure](./#post-structure "mention")

Each instance of a Post holds several pieces of information, including data, reactions, comments, metadata, child posts, and more. For text posts, you can access the actual data of the post through the data property. Similarly, for child posts, developers can also access the data through the same data property. Additionally, more details about uploaded files and images can be accessed through the provided functions; such as `getFileInfo()` or `getImageInfo()`.

To illustrate this concept, consider a post that contains both text and an image. In this case, the parent post would be a text post, and its child post would be an image post. By accessing the child post property of the parent post, you can easily access and manage the child post information, allowing for a more flexible and efficient approach to managing posts in social applications.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/4f4b50ef69421a85e2ffccaf9d145f37#file-access_post_and_its_children-swift" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/c161b5f7b1683a725d50fff536896138#file-amitypostgetchildren-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/1d57bf731ff42ec8b83b4c6a9a240c1c#file-getpostimageinformation-ts" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/37d71bd90adb0021882cbbcb9760964d" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/1e2cf97b44d5b9b66b5b8f9c2914da56#file-amitypostchildrenget-dart" %}
{% endtab %}
{% endtabs %}

## Image Post

Posting visual content such as photos, graphics, or images is facilitated by this type of post. The maximum size for an image is 1 GB, and the image will be automatically transformed into four different sizes for versatile usage which are:&#x20;

* Small
* Medium
* Large&#x20;
* Full

This allows for flexible usage and easy integration into various social applications. For more information about an image, please refer to the page - [image-handling.md](../../core-concepts/files-images-and-videos/image-handling.md "mention").

{% tabs %}
{% tab title="iOS" %}
There are two ways to download the uploaded image.&#x20;

1.  Using `FileRepository`&#x20;

    `FileRepository` class provides a `downloadImage(..)` method to download images uploaded using the same class.

    **Note:** This class does not perform any kind of caching for downloaded images. Please refer to the header docs for the download method for more details.


2.  Using any third-party library or your implementation&#x20;

    You can download the file/image directly from the provided `fileUrl` using your implementation or any custom third-party libraries of your choice.

{% embed url="https://gist.github.com/amythee/4ec31f260ef121cf2ceed18caa03b13e" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/3accc334b7949786ad142fa663826cdf" %}
{% endtab %}

{% tab title="JavaScript" %}
Supported ✅ (Please wait while we prepare a real example!)
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/1d57bf731ff42ec8b83b4c6a9a240c1c#file-getpostimageinformation-ts" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/7c3d2970b1767a66f623cfc129046f2f#file-amitypostimageget-dart" %}
{% endtab %}
{% endtabs %}

If you are using your implementation to download the image of appropriate size, you need to construct the download URL yourself by appending `size` query parameter.

For example, to download a small image:

* provided URL: [https://my-image-download-link-from-amity/123/456 ](https://my-image-download-link-from-amity/123/456)
* with size query parameter: [https://my-image-download-link-from-amity/123/456?size=small](https://my-image-download-link-from-amity/123/456?size=small)

{% hint style="info" %}
Value for `Size` query parameters can be: small, medium, large, or full.
{% endhint %}

## File Post

This is a post that contains a file attachment, such as a PDF, a Word document, or any other type of file. This is a useful type of post for sharing files within a channel, such as a document or a photo. The maximum size for a file is 1 GB. For more information about a video file, please refer to the page - [file.md](../../core-concepts/files-images-and-videos/file.md "mention")

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/e8c0b662aad18f413c73647fb740ddea" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/ec7206fe5753c8b2f042d2a40f8102e9" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/c1b1f345e7909aaf4ace7893b05b0922#file-getfile-js" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/2cc90ce550d6d647b7333389635de266" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/bdf7f3acd70eaba01582b0a832c6db80#file-amitypostfileget-dart" %}
{% endtab %}
{% endtabs %}

## Video Post

This is a useful type of post for sharing video content within a feed, such as a short clip or a longer video. The maximum size for a video is 1 GB, and the video will be automatically transcoded into different resolutions for versatile usage which are&#x20;

* 1080p
* 720p
* 480p
* 360p&#x20;
* original

Once you upload a video the videos undergo transcoding from their original resolution. You can quickly access the original size of the video right after you make the video post. However, it takes time for the transcoded resolutions to be ready. This allows for flexible usage and easy integration into various social applications.  For more information about a video file, please refer to the page - [video-handling.md](../../core-concepts/files-images-and-videos/video-handling.md "mention").

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/fa1923e6b09d50796ae7adf212580ca2" %}
Get video URL example
{% endembed %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/4239ee459ebb8399b94b74f76a3ad79d" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
import { PostRepository, PostDataType } from '@amityco/js-sdk';

...

async function getPost(postId) {
  return new Promise(resolve => {
    const liveObject = PostRepository.postForId(postId);
  
    liveObject.once('dataUpdated', data => {
      resolve(data);
      liveObject.dispose();
    });
  });
}

const post = await getPost(postId);
const postChildren = await Promise.all(post.children.map(getPost));
const postVideoChild = postChildren
  .filter(child => child.dataType === PostDataType.Video)[0];
```
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/780a1dfc759c19335d8c99da910002bb#file-playpostvideo-ts" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/e1ba4f88bf33a3421c9863a354720c6a" %}
{% endtab %}
{% endtabs %}

## Live stream Post

Live stream posts offer an effective means of creating captivating and interactive content that engages users and promotes deeper connections among them. The Social Plus SDK enables developers to swiftly integrate live stream posts into a social feed, allowing them to share their real-time experiences with other users on the platform. For more information about live streaming, please refer to the page - [video](../../video/ "mention").

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/e5f51a6800314ce42f7a9b050279dba2#file-get_stream_from_post-swift" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/b260d31360de3485f686babbcda0fb88" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/769831c506b5c89e214ee40c82d16562#file-getstream-ts" %}
{% endtab %}
{% endtabs %}

## Poll Post

To implement poll functionality in posts, developers can leverage the existing poll features in Social Plus SDK and integrate them into posts. Polls can be created as child posts within the post thread, with the poll data and options easily accessible to users. Users can then participate in the poll by selecting their preferred option, and the results can be displayed in posts. For more information about live streaming, please refer to the page - [poll.md](../../core-concepts/poll.md "mention").

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/4192a3d10e032e9ffc07c52a41a7f26d#file-get_poll_from_post-swift" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/f46836114c535b70e2f97f7986ef7cf9" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/52181e3bea5e64e8eabb24b3216919c2#file-getpoll-js" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/c6b5a9e25b503f9ab71f8948f150fbfe" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/5e9e2987b145eb80816678fd1e408d36#file-amitypollget-dart" %}
{% endtab %}
{% endtabs %}
