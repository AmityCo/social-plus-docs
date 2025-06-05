# Get Story Targets

## Get Story Target

The `getStoryTarget()` function in the Social Plus SDK enables real-time observation of StoryTarget based on specified targets. This function returns a **LiveObject** of StoryTarget, enabling users to receive updates and check whether the target possesses unseen stories. For example, you can call this method if you'd like to implement an unseen story ring for your story feed.

This function requires two parameters: targetType, targetId.

Here's an explanation of the function parameters:

* `targetType`: Represents the type of target, currently supporting 'community.'
* `targetId`: Corresponds to the ID of the designated target.

<Tabs>
  <Tab title="iOS">
    <Frame>
      <img src="https://gist.github.com/amythee/707d88bdf72bdcecd678efe124cb3fe3" />
    </Frame>
  </Tab>
  <Tab title="Android">
    <Frame>
      <img src="https://gist.github.com/amythee/0dc63e0767c38a1721ce473330f226fc" />
    </Frame>
  </Tab>
  <Tab title="TS">
    <Frame>
      <img src="https://gist.github.com/amythee/2cab1c6c55442d118f95a26066634599" />
    </Frame>
  </Tab>
</Tabs>

## Get Story Targets

In addition to the `getStoryTarget()` function, the Social Plus SDK provides `getStoryTargets()` function to enable retrieval of multiple StoryTargets. This function takes an input as an array of `targets` and returns a **LiveCollection** of StoryTargets, enabling users to observe updates of multiple StoryTargets.

Here's an explanation of the function parameter:

* `targets`: Represents an array of pairs of `targetType` and `targetId`

<Note>
The function can accept a maximum of 10 pairs of targets in the array.
</Note>

<Tabs>
  <Tab title="iOS">
    <Frame>
      <img src="https://gist.github.com/amythee/46d6faa2a09b72326175bb80c5f0ce37" />
    </Frame>
  </Tab>
  <Tab title="Android">
    <Frame>
      <img src="https://gist.github.com/amythee/3e23017fc1457f07e7204808285af69e" />
    </Frame>
  </Tab>
  <Tab title="TS">
    <Frame>
      <img src="https://gist.github.com/amythee/2cab1c6c55442d118f95a26066634599" />
    </Frame>
  </Tab>
</Tabs>