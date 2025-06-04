# Update Channel

## Update a Channel

The `updateChannel` function allows users to modify the properties of a channel. This function is useful in cases where a channel's details need to be updated, such as changing the channel's display name or avatar.

The function takes a `channelId` parameter as a required input, which specifies the channel to be modified. Additionally, users can pass in any number of optional parameters to update the channel's properties. These optional parameters include:

* `displayName`: The new display name for the channel.
* `avatarFileId`: A new avatar image for the channel - Used to store ID of image file that represents avatar of the channel. To obtain file ID to set as channel avatar please see [#upload-images](../../core-concepts/files-images-and-videos/image-handling.md#upload-images "mention") section
* `tags`: Arbitrary strings that can be used for define and query for the channels
* `metadata`: Additional metadata to be associated with the channel.

{% hint style="info" %}
`metadata` is implemented with _last writer wins_ semantics: multiple mutations by independent users to the metadata object will result in a single stored value. No locking, merging, or other coordination is performed across multiple writes on the data.
{% endhint %}

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/20d6ab0687edf6f8afa330524232e356" %}

{% embed url="https://gist.github.com/amythee/49b31e95208fb8462eb67ae4e8c3f954" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/046fe6b4c0ec308e77e905c6926bb233" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
await ChannelRepository.updateChannel({ 
    channelId: 'channelId', 
    displayName: channelName,
    avatarFileId: fileId,
    tags: ['tag1', 'tag2'],
    metadata: { hello: 'world' }
 })
```
{% endtab %}

{% tab title="TypeScript" %}
Version 6

{% embed url="https://gist.github.com/amythee/171b6247f3a739513afba5b6df52e046#file-updatechanneldisplayname-ts" %}
Updating Display Name and Tags
{% endembed %}

Beta (v0.0.1)

{% embed url="https://gist.github.com/75505a787713d152a5714c8b6bbb6382" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/5a98844e706d6af9f0147dd0a635bba4#file-amitychannelupdate-dart" %}
{% endtab %}
{% endtabs %}
