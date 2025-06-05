# Channel Push Notification Settings

The SDK offers push notification settings per channel, allowing users to configure whether to enable or disable push notifications for specific channel. This configuration applies universally to every device logged in as the same user.

## Get Channel Push Notification Settings

The SDK provides `getSettings()` function within Channel Notification to check whether push notification is enabled on the channel.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      ```swift
      channel.notifications.getSettings { result in
          switch result {
          case .success(let enabled):
              print("Push notification enabled: \(enabled)")
          case .failure(let error):
              print("Error: \(error)")
          }
      }
      ```
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
      ```kotlin
      channel.notifications.getSettings(
          onSuccess = { enabled ->
              println("Push notification enabled: $enabled")
          },
          onError = { error ->
              println("Error: $error")
          }
      )
      ```
    </CodeGroup>
  </Tab>
  <Tab title="Flutter">
    The functionality isn't currently supported by this SDK.
  </Tab>
</Tabs>

## Update Channel Push Notification Settings

The SDK provides `enable()` and `disable()` functions where user can choose whether to enable or disable push notifications coming from the channel.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      ```swift
      // Enable push notifications
      channel.notifications.enable { result in
          switch result {
          case .success:
              print("Successfully enabled push notifications")
          case .failure(let error):
              print("Error: \(error)")
          }
      }

      // Disable push notifications
      channel.notifications.disable { result in
          switch result {
          case .success:
              print("Successfully disabled push notifications")
          case .failure(let error):
              print("Error: \(error)")
          }
      }
      ```
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
      ```kotlin
      // Enable push notifications
      channel.notifications.enable(
          onSuccess = {
              println("Successfully enabled push notifications")
          },
          onError = { error ->
              println("Error: $error")
          }
      )

      // Disable push notifications
      channel.notifications.disable(
          onSuccess = {
              println("Successfully disabled push notifications")
          },
          onError = { error ->
              println("Error: $error")
          }
      )
      ```
    </CodeGroup>
  </Tab>
  <Tab title="Flutter">
    The functionality isn't currently supported by this SDK.
  </Tab>
</Tabs>