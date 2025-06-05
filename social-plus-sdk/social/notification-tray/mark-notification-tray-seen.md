# Mark Notification Tray Seen

Use `markTraySeen()` to update the tray's seen timestamp on the server when the user visits the Notification Tray screen.

This method supports global-level read tracking, separate from per-item seen state. Once invoked, future calls to `getNotificationTraySeen()` will return the new `isSeen` value. It is recommended to call this method as soon as the tray UI is opened.

<img src="../../../.gitbook/assets/Explore.jpg" alt="Have new notification" />

<img src="../../../.gitbook/assets/My Communities.jpg" alt="Notification already seen" />

<Tabs>
  <Tab title="iOS">
    <iframe src="https://gist.github.com/amythee/b48d79ffc410f8d55c1b9bb759b1bf73" />
  </Tab>
  <Tab title="Android">
    <iframe src="https://gist.github.com/48cf5214b0007d4fee540b53bab5f2c2" />
  </Tab>
  <Tab title="Web">
    <iframe src="https://gist.github.com/amythee/fda232837ec10e401fccacd386006815" />
  </Tab>
</Tabs>