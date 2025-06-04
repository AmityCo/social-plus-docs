# Delete Post

In Social Plus's social SDK, there are two types of post deletion: soft delete and hard delete. When a post is soft deleted, it is simply marked as deleted, with the `isDeleted` flag set to `true` in the database. The post still exists in the database but is no longer visible to users. By contrast, when a post is hard deleted, all associated data, including reactions, comments, child posts, and related data, is permanently removed from the database. This makes it impossible to retrieve the data once it has been hard deleted.

To perform a hard delete, developers can pass a boolean value of true to the delete post method in the PostRepository. For a soft delete, the boolean value should be false.  If no deletion type is specified, the default is soft deletion. By offering these two types of post deletion, Social Plus's social SDK provides developers with flexibility and control over managing their posts and associated data.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/d1d8b646627bba6af6f3c76e116b8b83" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/284f676a7d783f211bdd69980841561e#file-amitypostdelete-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/371f62fce0cd4b6325801d300c74514e#file-deletepost-js" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/caa31a0910a0e5f023e37ffcbcf7f8be#file-deletepost-ts" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/c41cec566872b8b4f636e4aa6673e0cd" %}
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Only the owner of the post or an admin can update and/or delete a post.

Hard deletion is only supported via the SDK at this time and is not yet available in the UIKit or Console. To delete a post in Social Plus's social SDK, developers can use the PostRepository and specify the post ID and the desired deletion type.

Please also note that the file in the post will not be automatically deleted when the post is deleted.
{% endhint %}
