from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

COMMENTS_GROUP = "comments"


def broadcast_new_comment(data: dict) -> None:
    """Push a freshly created comment to every client subscribed to the comments group."""
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return
    async_to_sync(channel_layer.group_send)(
        COMMENTS_GROUP,
        {"type": "comment.created", "comment": data},
    )
