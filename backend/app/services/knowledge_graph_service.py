"""Knowledge Graph Service - Stores and manages user's knowledge entities"""

from app.database import get_supabase
from datetime import datetime
import uuid

class KnowledgeGraphService:
    """Manages user knowledge graph (facts and relationships)"""

    async def store_entities(self, entities: list, user_id: str) -> dict:
        """
        Store extracted entities in database

        Args:
            entities: List of entity dicts from extraction service
            user_id: UUID of user

        Returns:
            Dict with stored entity IDs and stats
        """
        supabase = get_supabase()
        stored_ids = []
        parent_map = {}  # Track parent-child relationships

        try:
            for entity in entities:
                # Extract nested details before storing parent
                details = entity.pop("details", [])

                # Store parent entity
                entity_id = await self._store_single_entity(entity, user_id)
                stored_ids.append(entity_id)

                # Store details with parent reference
                if details:
                    for detail in details:
                        detail["parent_id"] = entity_id
                        detail_id = await self._store_single_entity(detail, user_id)
                        stored_ids.append(detail_id)

                        # Track for relationship creation
                        if entity_id not in parent_map:
                            parent_map[entity_id] = []
                        parent_map[entity_id].append(detail_id)

            return {
                "success": True,
                "stored_count": len(stored_ids),
                "entity_ids": stored_ids,
                "parent_child_map": parent_map
            }

        except Exception as e:
            print(f"Storage error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "stored_count": len(stored_ids)
            }

    async def _store_single_entity(self, entity: dict, user_id: str) -> str:
        """Store a single entity and return its ID"""
        supabase = get_supabase()

        # Generate ID if not present
        entity_id = entity.get("id") or str(uuid.uuid4())

        # Prepare data for database
        db_entity = {
            "id": entity_id,
            "user_id": user_id,
            "entity_type": entity.get("entity_type"),
            "parent_id": entity.get("parent_id"),
            "title": entity.get("title"),
            "description": entity.get("description"),
            "confidence_score": entity.get("confidence_score", 0.80),
            "is_confirmed": entity.get("is_confirmed", False),
            "source": entity.get("source", "conversation"),
            "source_reference": entity.get("source_reference"),
            "start_date": entity.get("start_date"),
            "end_date": entity.get("end_date"),
            "is_current": entity.get("is_current", False),
            "structured_data": entity.get("structured_data", {}),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

        # Insert into database
        result = supabase.table("knowledge_entities").insert(db_entity).execute()

        return entity_id

    async def create_relationships(self, relationships: list, entity_ids: list) -> dict:
        """
        Create relationships between entities

        Args:
            relationships: List of relationship dicts with from/to indexes
            entity_ids: List of entity IDs in order they were created

        Returns:
            Dict with created relationship IDs
        """
        supabase = get_supabase()
        created_ids = []

        try:
            for rel in relationships:
                # Convert indexes to actual entity IDs
                from_index = rel.get("from_entity_index")
                to_index = rel.get("to_entity_index")

                if from_index is None or to_index is None:
                    continue

                if from_index >= len(entity_ids) or to_index >= len(entity_ids):
                    continue

                from_id = entity_ids[from_index]
                to_id = entity_ids[to_index]

                # Create relationship
                rel_data = {
                    "id": str(uuid.uuid4()),
                    "from_entity_id": from_id,
                    "to_entity_id": to_id,
                    "relationship_type": rel.get("relationship_type", "related_to"),
                    "strength": rel.get("strength", 0.80),
                    "created_at": datetime.now().isoformat()
                }

                result = supabase.table("knowledge_relationships").insert(rel_data).execute()
                created_ids.append(rel_data["id"])

            return {
                "success": True,
                "created_count": len(created_ids),
                "relationship_ids": created_ids
            }

        except Exception as e:
            print(f"Relationship creation error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "created_count": len(created_ids)
            }

    async def get_pending_entities(self, user_id: str) -> dict:
        """
        Get all unconfirmed entities for user

        Args:
            user_id: UUID of user

        Returns:
            Dict with entities grouped by type
        """
        supabase = get_supabase()

        try:
            # Get all unconfirmed entities
            result = supabase.table("knowledge_entities")\
                .select("*")\
                .eq("user_id", user_id)\
                .eq("is_confirmed", False)\
                .order("created_at", desc=True)\
                .execute()

            entities = result.data

            # Group by type
            grouped = self._group_entities_by_type(entities)

            # Build parent-child hierarchy
            hierarchical = self._build_hierarchy(entities)

            return {
                "success": True,
                "total_pending": len(entities),
                "entities": entities,
                "grouped_by_type": grouped,
                "hierarchical": hierarchical
            }

        except Exception as e:
            print(f"Fetch error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "entities": []
            }

    async def get_user_knowledge_graph(self, user_id: str, confirmed_only: bool = True) -> dict:
        """
        Get complete knowledge graph for user

        Args:
            user_id: UUID of user
            confirmed_only: Only return confirmed facts

        Returns:
            Dict with entities, relationships, and summary
        """
        supabase = get_supabase()

        try:
            # Get entities
            query = supabase.table("knowledge_entities")\
                .select("*")\
                .eq("user_id", user_id)

            if confirmed_only:
                query = query.eq("is_confirmed", True)

            entities_result = query.order("created_at", desc=True).execute()
            entities = entities_result.data

            # Get relationships for these entities
            entity_ids = [e["id"] for e in entities]

            if entity_ids:
                relationships_result = supabase.table("knowledge_relationships")\
                    .select("*")\
                    .in_("from_entity_id", entity_ids)\
                    .execute()
                relationships = relationships_result.data
            else:
                relationships = []

            # Group and organize
            grouped = self._group_entities_by_type(entities)
            hierarchical = self._build_hierarchy(entities)
            summary = self._calculate_summary(entities)

            return {
                "success": True,
                "total_entities": len(entities),
                "entities": entities,
                "relationships": relationships,
                "grouped_by_type": grouped,
                "hierarchical": hierarchical,
                "summary": summary
            }

        except Exception as e:
            print(f"Graph fetch error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def confirm_entities(self, entity_ids: list, user_id: str) -> dict:
        """
        Mark entities as confirmed by user

        Args:
            entity_ids: List of entity IDs to confirm
            user_id: UUID of user (for security)

        Returns:
            Dict with confirmation stats
        """
        supabase = get_supabase()

        try:
            # Confirm entities
            result = supabase.table("knowledge_entities")\
                .update({
                    "is_confirmed": True,
                    "updated_at": datetime.now().isoformat()
                })\
                .in_("id", entity_ids)\
                .eq("user_id", user_id)\
                .execute()

            return {
                "success": True,
                "confirmed_count": len(result.data)
            }

        except Exception as e:
            print(f"Confirmation error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def update_entity(self, entity_id: str, updates: dict, user_id: str) -> dict:
        """
        Update entity data (when user edits before confirming)

        Args:
            entity_id: Entity to update
            updates: Dict of fields to update
            user_id: UUID of user (for security)

        Returns:
            Dict with updated entity
        """
        supabase = get_supabase()

        try:
            # Add updated timestamp
            updates["updated_at"] = datetime.now().isoformat()

            result = supabase.table("knowledge_entities")\
                .update(updates)\
                .eq("id", entity_id)\
                .eq("user_id", user_id)\
                .execute()

            return {
                "success": True,
                "entity": result.data[0] if result.data else None
            }

        except Exception as e:
            print(f"Update error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def delete_entity(self, entity_id: str, user_id: str) -> dict:
        """
        Delete entity (when user rejects extracted fact)

        Args:
            entity_id: Entity to delete
            user_id: UUID of user (for security)

        Returns:
            Dict with deletion status
        """
        supabase = get_supabase()

        try:
            # Delete entity (cascade will handle children and relationships)
            result = supabase.table("knowledge_entities")\
                .delete()\
                .eq("id", entity_id)\
                .eq("user_id", user_id)\
                .execute()

            return {
                "success": True,
                "deleted": True
            }

        except Exception as e:
            print(f"Delete error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def _group_entities_by_type(self, entities: list) -> dict:
        """Group entities by their type"""
        grouped = {}

        for entity in entities:
            entity_type = entity.get("entity_type", "other")
            if entity_type not in grouped:
                grouped[entity_type] = []
            grouped[entity_type].append(entity)

        return grouped

    def _build_hierarchy(self, entities: list) -> list:
        """Build parent-child hierarchy from flat list"""
        # Create lookup by ID
        entity_map = {e["id"]: {**e, "children": []} for e in entities}

        # Build hierarchy
        roots = []

        for entity in entities:
            parent_id = entity.get("parent_id")

            if parent_id and parent_id in entity_map:
                # Add to parent's children
                entity_map[parent_id]["children"].append(entity_map[entity["id"]])
            else:
                # Root-level entity
                roots.append(entity_map[entity["id"]])

        return roots

    def _calculate_summary(self, entities: list) -> dict:
        """Calculate summary statistics"""
        total = len(entities)
        confirmed = sum(1 for e in entities if e.get("is_confirmed"))

        by_type = {}
        for entity in entities:
            entity_type = entity.get("entity_type", "other")
            by_type[entity_type] = by_type.get(entity_type, 0) + 1

        return {
            "total_entities": total,
            "confirmed_entities": confirmed,
            "pending_confirmation": total - confirmed,
            "by_type": by_type,
            "completeness_score": round((confirmed / total * 100) if total > 0 else 0, 1)
        }


# Singleton instance
knowledge_graph_service = KnowledgeGraphService()
