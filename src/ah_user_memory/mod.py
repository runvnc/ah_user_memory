from lib.providers.commands import command
from lib.pipelines.pipe import pipe
from .memory_utils import (
    get_memories,
    save_memory,
    update_memory,
    delete_memory,
    format_memories
)
from loguru import logger

@pipe(name='filter_messages', priority=8)
def add_user_memories(data: dict, context=None) -> dict:
    """
    Add user memories to the end of the system message.
    """
    try:
        if context is None or not hasattr(context, 'username'):
            logger.warning("No username found in context for memories")
            return None

        # Get all memories for the user
        memories = get_memories(context.username)
        if not memories:
            return None

        # Format memories
        formatted_memories = format_memories(memories)

        # Add to first message (system message)
        if not data.get('messages') or len(data['messages']) == 0:
            logger.warning("No messages found in data for adding memories")
            return None

        first_msg = data['messages'][0]
        if isinstance(first_msg.get('content'), str):
            first_msg['content'] = first_msg['content'] + formatted_memories
        elif isinstance(first_msg.get('content'), dict) and first_msg['content'].get('type') == 'text':
            first_msg['content']['text'] = first_msg['content']['text'] + formatted_memories
        elif isinstance(first_msg.get('content'), list):
            first_msg['content'].append({"type": "text", "text": formatted_memories})

        return data

    except Exception as e:
        logger.error(f"Error in add_user_memories pipe: {str(e)}")
        return None

@command()
async def memory_add(content: str, context=None) -> dict:
    """
    Add a new memory for the user.
    Note: Keep memories concise while preserving important details.
    The system will maintain about 3-5 pages of notes total.
    When approaching the limit, memories should be consolidated
    and compressed rather than deleting important information.
    """
    if context is None or not hasattr(context, 'username'):
        raise ValueError("Username not available in context")

    try:
        memory = save_memory(context.username, content)
        return {"status": "success", "memory": memory}
    except Exception as e:
        logger.error(f"Failed to add memory: {str(e)}")
        raise

@command()
async def memory_update(memory_id: str, content: str, context=None) -> dict:
    """
    Update an existing memory.
    """
    if context is None or not hasattr(context, 'username'):
        raise ValueError("Username not available in context")

    try:
        memory = update_memory(context.username, memory_id, content)
        if memory is None:
            return {"status": "error", "message": "Memory not found"}
        return {"status": "success", "memory": memory}
    except Exception as e:
        logger.error(f"Failed to update memory: {str(e)}")
        raise

@command()
async def memory_delete(memory_id: str, context=None) -> dict:
    """
    Delete a memory.
    """
    if context is None or not hasattr(context, 'username'):
        raise ValueError("Username not available in context")

    try:
        success = delete_memory(context.username, memory_id)
        if not success:
            return {"status": "error", "message": "Memory not found"}
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Failed to delete memory: {str(e)}")
        raise
