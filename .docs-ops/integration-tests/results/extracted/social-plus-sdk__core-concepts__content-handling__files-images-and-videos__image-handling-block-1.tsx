/// <reference path="../../preamble.d.ts" />
// source: social-plus-sdk/core-concepts/content-handling/files-images-and-videos/image-handling.mdx:124-150

import React from 'react';
import { FileRepository } from '@amityco/ts-sdk';

const ImageUpload = () => {
  const changeHandler = async (event: React.ChangeEvent<HTMLInputElement>) => {
    if (!event.target.files) {
      return;
    }

    const data = new FormData();
    data.append('files', event.target.files[0]);

    const { data: image } = await FileRepository.uploadImage(
      data,
      // This function will be called with the percentage of upload progress
      (percent: number) => {
        console.log(`Upload progress: ${percent}%`);
      },
      // This is optional and can be used to provide an alternative text for the image
      'Alt text for the image',
    );

    return image;
  };

  return <input type="file" name="file" onChange={changeHandler} />;
};
