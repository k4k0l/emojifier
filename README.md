# Emojifier

This web app turns images or webcam frames into colorful emoji mosaics. The width slider controls how wide the emoji art is and the camera button starts a live feed.

The average colour of each block in the source image is matched to a coloured emoji. Additionally, a TensorFlow.js object detection model finds common objects and fills the matching blocks with fun emojis that represent them.
The app also loads BodyPix to segment detected people. Each body part is replaced with its own emoji.

## Usage

1. Select an image or start the camera.
2. The picture is divided into blocks that fit the art area (up to 1980px wide).
3. Each block's average colour is matched to an emoji from the palette.
4. Detected objects are overlaid with representative emojis.
5. When using the camera the emoji art updates in real time.
