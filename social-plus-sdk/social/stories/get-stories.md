# Get Stories

## Get Story

The '`getStory()`' function enables users to retrieve a single by `storyId.` The function returns a **LiveObject** of the story allowing observation of real-time updates of the story's properties such as reactions and `isSeen` state. Note that to be able to receive changes made remotely it is mandatory to explicitly subscribe to Realtime events.

Here's an explanation of the function parameter:

* `storyId`: Corresponds to the ID of the story.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/7ae5f19d10962d525aa50b04a02cff9b" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/e6757e55ae27b6784b544e6a02ed8f22" %}
{% endtab %}
{% endtabs %}

## Get Active Stories

The '`getActiveStories()`' function within the Social Plus SDK enables users to query non-expired stories based on a specified target, providing a **LiveCollection** of stories for seamless playback and browsing. Notably, the Social Plus SDK supports optimistic story creation, including un-synced stories within the collection. In sorting, priority is accorded to un-synced stories followed by synced ones, with secondary sorting based on the `sortOption`. It is important to note that real-time exclusion of expired stories from LiveCollection is not supported.

This function requires two parameters: targetType, and targetId.

Here's an explanation of the function parameters:

* `targetType`: Represents the type of target, currently supporting 'community.'
* `targetId`: Corresponds to the ID of the designated target.
* `sortOption`: Specifies the secondary sorting order for stories within the collection as 'firstCreated' or 'LastCreated.' The default value is 'firstCreated,' organizing stories chronologically based on creation time.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/c60009e9b42d9548d7b4324e46326d41" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/079f50140dd77235842a4ca31c7c916b" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/125f974cf91a79430b33bdb0bb513288" %}
{% endtab %}
{% endtabs %}

## Get Stories by Targets

For optimal user experience, the application may opt to pre-download content for seamless story playback. The `getStoriesByTargets()`function enables the retrieval of stories from multiple story targets. This function takes an input as an array of `targets` and returns a **LiveCollection** of only 'SYNCED' stories.&#x20;

Here's an explanation of the function parameters:

* `targets`: Represents an array of pairs of `targetType` and `targetId`
* `sortOption`: Represents how the collection should be sorted.&#x20;

{% hint style="info" %}
The function can accept a maximum of 10 pairs of targets in the array.
{% endhint %}

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/fb8de4b837cb828a6d2a4f5c16eb8c08" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/cdfefc39e4d2e67ede3418129371fa81" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/125f974cf91a79430b33bdb0bb513288" %}
{% endtab %}
{% endtabs %}
