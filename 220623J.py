import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def load_and_grey(path):
    # Convert to greyscale
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError(f"Failed to load image from: {path}")
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return grey


def ensure_8bit(grey):
    # Ensure image is 8-bit
    if grey.dtype == np.uint8:
        return grey
    else:
        img_pil = Image.fromarray(grey)
        img_8bit = img_pil.convert("L")   # Convert to 8-bit pixel depth image
        return np.array(img_8bit, dtype=np.uint8)


def pdf_cdf(grey):
    # Compute PDF and CDF
    hist = np.bincount(grey.ravel(), minlength=256).astype(np.float64)
    pdf = hist / hist.sum()
    cdf = np.cumsum(pdf)
    cdf[-1] = 1.0   # Ensure last value is exactly 1.0
    return pdf, cdf


def mapping_test(test_cdf, ref_cdf):
    # Build mapping from test image to reference
    mapping = np.zeros(256, dtype=np.uint8)
    for g in range(256):
        s_val = test_cdf[g]
        idx = np.searchsorted(ref_cdf, s_val, side="left")
        if idx == 0:
            k = 0
        elif idx >= 256:
            k = 255
        else:
            if abs(ref_cdf[idx] - s_val) < abs(ref_cdf[idx-1] - s_val):
                k = idx
            else:
                k = idx - 1
        mapping[g] = k
    return mapping


def apply_mapping(grey, mapping):
    # Apply intensity mapping
    return mapping[grey]


def save_pdf_cdf_side_by_side(pdf, cdf, filename, title):
    # Plot PDF and CDF side by side
    fig, axes = plt.subplots(1, 2, figsize=(12,4))
    
    axes[0].bar(np.arange(256), pdf, color='blue')
    axes[0].set_title(f"{title} PDF")
    axes[0].set_xlim(0,255)
    
    axes[1].plot(cdf, color='green')
    axes[1].set_title(f"{title} CDF")
    axes[1].set_xlim(0,255)
    
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()




if __name__ == "__main__":
    ref_image_path = "ref_220623J.png" 
    test_image_path = "test_220623J.jpg" 

    ref_grey = load_and_grey(ref_image_path)
    test_grey = load_and_grey(test_image_path)

    ref_grey = ensure_8bit(ref_grey)
    test_grey = ensure_8bit(test_grey)

    # Saving greyscale images 
    cv2.imwrite("ref_grey.png", ref_grey)
    cv2.imwrite("test_grey.png", test_grey)

    # PDF and CDF for reference image
    ref_pdf, ref_cdf = pdf_cdf(ref_grey)
    save_pdf_cdf_side_by_side(ref_pdf, ref_cdf, "rhist_220623J.png", "Reference")

    # PDF and CDF for test image before processing
    test_pdf_before, test_cdf_before = pdf_cdf(test_grey)
    save_pdf_cdf_side_by_side(test_pdf_before, test_cdf_before, "thist_before_process.png", "Test Before Processing")

    # Histogram matching
    mapping = mapping_test(test_cdf_before, ref_cdf)
    matched_test = apply_mapping(test_grey, mapping)

    # Saving matched image
    cv2.imwrite("test_after_process.png", matched_test)

    # PDF and CDF after matching for test image
    matched_pdf, matched_cdf = pdf_cdf(matched_test)
    save_pdf_cdf_side_by_side(matched_pdf, matched_cdf, "thist_220623J.png", "Test After Processing")

    print("All images and side-by-side histograms saved successfully.")
