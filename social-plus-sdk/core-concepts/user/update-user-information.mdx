# Update User Information

## Update User Information

Update current user information, including display name, avatar, user description, metadata, etc., using the `updateUser` method in the 'amityClient' class. This method `updateUser` accepts these optional parameters:

The method accepts the following optional parameters:

* `displayName` - user's display name
* `description` - user's description
* `avatarFile` - file ID of the user's avatar
* `avatarCustomUrl` - custom url of the user's avatar
* `metadata` - user's metadata

<Tabs>
<Tab title="iOS">
<CodeGroup>
```swift
https://gist.github.com/b46b48a1fc8d383b0d63de7eaf1d87a0
```
</CodeGroup>
Update the current user data
</Tab>

<Tab title="Android">
<CodeGroup>
```kotlin
https://gist.github.com/amythee/3ffd4d6210bde5423196799fd25f899c
```
</CodeGroup>
</Tab>

<Tab title="JavaScript">
The `updateCurrentUser` method accepts the following optional parameters:

* `displayName` - user's display name
* `description` - user's description
* `avatarFile` - file ID of the user's avatar
* `avatarCustomUrl` - custom url of the user's avatar
* `roles` - user's role
* `metadata` - user's metadata

Below is a sample code on how to update the current user's display name, description, and metadata. This method returns a promise. If the update is successful, the method will return `true,` else it throws an error.

```typescript
const myMetadata = { whatever: "i want", toPass: "is ok" }

const success = await amityClient.updateCurrentUser({
  displayName: "Batman",
  description : "Hero that Gotham needs",
  metadata: myMetadata,
})
```
</Tab>

<Tab title="TypeScript">
<CodeGroup>
```typescript
https://gist.github.com/29ae004285d65cdc225c7b2a309bbd79
```
</CodeGroup>

#### Flag/Unflag Users

To flag a user, call the following method:

<CodeGroup>
```typescript
https://gist.github.com/amythee/7e0f9b84353bf9768e92f2fbfcabee16#file-createuserreport-ts
```
</CodeGroup>

To unflag a user, call the following method:

<CodeGroup>
```typescript
https://gist.github.com/amythee/4fa947cd9dec69c3ed2d14db10327fcc#file-deleteuserreport-ts
```
</CodeGroup>

To check if the user is flagged by the current user:

<CodeGroup>
```typescript
https://gist.github.com/amythee/d1cde9887b6ee6ab377e6aca89917df8
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
<CodeGroup>
```dart
https://gist.github.com/amythee/4203037af5035faa8b1da00eea1e2f4e
```
</CodeGroup>
</Tab>
</Tabs>

### Update Current User's Avatar

You can upload an image and set it as an avatar for the current user.

<Tabs>
<Tab title="iOS">
First, you need to upload image using `AmityFileRepository` and then update the image info.

Step 1 — Upload an image:

<CodeGroup>
```swift
https://gist.github.com/ff0396fbc326057d5651087090262ca4
```
</CodeGroup>
Create `AmityFileRepository`

<CodeGroup>
```swift
https://gist.github.com/add75b73a735f0a60a88af5dfaa02e04
```
</CodeGroup>
Upload an image with `AmityFileRepository`

Step 2 — Passing `AmityImageData` from step 1 into the builder, and call user update API.

<CodeGroup>
```swift
https://gist.github.com/b17a8e13201d596432b0e580a4c82054
```
</CodeGroup>
Update the current user avatar

If you have an avatar present in your current system/server and just want to integrate that existing avatar to AmitySDK, you can just set the URL for the avatar directly.

<CodeGroup>
```swift
https://gist.github.com/f52bdb6f5515c66d16e5831ee9347b9f
```
</CodeGroup>
Update user custom avatar

_**Note**:_ `getAvatarInfo` _provides the information associated with a particular Avatar_
</Tab>

<Tab title="Android">
First, you need to upload image and then update the image info. If you have an avatar present in your current system/server and just want to integrate that existing avatar to AmitySDK, you can just set the URL for the avatar directly.

<CodeGroup>
```kotlin
https://gist.github.com/amythee/283414cbfadd7da03070ad5b84f689b0
```
</CodeGroup>

If you have an avatar present in your current system/server and just want to integrate that existing avatar to AmitySDK, you can just set the URL for the avatar directly.

<CodeGroup>
```kotlin
https://gist.github.com/amythee/91bedfdb58e078d87d02fee951b7c9b8
```
</CodeGroup>
</Tab>

<Tab title="JavaScript">
Either you wish to let us handle your user's avatar, or if you already have a system for it we got you covered. The 2 properties `avatarFileId` and `avatarCustomUrl` answer those two use-cases separately.

You can easily retrieve the url of a file from our FileRepository object and use it to display in your app later on. Here's an example in React:

```typescript
import { useState, useEffect, useMemo } from 'react'

// our image component
const FileImage = ({ fileId }) => {
  const [fileUrl, setFileUrl] = useState()

  useEffect(() => {
    const liveObject = FileRepository.fileInformationForId(fileId)

    liveObject.on('dataUpdated', model => setFileUrl(model.fileUrl))
    liveObject.model && setFileUrl(liveObject.model.fileUrl)

    return () => {
      liveObject.dispose()
    }
  }, [fileId])

  return fileUrl ? <img src={fileUrl} /> : null
}

// our user component
const UserHeader = ({ userId }) => {
  const [user, setUser] = useState({})

  const displayName = useMemo(
    () => user?.displayName ?? user?.userId,
    [user],
  )

  useEffect(() => {
    const liveObject = UserRepository.getUser(userId)

    liveObject.on('dataUpdated', setUser)
    liveObject.model && setUser(liveObject.model)

    return () => {
      liveObject.dispose()
    }
  }, [userId])

  return (
    <div>
     {user.avatarFileId && <FileImage fileId={user.avatarFileId} />}
     {user.avatarCustomUrl && <img src={user.avatarCustomUrl} />}
    </div>
  )
} 
```
</Tab>

<Tab title="TypeScript">
You can easily retrieve the url of a file using `observeFile` and use it to display in your app later on. Here's an example in React:​

<CodeGroup>
```typescript
https://gist.github.com/amythee/1369542cb897a9827343dfc675b9434e#file-dealingwithavatars-ts
```
</CodeGroup>
</Tab>

<Tab title="Flutter">
<CodeGroup>
```dart
https://gist.github.com/amythee/8941d21c7d88af572a7f4aa897098f61
```
</CodeGroup>
</Tab>
</Tabs>