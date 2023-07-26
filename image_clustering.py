"""Takes an input image and clusters the colors using k-means clustering.

Usage: python image_clustering.py <input> <output> <optional: k>

Some constant variables are defined at the top of the file.
Change them to allow more iterations or to change the convergence threshold.
"""

from dataclasses import dataclass
from PIL import Image
import numpy as np
import sys


DEFAULT_K = 8
MAX_ITERATIONS = 10  # Just in case we don't converge.
EPSILON = 0.1


def initialize_centroids(flattened_data, k) -> np.ndarray:
    """Returns starting, empty clusters, with randomly sampled centroids."""
    # Image data shape is height, width, number of channels.
    return flattened_data[np.random.randint(0, flattened_data.shape[0], k)]


def closest_centroid(flattened_data: np.ndarray, centroids: np.ndarray) -> np.ndarray:
    """Returns the index of the centroid closest to every pixel."""
    return np.argmin(
        np.linalg.norm(flattened_data - centroids[:, np.newaxis], axis=-1), axis=0
    )


def update_centroids(
    flattened_data, old_centroids, centroid_assignments
) -> tuple[np.ndarray, bool]:
    """Returns new centroids and True/False whether we've converged."""
    new_centroids = np.zeros_like(old_centroids, dtype=np.float32)
    #new_centroids = np.zeros_like(old_centroids)
    for i in range(old_centroids.shape[0]):
        masked_data = flattened_data[centroid_assignments == i]
        new_centroids[i] = np.mean(masked_data, axis=(0))
    converged = np.all(np.linalg.norm(new_centroids - old_centroids, axis=-1) < EPSILON)
    return new_centroids, converged


def output_file(source_shape, centroids, centroid_assignments, output_file):
    """Creates an image with the original colors and the clustered colors."""
    # Create a new image with the same dimensions as the source.
    output_data = np.zeros(centroid_assignments.shape + (3,), dtype=np.uint8)
    for i in range(centroids.shape[0]):
        # Loop through the centroid indices and assign each pixel to its cluster.
        output_data[centroid_assignments == i] = centroids[i]
    output_data = output_data.reshape(source_shape)
    with Image.fromarray(output_data) as output:
        output.save(output_file)


def cluster_loop(source_data: np.ndarray, k: int) -> np.ndarray:
    """Clusters the colors in source_data using k-means clustering."""
    flattened_data = source_data.reshape(-1, source_data.shape[-1])
    centroids = initialize_centroids(flattened_data, k)
    for i in range(MAX_ITERATIONS):
        print(f"Starting iteration {i}")
        # centroid_assignments is the index of the centroid closest to each pixel.
        centroid_assignments = closest_centroid(flattened_data, centroids)
        # Loop through the centroid indices and assign each pixel to its cluster.
        print("Updating centroids")
        centroids, converged = update_centroids(
            flattened_data, centroids, centroid_assignments
        )
        if converged:
            break
        output_file(
            source_data.shape, centroids, centroid_assignments, f"output_{i}.png"
        )
    return centroids, centroid_assignments


def main(input_path, output_path, k):
    """Reads an image from input_path, clusters the colors, and writes the result to output_path."""
    source_data = None
    with Image.open(input_path) as source:
        source_data = np.array(source.convert("RGB"))
    centroids, centroid_assignments = cluster_loop(source_data, k)
    output_file(source_data.shape, centroids, centroid_assignments, output_path)


if __name__ == "__main__":
    if 3 <= len(sys.argv) <= 4:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        k = int(sys.argv[3]) if len(sys.argv) == 4 else DEFAULT_K
        if k < 2:
            print("Must have at least 2 color clusters.")
            sys.exit(1)
        main(input_path, output_path, k)
    else:
        print("Usage: python image_clustering.py <input> <output> <optional: k>")
        sys.exit(1)
