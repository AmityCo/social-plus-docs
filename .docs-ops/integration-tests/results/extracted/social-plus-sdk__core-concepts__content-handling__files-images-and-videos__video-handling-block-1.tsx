/// <reference path="../../preamble.d.ts" />
// source: social-plus-sdk/core-concepts/content-handling/files-images-and-videos/video-handling.mdx:128-155

import React from 'react';
import { FileRepository, ContentFeedType } from '@amityco/ts-sdk';

const VideoUpload = () => {
  const changeHandler = async (event: React.ChangeEvent<HTMLInputElement>) => {
    if (!event.target.files) {
      return;
    }

    const data = new FormData();
    data.append('files', event.target.files[0]);

    /*
    Possible `feedType` value for createVideo:
    - ContentFeedType.STORY or 'story'
    - ContentFeedType.CLIP or 'clip'
    - ContentFeedType.CHAT or 'chat'
    - ContentFeedType.POST or 'post'
     */
    const feedType = ContentFeedType.POST;

    const didVideoUpload = await FileRepository.uploadVideo(data, feedType);

    return didVideoUpload;
  };

  return <input type="file" name="file" onChange={changeHandler} />;
};
