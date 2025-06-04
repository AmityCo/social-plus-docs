# File Handling

Files are an essential component of modern software applications. Social Plus provides a powerful file management system that enables you to easily handle different types of files, such as document files, videos, and audio files. In this section, we will introduce you to the concept of a file in Social Plus and provide an overview of file handling in Social Plus.

{% hint style="info" %}
Note: The maximum file size limits are up to 1 GB per post.
{% endhint %}

## File Data

| Property     | Description                       |
| ------------ | --------------------------------- |
| `fileId`     | Root file key on cloud storage    |
| `fileUrl`    | HTTP link for file download       |
| `type`       | File type                         |
| `createdAt`  | Date/time when a file is uploaded |
| `updatedAt`  | Date/time when a file is updated  |
| `attributes` | Information about the file        |

## Upload Files

To upload a file to the system, you can use the Social Plus File Upload API provided by the SDK. The API allows you to upload a file to the Social Plus server by giving the file's data and the file metadata, such as the file name, file type, and file size. The SDK simplifies the process of uploading files by providing pre-built components that you can easily integrate into your application.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/92a922edb304769ace1b3defbd3a326e" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/27ce0656b48e13f36f354e58a2cc5248" %}

On Android, you can separately observe uploading states outside of the uploading method by using:

{% embed url="https://gist.github.com/amythee/efc1168fa5c08f1b85f7e0cb96699aee" %}
{% endtab %}

{% tab title="JavaScript" %}
<pre class="language-javascript"><code class="lang-javascript"><strong>import { FileRepository, LoadingStatus } from '@amityco/js-sdk';
</strong>
const liveObject = FileRepository.createFile({ 
  file, // https://developer.mozilla.org/en-US/docs/Web/API/File
  onProgress: ({ currentFile, currentPercent }) => {
  },
});

liveObject.on('loadingStatusChanged', ({ newValue }) => {
  if (newValue === LoadingStatus.Loaded) {
    console.log('The file is uploaded', liveObject.model);
  }
});

liveObject.on('dataError', (error) => {
  console.error('can not upload the file', error);
});

// upload video
const liveObject = FileRepository.createVideo({ 
  file,
  onProgress: ({ currentFile, currentPercent }) => {
  },
});
Refer to the 
file model
 for the description of the response after a successful file creation. If an error is encountered while creating the file, it will return the following errors:
//Attached file payload is too large
{
  "status": "error",
  "code": 500000,
  "message": "Payload too large."
}

// Unexpected error
{
  "status": "error",
  "code": 500000,
  "message": "Unexpected error"
}
</code></pre>
{% endtab %}

{% tab title="TypeScript" %}
**Version 6 and Beta(v0.0.1)**

{% embed url="https://gist.github.com/amythee/15d4d9e9671dbf02a073c29ccf0d073f#file-createfile-ts" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/961f689cc424da0e56bac0a33b93a66a" %}
{% endtab %}
{% endtabs %}

## Retrieve Files

You can retrieve a file from Social Plus using the Social Plus File Retrieval API provided by the SDK. The API enables you to retrieve a file from the Social Plus server by supplying the file ID. The SDK streamlines the process of retrieving files by offering pre-made components that can be smoothly integrated into your app.&#x20;

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/0891318fc27c3d0b71e7f4f1c4b963f5" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/160487555d0eb46cc5ecb4d315d20204" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
import { FileRepository } from '@amityco/js-sdk';

let file;
const liveObject = FileRepository.getFile(fileId);

liveObject.on('dataUpdated', (updatedModel) => {
  file = updatedModel;
});

liveObject.on('dataError', (error) => {
  console.error('Can not get the file', error);
});

file = liveObject.model;
```
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/9be1af4a4462d2438da84f6a52aad5ff" %}
{% endtab %}
{% endtabs %}

## Delete Files

In addition to uploading and retrieving files, Social Plus provides a deleting function to delete a file that is no longer needed.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/050b0549f52947f3f970b2bd3ac2800e" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/7e45cd17295ddbdae89745b30c526cbe" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
import { FileRepository } from '@amityco/js-sdk';

const success = await FileRepository.deleteFile(fileId);
```

The response will return `true` if the file deletion is successful.
{% endtab %}

{% tab title="TypeScript" %}
**Version 6 and Beta(v0.0.1)**

{% embed url="https://gist.github.com/amythee/ec67896e4cfb946b3754e9649e4a516b#file-deletefile-ts" %}

The response will return `true` if the file deletion is successful.

```typescript
"data": {
    "success": true
  }
```

Otherwise, if an error is encountered during the deletion, it will return the following errors:

```typescript
//Permission denied error
{
  "status": "error",
  "code": 400301,
  "message": "Permission denied"
}

Resource Not Found error
{
  "status": "error",
  "code": 400400,
  "message": "Resource Not Found."
}

//Passed the wrong parameters error
{
  "status": "error",
  "code": 500000,
  "message": "Parameters error."
}
```
{% endtab %}
{% endtabs %}
