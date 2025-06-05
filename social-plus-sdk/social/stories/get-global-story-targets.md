# Get Global Story Targets

## Get Global Story Targets

The `getGlobalStoryTargets()` function retrieves all active story targets with non-expired stories. The resulting LiveCollection provides real-time updates on story creation per target. 'Unsynced story targets'—those with stories in 'syncing' or 'failed' states—are prioritized, followed by 'Synced story targets' with successful creations, sorted by most recent first.

Here's an explanation of the function parameter:

* `queryOption`: Represents how the collection should be filtered and sorted.
  * SEEN - A LiveCollection that contains only story targets that **don't have** unseen stories sorted by recent creation first.
  * UNSEEN - A LiveCollection that contains only story targets that **have** unseen stories sorted by recent creation first.
  * ALL - A LiveCollection that contains all active story targets sorted by recent creation first.
  * SMART - Concatenation of results from UNSEEN followed by SEEN option in a single LiveCollection.

<table>
  <thead>
    <tr>
      <th width="152">Query Option</th>
      <th width="130">Filter</th>
      <th width="263">Sorting</th>
      <th>Unsynced Story Targets</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SEEN</td>
      <td>Only seen</td>
      <td>Recent creation first</td>
      <td>Excluded</td>
    </tr>
    <tr>
      <td>UNSEEN</td>
      <td>Only unseen</td>
      <td>1st: Unsynced storyTarget first<br/>2nd: Recent creation first</td>
      <td>Included</td>
    </tr>
    <tr>
      <td>ALL</td>
      <td>-</td>
      <td>1st: Unsynced storyTarget first<br/>2nd: Recent creation first</td>
      <td>Included</td>
    </tr>
    <tr>
      <td>SMART</td>
      <td>-</td>
      <td>Concatenation of [UNSEEN] and [SEEN]</td>
      <td>Included</td>
    </tr>
  </tbody>
</table>

<Tabs>
  <Tab title="iOS">
    <Frame>
      <img src="https://gist.github.com/amythee/f6c23151620a8a9140aedd7a5ef3ae46" />
    </Frame>
  </Tab>
  <Tab title="Android">
    <Frame>
      <img src="https://gist.github.com/0ea454586f42487860d3d754fc084107" />
    </Frame>
  </Tab>
  <Tab title="TS">
    <Frame>
      <img src="https://gist.github.com/amythee/9c858cba487ceb075e26b6537f6a7700" />
    </Frame>
  </Tab>
</Tabs>