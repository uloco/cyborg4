// video stream
let video = document.querySelector("#video");
if (Hls.isSupported()) {
  let video = document.querySelector("#video");
  let hls = new Hls();
  // bind them together
  hls.attachMedia(video);
  hls.on(Hls.Events.MEDIA_ATTACHED, () => {
    console.log("video and hls.js are now bound together !");
    hls.loadSource(
      "https://d2zihajmogu5jn.cloudfront.net/bipbop-advanced/bipbop_16x9_variant.m3u8"
    );
    hls.on(Hls.Events.MANIFEST_PARSED, (event, data) => {
      console.log(
        "manifest loaded, found " + data.levels.length + " quality level"
      );
    });
  });
  video.play();
} else {
  console.error("HLS Video format is not supported");
}
