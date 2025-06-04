# User

## Identity

_Social Plus SDK's do not store or manage any user data_. This means that you do not have to import or migrate existing user profiles into the system, user management should be handled by your application code. Instead, every user is simply represented by a unique `userID`, which can be any string that uniquely identifies the user and is **immutable** throughout its lifetime.

> A database primary key would make an ideal `userID`. Conversely, something like username or emails is not recommended as those values may change over time.

If you wish to assign additional permissions for a user, for example, moderation privileges or different sending limits, you can provide an array of roles to assign to this user. Roles are defined in the admin panel and can be tied to an unlimited number of users. Once again, Social Plus does not store or manage any user data, which means you do not have to import or migrate existing users into the system. It also means that Social Plus cannot provide user management functionalities like a list of users, or limit actions of certain users (e.g. user permissions). Instead, these functionalities should be handled by the rest of your application's capabilities and your server.

### Description of Users

<table data-header-hidden><thead><tr><th width="240">Name</th><th>Data Type</th><th width="229">Description</th><th>Attributes</th></tr></thead><tbody><tr><td>Name</td><td>Data Type</td><td>Description</td><td>Attributes</td></tr><tr><td><code>userId</code></td><td><code>string</code></td><td>The id of this user</td><td></td></tr><tr><td><code>roles</code></td><td><code>Array.&#x3C;string></code></td><td>A list of user's roles</td><td></td></tr><tr><td><code>displayName</code></td><td><code>string</code></td><td>The display name of the user</td><td></td></tr><tr><td><code>flagCount</code></td><td><code>integer</code></td><td>The number of users that have flagged this user</td><td></td></tr><tr><td><code>metadata</code></td><td><code>Object</code></td><td>The metadata of the user</td><td></td></tr><tr><td><code>hashFlag</code></td><td><code>Object</code></td><td>A hash for checking internally if this user was flagged by the user</td><td></td></tr><tr><td><code>createdAt</code></td><td><code>date</code></td><td>The date/time the user was created at</td><td></td></tr><tr><td><code>updatedAt</code></td><td><code>date</code></td><td>The date/time the user was updated at</td><td></td></tr><tr><td><code>isGlobalBan</code></td><td><code>Boolean</code></td><td><p>Flag that indicates if the user is globally banned. <code>True</code> means the user is globally banned.<br></p><p><em><strong>Note</strong>: This is not yet supported for Typescript</em></p></td><td></td></tr><tr><td><code>avatarCustomUrl</code></td><td><code>String</code></td><td>Custom Url provided for this user avatar</td><td></td></tr><tr><td><code>isDeleted</code></td><td><code>Boolean</code></td><td>Flag that indicates if the user is deleted</td><td></td></tr></tbody></table>

### User Repository <a href="#user-details" id="user-details"></a>

Though the SDK does not store and should not be responsible for the handling User profile data for your application; We do provide tools to make some surface-level queries and searches for existing user accounts. With the help of our `UserRepository` class, you will be able to list all the users, search for list of users whose display name matches your search query and get `AmityUser` object from user ID.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/268ab78a93ddd797b4c9f678dc4b6204#file-create_user_repository-swift" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/aa7be7c29617edd0345fd8dd3b07bc13" %}
{% endtab %}

{% tab title="JavaScript" %}
```javascript
import { UserRepository } from '@amityco/js-sdk';
const userRepo = new UserRepository();
```
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/9f443d8012c76bda3bdfe1fe5bd5b3c6" %}
{% endtab %}
{% endtabs %}

### Ban User

You can ban a user globally. When users are globally banned, they can no longer access Social Plus's network and will be forcibly removed from all their existing channels.

Refer [global ban](../../../analytics-and-moderation/console/moderation-roles-and-privileges.md#global-ban) documentation for instructions on how to globally ban a user.



For more information please visit to [User & Content Management](broken-reference)&#x20;
