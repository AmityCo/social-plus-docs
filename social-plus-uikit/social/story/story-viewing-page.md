# Story Viewing Page

The Story Viewing Page is a pivotal component of Social Plus UIKit 4.0, enabling users to immerse themselves in the stories shared within their communities. It provides a streamlined interface for navigating through and engaging with content, contributing significantly to the social experience within the app.

<div><figure><img src="../../../../.gitbook/assets/image (16).png" alt="" width="281"><figcaption></figcaption></figure> <figure><img src="../../../../.gitbook/assets/image (15).png" alt="" width="281"><figcaption></figcaption></figure></div>

### Features

| Feature    | Description                        |
| ---------- | ---------------------------------- |
| View story | User can view image or video story |

### Customization

<table><thead><tr><th width="312">Config ID</th><th width="102">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>story_page/*/*</code></td><td>Page</td><td>You can customize <code>theme</code> </td></tr><tr><td><code>story_page/*/progress_bar</code></td><td>Element</td><td>You can customize <code>progress_color</code> and <code>background_color</code></td></tr><tr><td><code>story_page/*/overflow_menu</code></td><td>Element</td><td>You can customize <code>overflow_menu_icon</code></td></tr><tr><td><code>story_page/*/close_button</code></td><td>Element</td><td>You can customize <code>close_icon</code></td></tr><tr><td><code>story_page/*/story_impression_button</code></td><td>Element</td><td>You can customize <code>impression_icon</code></td></tr><tr><td><code>story_page/*/story_comment_button</code></td><td>Element</td><td>You can customize <code>comment_icon</code> and <code>background_color</code></td></tr><tr><td><code>story_page/*/story_reaction_button</code></td><td>Element</td><td>You can customize <code>reaction_icon</code> and <code>background_color</code></td></tr><tr><td><code>story_page/*/create_new_story_button</code></td><td>Element</td><td>You can customize <code>create_new_story_icon</code> and <code>background_color</code></td></tr><tr><td><code>story_page/*/speaker_button</code></td><td>Element</td><td>You can customize <code>mute_icon</code> , <code>unmute_icon</code> and <code>background_color</code></td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../customization/) page.

### Usage

{% tabs %}
{% tab title="iOS" %}
In the integration process for the Story Viewing Page on iOS, an essential step involves creating a `StoryTarget`. This object is crucial for specifying which community's stories are to be viewed, including details like the community's ID, display name, verification status, and avatar URL. This setup ensures the stories presented are relevant and correctly attributed to the specific community context.

{% embed url="https://gist.github.com/amythee/917c447d665da778def8a68201dcf5cd" %}

This setup ensures that the Story Viewing Page is initialized with community-specific stories, allowing users to engage with content that is most relevant to them.
{% endtab %}

{% tab title="Android" %}
For Android, the process involves starting a new activity dedicated to story viewing, with the target community's ID as a key parameter:

{% embed url="https://gist.github.com/amythee/b56c789ce415afebce4347007ac62177" %}

This code snippet illustrates how to launch the Story Viewing Page for a particular community, ensuring that users are presented with stories from communities they are interested in or affiliated with.
{% endtab %}

{% tab title="Web (React)" %}
```
import React from 'react';
import { AmityViewStoryPage } from '@amityco/ui-kit-open-source';

const App = () => {
  return (
      <AmityViewStoryPage page="story_page" targetId="targetId"/>
  );
};

export default App;
```



| Prop Name  | Type     | Default Value  | Description                                                                                                                                       |
| ---------- | -------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pageId`   | `string` | `'story_page'` | Specifies the unique identifier for the view stories page. It helps in distinguishing between different pages or sections within the application. |
| `targetId` | `string` | -              | Represents the ID of the target whose stories are being viewed. It is used to fetch and display the relevant stories for that target.             |
{% endtab %}

{% tab title="React Native" %}
For react native, the Story Drafting Page is exported as an usual React Native component. You can import `AmityViewStoryPage` from  `amity-react-native-social-ui-kit`, wrap with UIKit Provider for Authentication and use anywhere you want. \
\
For story view page, UIKit support only for community now. It means\
targetId is communityId and targetType is 'community'.&#x20;

```typescript
import {
  AmityDraftStoryPage,
  AmityUiKitProvider
} from 'amity-react-native-social-ui-kit';

const onCreateStory = () => {...}
const onDiscardStory = () => {...}
 <AmityUiKitProvider
      apiKey="API_KEY"
      apiRegion="API_REGION"
      userId="userId"
      displayName="displayName"
      apiEndpoint="https://api.{API_REGION}.amity.co"
  >
       <AmityDraftStoryPage 
          targetId={communityId}
          targetType={"community" | "user" | "content"}
          mediaType={mediaType}
          onCreateStory={onCreateStory}
          onDiscardStory={onDiscardStory}
       />
 </AmityUiKitProvider>
```
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/7fcccb7791f56fa5e31ee4724a7226b4" %}
{% endtab %}
{% endtabs %}

### Navigation Behavior

Story Viewing Page will navigate to other pages based on user's actions, you can override the behavior to navigate to your own pages.

For more details, please refer to the [Overriding Navigation Behavior](https://docs.amity.co/amity-uikit/uikit-v4-beta/customization/overriding-navigation-behaviour) page.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/38751148ddf2f7b30f84ebed09413283" %}
{% endtab %}

{% tab title="Andoid" %}
{% embed url="https://gist.github.com/d61526187cd0dc51a02d9205bfd3a8fc" %}
{% endtab %}
{% endtabs %}
