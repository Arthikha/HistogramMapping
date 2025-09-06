## Histogram Processing

This project contains a Python program (`220623J.py`) that performs histogram processing. It adjusts the pixel intensity distribution of a test image so that it matches the histogram of a reference image. This is useful for visual consistency (same exposure or same contrast) across different images.

### How it works

- The program reads a test image and a reference image.
- It computes the histogram of both images.
- The test image's histogram is transformed to match the reference image's histogram.
- The result is saved as a new image.

### Images in folder

- `test_220623J.jpg`: The original colored image whose histogram will be adjusted.
- `ref_220623J.png`: The colored image whose histogram will be used as the target for matching.
- `test_grey.png`: The greyscaled image whose histogram will be used as the target for matching.
- `ref_grey.png`: The greyscaled image whose histogram will be used as the target for matching.
- `test_after_process.png`: The output image after histogram matching, visually similar in tone and contrast to the reference image.
- `thist_before_process.png`: Histogram plot of the test image.
- `rhist_220623J.png`: Histogram plot of the reference image.
- `thist_220623J.png`: Histogram plot of the matched image, showing similarity to the reference histogram.

