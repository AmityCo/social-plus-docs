# User

## Identity

_Social Plus SDK's do not store or manage any user data_. This means that you do not have to import or migrate existing user profiles into the system, user management should be handled by your application code. Instead, every user is simply represented by a unique `userID`, which can be any string that uniquely identifies the user and is **immutable** throughout its lifetime.

> A database primary key would make an ideal `userID`. Conversely, something like username or emails is not recommended as those values may change over time.

If you wish to assign additional permissions for a user, for example, moderation privileges or different sending limits, you can provide an array of roles to assign to this user. Roles are defined in the admin panel and can be tied to an unlimited number of users. Once again, Social Plus does not store or manage any user data, which means you do not have to import or migrate existing users into the system. It also means that Social Plus cannot provide user management functionalities like a list of users, or limit actions of certain users (e.g. user permissions). Instead, these functionalities should be handled by the rest of your application's capabilities and your server.

### Description of Users

### User Repository

Though the SDK does not store and should not be responsible for the handling User profile data for your application; We do provide tools to make some surface-level queries and searches for existing user accounts. With the help of our `UserRepository` class, you will be able to list all the users, search for list of users whose display name matches your search query and get `AmityUser` object from user ID.

<Tabs>
  <Tab title="iOS">
    ```
    let userRepository = AmityUserRepository(client: client)
    ```
  </Tab>
  <Tab title="Android">
    ```
    val userRepository = AmityUserRepository(client)
    ```
  </Tab>
  <Tab title="JavaScript">
    ```
    import { UserRepository } from '@amityco/js-sdk';
    const userRepo = new UserRepository();
    ```
  </Tab>
  <Tab title="Flutter">
    ```
    final userRepository = AmityUserRepository();
    ```
  </Tab>
</Tabs>

### Ban User

You can ban a user globally. When users are globally banned, they can no longer access Social Plus's network and will be forcibly removed from all their existing channels.

Refer [global ban](../../../analytics-and-moderation/console/moderation-roles-and-privileges.md#global-ban) documentation for instructions on how to globally ban a user.

For more information please visit to [User & Content Management](broken-reference)