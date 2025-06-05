# Custom Post

If you'd like to display content on your app that cannot be represented by the available text, image, video, and file post types, you can create your own custom post type. Custom post types allow you to include the necessary data for rendering, such as additional metadata and custom data formatting. This is useful if you want to present specific types of content to your users.

To create a custom post type, you can query the user, community, or global feed using our SDK's APIs. Please refer to [feed](../../feed/ "mention"). For additional information on rendering custom posts with UIKit, please see [post-rendering.md](../../../../social-plus-uikit/uikit-3/ios/community/overriding-behavior/feed-ui-settings/post-rendering.md "mention").

* `dataType` - A string that defines the type of the post so you can distinguish your new post from others
* `data` - A free-form JSON object that can be customized based on your use cases.

<Info>
The **`dataType`** parameter should have the **`custom`** prefix.
</Info>

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      ```swift
      https://gist.github.com/amythee/76b8b6f601f828ab5d8cab5c8aed4ee5
      ```
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
      ```kotlin
      https://gist.github.com/27c6007ae889eeb431de2e7a21b9bf8d
      ```
    </CodeGroup>
  </Tab>
  <Tab title="JavaScript">
    <CodeGroup>
      ```javascript
      https://gist.github.com/amythee/e4147f4ec42cf5c1cc5a073473be708d#file-custompost-js
      ```
    </CodeGroup>
  </Tab>
  <Tab title="TypeScript">
    <CodeGroup>
      ```typescript
      https://gist.github.com/amythee/266f11a57af3acf065ca1f3531b9d717#file-createcustompost-ts
      ```
    </CodeGroup>
  </Tab>
  <Tab title="Flutter">
    <CodeGroup>
      ```dart
      https://gist.github.com/amythee/39fa10767faec05a50a92123d0282686
      ```
    </CodeGroup>
  </Tab>
</Tabs>