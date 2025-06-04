# Search Members

## Search Channel Members

The `searchMembers` function in the `AmityChannelParticipation` class is used to search for members in a channel when mentioning. It takes the following parameters:

The function returns a [#live-collection](../../core-concepts/live-objects-collections/#live-collection "mention") of `ChannelMember` objects. You can filter search results with more than one option, such as filtering by muted and banned users. The role filter takes the role enum as an argument.&#x20;

If no keyword is supplied, the list of users will be organized alphabetically by display name. When a keyword is provided, the list will be arranged based on search rank.

Here's an explanation of the function parameter:

`displayname|keyword` : A parameter accepting the string for searching

`memberships`: A parameter accepting an array of enum of membership status, enabling filtering members with matching one of the member statuses.

* `MEMBER` ->  Active members
* `MUTED` ->  Muted members
* `BANNED` ->  Banned members

`roles` : A parameter accepting an array of roles, enabling filtering members with matching roles

`includeDeleted` : A parameter accepting a boolean value.&#x20;

* `true` -> include a member whose user has been deleted &#x20;
* `false` -> exclude member whose user has been deleted



{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/a383044414f51aabdf7ccc3914c96295" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/8b6c5700af831618cc5cb54f177c002e" %}
{% endtab %}

{% tab title="JavaScript" %}
Supported ✅ (please wait while we prepare a real example!)
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/d42191da396cfa37ddb51586ccc03edb" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/c1476d8cc7e4a698c49460440b483151#file-amitychannelmembersearch-dart" %}
{% endtab %}
{% endtabs %}
