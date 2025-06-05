# Flag / Unflag User

Flag / Unflag User feature is an essential tool for maintaining a safe and engaging chat community. With Social Plus, you can use the flag and unflag user feature to allow moderators and administrators to monitor any inappropriate behavior within a chat channel.&#x20;

In this section, we will discuss how to use the flag and unflag user feature of Social Plus Chat SDK to maintain a safe and engaging chat community.

To flag / unflag users on iOS, Android and Flutter SDK, create an instance of `UserFlagger` first:

<Tabs>
<Tab title="iOS">
```swift
let userRepository: AmityUserRepository = AmityUserRepository(client: client)
let userToBeFlaggedObject: AmityObject<AmityUser> = userRepository.user(forId: "badUser")

guard let userToBeFlagged: AmityUser = userToBeFlaggedObject.object else { return }

let userFlagger = AmityUserFlagger(client: client, userId: IdOfuserToBeFlagged)
```
</Tab>

<Tab title="Android">
<Frame>
<img src="https://gist.github.com/amythee/860855679f2040d319a63670e1d329f7#file-amityuserflaginitialization-kt" />
</Frame>
</Tab>

<Tab title="Flutter">
<Frame>
<img src="https://gist.github.com/amythee/17854e36bf88b63a20e53f4ef8379a1f#file-amityuserflaginitialization-dart" />
</Frame>
</Tab>
</Tabs>

The `UserFlagger` lets you flag and unflag a user. It also exposes an asynchronous way to check whether the current logged-in user has already flagged the given user or not.

## Flag a User

To flag a user, call the following method:

<Tabs>
<Tab title="iOS">
<Frame>
<img src="https://gist.github.com/amythee/0bed67da80efc01f7abea0e59938f56d" />
</Frame>
</Tab>

<Tab title="Android">
<Frame>
<img src="https://gist.github.com/amythee/9bcce808fc17b8e6413414fb75d00d60" />
</Frame>
</Tab>

<Tab title="JavaScript">
```javascript
userRepo.flag({ userId: 'user123' })
```
</Tab>

<Tab title="TypeScript">
<Frame>
<img src="https://gist.github.com/amythee/d371ab71a49f05bd04937f7f7042d7a4" />
</Frame>
</Tab>

<Tab title="Flutter">
<Frame>
<img src="https://gist.github.com/amythee/89269b8e6bf4f447744c777f8c8a5336#file-amityuserflag-dart" />
</Frame>
</Tab>
</Tabs>

## Unflag a User

To unflag a user, call the following method:

<Tabs>
<Tab title="iOS">
<Frame>
<img src="https://gist.github.com/amythee/bbdce34d3ce9c76803669eefe7ae5782" />
</Frame>
</Tab>

<Tab title="Android">
<Frame>
<img src="https://gist.github.com/amythee/d7e34af4e3af711e6c19781592b4e770" />
</Frame>
</Tab>

<Tab title="JavaScript">
```javascript
userRepo.unflag({ userId: 'user123' })
```
</Tab>

<Tab title="TypeScript">
<Frame>
<img src="https://gist.github.com/amythee/14b167af0ff48a7901f8be73f898842f" />
</Frame>
</Tab>

<Tab title="Flutter">
<Frame>
<img src="https://gist.github.com/amythee/b4b4222bda5f64a3550419c45b9ade70#file-amityuserunflag-dart" />
</Frame>
</Tab>
</Tabs>

## Check Flagged By User

To check whether a user has been flagged by the current user:

<Tabs>
<Tab title="iOS">
<Frame>
<img src="https://gist.github.com/amythee/4418090e79803c830772ab2610b6eb32" />
</Frame>
</Tab>

<Tab title="Android">
<Frame>
<img src="https://gist.github.com/amythee/62668a4fb753f059d4c6dd26a7a632cd" />
</Frame>
</Tab>

<Tab title="JavaScript">
```javascript
userRepo.flag({ userId: 'user123' })
    .then(() => {})
    .catch(() => {})
```
</Tab>

<Tab title="TypeScript">
<Frame>
<img src="https://gist.github.com/amythee/a885c90bb0f15c49e07f27aba1113f4a#file-isuserreportedbyme-ts" />
</Frame>
</Tab>

<Tab title="Flutter">
<Frame>
<img src="https://gist.github.com/amythee/9a296a34273f6a8bdfea76a652f452a1#file-amityuserisflaggedbyme-dart" />
</Frame>
</Tab>
</Tabs>