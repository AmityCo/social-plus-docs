---
description: >-
  Here's an overview of stories and how you can get started with integrating
  them into your application
---

# Stories

<figure><img src="../../../.gitbook/assets/Screenshot 2566-12-21 at 20.12.55.png" alt=""><figcaption></figcaption></figure>

Stories, unlike traditional posts, excel in sharing time-sensitive updates like promotions or event highlights. With SP Stories, you're not just sharing content - you're crafting an experience. Imagine effortlessly sharing quick tips or behind-the-scenes glimpses. SP Stories is your platform to capture moments that matter, working in synergy alongside our existing posts and videos feature - further complementing your content strategy in driving user engagement.

Our SDK provides tools for creating, viewing, and interacting with diverse story content—images, videos, and links; as well as configurable story duration and expiry periods. Additionally, you can also collect valuable insights regarding story interactions for analytics and reporting purposes, such as views, reach (unique views), reactions, and Click-Through Rates (CTR). This data will also be made available on our Dashboard soon.

Stories can currently only be created in community feeds, by users with story creation permissions ("MANAGE_COMMUNITY_STORY"). By default, these permissions are automatically assigned to the following roles: moderator, community moderator, super-moderator, and global admin. If you have non-moderators whom you'd like to be able to contribute to the community's story feed, you can assign these permissions to your users. Read more [here](https://docs.amity.co/amity-sdk/core-concepts/user/user-permission#permissions).

Creating, viewing, and deleting stories is also [available](https://docs.amity.co/analytics-and-moderation/console/stories) on SP Console.

### Story Structure

<figure><img src="../../../.gitbook/assets/Screenshot 2566-12-21 at 20.22.57.png" alt=""><figcaption></figcaption></figure>

A Story is multi-layered. The primary content, "**Data**," depending on the dataType, can be either an IMAGE or a VIDEO. The secondary content, "**StoryItems**," complements the main content, serving as additional components. For instance, the first supported StoryItem is a Hyperlink, containing URL information and its alias. Overlaying the main content allows users to click and be redirected to the predefined destination.

### Story Repository

The functionality of stories can be utilized through the `StoryRepository`, which offers methods for interacting with a data source that stores stories. This includes methods for obtaining stories, creating a new story, and deleting a story.

<Tabs>
  <Tab title="iOS">
    <iframe src="https://gist.github.com/amythee/dabae8e942b652226adfffdd814911f2"></iframe>
  </Tab>
  <Tab title="Android">
    <iframe src="https://gist.github.com/4d966b687a17edc5192236b0f59f7fa8"></iframe>
  </Tab>
  <Tab title="Flutter">
    <iframe src="https://gist.github.com/amythee/a771269a678cfd77e67279ba9ecf3e57"></iframe>
  </Tab>
</Tabs>

### Story schema

| **Name** | **Data Type** | **Description** |
| -------- | ------------- | --------------- |
| storyId | String | ID of the story |
| targetType | Enum | Type of target. COMMUNITY |
| targetId | String | ID of the target |
| dataType | Enum | Type of the story. Either IMAGE or VIDEO. |
| data | Object | Data of the story based on dataType |
| metadata | Object | Metadata of the story |
| storyItems | Array<StoryItem> | StoryItems of the story |
| syncState | Enum | Sync state of the story. [FAILED \| SYNCING \| SYNCED] |
| isDeleted | Boolean | Flag indicates whether the story is deleted. |
| isSeen | Boolean | Flag indicates whether the story has been viewed by the user |
| myReactions | Array<String> | My reactions on the story |
| reactionsCount | Integer | Count of reactions on the story |
| commentsCount | Integer | Count of comments on the story |
| reactions | Map<String, Integer> | Map containing a key \| value of reaction \| reactionsCount. For ex., "like" \| 20 |
| reach | Integer | Count of reach of the story |
| impression | Integer | Count of impression of the story |
| creatorId | String | ID of the user who created the story |
| expiresAt | DateTime | Date/time the story expires |
| createdAt | DateTime | Date/time the story was created |

### StoryTarget schema

| **Name** | **Data Type** | **Description** |
| -------- | ------------- | --------------- |
| targetType | Enum | Type of target |
| targetId | String | ID of target |
| updatedAt | DateTime | Date/time the story target was updated |
| hasUnseen | Boolean | Flag indicates whether the StoryTarget possesses unseen stories. |

<Hint>
Public communities can have up to 100 active stories. Once the limit is reached, new stories cannot be created. However, when a story expires, users can create more.
</Hint>