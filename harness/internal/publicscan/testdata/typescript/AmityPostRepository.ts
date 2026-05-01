export class AmityPostRepository {
  async createPost(data: object): Promise<string> {
    return '';
  }

  async getPosts(communityId: string): Promise<string[]> {
    return [];
  }

  private deletePost(postId: string): void {}

  protected internalAction(): void {}
}
