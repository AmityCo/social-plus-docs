# Delete Comment

The SDK provides functionality for soft and hard deleting comments. Soft delete marks the comment as deleted while still keeping it in the system with the `isDeleted` flag set to true. On the other hand, hard delete completely removes the comment data, including its reactions and replies, from the system.&#x20;

The need for soft and hard delete functions arises when users want to manage the comments on their app. Soft delete is helpful in situations where the comment has been flagged and needs to be hidden from users without actually deleting the comment. Hard delete, on the other hand, is useful in cases where the comment content is inappropriate and must be permanently deleted from the app.

To hard delete a comment, you can use the AmityCommentRepository, which provides a deleteComment method. When using this method, you need to pass the `commentId` and a boolean `hardDelete` parameter. Set the boolean parameter to true for hard delete and false for soft delete. If you do not specify the boolean parameter, it will be set to false by default, equivalent to a soft delete. It's important to note that hard-deleting children's comments will not delete the parent's comments.

It's worth mentioning that hard deleting posts and comments is only supported via SDK, with UIKit and Console support potentially being added in the future. By implementing the soft and hard delete features provided by Social Plus SDK, you can give your app's users more control over the comments they interact with while maintaining a safe and appropriate community.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/20663654e04593672738ddb7caa6bbd4" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/0840fafb4b905a3aaef17568e572e2b4#file-amitycommentdelete-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
const comment = await CommentRepository.deleteComment('commentId', true);
```

If you will not specify the boolean parameter, it will be set to `false` by default which is just equivalent to a soft delete.

The `deleteComment` method returns a promise acknowledging the server's successful response. Use `await` to receive the result. It will return `true` if the deletion is successful. Otherwise, it will return `false`.

```javascript
{
    "success": true
}
```
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/7f1c4770ce7b3c672f495eb395e6cf06" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/d328b9fdadec1720b988528f3b215996#file-amitycommentdeletion-dart" %}
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Only the owner of the comment or an admin can update and/or delete a comment.
{% endhint %}
