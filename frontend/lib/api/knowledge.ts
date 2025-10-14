// API client for knowledge base operations

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface KnowledgeEntity {
  id: string;
  entity_type: string;
  title: string;
  description?: string;
  start_date?: string;
  end_date?: string;
  confidence_score: number;
  is_confirmed: boolean;
  metadata?: Record<string, any>;
  created_at?: string;
  updated_at?: string;
}

export interface GroupedEntities {
  jobs: KnowledgeEntity[];
  skills: KnowledgeEntity[];
  projects: KnowledgeEntity[];
  education: KnowledgeEntity[];
  [key: string]: KnowledgeEntity[];
}

export interface PendingResponse {
  entities: KnowledgeEntity[];
  grouped_by_type: GroupedEntities;
  total_pending: number;
}

export interface ConfirmedResponse {
  entities: KnowledgeEntity[];
  relationships: any[];
  summary: {
    total: number;
    by_type: Record<string, number>;
  };
}

export interface SummaryResponse {
  total: number;
  confirmed: number;
  pending: number;
  by_type: Record<string, { total: number; confirmed: number; pending: number }>;
}

export const knowledgeApi = {
  /**
   * Get all pending (unconfirmed) entities for a user
   */
  async getPending(userId: string): Promise<PendingResponse> {
    const response = await fetch(`${API_URL}/knowledge/pending/${userId}`);

    if (!response.ok) {
      throw new Error('Failed to fetch pending entities');
    }

    return response.json();
  },

  /**
   * Get all confirmed entities for a user
   */
  async getConfirmed(userId: string): Promise<ConfirmedResponse> {
    const response = await fetch(`${API_URL}/knowledge/confirmed/${userId}`);

    if (!response.ok) {
      throw new Error('Failed to fetch confirmed entities');
    }

    return response.json();
  },

  /**
   * Confirm one or more entities
   */
  async confirm(userId: string, entityIds: string[]): Promise<{ confirmed_count: number }> {
    const response = await fetch(`${API_URL}/knowledge/confirm`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, entity_ids: entityIds }),
    });

    if (!response.ok) {
      throw new Error('Failed to confirm entities');
    }

    return response.json();
  },

  /**
   * Update an entity
   */
  async updateEntity(entityId: string, updates: Partial<KnowledgeEntity>): Promise<{ entity: KnowledgeEntity }> {
    const response = await fetch(`${API_URL}/knowledge/entity/${entityId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates),
    });

    if (!response.ok) {
      throw new Error('Failed to update entity');
    }

    return response.json();
  },

  /**
   * Delete an entity
   */
  async deleteEntity(entityId: string): Promise<{ success: boolean }> {
    const response = await fetch(`${API_URL}/knowledge/entity/${entityId}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw new Error('Failed to delete entity');
    }

    return response.json();
  },

  /**
   * Get summary statistics
   */
  async getSummary(userId: string): Promise<SummaryResponse> {
    const response = await fetch(`${API_URL}/knowledge/summary/${userId}`);

    if (!response.ok) {
      throw new Error('Failed to fetch summary');
    }

    return response.json();
  },
};
