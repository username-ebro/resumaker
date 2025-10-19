// Core type definitions for Resumaker frontend

export interface User {
  id: string;
  email: string;
  created_at: string;
}

export interface Experience {
  title: string;
  company: string;
  location?: string;
  start_date: string;
  end_date: string;
  bullets: string[];
}

export interface ResumeStructure {
  contact_info: {
    name: string;
    email: string;
    phone?: string;
    location?: string;
    linkedin?: string;
    portfolio?: string;
  };
  summary: string;
  experience: Experience[];
  skills: { [key: string]: string[] };
  education: Education[];
  certifications: Certification[];
  optimization_report?: {
    ats_score: number;
    improvements_made: string[];
    warnings: string[];
    recommendations: string[];
  };
}

export interface Resume {
  id: string;
  user_id: string;
  html_content: string;
  content: ResumeStructure;
  status: string;
  version_number: number;
  ats_score: number;
  job_id: string | null;
  is_starred: boolean;
  is_archived: boolean;
  created_at: string;
  updated_at: string;
}

export interface KnowledgeEntity {
  id: string;
  user_id: string;
  entity_text: string;
  entity_type: string;
  source_type: string;
  verified: boolean;
  created_at: string;
}

export interface JobData {
  title: string;
  company: string;
  description: string;
  url?: string;
  keywords: string[];
}

export interface UploadResponse {
  success: boolean;
  extracted_data?: Record<string, unknown>;
  knowledge_extraction?: {
    success: boolean;
    entities_extracted?: number;
    error?: string;
  };
}

export interface ConversationMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface Conversation {
  id: string;
  user_id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface PendingEntity {
  id: string;
  entity_text: string;
  entity_type: string;
  source_type: string;
  verified: boolean;
}

export interface Relationship {
  id: string;
  source_entity_id: string;
  target_entity_id: string;
  relationship_type: string;
  metadata?: Record<string, unknown>;
}

export interface Education {
  degree: string;
  institution: string;
  location?: string;
  graduation_date?: string;
  gpa?: string;
}

export interface Certification {
  name: string;
  issuer: string;
  date_earned?: string;
  expiration_date?: string;
  credential_id?: string;
}
