---
hidden: true
---

# Backup

## Enable Unread Count

To enable the unread message count feature on the device, the user must start unread count syncing. This ensures that the user, as well as all channels and subchannels, have an up-to-date message unread count. To disable this feature, users simply stop the unread count syncing, which will stop updating the message unread count from their device.

#### Start unread count syncing

To start unread count syncing, you can use the following code:

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
```swift
SendbirdChat.startUnreadCountSync()
```
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
```java
SendbirdChat.startUnreadCountSync();
```
    </CodeGroup>
  </Tab>
  <Tab title="TypeScript">
    <CodeGroup>
```typescript
sb.startUnreadCountSync();
```
    </CodeGroup>
  </Tab>
</Tabs>

#### Stop unread count syncing

To stop unread count syncing, you can use the following code:

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
```swift
SendbirdChat.stopUnreadCountSync()
```
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
```java
SendbirdChat.stopUnreadCountSync();
```
    </CodeGroup>
  </Tab>
  <Tab title="TypeScript">
    <CodeGroup>
```typescript
sb.stopUnreadCountSync();
```
    </CodeGroup>
  </Tab>
</Tabs>