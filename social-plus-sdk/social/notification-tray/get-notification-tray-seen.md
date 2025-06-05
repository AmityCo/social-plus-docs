# Get Notification Tray Seen

The `getNotificationTraySeen()` method allows your app to determine whether there are unseen notifications by retrieving the current `isSeen` status of the notification tray.

This is particularly useful for reflecting read/unread indicators in the UI—such as toggling a bell icon badge—based on whether new notifications have arrived since the tray was last viewed.

The seen status is managed on the server and may be affected by actions from other devices. However, the state is **not updated via real-time events**, and thus requires manual refresh to stay current.

**🔁 Refresh Strategy**

To keep the seen status accurate across clients:

**1. On-demand refresh (recommended)**

* Invoke `getNotificationTraySeen()` whenever the Notification Tray UI is refreshed.
* Implement a pull-to-refresh gesture or a dedicated refresh button for user-initiated updates.

**2. Polling (not recommended)**

* If polling is used, set the interval to **120 seconds or more** to reduce the risk of server rate limiting.
* Continuous polling should be avoided unless absolutely necessary.

**🔄 Update Behavior**

* When `markNotificationTraySeen()` is invoked **on the same client**, the `isSeen` value returned by `getNotificationTraySeen()` will update immediately if the LiveObject is being observed.
* However, there is **no cross-device real-time sync**. If `markNotificationTraySeen()` is invoked from another device—or if the server adds a new notification—the local client must call `getNotificationTraySeen()` again to retrieve the updated state.

<img src="../../../.gitbook/assets/Explore.jpg" alt="" />

<Tabs>
  <Tab title="iOS">
    <Frame>
      <iframe src="https://gist.github.com/amythee/d6487d6b50c2ab3160ed61fe7f331052"></iframe>
    </Frame>
  </Tab>
  <Tab title="Android">
    <Frame>
      <iframe src="https://gist.github.com/67453175d068353e284ce720c64a77a0"></iframe>
    </Frame>
  </Tab>
  <Tab title="Web">
    <Frame>
      <iframe src="https://gist.github.com/amythee/20b26424bf19a43eca2b348b08b6a0d2"></iframe>
    </Frame>
  </Tab>
</Tabs>