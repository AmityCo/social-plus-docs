# Archive Channels

### Archive a Channel

The `archiveChannel` function allows users to archive a specific conversation channel. Archiving a channel removes it from the active list channel but retains its data for future reference. This function takes one parameter, channelId, which specifies the ID of the channel to be archived.

* **Effect for the User:** The archived chat is hidden from the user's main chat list view and moved to a separate archived chat list. This action only affects the user who archives the chat; the other participant(s) in the conversation will still see the chat in their main list as usual.
* **Messages:** Archiving does not delete any messages within the chat. Users can continue sending and receiving messages within the archived chat just like a normal chat.
* **Sorting:** Chats within the archived list are sorted based on the timestamp of the last message exchanged.

<Tabs>
  <Tab title="Flutter">
    <CodeGroup>
      <CodeGroupItem>
```dart
// Archive a channel
await client.archiveChannel(channelId: 'channel-id');
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
</Tabs>

#### Receiving New Messages in Archived Chats

* **Behavior:** If another user sends a message in a chat you have archived, the chat will remain in your archived list. It will not automatically move back to the main chat list.
* **Notifications:** You will **not** receive push notifications for new messages arriving in channels you have archived. The system prevents notifications for channels marked as archived by the recipient user.

#### Important Considerations & Limitations

* **Channel Type:** Only 'conversation' type channels (like DMs) can be archived.
* **Archive Limit:** A user can archive a maximum of 100 channels. An error message will be displayed if a user tries to exceed this limit.
* **Muted Chats:** If a chat is muted and then archived, it is treated as a normal, unmuted chat within the archive list regarding its behavior (though notifications remain disabled due to the archive status).

### Unarchive a Channel

The `unarchiveChannel` function allows users to restore an archived conversation channel back to the active channel list. This function takes one parameter, channelId, which specifies the ID of the channel to be unarchived.

* **Effect for the User:** The chat is removed from the archived list and reappears in the main chat list.
* **Sorting:** The unarchived chat is placed back into the main chat list according to the timestamp of its last message.

<Tabs>
  <Tab title="Flutter">
    <CodeGroup>
      <CodeGroupItem>
```dart
// Unarchive a channel
await client.unarchiveChannel(channelId: 'channel-id');
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
</Tabs>

### Query Archived Conversation Channels

The `queryArchivedChannels` function allows users to retrieve a list of archived channels. This function uses a live collection to fetch the data and provides real-time updates on the fetching status. It also supports pagination to load more data when the user scrolls to the end of the list.

<Tabs>
  <Tab title="Flutter">
    <CodeGroup>
      <CodeGroupItem>
```dart
// Query archived channels
final archivedChannels = await client.queryArchivedChannels();

// Listen to archived channels updates
archivedChannels.listen((channels) {
  // Handle updated channels list
});

// Load more archived channels
await archivedChannels.loadMore();
```
      </CodeGroupItem>
    </CodeGroup>
  </Tab>
</Tabs>