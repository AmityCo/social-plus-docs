# Accept/Decline Follow Request

The SDK product provides two important methods for managing follow requests between users: accept follow request and decline follow request. These methods enable users to accept or decline requests to follow other users within the app, promoting a more personalized and engaging user experience.

## Accept Follow Request

To accept a follow request from another user, users can call the `acceptMyFollower` method within the SDK and provide the `userId` of the user whose follow request they wish to accept. This will add the user to the list of followers and allow them to receive updates within Global feed and User feed.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/7c5e2ca46a570e31f86f293d243c5f34" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/a2bd0ca55b62f84d5feaa001714786fc#file-amityfollowaccept-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/c21376461534a36eda0267eea58a04ad#file-followuser-js" %}
{% endtab %}

{% tab title="TypeScript" %}
Version 6

{% embed url="https://gist.github.com/amythee/564d621321107d18126216ff4498cfb9#file-acceptfollower-ts" %}

Beta (v0.0.1)

{% embed url="https://gist.github.com/559418deb8a509031c954566fced3c42" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/10aebb7c52424e41f2482976306c2a83#file-amityfollowaccept-dart" %}
{% endtab %}
{% endtabs %}

## Decline Follow Request

Similarly, to decline a follow request from another user, users can call the `declineMyFollower` method within the SDK and provide the `userId` of the user whose follow request they wish to decline. This will remove the user's request to follow and prevent them from receiving updates within Global feed and User feed.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/388c2d1affd3891a0081ce0defeb0f1f" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/099bcbc066e484611d2853c331125c2c#file-amityfollowdecline-kt" %}
{% endtab %}

{% tab title="JavaScript" %}
{% embed url="https://gist.github.com/amythee/fd2073587293a90870e9b9bc0a552626#file-followuser-js" %}
{% endtab %}

{% tab title="TypeScript" %}
Version 6

{% embed url="https://gist.github.com/amythee/e1e4e1e854bc67427495a3c4b144d93a#file-declinefollower-ts" %}

Beta (v0.0.1)

{% embed url="https://gist.github.com/f2e16afd23fcac50e84149160164f0fe" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/fafc417086c3d98adebae550d48e7aed#file-amityfollowdecline-dart" %}
{% endtab %}
{% endtabs %}

{% hint style="info" %}
If the Follower request is no longer available (either the follower request sender has withdrawn the request or the request has been accepted or declined before), SDK will return the error message.
{% endhint %}
