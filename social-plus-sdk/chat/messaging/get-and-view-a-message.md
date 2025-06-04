# Get and View a Message

To view the content of a message using the Social Plus Chat SDK, developers can utilize a message object. The message content can then be used to display to the user in a chat interface or to perform other operations on the message data as needed. This allows developers to build chat applications that support messaging using the Social Plus Chat SDK and provides a foundation for building more advanced chat applications that require more complex message handling and processing. The Social Plus Chat SDK provides several methods for viewing messages in a chat channel. Here's how to use these methods in your app:

## Get a single message

To get a single message by its ID, use the getting message function of the Social Plus Chat SDK. This method returns a message live object, which you can use to display the message in your app. Here's an example:

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/922cff71e45268b73dc76237005c8bfb" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/47a9a839fb20f5da62e0350497c82cc8" %}
{% endtab %}

{% tab title="JavaScript" %}
You can use the `getMessage` method to get a single comment. You need to pass the `messageId` of the requested message as the parameter.

```javascript
import { MessageRepository } from '@amityco/js-sdk';

const liveObject = MessageRepository.getMessage('messageId');
let message = liveObject.model;

liveObject .on('dataUpdated', data => {
  message = data;
});

liveObject .on('dataError', error => {
  console.error(error);
});

// unobserve data changes once you are finished
liveObject.dispose();
```

The method returns a `liveobject` instance of a message model. It will throw an error if the passed `messageId` is not valid.
{% endtab %}

{% tab title="TypeScript" %}
**Version 6 and Beta**

{% embed url="https://gist.github.com/amythee/d8ad5efbeeb1c4d8aba9b89381ca0a96" %}
{% endtab %}

{% tab title="Flutter" %}
Supported ✅ (please wait while we prepare a real example!)
{% endtab %}
{% endtabs %}

## Get messages with a query

You can also use a query to get messages that match specific criteria. The querying and filtering messages function of the Social Plus Chat SDK enables you to retrieve messages based on different parameters such as a specific user, a date range, or a display name. please refer to the page - [query-and-filter-messages.md](query-and-filter-messages.md "mention")

## View a message

### Text Message

This is the most basic type of message and is useful for sending simple messages such as chat messages, system notifications, or status updates. Each text message has a character limit of 20,000 characters, making it suitable for sending concise messages.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/922cff71e45268b73dc76237005c8bfb" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/36e3729e6da94046910e38a39060b06a" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
import React, { useEffect, useState } from 'react';
import { FileRepository, MessageType } from '@amityco/js-sdk';

// renders a text message
const TextContent = ({ data, fileId }) => {
  return data?.text ? <p>{data!.text}</p> : null;
}
```
{% endtab %}

{% tab title="TypeScript" %}
v6.0.0 and Beta

{% embed url="https://gist.github.com/dab8384f3d0cee39775e89d7155d010b" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/d90b1de36e2a83b839742b474fe044c3#file-amitymessagetextview-dart" %}
{% endtab %}
{% endtabs %}

### Image Message

Sending visual content such as photos, graphics, or images in a channel is facilitated by this type of message. The maximum size for an image is 1 GB, and the image will be automatically transformed into four different sizes for versatile usage which are:&#x20;

* Small
* Medium
* Large&#x20;
* Full

This allows for flexible usage and easy integration into various chat applications. For more information about an image, please refer to the page - [image-handling.md](../../core-concepts/files-images-and-videos/image-handling.md "mention").

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/ae6b8f030d63a60b9fa9455ae522e7dd" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/67992670a6c79c4dc7af1ceb692beeda" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
import React, { useEffect, useState } from 'react';
import { FileRepository } from '@amityco/js-sdk';

const ImageMessageContent = ({ data, fileId }) => {
  const [file, setFile] = useState();

  useEffect(() => {
    const liveObject = FileRepository.getFile(fileId);

    liveObject.on('dataUpdated', setFile);
    liveObject.model && setFile(liveObject.model);

    return () => liveObject.dispose()
  }, [fileId])

  return (
    <>
      {data?.caption && <p>{data!.caption}</p>}
      {file && <img src={file.fileUrl} />}
    </>
  )
}
```
{% endtab %}

{% tab title="TypeScript" %}
Version 6

> In TypeScript SDK, viewing a file, image, and audio message have the same steps and sample code. You can query all file types with `observeFile`.

{% embed url="https://gist.github.com/amythee/b9f396a73150c00504a063191dd12183#file-displayimagemessage-ts" %}

Beta (v0.0.1)

{% embed url="https://gist.github.com/ba44c4831ddc44c20f3942e93f03d39e" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/a160651275e49be13b7d2f9f1ab02a68#file-amitymessageimageview-dart" %}
{% endtab %}
{% endtabs %}

### File Message

This is a message that contains a file attachment, such as a PDF, a Word document, or any other type of file. This is a useful type of message for sharing files within a channel, such as a document or a photo. The maximum size for a file is 1 GB. For more information about a file, please refer to the page - [file.md](../../core-concepts/files-images-and-videos/file.md "mention")

{% tabs %}
{% tab title="iOS" %}
{% hint style="info" %}
In **iOS** SDK, `AmityFileRepository` provides `downloadFile:` and `downloadFileAsData:` method to download the file from the URL. The same method can be used to download the audio.
{% endhint %}

{% embed url="https://gist.github.com/amythee/b8dfca52e5231dd97f91b7a0b2cfcf7f" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/383f4e192626795165fc8e01e4369744" %}
{% endtab %}

{% tab title="JavaScript" %}
```django
import React, { useEffect, useState } from 'react';
import { FileRepository, MessageType } from '@amityco/js-sdk';

// renders a file message
const FileContent = ({ data, fileId }) => {
  const [file, setFile] = useState();

  useEffect(() => {
    const liveObject = FileRepository.getFile(fileId);

    liveObject.on('dataUpdated', setFile);
    liveObject.model && setFile(liveObject.model);

    return () => liveObject.dispose()
  }, [fileId])

  return (
    <>
      {file && <a href={file.fileUrl} download>{file.attributes.name}</a>}
      {data?.caption && <p>{data!.caption}</p>}
    </>
  )
}
```
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/ea0fa2f25d3229cfcfd02869c978f6db" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/11e1b2dcf207655fafe1e017d922eca8#file-amitymessagefileview-dart" %}
{% endtab %}
{% endtabs %}

### Video Message

This is a useful type of message for sharing video content within a chat conversation, such as a short clip or a longer video. The maximum size for a video is 1 GB, and the video will be automatically transcoded into different resolutions for versatile usage which are&#x20;

* 1080p
* 720p
* 480p
* 360p&#x20;
* original

Once you upload a video the videos undergo transcoding from their original resolution. You can quickly access the original size of the video right after you make the video message. However, it takes time for the transcoded resolutions to be ready. This allows for flexible usage and easy integration into various chat applications. For more information about a video, please refer to the page - [video-handling.md](../../core-concepts/files-images-and-videos/video-handling.md "mention").

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/d88642eb714baeb23338f75fb3a677d5#file-play_video_example-swift" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/f9b1616865efb4b6386074b731ca49f0" %}
{% endtab %}

{% tab title="JavaScript" %}
Supported ✅ (please wait while we prepare a real example!)
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/772918f9ef8c3585f3b79e74f36cce86" %}
{% endtab %}
{% endtabs %}

### Custom Message

In addition to the built-in message types such as text, image, file, audio, and video, the Social Plus Chat SDK also provides support for "custom messages". Custom messages allow users to design their own JSON structure that can be used to represent any kind of data, essentially providing the freedom to create their own message types.

This can be useful for a variety of use cases. For example, a developer building a chat application for a sports team could use custom messages to create a "score update" message type that contains data such as the score of a game, the time remaining, and other relevant information. Similarly, a developer building a chat application for an e-commerce platform could use custom messages to create a "product update" message type that contains information such as product details, availability, pricing, and other relevant data.

The possibilities for custom messages are endless and can be tailored to the specific needs of any application. Custom messages can be sent and received using the Social Plus Chat SDK and can be queried and displayed in a chat channel just like any other message type.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/9888131c9671f869f65cfeebf407be1b" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/ccff8550940617d27dce81198a325661" %}
{% endtab %}

{% tab title="JavaScript" %}
Supported ✅ (please wait while we prepare a real example!)
{% endtab %}

{% tab title="TypeScript" %}
For custom messages, the data is in the data property.
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/7446eaed453c4c62a950fcd1550afb68#file-amitymessagecustomview-dart" %}
{% endtab %}
{% endtabs %}
