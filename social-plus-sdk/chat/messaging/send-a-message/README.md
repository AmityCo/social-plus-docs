# Send a Message

Messaging is an essential component of any chat application, and the SDK provides robust messaging features. The SDK optimizes the messaging flow for users by instantly displaying sent messages, even before they have been delivered to the server. To ensure the user's smooth messaging experience, the SDK provides the `syncState` property in the message model to monitor the message delivery status.

Social Plus supports the sending and receiving of five types of messages:

* [text-message.md](text-message.md "mention")
* [image-message.md](image-message.md "mention")
* [video-message.md](video-message.md "mention")
* [audio-message.md](audio-message.md "mention")
* [file-message.md](file-message.md "mention")
* [custom-message.md](custom-message.md "mention")

## Message Synchronization

**SDK (Android & iOS)** now supports resynchronization of messages if the internet connection is not available or interrupted at the time the user sends a message. To support resynchronization, we enhanced the internal architecture of how the messages are queued, processed, and synced with the server.

**SDK (Typescript)** supports message synchronization starting from version 6.27.0. However, the synchronization process is not fully supported, and we cannot guarantee the order of message creation or retry and delete for failed message creations.

### Local Message

When you create a message, SDK first creates the message locally. This locally created message will be reflected immediately in the related live collection that the user is observing at the moment. Then the SDK starts syncing this message with the server. Users can check the `syncState` property of the message model inside the live collection to reflect the current state of the message.

<Tabs>
  <Tab title="iOS">
    <iframe src="https://gist.github.com/amythee/e4088b5e168246d371dbd8d85bccf989"></iframe>
  </Tab>
  <Tab title="Android">
    <iframe src="https://gist.github.com/amythee/c97bf1d736565dc00d78f63cc27a1d65"></iframe>
  </Tab>
  <Tab title="Typescript">
    <iframe src="https://gist.github.com/amythee/280009117206ae0e8fddaa6cf63652f5"></iframe>
  </Tab>
</Tabs>

### Message Syncing

Once a message is created locally, SDK adds the message to the queue and starts the process of syncing this message with the server. After the message is synced with the server, the `syncState` of the message changes to `synced`. Here is the table showing various states of the message and its corresponding `syncState` value per platform.

<table>
  <thead>
    <tr>
      <th>Message State</th>
      <th>iOS</th>
      <th width="162">Android</th>
      <th>Typescript</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>When message is created locally and waiting in queue for syncing to server</td>
      <td>syncing</td>
      <td>created</td>
      <td>syncing</td>
    </tr>
    <tr>
      <td>When message is being synced to server</td>
      <td>syncing</td>
      <td>syncing</td>
      <td>syncing</td>
    </tr>
    <tr>
      <td>When message attachment is being uploaded to server</td>
      <td>syncing</td>
      <td>uploading</td>
      <td>syncing</td>
    </tr>
    <tr>
      <td>When message is synced successfully with the server</td>
      <td>synced</td>
      <td>synced</td>
      <td>synced</td>
    </tr>
    <tr>
      <td>When message syncing failed</td>
      <td>error</td>
      <td>error</td>
      <td>error</td>
    </tr>
  </tbody>
</table>

The messages are synced in the order they get added to the queue in the FIFO (First In First Out) order. SDK will maintain the causal ordering of the message of similar types.

#### **Causal Ordering:**

SDK maintains a causal ordering for **similar** types of messages i.e. (Text, Custom) & (Image/File/Audio/Video). Let's look at the example to understand this:

If the user creates messages in this order from left to right: [**Text1** → **Image1** → **Image2** → **Text2** → **Text3** → **Image3**]

* The ordering of text messages is maintained i.e. Text 2 will be synced after Text 1 & so on
  * [**Text1** → **Text2** → **Text3**]
* The ordering of Media messages is respected i.e. Image2 will be synced after Image 1 and so on.
  * [**Image1** → **Image2** → **Image3**]
* The ordering of all messages mixed might not be respected. Ex: If image1 takes a longer time to upload, the ordering can be:
  * [**Text1** → **Text2** → **Text3** → **Image1** → **Image2** → **Image3**]

#### **Waiting for connectivity:**

SDK automatically determines the internet connection availability on the user's device and waits for a stable connection before sending the request to sync with the server. Once the connection is available, SDK syncs the message with the server maintaining the causal ordering as described above.

### **Connection Interruption / Server Error Handling**

If the network connection is interrupted during the request or the server returns an error for the request, depending upon the interruption state & error returned, SDK will automatically retry syncing the message after some interval (~ 5 seconds). SDK will retry syncing up to a maximum of 3 times and if the message still cannot be synced, SDK will mark the message as failed and notify the user through callback of createMessage API. The `syncState` of the message would change to `failed` / `error`.

<Tabs>
  <Tab title="iOS">
    <iframe src="https://gist.github.com/amythee/69df4ea51776448f36c1c9a12fbd8f60"></iframe>
  </Tab>
  <Tab title="Android">
    <iframe src="https://gist.github.com/amythee/8af21da25840b2abc194e82b2a7dc0f7"></iframe>
  </Tab>
</Tabs>

### **Failed Message Handling**

The message syncing can fail for many reasons. The user should handle the error thrown from creating message API and decide what to do for failed messages. Once the status of the message is failed, SDK will not attempt to retry syncing that message anymore. The failed messages will not be automatically removed from the live collection. It's up to the user to decide if they should resend the same message or delete the failed message so that it disappears from the live collection. The `syncState` of the failed message would be `failed` / `error`.

#### **Deleting failed message:**

You can use existing `softDeleteMessage()` method in `AmityMessageRepository` class to delete specific failed messages.

<Tabs>
  <Tab title="iOS">
    <iframe src="https://gist.github.com/amythee/fcc802b6b4b2d4731d2bd62a5b4f89a9"></iframe>
  </Tab>
  <Tab title="Android">
    <iframe src="https://gist.github.com/amythee/3b6220333711696506a6cf88b1232589"></iframe>
  </Tab>
</Tabs>

#### Deleting all failed messages:

If you do not care about any failed messages, SDK also provides deleteFailedMessages() method in the AmityMessageRepository class to allow the deletion of all failed messages.

<Tabs>
  <Tab title="iOS">
    <iframe src="https://gist.github.com/amythee/ad88242edcbe4abe2434563ded4545c7"></iframe>
  </Tab>
  <Tab title="Android">
    <iframe src="https://gist.github.com/amythee/ea3261edbfcc01a2605b2bbd0c6cbaa6"></iframe>
  </Tab>
</Tabs>

#### Deleting all failed messages upon SDK Initialization:

This message syncing process is only maintained per active session per device. If the user logs out or if the user's current session is destroyed, all the active syncing process is terminated.

When the SDK is initialized again (i.e client instance is initialized), all the messages that were in `syncing` state from the previous session would be changed to `failed` state. Users can choose to delete particular failed messages (using `softDeleteMessage()` method) or delete all failed messages (using `deleteAllFailedMessages()` method).