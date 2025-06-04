# File Message

## Send a File Message

A file message is a type of message that allows users to share files with each other within a chat or messaging app. This can include documents, images, videos, and other types of files. To send a file message, the user simply selects the file they want to share and sends it through the app.

When a user receives a file message, they can view or download the file directly within the app. This makes it easy for users to share important files and collaborate with each other without having to switch between different applications or email clients.

A File message can include any of the following:

* Image
* Audio
* File
* Custom

To send a file message, you must provide a valid local file `URL` instance of the selected file and file name for the file. The default file name is `file`. The SDK will check the size of the data whether it is exceeding the limit or not before sending it to the server. If the size of the data is more than the limit, the callback will return an `Error` object with the error information that you can parse and then show an error message.

Here is a brief explanation of the function parameters:

* `text/caption`: A string that contains the text message that the user wants to send. This parameter is mandatory as it contains the actual message content.
* `attachment`: The local file path that the user wants to send on the device
* `subchannelId`: An identifier for the subchannel where the message will be sent. Subchannels are subdivisions within a channel that represent individual topics or chat threads. Messages and interactions occur within subchannels, not the main channel itself.
* `tags` - Arbitrary strings that can be used for defining and querying for the messages.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/f3022757d5bb3d6b7022cd5837047428" %}
{% endtab %}

{% tab title="Android" %}
**Version 6**

{% embed url="https://gist.github.com/amythee/5165b9699805027f71a777590bb8afb0" %}

**Version 5 (Maintained)**

{% embed url="https://gist.github.com/amythee/c3aee3ae6df5568d2de7788a8b14aa0f#file-amityfilehandling-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
Here's a small example on how to create a message with an image attached. The process is pretty simple:

1. Upload a file.
2. Create a message with the uploaded file ID.

{% hint style="info" %}
Refer to [#upload-files](../../../core-concepts/files-images-and-videos/file.md#upload-files "mention") for the sample code on how to upload a file to get `fileId.`
{% endhint %}

```javascript
import { MessageRepository, MessageType  } from '@amityco/js-sdk';

// this function takes in input a File from a <input type="file" />
const createFileMessage = (file: File) => {
  // first, create the file object.
  const liveFile = FileRepository.createFile({ file })

  // second, create the message object with the fileId from the liveFile
  const liveMessage = MessageRepository.createFileMessage({
    channelId: 'my-channel',
    fileId: id, // id of the file created with FileRepository.createFile
    caption: 'have a look!',
    tags: ['tag1', 'tag2'],
  })
}ja
```
{% endtab %}

{% tab title="TypeScript" %}
Here's a small example on how to create a message with an image attached. The process is pretty simple:

1. Upload a file.
2. Create a message with the uploaded file ID.

{% hint style="info" %}
Refer to [#upload-files](../../../core-concepts/files-images-and-videos/file.md#upload-files "mention") for the sample code on how to upload a file to get `fileId.`
{% endhint %}

Version 6

{% embed url="https://gist.github.com/3f0d2318c386cb562c039c7cd067b75a" %}

Beta (v0.0.1)

{% embed url="https://gist.github.com/53f7da5da5289eb8e59587e875a229e5" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/5b0640112b6939c9435164ef144bc27c#file-amitymessagefilecreate-dart" %}
{% endtab %}
{% endtabs %}
