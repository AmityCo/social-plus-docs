# Mentions



<figure><img src="../../.gitbook/assets/image-removebg-preview (2).png" alt=""><figcaption></figcaption></figure>

Mentions allow users to tag other users in messages, comments, and posts. It's a powerful tool for fostering engagement and collaboration within your social application. With mentions, users can easily direct messages to specific individuals or groups and can alert them to new content or important updates. In the SDK, mentions can be implemented in a range of ways, depending on your application's needs and user experience.  Here are the models that support mentions creation and highlighting:

* [mention-in-post.md](../social/posts/mention-in-post.md "mention")
* [mention-in-comment.md](../social/comments/mention-in-comment.md "mention")
* [mention-in-messages.md](../chat/messaging/mention-in-messages.md "mention")

you have the flexibility to define your own mention data structure for representing mentions. This allows you to highlight the mentioned text in a way that best suits the needs of your application and users. The most important aspect of mentions is to notify users when they have been mentioned, regardless of the specific data structure used. This ensures that users can quickly and easily engage with the content that is most relevant to them.

## Mention Users

Upon creating a model above (a post, comment, or message) with a mention, you can include a JSON object in the metadata parameter. The metadata represents the mentioned object, which depends on the design of your data structure. However, Social Plus provides a default structure to help you create the mentioned metadata.&#x20;

To ensure prompt notification of the person mentioned, it's important to provide the list of user IDs for the mentioned user parameter. This will help ensure that the mentioned users are notified and able to engage with the content.

* `mentionUsers(userIds)` -  In order to mention users and notify specific users. This function supports all mentionable models.&#x20;
* `mentionChannel(channelId)` - In order to mention and notify the whole channel. This function supports only a message model.&#x20;
* `metadata` - a flexible JSON object that can accommodate any information regarding the mentioned users. Our default structure for representing mentions is also in the metadata property.

#### Default Mention Metadata Structure&#x20;

To represent mentions using our structure, you will need to utilize the AmityMention object. This object can be created during mentionable model creation, as well as during rendering. The model contains four properties:

* `type` - type of the mention - the possible types are user and channel, for posts and comments, only support mentioning the user but the message supports mentioning the channel additionally.
* `index` - start index of current mention
* `userId` - userId of the user being mentioned. If the type of the mention is channel, then `userId` is undefined.
* `length` - length of the mention

{% hint style="info" %}
The length property doesn’t include the “@“ mention sign. For example, “@all” mention’s length is 3.
{% endhint %}

#### Mention Users Example

Below is an example to create a comment with mentions by using our default mention metadata structure:

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/957b35145e49d9645b041c8ee53e53bc#file-create_comment_with_mention-swift" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/1c9f2f7a2bc7dd8ddc742c6ef8fbee35#file-amitycommentmentioncreation-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/04e63c4ad13ee0dfdf174c7157ac8d5d#file-createcomment-js" %}

{% embed url="https://gist.github.com/4dd325324015b0e8b2b7fc4338054616" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/4dd325324015b0e8b2b7fc4338054616" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/8ba20704ecf3a127497a54c4db57a3e7" %}
{% endtab %}
{% endtabs %}

{% hint style="info" %}
We do not allow banned users to be mentioned, as we take a firm stance against harmful or inappropriate content in social applications. However, admins may still be able to access the names of banned users through the search users function. Once a message is sent, however, banned users' information will be excluded from the payload. Banned users will also not be notified or receive any push notifications if they are mentioned, further ensuring that they do not engage with the content.
{% endhint %}

## Render Mentions

As we mentioned we provided the flexibility for you to define your own mention object data structure to represent mentions. You can use the default data structure provided by the SDK to render mentions in your application, which can be accessed through the helper class. This allows you to easily retrieve mentions and render them. The mentionable model contains properties related to the mentioned feature:

* `mentionUsers` - The AmityUser object array contains details about users mentioned in the current content.
* `metadata` - a flexible JSON object that can accommodate any information regarding the mentioned users. Our predefined structure for representing mentions is also in the metadata property.

Below is an example to render mentions in a comment by using our default mention data structure:

{% tabs %}
{% tab title="iOS" %}
The following example demonstrates how `AmityMentionMapper` and `AmityMention` works in a comment. The function `getAttributedString` uses `AmityMentionMapper` to extract `AmityMention` from metadata, and return the highlighted text.

{% embed url="https://gist.github.com/amythee/9df177f623c122e3abd3093dc49c1747#file-get_highlighted_text_from_comment-swift" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/9f6fdf1d39d0d6ce7b909e278490ed12#file-amitycommentmentionrender-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
There is no restrictions over how you'll handle the highlighting the mentions in your UI. At Amity, we pass this metadata property inside `CommentRepository.createTextcomment` and `CommentRepository.editTextComment` along with other parameters to conveniently highlight across the platforms.

{% embed url="https://gist.github.com/amythee/81593be29f9baa66b9667f3ea743ce40#file-createcomment-js" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/c71937825a384c18915e4ac9a02c2f37" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/f4e91a73045d2278554ba9e8daf27dfc" %}
{% endtab %}
{% endtabs %}

## Mention Notifications

When users are mentioned, they will receive push notifications. You can customize the push notification content such as the title and the body using the [notification setting API](https://api-docs.amity.co/#/Notification/post\_admin\_v1\_notification\_setting). Providing the notification title and body in the `titleTemplate` and `bodyTemplate` parameters respectively. Here is a sample model:&#x20;

```json
{
  "level": "network",
  "isPushNotifiable": true,
  "notifiableEvents": [
   {
      "name": "text-mention-message.created",
      "isPushNotifiable": true,
      "titleTemplate": "{{UserDisplayName}} mentioned you in {{ChannelName}}",
      "bodyTemplate": "{{Message}}"
    }
  ]
}
```
