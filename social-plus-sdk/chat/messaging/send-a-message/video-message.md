# Video Message

## Send a Video Message

Video messages allow users to share videos within a chat or social platform. This could be anything from a quick clip to a longer, more detailed video. With the Social Plus SDK, developers can easily integrate video message functionality into their apps, allowing users to record, upload, and share videos in real-time.

To send a video message, you must pass a valid local file URL instance instead. You can also specify an optional caption as part of the message. This caption is accessible via the data property in the message model under the `caption` or `text` key. You can add up to 1,000 characters of text per message. When a video is uploaded, it is automatically resized to the maximum size of 480p.

For further information regarding video information please refer to [video-handling.md](../../../core-concepts/files-images-and-videos/video-handling.md "mention") page.

{% hint style="info" %}
* The maximum file size of the video is 1 GB.
* The thumbnail for the video message is created automatically.
{% endhint %}

Here is a brief explanation of the function parameters:

* `text/caption`: A string that contains the text message that the user wants to send. This parameter is mandatory as it contains the actual message content.
* `attachment`: The local video path that the user wants to send on the device
* `subchannelId`: An identifier for the subchannel where the message will be sent. Subchannels are subdivisions within a channel that represent individual topics or chat threads. Messages and interactions occur within subchannels, not the main channel itself.
* `tags` - Arbitrary strings that can be used for defining and querying for the messages.

{% tabs %}
{% tab title="iOS" %}
**Version 6**

{% embed url="https://gist.github.com/amythee/f891aebbc87b1524ac066fa75ae93c00" %}

**Version 5 (Maintained)**

{% embed url="https://gist.github.com/amythee/0f264196abc2b4b126aa35c644277b65" %}
{% endtab %}

{% tab title="Android" %}
**Version 6**

{% embed url="https://gist.github.com/amythee/49e821c197f3b17e0d6b3d0ee2b25af5" %}

**Version 5 (Maintained)**

{% embed url="https://gist.github.com/amythee/7f15998197ee7b9ad06a7a8aac40f682" %}
{% endtab %}

{% tab title="JavaScript" %}
Supported ✅ (please wait while we prepare a real example!)
{% endtab %}

{% tab title="TypeScript" %}
{% hint style="info" %}
Refer to [video-handling.md](../../../core-concepts/files-images-and-videos/video-handling.md "mention") for sample code on how to upload videos and check its progress.
{% endhint %}

Version 6

{% embed url="https://gist.github.com/amythee/772918f9ef8c3585f3b79e74f36cce86#file-createvideomessage-ts" %}

Beta (v0.0.1)

{% embed url="https://gist.github.com/e5c16806c6ebfd69a699d79549b15bcb" %}
{% endtab %}
{% endtabs %}
