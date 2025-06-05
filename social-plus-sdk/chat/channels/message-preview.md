# Message Preview

Messages preview is partial data of the message that offers a brief summary of incoming messages through channel and subchannel objects. It allows users to quickly assess partial message content without opening the entire message.

{% hint style="warning" %}
To enable this feature, please refer to the API and the sample cURL commands provided below:

**API:** [Enable message preview](https://api-docs.amity.co/#/Network%20Setting/put\_api\_v3\_network\_settings\_chat)

```json
curl --location --request PUT 'https://apix.sg.amity.co/api/v3/network-settings/chat' \
--header 'accept: application/json' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer xxx' \
--data '{
  "isAllowMentionedChannelEnabled": false,
  "messagePreviewSetting": {
    "enabled": true,
    "isIncludeDeleted": false
  },
  "isAllowAdminViewConversationMessage": true,
  "isAllowAdminManageConversationMessage": true
}'
```

_Note:_ Message Preview will be available only in channels and subchannels for new messages created after the feature is enabled.
{% endhint %}

### **Message Previews in Applications**

Message previews play a crucial role in enhancing user experience in messaging platforms. By offering a brief glimpse of incoming messages through channel and subchannel objects, users can assess the urgency, context, and relevance of messages without needing to open the entire conversation. This feature is particularly beneficial in various scenarios:

1. **Notifications**: When a user receives a push notification or a message alert, a message preview can be shown, allowing the user to decide whether to engage immediately or defer it to a later time.
2. **Chat List**: In a list of ongoing conversations, each chat item can display the latest message as a preview. This helps users quickly identify and prioritize which chat to respond to first.
3. **Data Economy**: In scenarios where users have limited bandwidth or are on metered connections, previews allow them to decide if they want to download or load the complete message or any associated media.

Integrating message previews into applications can significantly boost user engagement and satisfaction. By offering users an efficient way to manage their interactions, apps can optimize response times and streamline communication workflows.

### Message Preview attributes

<table><thead><tr><th>Name</th><th>Data Type</th><th width="213">Description</th><th>Attributes</th></tr></thead><tbody><tr><td>messageId</td><td>string</td><td>The id of this message</td><td>Content</td></tr><tr><td>channelId</td><td>string</td><td>The name of the channel this message was created in</td><td>Content</td></tr><tr><td>userId</td><td>string</td><td>The name of the user this message was created by</td><td>Content</td></tr><tr><td>type</td><td>string</td><td>The message type</td><td>enum*: text custom image file</td></tr><tr><td>data</td><td>Object</td><td>The message data (any text will be stored in text key)</td><td>text: Text message</td></tr><tr><td>isDeleted</td><td>boolean</td><td>The message has been marked as deleted</td><td>Content</td></tr><tr><td>createdAt</td><td>date</td><td>The date/time the message was created at</td><td>Content</td></tr><tr><td>updatedAt</td><td>date</td><td>The date/time the message was updated at</td><td>Content</td></tr></tbody></table>

### Channel message preview

Within our SDK, clients can effortlessly obtain message previews using a channel object attribute.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/7d1988d5ffd5bb8a7e76579e8dc60292" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/52ae304641f49e6c665d1124828116b9" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/7c01a28be980c405be01fa1fb071cda3" %}
{% endtab %}
{% endtabs %}

### Subchannel message preview

Our SDK offers clients a straightforward approach to access message previews for subchannels through dedicated subchannel object attributes.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/2a613aad8acab92134299a2e118d4edb" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/9e53ff015777f026d20bf264a7963fa9" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/b3e35552dfc7b5e098dfacec72d0a4d4" %}
{% endtab %}
{% endtabs %}