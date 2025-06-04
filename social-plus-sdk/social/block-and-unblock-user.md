# Block and Unblock User

This feature allows users to block and unblock other users, manage their list of blocked users, and interact with the users accordingly. The block and unblock features play an important roles in user experience and maintaining a safe, positive environment within a platform or community.

* **User safety and privacy:** The block feature allows users to protect themselves from unwanted interactions, harassment, or cyberbullying. By blocking another user, they can prevent the blocked user from viewing their content and engaging with them on the platform.
* **Control over personal space:** Users can maintain control over their online environment by choosing who they interact with and whose content they want to see. Blocking helps users curate their experience on the platform to match their preferences and comfort levels.
* **Reducing spam and inappropriate content:** Blocking enables users to filter out spam or content that they find offensive or irrelevant. This helps maintain a more pleasant experience for the user and reduces the negative impact that spam or inappropriate content can have on the platform's overall quality.

## Product Behavior for Blocked and Unblocked Users

#### When a user is blocked:

* Blocked users content in global feed, community feed, or user feed will be hidden
* Search user functionality will function normally, blocked users will still be visible.
* Some interactions will be disabled such as:
  * create a post on a blocker's user feed
  * create a comment on a blocker's user posts\* (please read limitations in the last section)
  * add or remove reactions on a blocker's posts
* The [connection status](follow-unfollow/get-connection-status-and-connection-counter.md#connection-status) on the blocked user will become `none` and the blocker will not be able to follow the blocked user.

#### When a user is unblocked:

* Blocked users content in global feed, community feed, or user feed content will be visible
* All prohibited Interactions will be enabled as mentioned above.
* The connection status on the blocked user will retain `none` regardless of the previous connection, and the blocker will be able to follow the unblocked user again.

## Block User

Users can block other users with the following constraints:

* Only users can be blocked, not Console Admins or communities.
* Community moderators or custom roles can be blocked, regardless of their roles.

When Alice blocks Bob:

* Alice can block Bob regardless of their connection status.
* Alice will see Bob's [connection status](follow-unfollow/get-connection-status-and-connection-counter.md#connection-status) as `blocked`.
* Bob will see Alice's [connection status](follow-unfollow/get-connection-status-and-connection-counter.md#connection-status) as `none`.
* Bob won't be notified of the block and can still block Alice.
* Bob's roles and community memberships remain unchanged.

Here's the explanation of the parameter:

* `userId`: This is a required parameter of type `String` that represents the unique identifier of the user you want to block.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/4058e0f09f4627c648048778581823d4" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/08d7211a06f993966cbaf6ea8a55bc75" %}
{% endtab %}

{% tab title="TS" %}
{% embed url="https://gist.github.com/amythee/5a8c85557faf22c46ab3ba2e1c77040c" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/7ff13cf7eaa70fce5b593452b7e56ade" %}
{% endtab %}
{% endtabs %}

## Unblock User

Users can also unblock blocked users with the following constraints:&#x20;

* Their connection status will not return to the state before the block if they were connected. The connection status will always be `none`.
* If Alice was following Bob, they'll need to reconnect with Bob after unblocking.
* If Alice and Bob were not connected, the connection status will remain `none` upon unblocking.

Here's the explanation of the parameter:

* `userId`: This is a required parameter of type `String` that represents the unique identifier of the user you want to unblock.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/df1e7e7d881eeb2a71aa6540493dc975" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/47969724b780c41ffb270a2ac5e58ebe" %}
{% endtab %}

{% tab title="TS" %}
{% embed url="https://gist.github.com/amythee/0b2f736c19114ee1cf243a94b2951ae6" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/97927bb8041dfcaf12165f28f3658c46" %}
{% endtab %}
{% endtabs %}

## Blocked Users List

Users can view and manage a list of users they've blocked. The list will display:

* User ID
* Display Name
* Avatar
* Other relevant user information

Blocked users that are inactive or deleted will not be shown in the list. Users can only view users they've blocked and not the users that have blocked them.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/3ce24573971e09c00893582f580a87a8" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/68819f07f28615a76d7a8dd7ac27446c" %}
{% endtab %}

{% tab title="TS" %}
{% embed url="https://gist.github.com/amythee/40f75fb25da7a1e501ee9420b5ca5a26" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/b7cbb5637bbaefa62810a5bed5e8dcd5" %}
{% endtab %}
{% endtabs %}

## Limitations

While the block and unblock features offer several benefits, there are limitations to their capabilities:

**Interaction with Content**

Blocking does not completely restrict interactions with the blocked user's content in the following scenarios:

* If Alice blocks Bob, and either of them knows the other's post ID, they can still comment on or react to each other's posts.

**Content Notifications**

Blocking does not affect notifications related to blocked users:

* If Alice or Bob creates a post in a community they are both members of, they will still receive notifications about the post created by the other person.
* No user-blocking related real-time events are provided to the SDK.
* Filtering blocked users' RTE is not supported. For example, if Alice and Bob subscribe to the same community feed and one of them creates a post, the other will still receive the post-created event.
