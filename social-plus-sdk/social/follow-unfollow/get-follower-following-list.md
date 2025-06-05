# Get Follower/Following List

## Get Followers List

To retrieve a [Live collection](../../core-concepts/live-objects-collections/) of followers for a particular user, simply call the `getFollowerList` method with the `userId` of the user whose follower list you wish to retrieve. The method will return a collection of follow relationship objects, each of which includes information about the target user, the source, and [follow status](get-connection-status-and-connection-counter.md#follow-status) of those two users.

The list of users following me will be arranged chronologically by the date they started following me. While there is no sorting parameter available, the default ordering is determined by the date of the follow action.

Additionally, our platform allows you to filter the follower list by following the status by passing the `status` parameter. For example:

* `accept` filter to retrieve only the followers who you have already accepted their requests.
* `pending` filter to retrieve the list of users who have sent you the following request. Please note that this filter can only be applied if the [connection method](./#user-connection-method-concept) configuration is Within the request process.

<Info>
Deleted users are excluded from the results
</Info>

<Tabs>
<Tab title="iOS">
#### Get My Followers List

<Embed url="https://gist.github.com/amythee/1dd180551211c92aa7bd227839f3ada8" />

#### Get Other User Followers List

<Embed url="https://gist.github.com/amythee/7ede9830e89815a746a8d7a2bb50c51d" />
</Tab>

<Tab title="Android">
#### Get My Followers List

<Embed url="https://gist.github.com/amythee/828e86613c151417ba45de1502afea3f#file-amityfollowfollowerselfquery-kt" />

#### Get Other User Followers List

<Embed url="https://gist.github.com/amythee/e8c6837ddf2aa223d1a4e0a5ca8e85dd#file-amityfollowfollowerselfquery-kt" />
</Tab>

<Tab title="JavaScript">
#### Get My Followers List

<Embed url="https://gist.github.com/amythee/1e5047f75df3aa5e28dee45498e15d0b#file-getfollowers-js" />

#### Get Other User Followers List

<Embed url="https://gist.github.com/amythee/57c067f3b22dc42d268a035fbc46af6e#file-getfollowers-js" />
</Tab>

<Tab title="TypeScript">
Version 6

#### Get My Followers List

<Embed url="https://gist.github.com/bb1c8185ec42e18598f4f151bb7fb342" />

#### Get Other User Followers List

<Embed url="https://gist.github.com/f68205080ff73aeeb63a5cf0d90ba61f" />

Beta (v0.0.1)

<Embed url="https://gist.github.com/amythee/72ed15cb4d5efd4c358d58f8e8425ed7#file-queryfollowers-ts" />
</Tab>

<Tab title="Flutter">
#### Get My Followers List

<Embed url="https://gist.github.com/amythee/47d03022e1700fa99ea1e8cadf55d414#file-amityfollowmyfollowerquery-dart" />

#### Get Other User Followers List

<Embed url="https://gist.github.com/amythee/fa886fc0edc55362d28c150c0f259881#file-amityfollowotherfollowerquery-dart" />
</Tab>
</Tabs>

<Info>
We currently do not support sorting the follower user list.
</Info>

## Get Following List

The `getFollowingList` method returns a [Live collection](../../core-concepts/live-objects-collections/) of follow relationship objects, each of which includes information about the target user, the source, and the follow status of those two users. This information can be used to better understand the user's social network and manage their following more effectively.

The list of users I am following will be arranged chronologically by the date I started following them. Although no sorting parameter is applicable, the default order is based on the date of the following action.

* `accept` filter to retrieve only the users who have already accepted your follow request.
* `pending` filter for retrieving the users whom you have not yet accepted your follow request. Please note that this filter can only be applied if the [connection method](./#user-connection-method-concept) configuration is within the request process.

<Info>
Deleted users are excluded from the results
</Info>

<Tabs>
<Tab title="iOS">
#### Get My Following List

<Embed url="https://gist.github.com/amythee/b19536a3e01eb09523f1291cf9921dd1" />

#### Get Other User Following List

<Embed url="https://gist.github.com/amythee/769af5c5112f52e2da3ed1e197da317c" />
</Tab>

<Tab title="Android">
#### Get My Following List

<Embed url="https://gist.github.com/amythee/0b20a99ff1412bad3aef40d6ecb1c092#file-amityfollowfollowingselfquery-kt" />

#### Get Other User Following List

<Embed url="https://gist.github.com/amythee/a610258e68e7f1ba4f14d8f7dd6afb4b#file-amityfollowfollowerselfquery-kt" />
</Tab>

<Tab title="JavaScript">
#### Get My Following List

<Embed url="https://gist.github.com/amythee/8fe849b4c01ec1b41b613e1c85dfcddb#file-getfollowings-js" />

#### Get Other User Following List

<Embed url="https://gist.github.com/amythee/89a36fa2d12b15db6d3afa40de4937f7#file-getfollowers-js" />
</Tab>

<Tab title="TypeScript">
Version 6

#### Get My Following List

<Embed url="https://gist.github.com/c2105c31c3700debae656f572eaa3b16" />

#### Get Other User Following List

<Embed url="https://gist.github.com/9fc8c897bf93120b0ae7a89aed60abef" />

Beta (v0.0.1)

<Embed url="https://gist.github.com/amythee/fb283bca0853ad9da307c84878f18acc#file-queryfollowings-ts" />
</Tab>

<Tab title="Flutter">
#### Get My Following List

<Embed url="https://gist.github.com/amythee/9c7083acaa6bea6f0f0221faf35a3e1f#file-amityfollowmyfollowingquery-dart" />

#### Get Other User Following List

<Embed url="https://gist.github.com/amythee/4b5c3699dc13fb04078efcc7e12dbea2#file-amityfollowotherfollowingquery-dart" />
</Tab>
</Tabs>

<Info>
We currently do not support sorting of the following user list.
</Info>