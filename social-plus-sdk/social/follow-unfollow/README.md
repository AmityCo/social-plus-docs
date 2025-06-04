# Follow/Unfollow

Following relationships are a key component of social networks and are essential for creating connections between users in social features. These connections are used to determine the visibility and accessibility of data in user feeds and global feed.

### **User Relationship Concept** <a href="#user-relationship-concept" id="user-relationship-concept"></a>

Currently, our SDK provides a one-directional relationship between users. For example, when user A follows user B, the system will know that user A has connected with user B. However, user B does not necessarily have to follow user A in return.

### **‌User Connection Method Concept** <a href="#user-connection-method-concept" id="user-connection-method-concept"></a>

To create relationships with other users, our SDK provides two methods:

1. With request process: In this method, once a user sends a "Follow" action to the target `userId`, the system will send a request to the target user. The connection will not be established until the target user accepts the follow request.
2. Without request process: In this method, once a user sends a "Follow" action to the target `userId`, the system will automatically establish the connection between the two users without requiring the target user to accept the follow request.

By providing these connection methods, our platform allows users to create and manage social connections effectively and efficiently, based on their specific needs and preferences.

{% hint style="info" %}
The default connection method is the **With request process**. If you wish to change the connection method, you can modify it by making an API call: [Follow with/without request API](https://api-docs.amity.co/#/Network%20Setting/put\_api\_v3\_network\_settings\_social).&#x20;

Please refer to the example below:

```json
curl --location --request PUT 'https://api.sg.amity.co/api/v3/network-settings/social' \
--header 'accept: application/json' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer xxx' \
--data '{
  "isFollowWithRequestEnabled": false
}'
```


{% endhint %}
