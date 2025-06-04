---
description: Build and nurture vibrant communities where users can exchange and connect.
---

# Communities

<figure><img src="../../../.gitbook/assets/image (124).png" alt=""><figcaption></figcaption></figure>

Social Plus includes a powerful Community feature that allows users to share their thoughts and engage with each other within your app. By harnessing the power of communities, you can create a more dynamic and engaging user experience, promoting collaboration, communication, and participation among users.

The community provides users with a dedicated space to discuss specific topics or interests, enabling them to connect with like-minded individuals and build deeper relationships within the community. By providing a structured and organized approach to community engagement, the Community can help to foster a more engaged and supportive community, promoting greater participation and collaboration among users.

### Community Types

Our product provides two types of communities: public and private.

1. **Public** - A public community is visible to anyone without any specific permissions. This means that anyone can find and join the community, and all content posted within the community is visible to anyone who has access to the community.
2. **Private** - On the other hand, a private community is only visible to the creator and invited members. This type of community provides greater privacy and control over the content shared within the community. Only members who have been invited to join the community can see and interact with the content and other members of the community.

Our product is designed to provide users with flexibility and control over their communities, allowing them to choose the type of community that best fits their needs and preferences.

### Community Post Settings

Community Post Settings allows the community creator and community moderators to control who can create posts within a community and how those posts are moderated.&#x20;

There are three possible options for Community Post Settings :

* `anyoneCanPost`: This setting allows anyone to create a post within the community and add it to the community feed immediately. There is no moderation required for these posts.
* `adminReviewPostRequired`: This setting allows users to create posts within the community but adds another layer of moderation. Community moderators can review each post and decide whether or not it should be included in the community feed.
* `onlyAdminCanPost`: This setting restricts post creation to community moderators only. Regular users are not able to create posts within the community.

To check the community post settings, users can call the `postSettings` property, which returns a `CommunityPostSettings` object. This allows community administrators to easily manage and adjust their community settings to meet the needs of their community and ensure a positive user experience.

{% hint style="info" %}
By default, the _`postSettings`_ value is set to `anyoneCanPost`. In this case, member's posts will be displayed in the community feed without any review from the admin.
{% endhint %}

### Community Description

<table data-header-hidden><thead><tr><th width="222">Name</th><th>Data Type</th><th>Description</th></tr></thead><tbody><tr><td>Name</td><td>Data Type</td><td>Description</td></tr><tr><td><code>communityId</code></td><td><code>String</code></td><td>ID of the community</td></tr><tr><td><code>channelId</code></td><td><code>String</code></td><td>ID of the channel</td></tr><tr><td><code>userId</code></td><td><code>String</code></td><td>ID of the user who created the comment</td></tr><tr><td><code>displayName</code></td><td><code>String</code></td><td>Community name for displaying</td></tr><tr><td><code>avatar</code></td><td><code>Object</code></td><td>Avatar object</td></tr><tr><td><code>description</code></td><td><code>String</code></td><td>Description of the community</td></tr><tr><td><code>isOfficial</code></td><td><code>Boolean</code></td><td>Is this community official?</td></tr><tr><td><code>isPublic</code></td><td><code>Boolean</code></td><td>Is this community public?</td></tr><tr><td><code>onlyAdminCanPost</code></td><td><code>Boolean</code></td><td>only admins can post in this community</td></tr><tr><td><code>tags</code></td><td><code>List</code></td><td>List of tags used for searching</td></tr><tr><td><code>metadata</code></td><td><code>Object</code></td><td>Additional properties to support custom fields</td></tr><tr><td><code>postsCount</code></td><td><code>Integer</code></td><td>Number of posts in community</td></tr><tr><td><code>membersCount</code></td><td><code>Integer</code></td><td>Number of members in community</td></tr><tr><td><code>isJoined</code></td><td><code>Boolean</code></td><td>Is this community joined?</td></tr><tr><td><code>categoryIds</code></td><td><code>List</code></td><td>ID of categories</td></tr><tr><td><code>isDeleted</code></td><td><code>Boolean</code></td><td>Is this community deleted?</td></tr><tr><td><code>createdAt</code></td><td><code>DateTime</code></td><td>Date/time when the community was created</td></tr><tr><td><code>updatedAt</code></td><td><code>DateTime</code></td><td>Date/time when a community is updated or deleted</td></tr><tr><td><code>hasFlaggedPost</code></td><td><code>Boolean</code></td><td>Flag for checking internally if post inside community is reported or not</td></tr><tr><td><code>postSettings</code></td><td><code>Object</code></td><td>Community post settings within a community, how  posts are moderated</td></tr></tbody></table>
