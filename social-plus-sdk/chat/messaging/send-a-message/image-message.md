# Image Message

## Send an Image Message

An image message is a type of message that includes an image file. It allows users to share visual information with others in a chat. Image messages can be used in a variety of ways, such as sharing photos with friends, sending documents, or any other visual content that needs to be shared quickly and easily. With image messages, users can easily convey information to others in a chat, making it a powerful tool for communication.

When calling this function, you can provide the local image path on the device and the ID of the subchannel where the message will be sent. The SDK will create an image message with the specified image and send it to the subchannel.

For further information regarding video information please refer to [image-handling.md](../../../core-concepts/files-images-and-videos/image-handling.md "mention") page.

Here is a brief explanation of the function parameters:

* `text/caption`: A string that contains the text message that the user wants to send. This parameter is mandatory as it contains the actual message content.
* `attachment`: The local image path that the user wants to send on the device
* `subchannelId`: An identifier for the subchannel where the message will be sent. Subchannels are subdivisions within a channel that represent individual topics or chat threads. Messages and interactions occur within subchannels, not the main channel itself.
* `tags` - Arbitrary strings that can be used for defining and querying the messages.

<Tabs>
<Tab title="iOS">
**Version 6**

<Frame>
<Embed url="https://gist.github.com/amythee/59b9eff6d945b1393631219179f7f935" />
</Frame>

**Version 5 (Maintained)**

<Frame>
<Embed url="https://gist.github.com/amythee/7ac734cd6aa90ebfe25764f749780cad" />
</Frame>
</Tab>

<Tab title="Android">
**Version 6**

To send an image in original size, set optional `isFullImage()` to true.

<Frame>
<Embed url="https://gist.github.com/amythee/034a83d4adaae68b3d05959fe5ac5f6f" />
</Frame>

**Version 5 (Maintained)**

<Frame>
<Embed url="https://gist.github.com/amythee/dbd11302fc8ac6a1353e6638f7ebb249" />
</Frame>
</Tab>

<Tab title="JavaScript">
Here's a small example on how to create a message with an image attached. The process is pretty simple:

1. Upload an image.
2. Create a message with the uploaded image ID.

<Note>
Refer to [#upload-images](../../../core-concepts/files-images-and-videos/image-handling.md#upload-images "mention") for the sample code on how to upload a file to get `fileId.`
</Note>

```javascript
import { FileRepository, MessageRepository } from '@amityco/js-sdk';

// this function takes in input a File from a <input type="file" />
const createImageMessage = (file: File) => {
  // first, create the file object.
  const liveFile = FileRepository.createFile({ file })

  // second, create the message object with the fileId from the liveFile
  const liveMessage = MessageRepository.createImageMessage({
    channelId: 'my-channel',
    imageId: liveFile.model.fileId,
    caption: 'have a look!',
    tags: ['tag1', 'tag2'],
  })
}
```
</Tab>

<Tab title="TypeScript">
Here's a small example on how to create a message with an image attached. The process is pretty simple:

1. Upload an image.
2. Create a message with the uploaded image ID.

<Note>
Refer to [#upload-images](../../../core-concepts/files-images-and-videos/image-handling.md#upload-images "mention") for the sample code on how to upload a file to get `fileId.`
</Note>

Version 6

<Frame>
<Embed url="https://gist.github.com/amythee/08dea2bf5ae027d420e43ce4f72febaa" />
</Frame>

Beta (v0.0.1)

<Frame>
<Embed url="https://gist.github.com/988e77e33f047a5c6f714fa83e029298" />
</Frame>
</Tab>

<Tab title="Flutter">
To send an image in original size, set optional `isFullImage()` to true.

<Frame>
<Embed url="https://gist.github.com/amythee/828573cec6756faac2b872a978828bf9#file-amitymessageimagecreate-dart" />
</Frame>
</Tab>
</Tabs>

## Image Upload & Sizing

The SDK will resize and process the image object before sending it to the server. When an image is uploaded, it is automatically resized into multiple sizing options.

The size of the image is determined by its longest dimension (in pixels) with the aspect ratios being unchanged. The maximum file size of an image cannot exceed 1 GB. Social Plus will automatically optimize the image and when queried, will return the image in small, medium, and large sizes.

If the image is marked as `isFull` on upload, the original size of the image can also be returned. Note that this can drastically reduce the speed of message sending, depending on the original image size. If the `fullImage` is set to `false`, then the uploaded image size will be up to 1500x1500 pixels.

You can also pass an optional caption as part of the message. This caption will be accessible under the `data` property in the message model, under the `caption` key. You can add up to 1,000 characters of text caption per message.

<Warning>
Supported image formats are JPG, PNG, and HEIC and cannot exceed 1GB in size
</Warning>