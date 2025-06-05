# Start / stop message read receipt sync

To ensure that the message read count is up to date for a channel, users need to start reading the channel. When a user opens a channel, the chat system updates the read count for all messages in that channel, based on the user's reading status. This feature is designed to provide accurate read counts for channels, ensuring that users have a clear understanding of which messages have been read and which are still unread.

### Start message read receipt sync

Active syncing read receipt of a channel and letting the chat system know that reading status can update the message read count in that channel. The system will update the read count for all messages in the channel that the user has not yet read.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      <CodeBlock>
        channel.startReading()
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
      <CodeBlock>
        channel.startReading()
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="TypeScript">
    <CodeGroup>
      <CodeBlock>
        await channel.startReading();
      </CodeBlock>
    </CodeGroup>
  </Tab>
</Tabs>

### Stop message read receipt sync

To optimize performance and reduce unnecessary memory consumption, it's important to stop syncing message read receipts before exiting the chatroom page. By halting the read receipt synchronization process, the application can avoid continuing to observe message read statuses when they're no longer relevant. This ensures that system resources are not wasted on monitoring activities that have ceased to be useful, thus enhancing application efficiency and ensuring smoother operation for the user.

<Info>
`stopReading` will be called automatically if the internet connection drops or is disconnected. It lasts for one minute. This means that if an internet connection drops after one minute, `stopReading` will be automatically called, and after it is re-established, `startReading` will be called again.
</Info>

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      <CodeBlock>
        channel.stopReading()
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
      <CodeBlock>
        channel.stopReading()
      </CodeBlock>
    </CodeGroup>
  </Tab>
  <Tab title="TypeScript">
    <CodeGroup>
      <CodeBlock>
        await channel.stopReading();
      </CodeBlock>
    </CodeGroup>
  </Tab>
</Tabs>