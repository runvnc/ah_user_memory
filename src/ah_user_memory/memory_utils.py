import os
import json
from datetime import datetime, timezone
from typing import List, Dict, Optional
from loguru import logger
from nanoid import generate

def get_memory_dir(username: str) -> str:
    """Create and return the memory directory path for a user."""
    path = os.path.join("data", username, "memories")
    os.makedirs(path, exist_ok=True)
    return path

def get_memories(username: str) -> List[Dict]:
    """Retrieve all memories for a user."""
    memory_dir = get_memory_dir(username)
    memories = []
    
    if not os.path.exists(memory_dir):
        return memories
    
    for file in os.listdir(memory_dir):
        if file.endswith(".json"):
            filepath = os.path.join(memory_dir, file)
            try:
                with open(filepath, "r") as f:
                    memory = json.load(f)
                    memories.append(memory)
            except Exception as e:
                logger.warning(f"Failed to load memory {filepath}: {str(e)}")
                continue
    
    memories.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
    return memories

def save_memory(username: str, content: str) -> Dict:
    """Save a new memory."""
    memory_id = generate()
    timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)
    
    memory = {
        "id": memory_id,
        "timestamp": timestamp,
        "content": content,
        "last_accessed": timestamp
    }

    memory_dir = get_memory_dir(username)
    filepath = os.path.join(memory_dir, f"memory_{memory_id}.json")
    
    try:
        with open(filepath, "w") as f:
            json.dump(memory, f)
        return memory
    except Exception as e:
        logger.error(f"Failed to save memory to {filepath}: {str(e)}")
        raise

def update_memory(username: str, memory_id: str, content: str) -> Optional[Dict]:
    """Update an existing memory."""
    memory_dir = get_memory_dir(username)
    filepath = os.path.join(memory_dir, f"memory_{memory_id}.json")
    
    if not os.path.exists(filepath):
        return None
        
    try:
        with open(filepath, "r") as f:
            memory = json.load(f)
            
        memory["content"] = content
        memory["last_accessed"] = int(datetime.now(timezone.utc).timestamp() * 1000)
        
        with open(filepath, "w") as f:
            json.dump(memory, f)
        return memory
    except Exception as e:
        logger.error(f"Failed to update memory {memory_id}: {str(e)}")
        raise

def delete_memory(username: str, memory_id: str) -> bool:
    """Delete a memory."""
    memory_dir = get_memory_dir(username)
    filepath = os.path.join(memory_dir, f"memory_{memory_id}.json")
    
    if not os.path.exists(filepath):
        return False
        
    try:
        os.remove(filepath)
        return True
    except Exception as e:
        logger.error(f"Failed to delete memory {memory_id}: {str(e)}")
        raise

def format_memories(memories: List[Dict]) -> str:
    """Format memories for display in system message."""
    if not memories:
        return ""
        
    formatted = """

# User Memories
Important information about this user that persists across chat sessions.

"""
    for memory in memories:
        timestamp = datetime.fromtimestamp(memory['timestamp']/1000, timezone.utc)
        memory_id = memory.get("id", "unknown")
        formatted += (
            f"--- Memory ID: {memory_id} | "
            f"{timestamp.strftime('%Y-%m-%d %H:%M:%S %Z')} ---\n"
            f"{memory.get('content', '')}\n\n"
        )
    
    return formatted
