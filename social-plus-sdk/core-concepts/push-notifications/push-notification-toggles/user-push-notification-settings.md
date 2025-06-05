# User Push Notification Settings

The SDK offers push notification settings per user, allowing users to configure whether to enable or disable push notifications for specific feature modules. This configuration applies universally to every device logged in as the same user.

Configurable modules include `CHAT`, `SOCIAL`, and `LIVE_STREAM`.

## Get User Push Notification Settings

The SDK provides `getSettings()` function within User Notification to inspect the current settings of each feature module.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      ```swift
      // Get settings
      userNotification.getSettings { result in
          switch result {
          case .success(let settings):
              // Handle success
              print("Settings: \(settings)")
          case .failure(let error):
              // Handle error
              print("Error: \(error)")
          }
      }
      ```
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
      ```kotlin
      // Get settings
      userNotification.getSettings(object : UserNotificationSettingsCallback {
          override fun onSuccess(settings: UserNotificationSettings) {
              // Handle success
          }
          
          override fun onError(error: SdkError) {
              // Handle error
          }
      })
      ```
    </CodeGroup>
  </Tab>
  <Tab title="Flutter">
    The functionality isn't currently supported by this SDK.
  </Tab>
</Tabs>

## Update Push Notification Settings

The SDK provides `enable()` function where user can specify the settings of each module and `disableAll()` function where user can choose to disable notifications on every module.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      ```swift
      // Enable specific modules
      userNotification.enable([.chat, .social]) { result in
          switch result {
          case .success:
              // Handle success
              print("Settings updated")
          case .failure(let error):
              // Handle error
              print("Error: \(error)")
          }
      }

      // Disable all modules
      userNotification.disableAll { result in
          switch result {
          case .success:
              // Handle success
              print("All notifications disabled")
          case .failure(let error):
              // Handle error
              print("Error: \(error)")
          }
      }
      ```
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
      ```kotlin
      // Enable specific modules
      val modules = arrayOf(NotificationModule.CHAT, NotificationModule.SOCIAL)
      userNotification.enable(modules, object : UserNotificationCallback {
          override fun onSuccess() {
              // Handle success
          }
          
          override fun onError(error: SdkError) {
              // Handle error
          }
      })

      // Disable all modules
      userNotification.disableAll(object : UserNotificationCallback {
          override fun onSuccess() {
              // Handle success
          }
          
          override fun onError(error: SdkError) {
              // Handle error
          }
      })
      ```
    </CodeGroup>
  </Tab>
  <Tab title="Flutter">
    The functionality isn't currently supported by this SDK.
  </Tab>
</Tabs>