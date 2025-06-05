# Get and View a Message

To view the content of a message using the Social Plus Chat SDK, developers can utilize a message object. The message content can then be used to display to the user in a chat interface or to perform other operations on the message data as needed. This allows developers to build chat applications that support messaging using the Social Plus Chat SDK and provides a foundation for building more advanced chat applications that require more complex message handling and processing. The Social Plus Chat SDK provides several methods for viewing messages in a chat channel. Here's how to use these methods in your app:

## Get a single message

To get a single message by its ID, use the getting message function of the Social Plus Chat SDK. This method returns a message live object, which you can use to display the message in your app. Here's an example:

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
AmityMessageRepository.getMessage("messageId")
```
</CodeGroup>
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
messageRepository.getMessage("messageId")
```
</CodeGroup>
</Tab>

<Tab title="JavaScript">
You can use the `getMessage` method to get a single comment. You need to pass the `messageId` of the requested message as the parameter.

```javascript
import { MessageRepository } from '@amityco/js-sdk';

const liveObject = MessageRepository.getMessage('messageId');
let message = liveObject.model;

liveObject.on('dataUpdated', data => {
  message = data;
});

liveObject.on('dataError', error => {
  console.error(error);
});

// unobserve data changes once you are finished
liveObject.dispose();
```

The method returns a `liveobject` instance of a message model. It will throw an error if the passed `messageId` is not valid.
</Tab>

<Tab title="TypeScript">
**Version 6 and Beta**

<CodeGroup>
```typescript
const liveObject = MessageRepository.getMessage(messageId);
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
Supported ✅ (please wait while we prepare a real example!)
</Tab>
</Tabs>

## Get messages with a query

You can also use a query to get messages that match specific criteria. The querying and filtering messages function of the Social Plus Chat SDK enables you to retrieve messages based on different parameters such as a specific user, a date range, or a display name. please refer to the page - [query-and-filter-messages.md](query-and-filter-messages.md "mention")

## View a message

### Text Message

This is the most basic type of message and is useful for sending simple messages such as chat messages, system notifications, or status updates. Each text message has a character limit of 20,000 characters, making it suitable for sending concise messages.

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
let message = channel.messages[indexPath.row]
if let textMessage = message as? AmityTextMessage {
    print("Message text: \(textMessage.text)")
}
```
</CodeGroup>
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
val message = messageAdapter.getItem(position)
if (message.getMessageType() == AmityMessage.Type.TEXT) {
    val textData = message.getData() as AmityMessage.TextData
    println("Message text: ${textData.getText()}")
}
```
</CodeGroup>
</Tab>

<Tab title="JavaScript">
```javascript
import React, { useEffect, useState } from 'react';
import { FileRepository, MessageType } from '@amityco/js-sdk';

// renders a text message
const TextContent = ({ data, fileId }) => {
  return data?.text ? <p>{data!.text}</p> : null;
}
```
</Tab>

<Tab title="TypeScript">
v6.0.0 and Beta

<CodeGroup>
```typescript
const message = await client.getMessageById(messageId);
if (message.type === MessageType.TEXT) {
  console.log(message.data.text);
}
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
<CodeGroup>
```dart
Widget build(BuildContext context) {
  return Text(widget.message.data?.text ?? '');
}
```
</CodeGroup>
</Tab>
</Tabs>

### Image Message

Sending visual content such as photos, graphics, or images in a channel is facilitated by this type of message. The maximum size for an image is 1 GB, and the image will be automatically transformed into four different sizes for versatile usage which are:&#x20;

* Small
* Medium
* Large&#x20;
* Full

This allows for flexible usage and easy integration into various chat applications. For more information about an image, please refer to the page - [image-handling.md](../../core-concepts/files-images-and-videos/image-handling.md "mention").

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
if let imageMessage = message as? AmityImageMessage {
    imageView.image = imageMessage.image
}
```
</CodeGroup>
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
if (message.getMessageType() == AmityMessage.Type.IMAGE) {
    val imageData = message.getData() as AmityMessage.ImageData
    Glide.with(context)
        .load(imageData.getFileUrl())
        .into(imageView)
}
```
</CodeGroup>
</Tab>

<Tab title="JavaScript">
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
</Tab>

<Tab title="TypeScript">
Version 6

> In TypeScript SDK, viewing a file, image, and audio message have the same steps and sample code. You can query all file types with `observeFile`.

<CodeGroup>
```typescript
const file = await client.observeFile(fileId);
console.log(file.url);
```
</CodeGroup>

Beta (v0.0.1)

<CodeGroup>
```typescript
const message = await client.getMessageById(messageId);
if (message.type === MessageType.IMAGE) {
  console.log(message.data.fileUrl);
}
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
<CodeGroup>
```dart
Widget build(BuildContext context) {
  return Image.network(widget.message.data?.fileUrl ?? '');
}
```
</CodeGroup>
</Tab>
</Tabs>

### File Message

This is a message that contains a file attachment, such as a PDF, a Word document, or any other type of file. This is a useful type of message for sharing files within a channel, such as a document or a photo. The maximum size for a file is 1 GB. For more information about a file, please refer to the page - [file.md](../../core-concepts/files-images-and-videos/file.md "mention")

<Tabs>
<Tab title="iOS">
<Info>
In **iOS** SDK, `AmityFileRepository` provides `downloadFile:` and `downloadFileAsData:` method to download the file from the URL. The same method can be used to download the audio.
</Info>

<CodeGroup>
```swift
if let fileMessage = message as? AmityFileMessage {
    print("File URL: \(fileMessage.fileURL)")
}
```
</CodeGroup>
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
if (message.getMessageType() == AmityMessage.Type.FILE) {
    val fileData = message.getData() as AmityMessage.FileData
    println("File URL: ${fileData.getFileUrl()}")
}
```
</CodeGroup>
</Tab>

<Tab title="JavaScript">
```javascript
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
</Tab>

<Tab title="TypeScript">
<CodeGroup>
```typescript
const message = await client.getMessageById(messageId);
if (message.type === MessageType.FILE) {
  console.log(message.data.fileUrl);
}
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
<CodeGroup>
```dart
Widget build(BuildContext context) {
  return Text(widget.message.data?.fileName ?? '');
}
```
</CodeGroup>
</Tab>
</Tabs>

### Video Message

This is a useful type of message for sharing video content within a chat conversation, such as a short clip or a longer video. The maximum size for a video is 1 GB, and the video will be automatically transcoded into different resolutions for versatile usage which are&#x20;

* 1080p
* 720p
* 480p
* 360p&#x20;
* original

Once you upload a video the videos undergo transcoding from their original resolution. You can quickly access the original size of the video right after you make the video message. However, it takes time for the transcoded resolutions to be ready. This allows for flexible usage and easy integration into various chat applications. For more information about a video, please refer to the page - [video-handling.md](../../core-concepts/files-images-and-videos/video-handling.md "mention").

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
if let videoMessage = message as? AmityVideoMessage {
    videoPlayer.play(url: videoMessage.fileURL)
}
```
</CodeGroup>
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
if (message.getMessageType() == AmityMessage.Type.VIDEO) {
    val videoData = message.getData() as AmityMessage.VideoData
    videoPlayer.setVideoPath(videoData.getFileUrl())
}
```
</CodeGroup>
</Tab>

<Tab title="JavaScript">
Supported ✅ (please wait while we prepare a real example!)
</Tab>

<Tab title="TypeScript">
<CodeGroup>
```typescript
const message = await client.getMessageById(messageId);
if (message.type === MessageType.VIDEO) {
  console.log(message.data.fileUrl);
}
```
</CodeGroup>
</Tab>
</Tabs>

### Custom Message

In addition to the built-in message types such as text, image, file, audio, and video, the Social Plus Chat SDK also provides support for "custom messages". Custom messages allow users to design their own JSON structure that can be used to represent any kind of data, essentially providing the freedom to create their own message types.

This can be useful for a variety of use cases. For example, a developer building a chat application for a sports team could use custom messages to create a "score update" message type that contains data such as the score of a game, the time remaining, and other relevant information. Similarly, a developer building a chat application for an e-commerce platform could use custom messages to create a "product update" message type that contains information such as product details, availability, pricing, and other relevant data.

The possibilities for custom messages are endless and can be tailored to the specific needs of any application. Custom messages can be sent and received using the Social Plus Chat SDK and can be queried and displayed in a chat channel just like any other message type.

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
if let customMessage = message as? AmityCustomMessage {
    let data = customMessage.data
    // Handle custom data
}
```
</CodeGroup>
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
if (message.getMessageType() == AmityMessage.Type.CUSTOM) {
    val customData = message.getData() as AmityMessage.CustomData
    // Handle custom data
}
```
</CodeGroup>
</Tab>

<Tab title="JavaScript">
Supported ✅ (please wait while we prepare a real example!)
</Tab>

<Tab title="TypeScript">
For custom messages, the data is in the data property.
</Tab>

<Tab title="Flutter">
<CodeGroup>
```dart
Widget build(BuildContext context) {
  return Text(widget.message.data?.customData.toString() ?? '');
}
```
</CodeGroup>
</Tab>
</Tabs>