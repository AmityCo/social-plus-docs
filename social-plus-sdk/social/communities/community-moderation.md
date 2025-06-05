# Community Moderation

Social Plus Community Moderation provides a way to moderate the community in multiple ways. This provides another layer of control over community member access and permissions, allowing the creator or admin to manage the community more effectively and ensure that members have the appropriate roles and permissions to perform their duties within the community.

## Add Roles

To add roles to community members, users can provide the `roles` and `userIds` as parameters, specifying which roles should be added to which members.

<Tabs>
  <Tab title="iOS">
    <iframe src="https://gist.github.com/amythee/348e1b5640beff25a05c7a8e5ae02530"></iframe>
  </Tab>
  <Tab title="Android">
    <iframe src="https://gist.github.com/amythee/08dffb2bdf978115b467994c1b5bdd1a#file-amitycommunityaddandremoverole-kt"></iframe>
  </Tab>
  <Tab title="JavaScript">
    <iframe src="https://gist.github.com/amythee/8bdf2941d7240f9e770a4323a4d74838#file-assignrolestousers-js"></iframe>
  </Tab>
  <Tab title="TypeScript">
    <iframe src="https://gist.github.com/d352fa32d7807d8847d556364451a1fc"></iframe>
  </Tab>
  <Tab title="Flutter">
    <iframe src="https://gist.github.com/amythee/fdcbc7e3baaf14159c1051903869df15#file-amitycommunityaddrole-dart"></iframe>
  </Tab>
</Tabs>

## Remove Roles

Similarly, to remove roles from community members, users can provide the `roles` and `userIds` as parameters, specifying which roles should be removed from which members.

<Tabs>
  <Tab title="iOS">
    <iframe src="https://gist.github.com/amythee/d0b9734e79fd037e7f58a38835d5332b"></iframe>
  </Tab>
  <Tab title="Android">
    <iframe src="https://gist.github.com/amythee/08dffb2bdf978115b467994c1b5bdd1a#file-amitycommunityaddandremoverole-kt"></iframe>
  </Tab>
  <Tab title="JavaScript">
    <iframe src="https://gist.github.com/amythee/85bda8f7d003d8d5d6a1719c4d17b7a3#file-removerolesfromusers-js"></iframe>
  </Tab>
  <Tab title="TypeScript">
    <iframe src="https://gist.github.com/b259f22ba50e6a917eb7f26c8dfab73d"></iframe>
  </Tab>
  <Tab title="Flutter">
    <iframe src="https://gist.github.com/amythee/7ccfbb26c717e9be0af8a771e6f5ceae#file-amitycommunityremoverole-dart"></iframe>
  </Tab>
</Tabs>

<Info>
`addRoles` and `removeRoles` do not create new roles but assign and remove existing roles from given users. You can add or remove default roles as well as custom roles.
</Info>

## Add Members

To add members to a community, users can specify the `userIds` and `communityId` of the members they want to add. This function will add the specified users to the specified community, granting them access to the community and its content.

<Tabs>
  <Tab title="iOS">
    <iframe src="https://gist.github.com/amythee/1032652b1a5cf9399de3dcc032b9da30"></iframe>
  </Tab>
  <Tab title="Android">
    <iframe src="https://gist.github.com/amythee/ca292aa610e91a4d94e5e296a6376f30"></iframe>
  </Tab>
  <Tab title="JavaScript">
    <iframe src="https://gist.github.com/amythee/b3017d4b58ebe705d1175d5596e0a601#file-addmembers-js"></iframe>
  </Tab>
  <Tab title="TypeScript">
    <iframe src="https://gist.github.com/ee7106c847e277beade11e1dcbdb5b00"></iframe>
  </Tab>
  <Tab title="Flutter">
    <iframe src="https://gist.github.com/amythee/e4faeae2af37d48fab6ac1d9fa15849c"></iframe>
  </Tab>
</Tabs>

## Remove Members

To remove members from a community, users can specify the `userIds` and `communityId` of the members they want to remove. This function will remove the specified users from the specified community, revoking their access to the community and its content.

<Tabs>
  <Tab title="iOS">
    <iframe src="https://gist.github.com/amythee/f4c69cd80c11c299fad891a71cfcc889"></iframe>
  </Tab>
  <Tab title="Android">
    <iframe src="https://gist.github.com/amythee/62e95e42bfbffcbb2806ba33ad5a1b81"></iframe>
  </Tab>
  <Tab title="JavaScript">
    <iframe src="https://gist.github.com/amythee/5651b0d0cf13c6689fc604663ac2b3e2#file-removemembers-js"></iframe>
  </Tab>
  <Tab title="TypeScript">
    Version 6

    <iframe src="https://gist.github.com/e993c4cf701fecadd76d7c4ad2b7ac2f"></iframe>

    Beta (v0.0.1)

    <iframe src="https://gist.github.com/amythee/2e1a7c11754c93710888a4dc2876218a#file-removecommunitymembers-ts"></iframe>
  </Tab>
  <Tab title="Flutter">
    <iframe src="https://gist.github.com/amythee/707f432c466854f13bb1c047ec367edc"></iframe>
  </Tab>
</Tabs>

## Ban Users

The `banMembers` method accepts an array of `userId` as a parameter, which allows the creator or moderators of a community to ban multiple members at once. This feature provides a quick and efficient way to enforce community rules and ensure that members who violate those rules are appropriately restricted.

<Tabs>
  <Tab title="iOS">
    <iframe src="https://gist.github.com/amythee/68d18eae8e418f360827b071d085a1e4"></iframe>
  </Tab>
  <Tab title="Android">
    <iframe src="https://gist.github.com/amythee/43decda594f1c598e4be2565be8bbb16"></iframe>
  </Tab>
  <Tab title="JavaScript">
    <iframe src="https://gist.github.com/amythee/48f341215518d7e679138dafe17f6b1a#file-banusers-js"></iframe>
  </Tab>
  <Tab title="TypeScript">
    Version 6

    <iframe src="https://gist.github.com/9cf9c8b31103a451bf1e0afd74fb0adb"></iframe>
  </Tab>
  <Tab title="Flutter">
    <iframe src="https://gist.github.com/amythee/dc37764acf5e623db07c1846814102f7#file-amitycommunitymemberban-dart"></iframe>
  </Tab>
</Tabs>

## Unban Users

The `unbanMembers` function accepts an array of `userId` as a parameter, which allows the creator or moderators of a community to quickly remove the ban from multiple members. This feature can be useful when a banned member has corrected their behavior and is ready to rejoin the community.

<Tabs>
  <Tab title="iOS">
    <iframe src="https://gist.github.com/amythee/1dbbcf81654000177e300be87445329a"></iframe>
  </Tab>
  <Tab title="Android">
    <iframe src="https://gist.github.com/amythee/27f75dc32788fc76bd4c17a45e8cfafa"></iframe>
  </Tab>
  <Tab title="JavaScript">
    <iframe src="https://gist.github.com/amythee/07a2a3269e302b8e2bb39dea468ef130#file-unbanusers-js"></iframe>
  </Tab>
  <Tab title="TypeScript">
    Version 6

    <iframe src="https://gist.github.com/54ce6fe0d84a9390bf9e6aa9b164fad7"></iframe>
  </Tab>
  <Tab title="Flutter">
    <iframe src="https://gist.github.com/amythee/58b07bb02f6cc142f5ab21237cebb4ba#file-amitycommunitymemberban-dart"></iframe>
  </Tab>
</Tabs>

<Info>
**Note:**

1. The community creator is automatically assigned as the community moderator.
2. The previous/last moderator is not allowed to leave a community and an error is displayed.
3. The community moderator can promote a user/member to a moderator.
4. The community moderator can demote a moderator to a user/member.

This applies only to Live and Community channels'. This does not apply to the Conversation Channel.
</Info>

## Permission

The SDK provides a convenient way for users to check their permissions within a community by using the `Client.hasPermission` method.

To use this method, users can send one of the available Permission enums as a parameter to the method. The method will then check if the user has the specified permission within the community and return a boolean value indicating whether or not the user has that permission.

<Tabs>
  <Tab title="iOS">
    <iframe src="https://gist.github.com/amythee/d6a0dd33ecae8cb34d18477675737225"></iframe>
  </Tab>
  <Tab title="Android">
    <iframe src="https://gist.github.com/amythee/c4d90f2bf854c3aa2612f21f0a886d60#file-amitycommunitypermissioncheck-kt"></iframe>
  </Tab>
  <Tab title="TypeScript">
    <iframe src="https://gist.github.com/amythee/59690393b1c1997d2252739d51bbd558#file-checkcommunitypermission-ts"></iframe>
  </Tab>
  <Tab title="Flutter">
    <iframe src="https://gist.github.com/amythee/b3d87d6158f2402de208babfadbdef3b"></iframe>
  </Tab>
</Tabs>