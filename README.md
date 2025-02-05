# User Memory Plugin

This plugin provides persistent memory storage for users, automatically displaying memories in system messages.

## Features

- Stores user memories persistently
- Automatically adds memories to system messages
- Maintains chronological order of memories
- Aims to keep content within 3-5 pages
- Focuses on concise but complete information

## Commands

### memory_add
Add a new memory. Memories should be concise while preserving important details.

```python
memory_add("User expressed preference for brief, technical explanations")
```

### memory_update
Update an existing memory by its ID.

```python
memory_update("memory_id_here", "Updated content here")
```

### memory_delete
Delete a memory by its ID.

```python
memory_delete("memory_id_here")
```

## Storage

Memories are stored as JSON files in `data/username/memories/` with the following structure:

```json
{
  "id": "unique_nanoid",
  "timestamp": 1234567890000,
  "content": "Memory content here",
  "last_accessed": 1234567890000
}
```

## Best Practices

1. Keep memories concise but don't omit important details
2. When approaching 3 pages of notes, focus on consolidating and compressing existing memories
3. Maintain about 3-5 pages of notes total
4. Update existing memories when adding related information rather than creating duplicates
