# Query Community Members

### Retrieve a list of community members

To retrieve a list of community members, users can call the relevant method and provide the desired membership options and sorting parameters. For example, they may choose to sort the list of members by name or by date created, or they may specify certain membership options, such as only retrieving members who are not banned. The result of the method will always return as [Live collection](../../core-concepts/live-objects-collections/).

To query community members with certain criteria, the following parameters are used:

* `membershipOptions`:  allows users to filter the results based on the membership status of community members.  Passing an empty option or not passing an option set for `membershipOptions` parameter will default to `member`.
  * `member` - will filter out all banned members and only include unbanned members.
  * `ban` - will only include banned members in the results.
* `roles`:  allows users to query for members with default moderator roles by using "_channel-moderator_" or "_community-moderator_" as the value. At this moment, we do not have a way to query for member-only roles. For custom roles assigned to members, users can pass in `roleId` of the custom role to filter members by this role.
* `includeDeleted` : A parameter accepting a boolean value.&#x20;
  * `true` -> include a member whose user has been deleted &#x20;
  * `false` -> exclude member whose user has been deleted

{% hint style="info" %}
Community member count value is based on all members in the community including the members whose user has been deleted.
{% endhint %}

* `sortBy`: allows users to specify the sorting method for the returned collection. The possible values include `displayName`, `firstCreated`, `lastCreated`. The `firstCreated` sort option will be specified by default if it isn't specified. When a keyword is provided, leading to a list sorted by search rank.

{% hint style="info" %}
To query community banned members, only the 'Admin' role is currently allowed, while 'Moderators' and 'Users' are not allowed to query community banned members.
{% endhint %}

{% hint style="info" %}
Please note that you can only assign custom roles to a member in a community via the SDK. This feature is **not** yet available in the Social Plus Console.

If you assign a custom role to a user via the Social Plus console, the role will only be applied at the user level and not at the community level, and if you try to query for a member with this custom role, no results will be returned.
{% endhint %}

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/ce469dc032b6bf717caeba5c174344f2" %}

{% embed url="https://gist.github.com/amythee/08af3be2ec7c961809c9351d3063885a" %}

{% embed url="https://gist.github.com/amythee/9483f168819462accb8e55ad8028a90a" %}

{% embed url="https://gist.github.com/amythee/5934c43f99f405aacc59bfca25249d5c#file-get-members-parameter-example-swift" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/f38d5663b3acd75e76acf6079bb6a7de" %}

Passing an empty option set for `membershipOptions` parameter will default to `.member`.
{% endtab %}

{% tab title="JavaScript" %}
Below is the sample code to get a list of community members. This method will return a `LiveCollection` instance.&#x20;

{% embed url="https://gist.github.com/amythee/374eb7565502773a939950a2a77abd34#file-getcommunitymembers-js" %}
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/amythee/f0c1cf3f012e0f6aa65a45d3dbdb898a#file-querycommunitymembers-ts" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/ea7c1c5243209d65ceecc7f0e5eff00d" %}
{% endtab %}
{% endtabs %}

### Search for community members

To search for community members, users can call the relevant method and provide the desired keyword, roles, and membership options parameters. For example, they may specify certain membership options, such as only retrieving members who are not banned. The result of the method will always return as [Live collection](../../core-concepts/live-objects-collections/).

If no keyword is supplied, the list of users for the specified community will be sorted by the date they joined.&#x20;

To search for community members with certain criteria, the following parameters are used:

* `keyword`: allows users to specify the keyword to search for. The result contains members with either matching `displayName` or `userId`
* `membershipOptions`:  allows users to filter the results based on the membership status of community members.  Passing an empty option or not passing and option set for `membershipOptions` parameter will default to `member`.
  * `member` - will filter out all banned members and only include unbanned members.
  * `ban` - will only include banned members in the results.
* `roles`:  allows users to query for members with default moderator roles by using "_channel-moderator_" or "_community-moderator_" as the value. At this moment, we do not have a way to query for member-only roles. For custom roles assigned to members, users can pass in the `roleId` of the custom role to filter members by this role.
* `includeDeleted` : A parameter accepting a boolean value.&#x20;
  * `true` -> include a member whose user has been deleted &#x20;
  * `false` -> exclude member whose user has been deleted
* `sortBy`: allows users to specify the sorting method for the returned collection. The possible values include `displayName`, `firstCreated`, `lastCreated`. The `displayName` sort option will be specified by default if it isn't specified. When a keyword is provided, leading to a list sorted by search rank.

{% hint style="info" %}
To query community banned members, only the 'Admin' role is currently allowed, while 'Moderators' and 'Users' are not allowed to query community banned members.
{% endhint %}

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/ce469dc032b6bf717caeba5c174344f2" %}

{% embed url="https://gist.github.com/amythee/9483f168819462accb8e55ad8028a90a" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/35215ee00c0fa2617e097f2feacf405a" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/ea7c1c5243209d65ceecc7f0e5eff00d" %}
{% endtab %}
{% endtabs %}
