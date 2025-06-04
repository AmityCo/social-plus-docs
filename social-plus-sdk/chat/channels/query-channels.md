# Query Channels

## Query Channels

The `getChannels` function is a powerful function that allows you to search for and retrieve channels that match specific criteria. With this function, you can quickly and easily find the channels you need.

The function accepts several parameters that allow you to customize your search. The `displayName` parameter is a string that specifies the search query, allowing you to search for channels based on their public display name.&#x20;

Once you have made your query, the function returns a [#live-collection](../../core-concepts/live-objects-collections/#live-collection "mention") of channels that match your query criteria. You can use this collection to display the search results in your app or to further filter the results as needed.

**You can query channels with the following criteria:**

* `displayName`: The public display name of the channel.
* `includeDeleted` : Specify whether to search for channels that have been closed. Possible values are:
  * `null` (default) - Show both channels are active and closed.
  * `false` - Search for channels that are still open
* `tags` : Search for channels with specific tags. If more than 1 tags are specified in the query, the system will search for channels that contain any of those tags.
* `excludeTags` : Search for channels without the specific tags. If more than 1 tags are specified in the query, the system will search for channels that do not contain any one of those tags.
* `filter` : Membership status of the user. Possible values are:
  * `all` (default) - Search for channels&#x20;
  * `member` - Search for channels that the user is a member of
  * `notMember` - Search for channels that the user is not a member of
  * `flagged` - Search for channels that the user flagged
* `types` : type of channel to search for - `conversation` , `broadcast` , `live` or `community`
* &#x20;`userId` : Search for channels that are created by a given User ID (only if you're an admin).

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/ca6c57abdcee0e981b23c94f0b337eca#file-query_channels-swift" %}

{% hint style="info" %}
If you use a `UITableView` or `UICollectionView` to display channel list data, the ideal location to reload table data is directly in the observed block of the live collection that you are displaying.
{% endhint %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/d4c591a99293da23de05cdabe6fdc68f" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
import { 
  ChannelRepository, 
  ChannelType, 
  ChannelFilter, 
  ChannelSortingMethod,
} from '@amityco/js-sdk';

let channels;

const liveCollection = ChannelRepository.queryChannels({
  keyword: 'asd',
  types: [ChannelType.Conversation],
  filter: ChannelFilter.Member,
  isDeleted: false,
  tags: ['tag1'],
  excludeTags: ['tag2'],
  sortBy: ChannelSortingMethod.LastCreated
});

liveCollection.on('dataUpdated', models => {
  channels = models;
});

channels = liveCollection.models;
```
{% endtab %}

{% tab title="TypeScript" %}
Version 6&#x20;

{% embed url="https://gist.github.com/068f8002170002b1d581b058b92dc5a1" fullWidth="false" %}

Beta(v0.0.1)

{% embed url="https://gist.github.com/trustratch/983679c9534c8c9607820714af6a8463" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/009393e93159effa667638bcb48d2884" fullWidth="true" %}
{% endtab %}
{% endtabs %}
