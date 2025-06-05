# Pinned Post

Pinned posts empower community moderators to highlight key announcements, discussions, or content critical for community engagement. Social Plus maintains separate collections for pinned posts based on their intended placement, currently supporting `default`, `announcement`  and `global` placements.

<Info>
Currently supporting post pinning via ASC console
</Info>

## Query pinned post

Pinned posts must be viewed first when users enter a community and scroll down the feed. To achieve this, the Social Plus SDK provides `getPinnedPost()` function, which offers a separate collection of posts to be rendered at the top of the community feed. This allows the community feed to recognize which posts have been rendered as pinned and optionally exclude those items from the main feed.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
```swift
func getPinnedPost() {
    let request = GetPinnedPostsRequest(
        communityId: "COMMUNITY_ID",
        placement: .default
    )
    
    client.getPinnedPosts(request) { result in
        switch result {
        case .success(let response):
            // Handle pinned posts
            print("Pinned posts: \(response.posts)")
        case .failure(let error):
            // Handle error
            print("Error: \(error)")
        }
    }
}
```
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
```kotlin
fun getPinnedPost() {
    val request = GetPinnedPostsRequest(
        communityId = "COMMUNITY_ID",
        placement = PinnedPostPlacement.DEFAULT
    )
    
    client.getPinnedPosts(request).enqueue(object : Callback<GetPinnedPostsResponse> {
        override fun onResponse(
            call: Call<GetPinnedPostsResponse>,
            response: Response<GetPinnedPostsResponse>
        ) {
            // Handle pinned posts
            println("Pinned posts: ${response.body()?.posts}")
        }
        
        override fun onFailure(call: Call<GetPinnedPostsResponse>, t: Throwable) {
            // Handle error
            println("Error: ${t.message}")
        }
    })
}
```
    </CodeGroup>
  </Tab>
  <Tab title="Typescript">
    <CodeGroup>
```typescript
async function getPinnedPost() {
  try {
    const response = await client.getPinnedPosts({
      communityId: 'COMMUNITY_ID',
      placement: 'default'
    });
    // Handle pinned posts
    console.log('Pinned posts:', response.posts);
  } catch (error) {
    // Handle error
    console.error('Error:', error);
  }
}
```
    </CodeGroup>
  </Tab>
</Tabs>

## Query announcements

Another type of pinned post is an `announcement`. These posts are tracked separately, similar to default pinned posts but with different behavior. Announcements are typically housed at the top of the community in a separate section, making them easily accessible without forcing users to go through every announcement. This type of pinned post is suitable for multiple important posts that need to be highlighted simultaneously, such as reminders, updates, or informational content.

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
```swift
func getAnnouncements() {
    let request = GetPinnedPostsRequest(
        communityId: "COMMUNITY_ID",
        placement: .announcement
    )
    
    client.getPinnedPosts(request) { result in
        switch result {
        case .success(let response):
            // Handle announcements
            print("Announcements: \(response.posts)")
        case .failure(let error):
            // Handle error
            print("Error: \(error)")
        }
    }
}
```
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
```kotlin
fun getAnnouncements() {
    val request = GetPinnedPostsRequest(
        communityId = "COMMUNITY_ID",
        placement = PinnedPostPlacement.ANNOUNCEMENT
    )
    
    client.getPinnedPosts(request).enqueue(object : Callback<GetPinnedPostsResponse> {
        override fun onResponse(
            call: Call<GetPinnedPostsResponse>,
            response: Response<GetPinnedPostsResponse>
        ) {
            // Handle announcements
            println("Announcements: ${response.body()?.posts}")
        }
        
        override fun onFailure(call: Call<GetPinnedPostsResponse>, t: Throwable) {
            // Handle error
            println("Error: ${t.message}")
        }
    })
}
```
    </CodeGroup>
  </Tab>
  <Tab title="Typescript">
    <CodeGroup>
```typescript
async function getAnnouncements() {
  try {
    const response = await client.getPinnedPosts({
      communityId: 'COMMUNITY_ID',
      placement: 'announcement'
    });
    // Handle announcements
    console.log('Announcements:', response.posts);
  } catch (error) {
    // Handle error
    console.error('Error:', error);
  }
}
```
    </CodeGroup>
  </Tab>
</Tabs>

## Query global featured posts

Global featured posts keep your key content prominently displayed at the top of the main feed, the typical landing page on both web and app platforms. This ensures your announcements reach the entire in-app community, maximizing visibility. The `getGlobalPinnedPost()` function in the Social Plus SDK provides a dedicated collection of featured posts that are intended to appear at the top of the global feed, ensuring users see these posts first, regardless of community affiliation.

<Info>
To maintain a balanced feed with fresh content from your communities, we recommend limiting the number of posts featured globally.
</Info>

<Tabs>
  <Tab title="iOS">
    <CodeGroup>
```swift
func getGlobalPinnedPost() {
    let request = GetPinnedPostsRequest(placement: .global)
    
    client.getPinnedPosts(request) { result in
        switch result {
        case .success(let response):
            // Handle global pinned posts
            print("Global pinned posts: \(response.posts)")
        case .failure(let error):
            // Handle error
            print("Error: \(error)")
        }
    }
}
```
    </CodeGroup>
  </Tab>
  <Tab title="Android">
    <CodeGroup>
```kotlin
fun getGlobalPinnedPost() {
    val request = GetPinnedPostsRequest(
        placement = PinnedPostPlacement.GLOBAL
    )
    
    client.getPinnedPosts(request).enqueue(object : Callback<GetPinnedPostsResponse> {
        override fun onResponse(
            call: Call<GetPinnedPostsResponse>,
            response: Response<GetPinnedPostsResponse>
        ) {
            // Handle global pinned posts
            println("Global pinned posts: ${response.body()?.posts}")
        }
        
        override fun onFailure(call: Call<GetPinnedPostsResponse>, t: Throwable) {
            // Handle error
            println("Error: ${t.message}")
        }
    })
}
```
    </CodeGroup>
  </Tab>
  <Tab title="Typescript">
    <CodeGroup>
```typescript
async function getGlobalPinnedPost() {
  try {
    const response = await client.getPinnedPosts({
      placement: 'global'
    });
    // Handle global pinned posts
    console.log('Global pinned posts:', response.posts);
  } catch (error) {
    // Handle error
    console.error('Error:', error);
  }
}
```
    </CodeGroup>
  </Tab>
</Tabs>