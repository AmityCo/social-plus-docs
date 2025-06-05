# Video Handling

## Video Data <a name="image-data" id="image-data"></a>

The video data is the representation of the video that has been uploaded using the SDK. The uploaded video will be transcoded to other different resolutions depending on console settings. Below is a table of properties that it contains.

<Note>
Note: The maximum video file size limits are up to 2 GB per post.
</Note>

<table><thead><tr><th width="202">Property</th><th>Description</th></tr></thead><tbody><tr><td><code>fileId</code></td><td>Identifier for the uploaded file</td></tr><tr><td><code>fileUrl</code></td><td>The HTTP web URL for the uploaded file. You can use this <code>fileUrl</code> for downloading the original video file. (The file format remains unchanged)</td></tr><tr><td><code>attributes</code></td><td>Contains a dictionary with values for <code>name</code>, <code>extension</code>, <code>size</code> and <code>mimeType</code> of uploaded video.</td></tr><tr><td><code>attributes.metadata</code></td><td>Contains a dictionary with values for <code>video</code> and <code>audio</code> of uploaded video.</td></tr><tr><td><code>attributes.metadata.video</code></td><td>Contains a dictionary with values for <code>width</code>, <code>height</code>, <code>duration</code>, <code>bit_rate</code>, <code>avg_frame_rate</code> and <code>display_aspect_ratio</code></td></tr><tr><td><code>attributes.metadata.audio</code></td><td>Contains a dictionary with values for <code>duration</code>, <code>bit_rate</code> and <code>sample_rate</code></td></tr><tr><td><code>videoUrl</code></td><td><p>After video uploaded and transcoded by the server. The video data will contain <code>videoUrl</code> that provides different video URLs for each resolution.</p><ol><li><strong>original</strong> - the equivalent resolution to <code>fileUrl</code></li><li><strong>1080p</strong> - 1920×1080 in horizontal, and 1080x1920 in vertical</li><li><strong>720p</strong> - 1280×720 horizontal, and 720x1280 in vertical</li><li><strong>480p</strong> - 640x480 horizontal, and 480x640 in vertical</li><li><strong>360p</strong> - 480x360 horizontal, and 360x480 in vertical</li></ol><p>(All transcoded videos are in MP4 format)</p></td></tr><tr><td><code>status</code></td><td><p>An enum represents 4 video statues</p><ol><li><strong>uploaded</strong> - the video is uploaded and users can watch the original raw file on <code>fileUrl</code></li><li><strong>transcoding</strong> - the video is being transcoded to pre-defined resolutions</li><li><strong>transcoded</strong> - the video is transcoded and the resolutions are provided to <code>videoUrl</code></li><li><strong>error</strong> - the video encounters an issue while transcoding</li></ol></td></tr></tbody></table>

<Note>
The `fileUrl` and `videoUrl.original` provides the URL of the same video resolution.
The difference being, `fileUrl` returns the actual file format while `videoUrl.original` returns MP4 format.
</Note>

## Upload Videos

To upload a video to the system, you can use the Social Plus Video Upload API provided by the SDK. The API allows you to upload a video to the Social Plus server. The SDK simplifies the process of uploading videos by providing pre-built components that you can easily integrate into your application.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      <CodeBlock>
        {`https://gist.github.com/amythee/88605cdb8973e262a01024e76c071c65`}
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
      <CodeBlock>
        {`https://gist.github.com/amythee/3aeb5fe489319c2c72c45ad4a378b6e0#file-amitypostvideoupload-kt`}
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="JavaScript">
    Supported ✅ (please wait while we prepare a real example!)
  </Tab>
  <Tab title="TypeScript">
    **Version 6 and Beta(v0.0.1)**

    <CodeGroup>
      <CodeBlock>
        {`https://gist.github.com/amythee/68780fdfd0ce758fca807f25bfb29300#file-createvideo-ts`}
      </CodeBlock>
    </CodeGroup>

    If an error is encountered while creating the file, it will return the following errors:

    ```typescript
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
  <Tab title="Flutter">
    <CodeGroup>
      <CodeBlock>
        {`https://gist.github.com/amythee/6a1ea5fee0a85151699e40bedccc534c`}
      </CodeBlock>
    </CodeGroup>
  </Tab>
</Tabs>

## Retrieve Videos

#### Get a Specific Video Resolution

Once you upload a video the videos undergo transcoding from their original resolution. You can quickly access the original size of the video right after you make the video message. However, it takes time for the transcoded resolutions to be ready. Here are the available transcoded resolutions.

* 1080p
* 720p
* 480p
* 360p
* original

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      <CodeBlock>
        {`https://gist.github.com/amythee/76a284b9764d4c0d70a150fc0a30c1cc`}
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
      <CodeBlock>
        {`https://gist.github.com/a713152f2c45c58b4b3eb103705b088a`}
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="JavaScript">
    Supported ✅ (please wait while we prepare a real example!)
  </Tab>
  <Tab title="TypeScript">
    <CodeGroup>
      <CodeBlock>
        {`https://gist.github.com/amythee/0d1ade38440b9d08fc942b8af5c09079`}
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="Flutter">
    Here's an example of getting a specific video resolution from a post.

    <CodeGroup>
      <CodeBlock>
        {`https://gist.github.com/amythee/e1ba4f88bf33a3421c9863a354720c6a`}
      </CodeBlock>
    </CodeGroup>
  </Tab>
</Tabs>

#### Get a Video Thumbnail Image

Additionally, you can display a video preview in the user interface by utilizing a video thumbnail image. This allows for a more visually appealing representation of the video and provides a quick preview for users before they choose to view the full video. The thumbnail may not be immediately available after the video is uploaded. However, eventually, the thumbnail will become available.

<Tabs>
  <Tab title="iOS">
    ```javascript
    let fileRepository = AmityFileRepository(client: client)
        ...
        
        func downloadVideoThumbnailAsData(from message: AmityMessage) {
            guard let thumbnailFileId = message.data?["thumbnailFileId"] as? String,
                  !thumbnailFileId.isEmpty,
                  let imageInfo = message.getVideoThumbnailImageInfo() else { return }
            
            
            // Download from url and return saved image url.
            fileRepository.downloadImage(fromURL: imageInfo.fileURL, size: .small) { imageUrl, error in
                // Handle image url and error.
            }
        }
        
        func downloadVideoThumbnailAsUIImage(from message: AmityMessage) {
            guard let thumbnailFileId = message.data?["thumbnailFileId"] as? String,
                  !thumbnailFileId.isEmpty,
                  let imageInfo = message.getVideoThumbnailImageInfo() else { return }
            
            // Download from url and return image.
            fileRepository.downloadImageAsData(fromURL: imageInfo.fileURL, size: .small) { image, size, error in
                // Handle image and error.
            }
        }
    ```
  </Tab>
  <Tab title="Android">
    Supported ✅ (please wait while we prepare a real example!)
  </Tab>
  <Tab title="JavaScript">
    Supported ✅ (please wait while we prepare a real example!)
  </Tab>
  <Tab title="TypeScript">
    <CodeGroup>
      <CodeBlock>
        {`https://gist.github.com/amythee/dea45af62feca26e0c8f76b4874d560d`}
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="Flutter">
    The functionality isn't currently supported by this SDK.
  </Tab>
</Tabs>