---
description: This page provides media picking and camera for story creation.
---

# Story Creation Page

The Camera Page component of Social Plus UIKit 4.0 offers an immersive, easy-to-integrate solution for adding camera functionality to your app. It enables users to capture and share moments directly within stories, enhancing the storytelling experience within communities.

### Photos

<div align="center" data-full-width="true"><figure><img src="../../../../../.gitbook/assets/CreateStory Page.jpg" alt="Camera page" width="188"><figcaption><p>Capturing a photo with camera</p></figcaption></figure> <figure><img src="../../../../../.gitbook/assets/Photo Permission Dialog.jpg" alt="" width="188"><figcaption><p>Selecting an image from gallery</p></figcaption></figure></div>

### &#x20;Videos

###

<div align="center" data-full-width="true"><figure><img src="https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-MX0mOAVWkotGme0iRzu%2Fuploads%2Fz01LQbIAQALLd5qgNofE%2FCreateStory%20Page%20(1).png?alt=media&#x26;token=fa33d310-a21f-4fbe-a69c-8fac5f76fe0a" alt="Camera page" width="188"><figcaption><p>Recording a video with camera</p></figcaption></figure> <figure><img src="../../../../../.gitbook/assets/Photo Permission Dialog.jpg" alt="" width="188"><figcaption><p>Selecting a video from gallery</p></figcaption></figure></div>

### Features

| Feature      | Description                                            |
| ------------ | ------------------------------------------------------ |
| Camera view  | User can capture image or record video to create story |
| Media picker | User can select media image or video to create story   |

### Customization

<table><thead><tr><th width="213">Config ID</th><th width="102">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>camera_page/*/*</code></td><td>Page</td><td>You can customize <code>theme</code> </td></tr><tr><td><code>camera_page/*/close_button</code></td><td>Element</td><td>You can customize <code>close_icon</code> and <code>background_color</code></td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../../customization/) page.

### Usage

{% tabs %}
{% tab title="iOS" %}
For integrating the Story Creation Page into an iOS app, use the `AmityCreateStoryPage` component. Here's a simple example of navigating to the story creation page, specifying a community ID and optionally an avatar image URL.

{% embed url="https://gist.github.com/amythee/9b39c8885f10e3dfa947deed45b5e703" %}

This code snippet demonstrates how to initialize the story creation component with a specific target community ID and user avatar, and then embed it within a SwiftUI hosting controller for presentation.
{% endtab %}

{% tab title="Android" %}
Integrating the Story Creation Page in an Android application involves starting a new activity. Below is a method example that launches the story creation activity, utilizing the community ID to tailor the experience.

{% embed url="https://gist.github.com/amythee/2d6efdfe8d061bed6d2ae6bd2491671f" %}

This function shows how to initiate the story creation page activity with the community ID as the target for the story, ensuring the content is relevant to the specified community.
{% endtab %}

{% tab title="React Native" %}
For react native, the Story Create Story Page is exported as an usual React Native component. You can import `AmityCreateStoryPage` from  `amity-react-native-social-ui-kit`, wrap with UIKit Provider for Authentication and use anywhere you want. \
\
For story creation, UIKit support only for community now. It means\
targetId is communityId and targetType is 'community'. \
\
onCreateStory: will be called after creation finished. \


```typescript
import {
  AmityCreateStoryPage,
  AmityUiKitProvider
} from 'amity-react-native-social-ui-kit';

const onCreateStory = () => {...}

 <AmityUiKitProvider
      apiKey="API_KEY"
      apiRegion="API_REGION"
      userId="userId"
      displayName="displayName"
      apiEndpoint="https://api.{API_REGION}.amity.co"
  >
       <AmityCreateStoryPage 
          targetId={communityId}
          targetType={"community" | "user" | "content"}
          onCreateStory={onCreateStory}
       />
 </AmityUiKitProvider>
```
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/359cb90a2477ceb1e65fdaea0dda0959" %}
{% endtab %}
{% endtabs %}

### Navigation Behavior

Story Creation Page will navigate to other pages based on user's actions, you can override the behavior to navigate to your own pages.

For more details, please refer to the [Overriding Navigation Behavior](https://docs.amity.co/amity-uikit/uikit-v4-beta/customization/overriding-navigation-behaviour) page.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/0e24f24e04c5cd9e2d4c3d28489e6d8e" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/ed4841ad88c230abd860cdd7fab01952" %}
{% endtab %}
{% endtabs %}
