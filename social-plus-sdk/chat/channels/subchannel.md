# Subchannel

Subchannels are part of a channel. They are separate topics or chat threads inside a channel. Messages can be sent and received in subchannels. By default, a channel generates a main subchannel once it's created. You can create, update, delete, and query subchannels inside a channel. For the structure and relationship of channels and subchannels, please visit.

{% hint style="info" %}
Limitations:

* Sub-channel creation is supported for `Conversation` and `Community` channel types.
* Users can create up to 300 sub-channels per channel.
{% endhint %}

### **Create Subchannel**

In the concept of channels and subchannels, a channel is a primary container that can hold multiple subchannels. Creating a subchannel will serve as a thread where users can send messages and participate in discussions related to a specific thread. The subchannel creation function requires two parameters: `channelId` and `displayName`.

* `channelId`: specifies the unique identifier of the parent channel where the subchannel will be created. This allows the SDK to link the subchannel to the correct parent channel, and organize it within the proper hierarchy.
* `displayName`: Specifies the public name or label of the subchannel that will be visible to users.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/5e295542faf2d97e5313d385427e04e3" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/479c96883ecd327204f542bc17f4bbc7" %}
{% endtab %}

{% tab title="JavaScript" %}
We don't support this feature in JS SDK.
{% endtab %}

{% tab title="TypeScript" %}
Version 6

{% embed url="https://gist.github.com/amythee/753487dd9103bef916c746e8d0afa9f9#file-createsubchannel-ts" %}

Beta (v0.0.1)

{% embed url="https://gist.github.com/811dcedbdd8a6794a03c18ea92e3e60c" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/38bae0e3d64be4ffc191574ac4b9ce16" %}
{% endtab %}
{% endtabs %}

### **Update Subchannel**

When you update a subchannel's properties, the changes will be reflected for all users who are members of that subchannel. Please note that the `updateSubChannel` function only updates the properties of the subchannel itself, and does not affect any messages or other content that has been sent within the subchannel.

The function requires two parameters: `subchannelId` and `displayName`.

* `subhannelId`: This is the unique identifier of the subchannel that you'd like to update.
* `displayName`: This is the updated public name or label of the subchannel that will be visible to users.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/2633f916083b1d3e88dd1abfc5108722" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/b16585280ad24b4d12cf01fdfe13d8f1" %}
{% endtab %}

{% tab title="JavaScript" %}
We don't support this feature in JS SDK.
{% endtab %}

{% tab title="TypeScript" %}
Version 6

{% embed url="https://gist.github.com/amythee/3d28acf08ecd7e25698a4d9a0dc8fa14#file-updatesubchannel-ts" %}

Beta (v0.0.1)

{% embed url="https://gist.github.com/fc105757d06524126646d5619d6ad006" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/74fe4f76d2223ee4df64a77953cb0290" %}
{% endtab %}
{% endtabs %}

### **Delete Subchannel**

The `subchannelId` parameter specifies the ID of the subchannel that you'd like to delete. The `hardDelete` parameter is a boolean value that determines whether to perform a hard delete or a soft delete.

A soft delete will mark the subchannel as deleted but keep its data in the system. A hard delete will immediately and permanently delete the subchannel and all its data from the system.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/c9692fef1bdd31bdae57200f81270d8d" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/6d43dea2ba1790c47e7d56a6e0396928" %}
{% endtab %}

{% tab title="JavaScript" %}
We don't support this feature in JS SDK.
{% endtab %}

{% tab title="TypeScript" %}
Version 6

{% embed url="https://gist.github.com/amythee/fa9709c686bb2f9940c98ca2f1b23c14#file-deletesubchannel-ts" %}

Beta (v0.0.1)

{% embed url="https://gist.github.com/083590e91d6ad604582a038200e691a4" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/719b77134cce1af2b8f2fd8702cf7c90" %}
{% endtab %}
{% endtabs %}

### **Get Subchannel**

To get a subchannel, you can use the `getSubchannel` method provided by the `SubchannelRepository`. This method accepts a `subchannelId` parameter and returns a [#live-object](../../core-concepts/live-objects-collections/#live-object "mention") of the `AmitySubchannel` class.

The `AmitySubchannel` class represents a subchannel in a channel. It contains information about the subchannel, such as its ID, display name, avatar, creation time, and more.

By using a [#live-object](../../core-concepts/live-objects-collections/#live-object "mention") combines with [#real-time-events](subchannel.md#real-time-events "mention"), you can observe any changes made to the subchannel in real-time. This is particularly useful in cases where multiple users may be interacting with the same subchannel and you need to keep the UI up-to-date with the latest data.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/3249734aae5b61fdef8c913eb6c303fb#file-get_sub_channel-swift" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/acfe376bc61b1599b70887a948961386" %}
{% endtab %}

{% tab title="JavaScript" %}
We don't support this feature in JS SDK.
{% endtab %}

{% tab title="TypeScript" %}
Version 6 and Beta(v0.0.1)

{% embed url="https://gist.github.com/amythee/13ecf642c77f17172b939a7d4c821ccf#file-getsubchannel-ts" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/6690ef5eac7d0c4babe8a617c0329bca" %}
{% endtab %}
{% endtabs %}

### **Query Subchannels**

The `getSubChannels` function allows you to retrieve a list of subchannels within a specific channel. It accepts the `channelId` parameter to specify which channel to retrieve subchannels from.

The function returns a [#live-collection](../../core-concepts/live-objects-collections/#live-collection "mention"), which allows you to observe changes to the collection in real-time.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/5e21f19971285b774b4cc5be55d90bb6#file-query_sub_channel-swift" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/3f4781bc4633741b2bcf6e42b5fe8b69" %}
{% endtab %}

{% tab title="JavaScript" %}
We don't support this feature in JS SDK.
{% endtab %}

{% tab title="TypeScript" %}
Version 6 and Beta(v0.0.1)

{% embed url="https://gist.github.com/amythee/d403c59daa269eb4f25e40d80c59a448#file-querysubchannels-ts" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/19e610ef431c7634341eb945cf52aa76" %}
{% endtab %}
{% endtabs %}
