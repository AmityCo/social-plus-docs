# Flag/Unflag

## Flag

The Social Plus SDK product also includes a flag method that allows users to flag comments in their app. Once a comment is flagged, an indicator will appear in the Admin console, where an administrator can review and validate the flag. If the content is found to be in violation of your app's policies, it can be deleted from the app. On the other hand, if the content is not found to be in violation, the flag can be revoked.

This method allows users to notify the community moderators or admins about comments that they believe violate the community guidelines or are otherwise inappropriate. By flagging a post with reason that we provided, users can help ensure that the community remains a safe and welcoming place for all members.

| AmityContentFlagReason       | Description                            |
| ---------------------------- | -------------------------------------- |
| CommunityGuidelines          | Against community guidelines           |
| HarassmentOrBullying         | Harassment or bullying                 |
| SelfHarmOrSuicide            | Self-harm or suicide                   |
| ViolenceOrThreateningContent | Violence or threatening content        |
| SellingRestrictedItems       | Selling and promoting restricted items |
| SexualContentOrNudity        | Sexual message or nudity               |
| SpamOrScams                  | Spam or scams                          |
| FalseInformation             | False information or misinformation    |
| Others                       |  Optional explanation (Max. 300 chars) |

{% hint style="info" %}
Flag reason is only available in iOS, Android, and TypeScript
{% endhint %}

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/1adef7b1065c7cc07a5317dfc10dbd43" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/a0412ea9d47dd8d03ec74959770d6b5e#file-amitycommentflag-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/3b9537c6175d505d45d2e8f74b2fc5ab#file-flagcomment-js" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/75e440748d10bf9bae51af30bdee35d4" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/4f0ad182dd563356e707e05f3e60fb93" %}
{% endtab %}
{% endtabs %}

## Unflag

Another useful feature is the unflag method, which enables users to revoke a previously flagged comment. If a user flags a comment by mistake or if the comment is found not to violate your app's policies after review, the unflag method can be used to remove the flag from the comment. It ensures that users have control over the content they flag and the ability to reverse their flag if necessary.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/9b201be534a6aab96e61a2207bce32a6" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/a0412ea9d47dd8d03ec74959770d6b5e#file-amitycommentflag-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/40dd77c46ecc0a6a5447f0ebc937f499#file-unflagcomment-js" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/b884a7dbc2f8702ce12f4156e7f5ba1d" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/153e5d152eac89f1050a9c1e32481b8b" %}
{% endtab %}
{% endtabs %}

## Check for isFlaggedByMe

The `isFlaggedByMe` method allows users to check whether they have previously flagged a particular comment. This method provides a convenient way for users to keep track of the content they have flagged and to ensure that they are staying up-to-date with their moderation activities.

By using the isFlaggedByMe method, your app's users can quickly determine whether they have already flagged a particular comment and avoid duplicating their efforts.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/635c37363b387643973568107b70e678" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/a0412ea9d47dd8d03ec74959770d6b5e#file-amitycommentflag-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/15b4125842747c86b6ab70e821354cf8#file-checkflagged-js" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/062dd66b5d9fbcae0aec3ac5e90e4f76" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/f192a0901b323ba0fec688f865e429c7" %}
{% endtab %}
{% endtabs %}
