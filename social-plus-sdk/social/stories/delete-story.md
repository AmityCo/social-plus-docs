# Delete Story

There are two types of story deletion: soft delete and hard delete. When a story is soft deleted, it is simply marked as deleted, with the isDeleted flag set to true in the database. The story still exists in the database, but is no longer visible to users. By contrast, when a story is hard deleted, all associated data, including reactions, comments is permanently removed from the database. This makes it impossible to retrieve the data once it has been hard deleted. Note that both soft delete and hard delete permanently remove unsynced stories from cache.

## Soft Delete Story

The '`softDeleteStory()`' function allows users to mark a story as deleted on the server, rendering it inaccessible to users.

This function requires one parameter: 'storyId.' Here's an explanation of the function parameter:

* `storyId`: Corresponds to the ID of the story.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/685004d2dbaa2f3d56fef1f18d3f1b4b" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/03fc9204752c0f33e97bbb9121510c41" %}
{% endtab %}

{% tab title="TS" %}
{% embed url="https://gist.github.com/amythee/86a6be5c6011b23d5347612193cd7e85" %}
{% endtab %}
{% endtabs %}

## Hard Delete Story

The '`hardDeleteStory()`' function permanently deletes the story and all associated data, including reactions and comments from the server.

This function requires one parameter: 'storyId.' Here's an explanation of the function parameter:

* `storyId`: Corresponds to the ID of the story.

{% tabs %}
{% tab title="iOS" %}
{% embed url="https://gist.github.com/amythee/4537756cbf7c048fb4468221669d8d1c" %}
{% endtab %}

{% tab title="Android" %}
{% embed url="https://gist.github.com/amythee/6610d5456a87582d879c47171ba382d7" %}
{% endtab %}

{% tab title="TS" %}
{% embed url="https://gist.github.com/amythee/926631131f26c91082e48d287aace9d8" %}
{% endtab %}
{% endtabs %}

