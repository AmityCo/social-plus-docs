# Poll Post

Prior to creating a poll post, it is crucial to create the poll that will be included in the post data to ensure that the necessary information is accessible and can be linked to the post. This requires creating the poll first, to obtain the data that will be used in creating the poll post. For more information about polls including vote, close, or delete a poll, please refer to the page - [poll.md](../../../core-concepts/poll.md "mention").

* `text`: This is a required parameter of type `String`, which represents the text content of the new post. You can pass in any text you want to include in the post, up to a maximum length of 20,000 characters.
* `pollId`: The ID of the created poll to include in a post.
* `targetType` - Type of the target, either a particular community or a user feed.
* `tags` - Arbitrary strings that can be used for defining and querying for the posts (Except Flutter).
* `metaData` - Additional properties to support custom fields.

&#x20;As demonstrated in the code sample below, here's a way to create a poll and poll post.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/78313a66ea1f4da62a05e9f501d7f975" %}

{% embed url="https://gist.github.com/amythee/98b329998185f1b9fdf809815155a7de" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/589b716862b43e8dc55822ab0cac33b2#file-amitypostpollupload-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/408686f116cda4ba97ba7cf155db82d6#file-createpoll-js" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/57910fde04cc2edc0dcc37c670774398" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/7ad2ce65b2a60bf8117ba323093087d7#file-amitypollcreate-dart" %}
{% endtab %}
{% endtabs %}
