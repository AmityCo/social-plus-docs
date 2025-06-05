# Delete User

Delete User API is called to delete a user from the system. The display name of the deleted user is replaced with "Deleted User". This API can be called only by admin users.

<Info>
Please note that this action is a **hard delete**, and **all deleted data will be lost and cannot be recovered**.
</Info>

When deleting a user, you can specify that the user should be marked as deleted but the user's data should remain unchanged, or you can specify that all personal data associated with the user should be deleted:

* if the `deleteAll` parameter is set to true, and all personal data (i.e. profile, photos, images, and files), message channels, posts, and comments of the user will be deleted.
* the `markMessageDeleted` parameter, when set to true, deletes all message channels and messages that the user has created
* the `hardDeletePost` parameter, if set to true, deletes all posts created by the user as well as the comments, reactions, child posts, and child comments of the corresponding post
* the `hardDeleteComment` parameter, if set to true, deletes all comments and reactions of the user

### What happens when a user is deleted?

#### **The user cannot be reactivated**

Once a user has been deleted from the system, the account cannot be reactivated under any circumstances. In order to protect the user account data, no other user will be allowed to reactivate the account after it has been deleted by the user.

#### **The user's system ID is still saved, but the username is deleted and replaced with "Deleted User"**

The user's system ID will still be stored in the database, but to protect the user's identity, the account's username will be replaced with the text "Deleted User". All deleted accounts will be marked as "Deleted Accounts".

#### **All conversation channels created by the user will be deleted**

If the user account is deleted, all conversation channels created by that user will be deleted immediately and no other user will be able to access those channels afterwards.

#### **All messages, channel names, and file attachments that the User created will be deleted**

After the account is deleted, all messages for all channels and all attachments created by the user are deleted and cannot be restored.

#### **Channel member count will be updated**

When a user is deleted, the channel members are updated in all channels where the user was a member, so that only active users are counted in the channels.

#### **All user-related data will be permanently deleted and cannot be recovered**

All the user's data, including profile, photos, videos, images, text, audio, video, attachments, files, and anything else that the user has added to the system as a user will be permanently deleted from the system and cannot be recovered.

#### Posts, comments, and associated IDs, as well as subordinate posts and subordinate comments of the user, will be marked as deleted

All posts created/shared by the deleted user will be deleted and all comments added by the deleted user will also be removed from all posts. No comments or sub-posts will be available after the user deletes the account.

#### **Reaction and comment count will be updated**

All reactions and comments posted by the deleted user are detected and updated in the posts.

#### **The user will be marked as deleted when queried**

The status of the user's account is marked as "deleted" when queried and the user can no longer access it.

## **API Parameters**

### **Headers**

| Content-type  | application/json        |
| ------------- | ----------------------- |
| Authorization | Bearer\{{Admin Token\}} |

### Path

| Path   | Data field     |
| ------ | -------------- |
| UserID | User public id |

The API response will be different based on the request and records match. The request may have a successful response, or it may have a bad request error, and it may respond as a User not found. The responses to API calls are mentioned below.

#### Success

<Note type="success">
{
"success":true
}
</Note>

#### Bad Request error

<Note type="warning">
{
"status": "error",
"code": 400000,
"message": "User is already deleted"
}
</Note>

#### User Not Found error

<Note type="warning">
{
"status": "error",
"code": 400400,
"message": "User Not Found."
}
</Note>