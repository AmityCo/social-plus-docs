# Broadcast Live Stream

To broadcast a live stream video, we have provided a convenient broadcaster tool called `AmityStreamBroadcaster`. You will need to import `AmityLiveVideoBroadcastKit.framework` into your app.

### Authorize the required permissions

`AmityStreamBroadcaster` requires the following permissions to work properly.

1. Camera access
2. Microphone access

Before using `AmityStreamBroadcaster`, please make sure these permissions are already granted.

Here are the steps to ask for the permissions.

1. Add `NSCameraUsageDescription` to your app's `info.plist`.
2. Add `NSMicrophoneUsageDescription` to your app's `info.plist`.
3. Call `AVCaptureDevice.requestAccess(for: .video, completion: ...)`
4. Call `AVAudioSession.sharedInstance().requestRecordPermission(_:)`

### **Create an AmityStreamBroadcaster**

You can create broadcaster instance by providing `AmityClient`.

```
broadcaster = AmityStreamBroadcaster(client: client)
```

### Prepare a configuration

Before going live, you will need to set up the broadcaster session by creating `AmityStreamBroadcasterConfiguration`. This configuration will be applied for the next live session.

```swift
// Prepare configs
let config = AmityStreamBroadcasterConfiguration()
config.canvasFitting = .fill
config.bitrate = 3_000_000 // 3mbps
config.frameRate = .fps30

// Setup the next live session with the given configs.
broadcaster.setup(with: config)
```

### Preview the video

The broadcaster object provides **"preview view"**. After finish setting up the broadcaster, you then can take the preview view to attach into your screen.

```swift
// Attach the preview view to show on the screen.
myView.addSubview(broadcaster.previewView)
```

### Setup video resolution

You can set up video resolution anytime **"before"** going live. This setting will affect both the rendering of preview view, and the resolution of live stream session.

```swift
// This settings apply the following changes.
// 1. The preview view to render at 720p.
// 2. The live stream session to broadcast at 720p.
broadcaster.videoResolution = CGSize(width: 1280, height: 720)
```

### Start live stream session

To begin broadcasting the live stream, call

```swift
broadcaster.startPublish(title: "title", description: "description")
```

### Stop live stream session

To stop broadcasting the live stream, call

```swift
broadcaster.stopPublish()
```

### Switch camera position

By default, the broadcaster will use the back camera. However, you can switch camera position anytime by calling

```swift
// Use the back camera
broadcaster.cameraPosition = .back

// Use the front camera
broadcaster.cameraPosition = .front
```

### Observe a broadcaster state

To observe a broadcaster state, we provide a delegate object that you can set to listen to broadcaster's events.

```swift
broadcaster.delegate = self
```

`AmityStreamBroadcasterState`  represents all the possible states.

* `.idle` indicates a state of stream in an idle state.
* `.connecting`   indicates a state of stream that it's connecting to the stream server.
* `.connected` indicates a state of stream that it's connected to the stream server.
* `.disconnected` indicates a status of stream that it's disconnected.

The code below shows an example of printing out the state of broadcaster, when it changes.

```swift
extension MyViewController: AmityStreamBroadcasterDelegate {
    
    func amityStreamBroadcasterDidUpdateState(_ broadcaster: AmityStreamBroadcaster) {
        print(broadcaster.state)
    }
    
}
```
