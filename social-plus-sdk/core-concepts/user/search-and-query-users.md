# Search and Query Users

### Search User

Query for users by their display name, receiving a collection of `AmityUser` matching your search. It requires two parameters: the display name you're searching for, and a 'sort option' from the `AmityUserSortOption` enum.  If no keyword is supplied, the list of users will be organized alphabetically by display name.&#x20;

Users also have the option to sort by `lastCreated`, `firstCreated`, or `displayName`. When a keyword is provided, the list will be arranged based on search rank.  The `displayName` sorting option will be specified by default if it isn't specified.

With the `displayName` sorting option, users are sorted alphabetically by their display names using ICU collation for the English locale. This means that special characters such as **Ä** are treated as variants of **A**. For example, a sorted list might appear as:\
`adam, Älex, Alice, Arthur, charlie, Kristen`.

When providing a search keyword, the API performs an exact-match lookup for special characters.

* For instance, if you search for **"Äli"**, only users whose display name contains the **"Äli"** characters (e.g., **"Älise"**) will be returned.
* Conversely, searching for **"Alice"** will not return **"Älice"**.

{% hint style="info" %}
- The search keyword must be **at least 3 characters long**.
- Deleted users are excluded from the results
{% endhint %}

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/c2fa08ba1c32a8b990f61ddd2ea57028" %}
Search users by display name
{% endembed %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/e6efe625dd44688833a0e78dca54ecea" %}

The code above will provide you with the list of users which matches with display name "Brian".
{% endtab %}

{% tab title="JavaScript" %}
```javascript
userRepo.searchUserByDisplayName('Test User 1')
```

The above example searches for all users whose display names _start with_ "Test User 1".&#x20;
{% endtab %}

{% tab title="TypeScript" %}
The `queryUsers` provides a way to search for users by their display name.

{% embed url="https://gist.github.com/4e64739fbc3013367170ba7d2f33b74e" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/3ee3dab5280389461b9417ce8a7734d6#file-amityusersearchbydisplayname-dart" %}
{% endtab %}
{% endtabs %}

### Query Users

Query for users to receive a collection of `AmityUser` based on a single parameter: a 'sort option' from the `AmityUserSortOption` enum. Sort the list by options such as `displayName`, `firstCreated`, or `lastCreated`. The `displayName` sort option will be specified by default if it isn't specified.

With the `displayName` sorting option, users are sorted alphabetically by their display names using ICU collation for the English locale. This means that special characters such as **Ä** are treated as variants of **A**. For example, a sorted list might appear as:\
`adam, Älex, Alice, Arthur, charlie, Kristen`.

{% hint style="info" %}
Deleted users are excluded from the results
{% endhint %}

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/b95e6bbe016d7a3d7e1666afe71cd96d" %}
Query users
{% endembed %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/d07130ddf29326ce4f160ac361a3984b" %}
{% endtab %}

{% tab title="JavaScript" %}
```typescript
const liveUserCollection = UserRepository.queryUsers({
    keyword?: string, 
    filter?: 'all' | 'flagged', 
    sortBy?: 'lastCreated' | 'firstCreated' | 'displayName'
})

// filter if flagCount is > 0
// lastCreated: sort: createdAt desc 
// firstCreated: sort: createdAt asc 
// displayName: sort: alphanumerical asc

liveUserCollection.on(“dataUpdated”, models => {
  models.map(model => console.log(model.userId))
})
```

###
{% endtab %}

{% tab title="TypeScript" %}
{% embed url="https://gist.github.com/56048b7aafbce478752770202e5d6a24" %}

If you wish to observe for changes to a collection of users, you can use `liveUsers`

{% embed url="https://gist.github.com/bfbb6d5f0408dbb9cadfa8be0fa9c3aa" %}
{% endtab %}

{% tab title="Flutter" %}
{% embed url="https://gist.github.com/amythee/ee07f318a29fc7db6f103487f5f32b78#file-amityusergetusers-dart" %}
{% endtab %}
{% endtabs %}
