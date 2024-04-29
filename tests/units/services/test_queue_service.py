import pytest
from src.services.queue_service import QueueService


@pytest.mark.asyncio
async def test_queue_service_init(gcp_pubsub_client, mock_settings):
    queue_service = QueueService(settings=mock_settings)
    gcp_pubsub_client.assert_called_once()
    assert queue_service.project == mock_settings.google_project_id
    assert queue_service.topic == mock_settings.pubsub_movies_fetch_topic


@pytest.mark.asyncio
async def test_publish_on_fetch_topic(gcp_pubsub_client, mock_settings):
    queue_service = QueueService(settings=mock_settings)
    message = "test_message"
    attrs = {"attr1": "value1", "attr2": "value2"}

    result = queue_service.publish_on_fetch_topic(message=message, **attrs)

    topic_path_method = gcp_pubsub_client.return_value.topic_path
    publish_method = gcp_pubsub_client.return_value.publish

    publish_method.assert_called_once_with(
        topic=topic_path_method.return_value,
        data=message.encode(),
        **attrs,
    )
    assert result == publish_method.return_value.result.return_value
