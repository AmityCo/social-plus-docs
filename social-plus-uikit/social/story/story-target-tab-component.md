# Story Target Tab Component

The Story Target Tab Component is a dynamic feature of the Social Plus UIKit 4.0 that enhances the application page by allowing members to share and engage with stories. This new version introduces a suite of customization options and interactive capabilities designed to improve user experience and foster community interaction.

<div><figure><img src="../../../../.gitbook/assets/image (2) (1) (1) (1).png" alt=""><figcaption><p>Story Target (Community Level)</p></figcaption></figure> <figure><img src="../../../../.gitbook/assets/image (3) (1) (1) (1).png" alt=""><figcaption><p>Story Target (Community Level)</p></figcaption></figure></div>

<figure><img src="../../../../.gitbook/assets/image (157).png" alt=""><figcaption><p>Story Targets (Global Level)</p></figcaption></figure>

### Features

| Story Target (Community Level) | User can click to see a list of stories from a community or can create a story to a community.                                |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| Story Targets (Global Level)   | A list of story targets will show in newsfeed. User can click one of the targets to see the stories posted in that community. |

### Customization

Explore the variety of customization options available for the Story Tab Component to align with your app's design and user expectations.

<table><thead><tr><th width="213">Config ID</th><th width="122">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>*/story_tab_component/*</code></td><td>Component</td><td>You can customize <code>theme</code> </td></tr><tr><td><code>*/story_tab_component/story_ring</code></td><td>Element</td><td>You can specify list of colors to <code>progress_color</code> and <code>background_color</code> for ring color</td></tr><tr><td><code>*/story_tab_component/create_new_story_button</code></td><td>Element</td><td>You can specify <code>create_new_story_icon</code> and <code>background_color</code> </td></tr></tbody></table>

For more details on customization, please refer to the [Customization](../../customization/) page.

### Usage

Integrating the Story Target Tab Component into your iOS or Android app enhances the community profile page by allowing users to engage with stories directly related to a specific community. This section provides a detailed usage description and explanation for both iOS and Android platforms.

{% tabs %}
{% tab title="iOS" %}
To integrate the Story Target Tab Component in an iOS application, you utilize the `AmityStoryTabComponent` initializer with a specified `storyFeedType`. For a community-specific story feed, you pass the `.community(community)` as the parameter, where `community` is an instance of your AmityCommunity object.

{% embed url="https://gist.github.com/amythee/18ba8cab83c28ad0bd4f2e4f208bb1b0" %}

This snippet creates a `storyTabComponent` configured for a specific community. It then wraps this component in a `SwiftUIHostingController` to integrate it seamlessly into your SwiftUI application structure. This approach ensures that the story tab is dedicated to displaying stories from the specified community, enhancing content relevance and user engagement within that community space.
{% endtab %}

{% tab title="Android" %}
For Android, the Story Target Tab Component is available as a Composable function, making it easy to integrate within Jetpack Compose-based UI. Here's how you can use it:

{% embed url="https://gist.github.com/amythee/3f23dc1b5018132d1b891ac1f9f067fb" %}

This function demonstrates how to display the Story Target Tab Component for a specific community by utilizing the `AmityStoryCommunityTargetTabComponent` composable. You need to provide the `communityId`, which is obtained from the `AmityCommunity` object or other sources, ensuring that the stories displayed are related to this community.
{% endtab %}

{% tab title="Web (React)" %}
```
import React from 'react';
import { AmityStoryTabComponent } from '@amityco/ui-kit';

const CommunityStoriesTab = ({ communityId }) => {
  return (
    <AmityStoryTabComponent 
          pageId='*',
          title='Story',
          haveStoryPermission={false},
          storyRing={false},
          isSeen={false},
          uploadingStory={false},
          isErrored={false},
          avatar="",
          onClick={() => {}},
          onChange{() => {}},
     />
  );
};

export default CommunityStoriesTab;
```

In this example, we define a functional component called `CommunityStoriesTab` that takes a `communityId` prop. Inside the component, we render the `AmityStoryTabComponent` and pass the `communityId` as the value for the `communityFeed` property within the `type` prop.
{% endtab %}

{% tab title="React Native" %}
For react native, the Story Target Tab Component is exported as an usual React Native component. You can import `AmityStoryTabComponent` from  `amity-react-native-social-ui-kit`, wrap with UIKit Provider for Authentication and use anywhere you want. \
\
AmityStoryTabComponentEnum can be globalFeed or communityFeed. communityFeed require targetId as communityId&#x20;

```typescriptreact
import {
  AmityStoryTabComponent,
  AmityUiKitProvider,
  AmityStoryTabComponentEnum
} from 'amity-react-native-social-ui-kit';

 <AmityUiKitProvider
      apiKey="API_KEY"
      apiRegion="API_REGION"
      userId="userId"
      displayName="displayName"
      apiEndpoint="https://api.{API_REGION}.amity.co"
  >
       <AmityStoryTabComponent 
          type={AmityStoryTabComponentEnum.communityFeed}
          targetId={communityId}
       />
 </AmityUiKitProvider>
```
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/b5a5ea5a79dc5ea1278af7ce60eec968" %}
{% endtab %}
{% endtabs %}

### Navigation Behavior

Story Target Tab Component will navigate to other pages based on the user's actions, you can override the behavior to navigate to your own pages.

For more details, please refer to the [Overriding Navigation Behavior](https://docs.amity.co/amity-uikit/uikit-v4-beta/customization/overriding-navigation-behaviour) page.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/46c75dcb8145883e636e2a8c448d5a29" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/799eb459979731e772dcce17e4a31559" %}
{% endtab %}
{% endtabs %}
