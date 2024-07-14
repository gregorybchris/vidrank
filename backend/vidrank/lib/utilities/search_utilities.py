from typing import Iterator

from vidrank.lib.youtube.playlist_item import PlaylistItem


def iter_filtered_playlist_items(playlist_items: list[PlaylistItem], query: str) -> Iterator[PlaylistItem]:
    """Filters out the playlist items that are not videos.

    Args:
        playlist_items (list[PlaylistItem]): The playlist items to filter.
        query (str): The query to filter by.

    Returns:
        Iterator[PlaylistItem]: An iterator over the filtered playlist items.
    """
    for item in playlist_items:
        if query.lower() in item.title.lower():
            yield item
