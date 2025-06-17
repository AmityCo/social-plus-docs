---
description: This page provides draft preview for story creation.
---

# Story Drafting Page

The Story Draft Page component of Social Plus UIKit 4.0 is designed to offer users the ability to prepare and preview their story content before publishing. It supports both image and video media types, enhancing the storytelling process with a seamless draft and review experience.

<div><figure><img src="../../../../../.gitbook/assets/image (12).png" alt="" width="281"><figcaption></figcaption></figure> <figure><img src="../../../../../.gitbook/assets/image (6).png" alt="" width="281"><figcaption></figcaption></figure></div>

<div><figure><img src="../../../../../.gitbook/assets/image (156).png" alt=""><figcaption></figcaption></figure> <figure><img src="../../../../../.gitbook/assets/image (155).png" alt=""><figcaption></figcaption></figure></div>

### Features

| Feature    | Description                                                                       |
| ---------- | --------------------------------------------------------------------------------- |
| Draft view | User can view content of the story before sharing, add hyperlink or adjust image. |
| Hyperlink  | User can add link and customize link text to story.                               |

### Customization

<table><thead><tr><th width="265">Config ID</th><th width="124">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>create_story_page/*/*</code></td><td>Page</td><td>You can customize <code>theme</code> </td></tr><tr><td><code>create_story_page/*/back_button</code></td><td>Element</td><td>You can customize <code>back_icon</code> and <code>background_color</code></td></tr><tr><td><code>create_story_page/*/aspect_ratio_button</code></td><td>Element</td><td>You can customize <code>aspect_ratio_icon</code> and <code>background_color</code></td></tr><tr><td><code>create_story_page/*/story_hyperlink_button</code></td><td>Element</td><td>You can customize <code>hyperlink_button_icon</code> and <code>background_color</code></td></tr><tr><td><code>create_story_page/*/hyper_link</code></td><td>Element</td><td>You can customize <code>hyper_link_icon</code> and <code>background_color</code></td></tr><tr><td><code>create_story_page/*/share_story_button</code></td><td>Element</td><td>You can customize <code>share_icon</code> , <code>background_color</code> and <code>hide_avatar</code></td></tr><tr><td><code>*/hyper_link_config_component/*</code></td><td>Component</td><td>You can customize <code>theme</code></td></tr><tr><td><code>*/hyper_link_config_component/done_button</code></td><td>Element</td><td>You can customize <code>done_icon</code> ,<code>done_button_text</code> and <code>background_color</code></td></tr><tr><td><code>*/hyper_link_config_component/cancel_button</code></td><td>Element</td><td>You can customize <code>cancel_icon</code> and <code>cancel_button_text</code></td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../../customization/) page.

### Usage

{% tabs %}
{% tab title="iOS" %}
Integrating the Story Draft Page allows users to preview and potentially edit their story drafts before publication. This integration involves creating instances of the `AmityDraftStoryPage` for image or video media types, showcasing the versatility of the component in handling different content forms:

{% embed url="https://gist.github.com/amythee/afe4b067680b936dddc5e207f7e3b4bd" %}

These snippets illustrate how to instantiate the draft page for both image and video stories, integrating them into the SwiftUI view hierarchy. The distinction between media types (image vs. video) allows for tailored preview experiences, ensuring users can effectively review and adjust their stories as needed.
{% endtab %}

{% tab title="Android" %}
On Android, integrating the Story Draft Page into your application involves launching an activity tailored for either image or video story drafts. Here's an example of how to initiate this activity, which takes into account the media type (image or video) and the associated file URI:

{% embed url="https://gist.github.com/amythee/3f8cdf76d0ebf2bcb54f445924cba509" %}

This Kotlin function demonstrates initiating the Story Draft Page activity with essential parameters like the community ID, a boolean indicating if the draft is an image, and the URI of the file. This allows for a dynamic draft creation experience where users can prepare and preview their stories, whether they're sharing an image or a video.
{% endtab %}

{% tab title="Web (React)" %}
```
import React from 'react';
import { AmityCreateStoryPage } from '@amityco/ui-kit-open-source';

const DraftPage = () => {
return (
          <AmityCreateStoryPage 
          pageId="create_story_page"
          file={null}
          creatorAvatar=""
          onCreateStory={() => {}}
          onDiscardStory={() => {}}
          />
);

```



| Prop Name        | Type             | Description                                                                                                                                                                                     |
| ---------------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pageId`         | `string`         | Specifies the unique identifier for the create story page. It helps in distinguishing between different pages or sections within the application.                                               |
| `file`           | `File` or `null` | Represents the file (image or video) selected by the user for creating the story. If no file is selected, it should be set to `null`.                                                           |
| `creatorAvatar`  | `string`         | Specifies the URL or path to the avatar image of the user who is creating the story. It is used to display the user's avatar in the create story page.                                          |
| `onCreateStory`  | `function`       | A callback function that is invoked when the user submits the story creation form. It should be implemented to handle the story creation logic based on the selected file and other parameters. |
| `onDiscardStory` | `function`       | A callback function that is invoked when the user discards or cancels the story creation process. It should be implemented to handle the discard logic and any necessary cleanup.               |
{% endtab %}

{% tab title="React Native" %}
For react native, the Story Drafting Page is exported as an usual React Native component. You can import `AmityDraftStoryPage` from  `amity-react-native-social-ui-kit`, wrap with UIKit Provider for Authentication and use anywhere you want. \
\
For story draft page, UIKit support only for community now. It means\
targetId is communityId and targetType is 'community'. \
mediaType: PhotoFile or VideoFile type from react-native-vision-camera + {uri: string, name: string}\
onFinish:  will be called after story finished. \
onPressAvatar: will be called when user pressed avatar icon\
onPressCommunityName: will be called when user press community name

```typescript
import {
  AmityViewStoryPage,
  AmityUiKitProvider
} from 'amity-react-native-social-ui-kit';

const onFinish = () => {...}
const onPressAvatar = () => {...}
const onPressCommunityName = () => {...}
 <AmityUiKitProvider
      apiKey="API_KEY"
      apiRegion="API_REGION"
      userId="userId"
      displayName="displayName"
      apiEndpoint="https://api.{API_REGION}.amity.co"
  >
        <AmityViewStoryPage
          targetId={communityId}
          targetType="community"
          onFinish={onFinish}
          onPressAvatar={onPressAvatar}
          onPressCommunityName={onPressCommunityName}
        />
 </AmityUiKitProvider>
```
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/6f90e4cfca8b1171ce2d997b77677c70" %}
{% endtab %}
{% endtabs %}
