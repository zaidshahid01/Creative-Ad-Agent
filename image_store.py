"""
In-memory image store for the Creative Ad Agent.
Images live in RAM and are automatically discarded when the session ends.
"""

import io
import base64
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class StoredImage:
    """Represents a single stored image."""
    name: str
    data: bytes
    content_type: str
    size: int
    uploaded_at: datetime = field(default_factory=datetime.now)

    @property
    def base64(self) -> str:
        """Return the image as a base64-encoded string."""
        return base64.b64encode(self.data).decode("utf-8")

    @property
    def data_url(self) -> str:
        """Return the image as a data URL for embedding in HTML/Markdown."""
        return f"data:{self.content_type};base64,{self.base64}"


class ImageStore:
    """
    A simple in-memory store for product images.
    All data lives in RAM and is lost when the session ends.
    """

    def __init__(self):
        self._images: dict[str, StoredImage] = {}

    def add(self, name: str, data: bytes, content_type: str = "image/png") -> StoredImage:
        """Add an image to the store. Returns the stored image."""
        image = StoredImage(
            name=name,
            data=data,
            content_type=content_type,
            size=len(data),
        )
        self._images[name] = image
        return image

    def get(self, name: str) -> Optional[StoredImage]:
        """Retrieve an image by name."""
        return self._images.get(name)

    def remove(self, name: str) -> bool:
        """Remove an image by name. Returns True if it existed."""
        if name in self._images:
            del self._images[name]
            return True
        return False

    def clear(self):
        """Remove all images from the store."""
        self._images.clear()

    def list_all(self) -> list[StoredImage]:
        """Return all stored images as a list."""
        return list(self._images.values())

    def __len__(self) -> int:
        return len(self._images)

    def __contains__(self, name: str) -> bool:
        return name in self._images

    @property
    def total_size(self) -> int:
        """Total size of all stored images in bytes."""
        return sum(img.size for img in self._images.values())

    @property
    def is_empty(self) -> bool:
        return len(self._images) == 0
