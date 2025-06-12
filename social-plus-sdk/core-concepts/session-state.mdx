# Session State

Session state is a key concept in the SDK that describes the authentication status of the client device. There are several session states that the SDK can be in, including:

* `notLoggedIn`
* `establishing`
* `established`
* `tokenExpired`
* `terminated`

The `established` state is the normal and fully authenticated state in which the SDK is usable. The other states represent different stages of the authentication process or an error condition.

<Frame>
  <img src="../../.gitbook/assets/SDK session management-State Diagram Public.drawio-2.png" alt="" />
  <p>Session State Diagram</p>
</Frame>

When SDK is initialized:

* If the user is not logged in, the SDK starts in the initial "`notLoggedIn`" state.
* If the user is already logged in, the SDK automatically resumes the logged-in session and immediately switches to the `established` state.

<Info>
When TS SDK is initialized, the session state always begins as `notLoggedIn`.
</Info>

When logging in:

* If login succeeds, it moves to `established` state.
* If login fails, it moves to `notLoggedIn` state.

When logging out manually:

* It moves to `notLoggedIn` state.

When the user is logged in, but the user is banned or deleted from the system.

* It moves to `terminated` state.

<Info>
The error code will be presented in `terminated` state. Please refer to [error-handling.md](error-handling.md) for more details.
</Info>

When token has expired:

* It moves to `tokenExpired` state.

<Info>
If the access token has expired, all network requests will fail. However, the SDK includes an automatic process for renewing the access token. As long as this process is implemented correctly, it is unlikely that the app will encounter this problem.

Please refer to [#session-handler](#session-handler) for more details.
</Info>

## Read and Observe Session State

The SDK provides APIs for reading and observing the session state.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
      ```swift
      // Observe Session State
      let subscription = sdk.sessionState.subscribe { state in
          switch state {
          case .notLoggedIn:
              // Not logged in
          case .establishing:
              // Logging in
          case .established:
              // Logged in
          case .tokenExpired:
              // Access token expired
          case .terminated:
              // Session terminated
          }
      }
      ```
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    ```kotlin
    // Observe Session State
    val subscription = sdk.sessionState.subscribe { state ->
        when (state) {
            SessionState.NOT_LOGGED_IN -> {
                // Not logged in
            }
            SessionState.ESTABLISHING -> {
                // Logging in
            }
            SessionState.ESTABLISHED -> {
                // Logged in
            }
            SessionState.TOKEN_EXPIRED -> {
                // Access token expired
            }
            SessionState.TERMINATED -> {
                // Session terminated
            }
        }
    }
    ```
  </Tab>
  <Tab title="JavaScript">
    ```javascript
    // Observe Session State
    const subscription = sdk.sessionState.subscribe(state => {
      switch (state) {
        case 'notLoggedIn':
          // Not logged in
          break
        case 'establishing':
          // Logging in
          break
        case 'established':
          // Logged in
          break
        case 'tokenExpired':
          // Access token expired
          break
        case 'terminated':
          // Session terminated
          break
      }
    })
    ```
  </Tab>
  <Tab title="TypeScript">
    ```typescript
    // Observe Session State
    const subscription = sdk.sessionState.subscribe(state => {
      switch (state) {
        case 'notLoggedIn':
          // Not logged in
          break
        case 'establishing':
          // Logging in
          break
        case 'established':
          // Logged in
          break
        case 'tokenExpired':
          // Access token expired
          break
        case 'terminated':
          // Session terminated
          break
      }
    })
    ```
  </Tab>
  <Tab title="Flutter">
    ```dart
    // Observe Session State
    final subscription = sdk.sessionState.subscribe((state) {
      switch (state) {
        case SessionState.notLoggedIn:
          // Not logged in
          break;
        case SessionState.establishing:
          // Logging in
          break;
        case SessionState.established:
          // Logged in
          break;
        case SessionState.tokenExpired:
          // Access token expired
          break;
        case SessionState.terminated:
          // Session terminated
          break;
      }
    });
    ```
  </Tab>
</Tabs>

### Implementing an app based on session state

Session state is designed to align with the typical flow of an app. For example, developers can use the session state to guide app navigation, like this:

<Tabs>
  <Tab title="iOS">
    ```swift
    let subscription = sdk.sessionState.subscribe { state in
        switch state {
        case .notLoggedIn:
            // Show login screen
            showLoginScreen()
        case .establishing:
            // Show loading screen
            showLoadingScreen()
        case .established:
            // Show main screen
            showMainScreen()
        case .tokenExpired:
            // Show login screen
            showLoginScreen()
        case .terminated:
            // Show login screen with error
            showLoginScreen(withError: "Session terminated")
        }
    }
    ```
  </Tab>
  <Tab title="Android">
    ```kotlin
    val subscription = sdk.sessionState.subscribe { state ->
        when (state) {
            SessionState.NOT_LOGGED_IN -> {
                // Show login screen
                showLoginScreen()
            }
            SessionState.ESTABLISHING -> {
                // Show loading screen
                showLoadingScreen()
            }
            SessionState.ESTABLISHED -> {
                // Show main screen
                showMainScreen()
            }
            SessionState.TOKEN_EXPIRED -> {
                // Show login screen
                showLoginScreen()
            }
            SessionState.TERMINATED -> {
                // Show login screen with error
                showLoginScreen("Session terminated")
            }
        }
    }
    ```
  </Tab>
  <Tab title="JavaScript">
    ```javascript
    const subscription = sdk.sessionState.subscribe(state => {
      switch (state) {
        case 'notLoggedIn':
          // Show login screen
          showLoginScreen()
          break
        case 'establishing':
          // Show loading screen
          showLoadingScreen()
          break
        case 'established':
          // Show main screen
          showMainScreen()
          break
        case 'tokenExpired':
          // Show login screen
          showLoginScreen()
          break
        case 'terminated':
          // Show login screen with error
          showLoginScreen('Session terminated')
          break
      }
    })
    ```
  </Tab>
  <Tab title="TypeScript">
    ```typescript
    const subscription = sdk.sessionState.subscribe(state => {
      switch (state) {
        case 'notLoggedIn':
          // Show login screen
          showLoginScreen()
          break
        case 'establishing':
          // Show loading screen
          showLoadingScreen()
          break
        case 'established':
          // Show main screen
          showMainScreen()
          break
        case 'tokenExpired':
          // Show login screen
          showLoginScreen()
          break
        case 'terminated':
          // Show login screen with error
          showLoginScreen('Session terminated')
          break
      }
    })
    ```
  </Tab>
  <Tab title="Flutter">
    ```dart
    final subscription = sdk.sessionState.subscribe((state) {
      switch (state) {
        case SessionState.notLoggedIn:
          // Show login screen
          showLoginScreen();
          break;
        case SessionState.establishing:
          // Show loading screen
          showLoadingScreen();
          break;
        case SessionState.established:
          // Show main screen
          showMainScreen();
          break;
        case SessionState.tokenExpired:
          // Show login screen
          showLoginScreen();
          break;
        case SessionState.terminated:
          // Show login screen with error
          showLoginScreen('Session terminated');
          break;
      }
    });
    ```
  </Tab>
</Tabs>

## Session Handler

For logging, the SDK requires `SessionHandler`. SDK uses this object to communicate with the app when session handling is required. Currently, `SessionHandler` is used for:

* Initiate access token renewal when it is about to expire or has expired.

<Tabs>
  <Tab title="iOS">
    ```swift
    class SessionHandler: SessionHandlerProtocol {
        func sessionWillRenewAccessToken(_ renewal: AccessTokenRenewal) {
            // Renew access token without auth token
            renewal.renew()
        }
    }
    ```
  </Tab>
  <Tab title="Android">
    ```kotlin
    class SessionHandler : SessionHandlerProtocol {
        override fun sessionWillRenewAccessToken(renewal: AccessTokenRenewal) {
            // Renew access token without auth token
            renewal.renew()
        }
    }
    ```
  </Tab>
  <Tab title="JavaScript">
    ```javascript
    const sessionHandler = {
      sessionWillRenewAccessToken: renewal => {
        // Renew access token without auth token
        renewal.renew()
      }
    }
    ```
  </Tab>
  <Tab title="TypeScript">
    ```typescript
    const sessionHandler: SessionHandler = {
      sessionWillRenewAccessToken: renewal => {
        // Renew access token without auth token
        renewal.renew()
      }
    }
    ```
  </Tab>
  <Tab title="Flutter">
    ```dart
    class SessionHandler extends SessionHandlerProtocol {
      @override
      void sessionWillRenewAccessToken(AccessTokenRenewal renewal) {
        // Renew access token without auth token
        renewal.renew();
      }
    }
    ```
  </Tab>
</Tabs>

The code above shows a simple session handler. Please note that each function in `SessionHandler` can be customized to your app logic.

### Access Token Renewal

When a user logs in to the SDK for the first time, an access token is issued that is valid for 30 days.

If the access token is about to expire or has already expired, the SDK automatically initiates the renewal process through the `sessionWillRenewAccessToken` method of the `SessionHandler`.

During the renewal process, the SDK passes an `AccessTokenRenewal` object to the app. The app must call either one of the following methods on this object to complete the process.

<table>
  <thead>
    <tr>
      <th width="344.5">Method on renewal object</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>renew()</code></td>
      <td>Indicates the SDK to renew the access token without an auth token.</td>
    </tr>
    <tr>
      <td><code>renewWithAuthToken(...)</code></td>
      <td>Indicates the SDK to renew the access token with an auth token. (Required for secure login)</td>
    </tr>
    <tr>
      <td><code>unableToRetrieveAuthToken()</code></td>
      <td>
        Indicates the SDK to postpone renewal.
        SDK will re-initiate access token renewal at a later time, but no sooner than 10 minutes.
      </td>
    </tr>
  </tbody>
</table>

The following code shows how the app can implement the `sessionWillRenewAccessToken` method by providing an auth token for renewal.

<Tabs>
  <Tab title="iOS">
    ```swift
    class SessionHandler: SessionHandlerProtocol {
        func sessionWillRenewAccessToken(_ renewal: AccessTokenRenewal) {
            // Get auth token from your auth system
            getAuthToken { authToken in
                if let authToken = authToken {
                    // Renew access token with auth token
                    renewal.renewWithAuthToken(authToken)
                } else {
                    // Unable to get auth token
                    renewal.unableToRetrieveAuthToken()
                }
            }
        }
    }
    ```
  </Tab>
  <Tab title="Android">
    ```kotlin
    class SessionHandler : SessionHandlerProtocol {
        override fun sessionWillRenewAccessToken(renewal: AccessTokenRenewal) {
            // Get auth token from your auth system
            getAuthToken { authToken ->
                if (authToken != null) {
                    // Renew access token with auth token
                    renewal.renewWithAuthToken(authToken)
                } else {
                    // Unable to get auth token
                    renewal.unableToRetrieveAuthToken()
                }
            }
        }
    }
    ```
  </Tab>
  <Tab title="JavaScript">
    ```javascript
    const sessionHandler = {
      sessionWillRenewAccessToken: renewal => {
        // Get auth token from your auth system
        getAuthToken().then(authToken => {
          if (authToken) {
            // Renew access token with auth token
            renewal.renewWithAuthToken(authToken)
          } else {
            // Unable to get auth token
            renewal.unableToRetrieveAuthToken()
          }
        })
      }
    }
    ```
  </Tab>
  <Tab title="TypeScript">
    ```typescript
    const sessionHandler: SessionHandler = {
      sessionWillRenewAccessToken: renewal => {
        // Get auth token from your auth system
        getAuthToken().then(authToken => {
          if (authToken) {
            // Renew access token with auth token
            renewal.renewWithAuthToken(authToken)
          } else {
            // Unable to get auth token
            renewal.unableToRetrieveAuthToken()
          }
        })
      }
    }
    ```
  </Tab>
  <Tab title="Flutter">
    ```dart
    class SessionHandler extends SessionHandlerProtocol {
      @override
      void sessionWillRenewAccessToken(AccessTokenRenewal renewal) {
        // Get auth token from your auth system
        getAuthToken().then((authToken) {
          if (authToken != null) {
            // Renew access token with auth token
            renewal.renewWithAuthToken(authToken);
          } else {
            // Unable to get auth token
            renewal.unableToRetrieveAuthToken();
          }
        });
      }
    }
    ```
  </Tab>
</Tabs>