# React Native (Beta)

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

| Region        | Endpoint       | Endpoint URL    |
| ------------- | -------------- | --------------- |
| Europe        | ApiEndpoint.EU | api.eu.amity.co |
| Singapore     | ApiEndpoint.SG | api.sg.amity.co |
| United States | ApiEndpoint.US | api.us.amity.co |

### Authentication <a href="#authentication" id="authentication"></a>

You must first register the current device with a `userId`. A device registered with a `userId` will be permanently tied to that `userId` until you deliberately unregister the device, or until the device has been inactive for more than 90 days. A device registered with a specific `userId` will receive all messages belonging to that user.

```javascript
import {
  AmityUiKitSocial,
  AmityUiKitProvider,
} from 'amity-react-native-social-ui-kit';

export default function App() {
  return (
    <AmityUiKitProvider
      apiKey="API_KEY"
      apiRegion="API_REGION"
      userId="userId"
      displayName="displayName"
      apiEndpoint="https://apix.{API_REGION}.amity.co" //eu, us, or sg
    >
      <AmityUiKitSocial />
    </AmityUiKitProvider>
  );
}
```
