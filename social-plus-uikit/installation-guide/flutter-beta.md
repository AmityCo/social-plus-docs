# Flutter (Beta)

### **Prerequisites**

1. Flutter and Dart are installed on your system.
2. Flutter SDK version `>=2.5.0`
3. Dart SDK version `>=2.17.6 <3.0.0`
4. Valid Installation or Android Studio
5. A valid Amity Social Cloud account and an API key.

### **Step 1: Add** Social Plus **UIKit Dependency**

Add Social Plus UIKit to your project using this command

```
flutter pub add amity_uikit_beta_service
```

### **Step 2: Setup Required Permissions For iOS project**

Your application needs the following permissions to access the camera, microphone, and photo library:

* In your `info.plist`, add the following keys with appropriate descriptions:
  * `NSCameraUsageDescription`
  * `NSMicrophoneUsageDescription`
  * `NSPhotoLibraryUsageDescription`

### **Step 3: Customizing the UI**

Social Plus UIKit supports extensive customization options via a `config.json` file. You can modify themes, colors, and icons for various components and elements of the story feature according to your application's design requirements.

* Example customization snippet:

```json
"global_theme": {
  "light_theme": {
    "primary_color": "#FFFFFF",
    "secondary_color": "#AB1234"
  }
}
```

* You can exclude certain UI elements or customize specific components and elements as per your needs.

You have now successfully integrated the Social feature into your Flutter application. For further customization options, refer to the detailed documentation provided with the SDK. If you encounter any issues or require assistance, our community forum at community.social.plus.co is always here to help.
