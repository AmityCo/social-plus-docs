# Intelligent Search - Community

## **Introduction**

The Intelligent Search Community API allows users to search for communities with advanced filtering options. The search covers all communities across categories and tags. However, you can refine the results by applying specific filters such as category IDs, tags, or membership status.

### **Category Filtering**

By default, the search will include communities from all categories. However, you can narrow the search scope to specific categories by specifying `categoryIds` array.

### **Tag Filtering**

By default, the search will include communities regardless of tags. However, you can narrow the search scope to specific tags by specifying `tags` array.

### **Membership Status Filtering**

You can choose to narrow the search by membership status option

`ALL` - Include communities regardless of membership status (default option)

`MEMBER` - Include only communities that the user is a member of.

`NOT_MEMBER` - Include only communities that the user is **not** a member of.

### Example Use Cases

### **Search for Communities**

When the user searches for "ice cream," the output may include communities ranked by their relevance score. For example:

```
Community 1st:
Name: "Ice Cream Society"
Description: "Share your favorite frozen dessert spots and homemade recipes."


Community 2nd:
Name: "Summer Vibes"
Description: "Your guide to the best ice cream parlors and gelato shops in town."


Community 3rd:
Name: "Frozen Treats United"
Description: "Connect with other ice cream and gelato enthusiasts."


Community 4th:
Name: "Sweet Tooth Adventures"
Description: "Explore the world of frozen desserts, from gelato to sorbets."


Community 5th:
Name: "Pastry Lovers"
Description: "Indulge in the best dessert experiences, from cakes to chilled treats."
```

The following code snippet demonstrates how to search for communities across the entire network using semantic search.

<Tabs>
  <Tab title="iOS">
    <Frame>
      <img src="https://gist.github.com/amythee/476c37ec3b37d59130cd4720958e57cb#file-semantic_search_communities-swift" />
    </Frame>
  </Tab>
  <Tab title="Android">
    <Frame>
      <img src="https://gist.github.com/amythee/dd8864a04a45393431c883005933c59f#file-amitycommunitysemanticsearch-kt" />
    </Frame>
  </Tab>
  <Tab title="Typescript">
    <Frame>
      <img src="https://gist.github.com/amythee/652174c82bdfc4fb1c11ffb395b38e21" />
    </Frame>
  </Tab>
</Tabs>

### Limitations

* The search is limited to community names and descriptions, excluding all content within communities