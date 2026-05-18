/// <reference path="../../preamble.d.ts" />
// source: social-plus-sdk/social/content-management/posts/retrieval/viewing-content.mdx:923-964

// Using HTML5 Video element or a video library like Video.js or HLS.js

function playRoomVideo(url: string, videoElement: HTMLVideoElement) {
  // For HLS streams, use HLS.js library
  if (url.includes('.m3u8')) {
    import('hls.js').then(({ default: Hls }) => {
      if (Hls.isSupported()) {
        const hls = new Hls();
        hls.loadSource(url);
        hls.attachMedia(videoElement);
        hls.on(Hls.Events.MANIFEST_PARSED, () => {
          videoElement.play();
        });
      } else if (videoElement.canPlayType('application/vnd.apple.mpegurl')) {
        // Native HLS support (Safari)
        videoElement.src = url;
        videoElement.play();
      }
    });
  } else {
    // For regular video URLs
    videoElement.src = url;
    videoElement.play();
  }
}

// React example
function RoomVideoPlayer({ roomId }: { roomId: string }) {
  const videoRef = useRef<HTMLVideoElement>(null);
  
  useEffect(() => {
    async function loadVideo() {
      const urls = await getRoomPlaybackUrls(roomId);
      if (urls.length > 0 && videoRef.current) {
        playRoomVideo(urls[0], videoRef.current);
      }
    }
    loadVideo();
  }, [roomId]);
  
  return <video ref={videoRef} controls />;
}
