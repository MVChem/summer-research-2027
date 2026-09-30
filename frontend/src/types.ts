export interface Contact {
  id: number; name: string; school: string; direction: string; themes: string[];
  homepage: string; rank: string; joined: string; joinYear: number | null; newAp: boolean;
  careerSource: string; priority: string; publicOpening: string; openingEvidence: boolean;
  openingUrl: string; email: string; contactRoute: string; durationNote: string;
  remote: string; funding: string; note: string; checkedAt: string;
  batch: string; fitCategory: 'ai-real' | 'ai-pending' | 'robotics'; fitLabel: string; fitReason: string;
  researchAreas: string[]; sources: { label: string; url: string }[];
  institutionCountry: string; nationality: string; nationalitySource: string;
  selfReportedEthnicity: string; ethnicitySource: string; selfReportedGender: string; genderSource: string;
}
export interface Dataset {
  meta: {
    title: string; checkedAt: string; profile: string; statement: string; newApDefinition: string;
    total: number; schools: number; newAp: number; publicOpenings: number; themes: string[];
    policyLinks: { label: string; url: string }[]; emailTemplate: string;
    version: string; added: number; fitCounts: Record<string, number>; researchAreas: string[];
    identityNote: string; fitNote: string;
  };
  contacts: Contact[];
}
export type View = 'all' | 'added' | 'new' | 'opening' | 'saved';
export type Status = '未联系' | '已联系' | '已回复' | '暂不联系';
export interface ContactProgress { saved?: boolean; status?: Status; personalNote?: string; noteUpdatedAt?: string }
export type Progress = Record<string, ContactProgress>;
export interface Recording { id: string; contactName: string; createdAt: string; duration: number; mimeType: string }
export type Recordings = Record<string, Recording[]>;
