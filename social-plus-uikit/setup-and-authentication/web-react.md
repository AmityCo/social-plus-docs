# Web React

## **Setup API Key**

`AmityUIKitProvider` requires an API key. You need a valid API key to begin using the UIKit. Please find your account API key in the [Social Plus Console.](https://portal.amity.co/login)&#x20;

After logging in Console:

1. Click **Settings** to expand the menu.
2. Select **Security**.
3. On the **Security** page, you can find the API key in the **Keys** section.

![API key in Security page](../../../.gitbook/assets/webconsole.png)

#### **Specify Endpoints Manually (Optional)**

You can specify endpoints manually via optional parameters. API endpoints for each data center are different so you need to adjust the endpoint accordingly.

We currently support multi-data center capabilities for the following regions:

| Region        | apiRegion | Endpoint URL     |
| ------------- | --------- | ---------------- |
| Europe        | eu        | apix.eu.amity.co |
| Singapore     | sg        | apix.sg.amity.co |
| United States | us        | apix.us.amity.co |

### Authentication <a href="#authentication" id="authentication"></a>

You must first register the current device with a `userId`. A device registered with a `userId` will be permanently tied to that `userId` until you deliberately unregister the device, or until the device has been inactive for more than 90 days. A device registered with a specific `userId` will receive all messages belonging to that user.

```javascript
export default function Wrapper({ apiKey, apiEndpoint, userId, displayName }) => {
    const getAuthToken = async () => {
      const authToken = await getAuthTokenFromApi()
      return authToken;
    }
    <AmityUiKitProvider
          key={userId}
          apiKey={apiKey}
          userId={userId}
          apiRegion={apiRegion} //eu, us, or sg
          getAuthToken={getAuthToken} //for secure mode authentication
        >
          <div
            style={{
              position: "absolute",
              left: 0,
              top: 0,
              width: "100vw",
              height: "100dvh",
            }}
          >
            <AmityUiKitSocial />
          </div>
        </AmityUiKitProvider>
```

{% hint style="info" %}
`AmityUIKitProvider` should be placed only once at the top of your application. Having multiple providers will create connection problems.
{% endhint %}

## Integrating CSS Styles

To use the Uikit components with styling, css should be imported.

```javascript
import "@amityco/ui-kit/dist/index.css";
```
