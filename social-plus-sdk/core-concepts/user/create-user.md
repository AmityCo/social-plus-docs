# Create User

In Social Plus SDK, creating a new user can be done through the login method. Once the user account has been created, the user can then log into the app using their `userId` and `displayName` using the SDK's social and chat features.

You may need to create a new user account via the SDK, such as when integrating the SDK with an existing user authentication system. In these cases, you can use the `login` method. Here's how the `login` method works:

* If a user already exists for the specified `userId`, the SDK will log the user into the app using the provided `userId`. The `displayName` parameter can be updated upon calling the `login` method. If the `displayName` parameter is not provided, the system will retain the existing user's `displayName`.
* If a user account does not already exist for the specified `userId`, the SDK will automatically create a new user account with the provided `displayName` and log the user into the app. If  `displayName` is not provided, the `userId` will be used as `displayName`.

<Note>
* When user edits / adds their display name, it can be up to 100 characters in length.
* When a user ID is created, it can be up to 50 characters in length.
* If `displayName` is passed, but [secured mode](../../../analytics-and-moderation/console/settings/security/#secure-mode) is enabled, the values will be ignored.
</Note>

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      ```kt
      https://gist.github.com/amythee/f0b45fe6861bd0bb3011f7c4fe3fb55f#file-amityusercreation-kt
      ```
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
      ```kt
      https://gist.github.com/amythee/b6d53829e0295df991381bdccf13e317
      ```
    </CodeGroup>
  </Tab>
  <Tab title="JavaScript">
    <CodeGroup>
      ```javascript
      https://gist.github.com/amythee/1154b128523e919c030881c449924283
      ```
    </CodeGroup>
    Without Auth Token

    <CodeGroup>
      ```javascript
      https://gist.github.com/amythee/3b7ae26d1294f65bdd4f5e48089083f1
      ```
    </CodeGroup>
    With Auth Token
  </Tab>
  <Tab title="TypeScript">
    <CodeGroup>
      ```typescript
      https://gist.github.com/amythee/8bdba9f89c8780fae2a49e5c7dad33ee#file-login-ts
      ```
    </CodeGroup>
    Without Auth Token

    <CodeGroup>
      ```typescript
      https://gist.github.com/amythee/48cf885fe2816e10fd3aa95b8dce8411#file-login-ts
      ```
    </CodeGroup>
    With Auth Token
  </Tab>
  <Tab title="Flutter">
    <CodeGroup>
      ```dart
      https://gist.github.com/amythee/4a3d37b5e164655802bdd2c646f9d44a
      ```
    </CodeGroup>
  </Tab>
</Tabs>