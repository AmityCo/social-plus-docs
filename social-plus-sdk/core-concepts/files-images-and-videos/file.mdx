# File Handling

Files are an essential component of modern software applications. Social Plus provides a powerful file management system that enables you to easily handle different types of files, such as document files, videos, and audio files. In this section, we will introduce you to the concept of a file in Social Plus and provide an overview of file handling in Social Plus.

<Info>Note: The maximum file size limits are up to 1 GB per post.</Info>

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

<Tabs>
<Tab title="iOS">
<Frame>
```swift
let fileData = "file_data".data(using: .utf8)!
let file = AmityFile(fileData: fileData, attributes: nil)
AmityFileRepository().uploadFile(file) { (progress, file, error) in
    if let error = error {
        print("Error uploading file: \(error)")
        return
    }
    
    if let file = file {
        print("File uploaded successfully: \(file)")
    }
}
```
</Frame>
</Tab>

<Tab title="Android">
<Frame>
```kotlin
val file = File("path/to/file")
val fileRepository = AmityFileRepository(client)
fileRepository.uploadFile(file).subscribe { file ->
    // Handle the uploaded file
}
```
</Frame>

On Android, you can separately observe uploading states outside of the uploading method by using:

<Frame>
```kotlin
fileRepository.getUploadInfo(fileId).subscribe { uploadInfo ->
    when (uploadInfo.getState()) {
        State.UPLOADING -> {
            val progress = uploadInfo.getProgress()
            // Handle upload progress
        }
        State.COMPLETED -> {
            // Handle upload completion
        }
        State.FAILED -> {
            val error = uploadInfo.getError()
            // Handle upload failure
        }
    }
}
```
</Frame>
</Tab>

<Tab title="JavaScript">
```javascript
import { FileRepository, LoadingStatus } from '@amityco/js-sdk';

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
```
</Tab>

<Tab title="TypeScript">
**Version 6 and Beta(v0.0.1)**

<Frame>
```typescript
import { FileRepository } from '@amityco/js-sdk';

const file = new File([''], 'filename');
const { data: fileUpload } = await FileRepository.createFile(file);
```
</Frame>
</Tab>

<Tab title="Flutter">
<Frame>
```dart
final file = File('path/to/file');
final result = await AmityFileRepository().uploadFile(file);
```
</Frame>
</Tab>
</Tabs>

## Retrieve Files

You can retrieve a file from Social Plus using the Social Plus File Retrieval API provided by the SDK. The API enables you to retrieve a file from the Social Plus server by supplying the file ID. The SDK streamlines the process of retrieving files by offering pre-made components that can be smoothly integrated into your app.

<Tabs>
<Tab title="iOS">
<Frame>
```swift
AmityFileRepository().getFile(withFileId: "fileId") { (file, error) in
    if let error = error {
        print("Error retrieving file: \(error)")
        return
    }
    
    if let file = file {
        print("File retrieved successfully: \(file)")
    }
}
```
</Frame>
</Tab>

<Tab title="Android">
<Frame>
```kotlin
val fileRepository = AmityFileRepository(client)
fileRepository.getFile(fileId).subscribe { file ->
    // Handle the retrieved file
}
```
</Frame>
</Tab>

<Tab title="JavaScript">
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
</Tab>

<Tab title="TypeScript">
<Frame>
```typescript
import { FileRepository } from '@amityco/js-sdk';

const { data: file } = await FileRepository.getFile(fileId);
```
</Frame>
</Tab>
</Tabs>

## Delete Files

In addition to uploading and retrieving files, Social Plus provides a deleting function to delete a file that is no longer needed.

<Tabs>
<Tab title="iOS">
<Frame>
```swift
AmityFileRepository().deleteFile(withFileId: "fileId") { (success, error) in
    if let error = error {
        print("Error deleting file: \(error)")
        return
    }
    
    if success {
        print("File deleted successfully")
    }
}
```
</Frame>
</Tab>

<Tab title="Android">
<Frame>
```kotlin
val fileRepository = AmityFileRepository(client)
fileRepository.deleteFile(fileId).subscribe { success ->
    // Handle the deletion result
}
```
</Frame>
</Tab>

<Tab title="JavaScript">
```javascript
import { FileRepository } from '@amityco/js-sdk';

const success = await FileRepository.deleteFile(fileId);
```

The response will return `true` if the file deletion is successful.
</Tab>

<Tab title="TypeScript">
**Version 6 and Beta(v0.0.1)**

<Frame>
```typescript
import { FileRepository } from '@amityco/js-sdk';

const { data } = await FileRepository.deleteFile(fileId);
```
</Frame>

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
</Tab>
</Tabs>