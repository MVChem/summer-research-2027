from pydantic import BaseModel, Field

class Contact(BaseModel):
    id: int
    name: str
    school: str
    direction: str
    themes: list[str]
    homepage: str
    rank: str
    joined: str
    joinYear: int | None
    newAp: bool
    careerSource: str
    priority: str
    publicOpening: str
    openingEvidence: bool
    openingUrl: str
    email: str
    contactRoute: str
    durationNote: str
    remote: str
    funding: str
    note: str
    checkedAt: str
    batch: str
    fitCategory: str
    fitLabel: str
    fitReason: str
    researchAreas: list[str]
    sources: list['PolicyLink']
    institutionCountry: str
    nationality: str
    nationalitySource: str
    selfReportedEthnicity: str
    ethnicitySource: str
    selfReportedGender: str
    genderSource: str

class PolicyLink(BaseModel):
    label: str
    url: str

class Meta(BaseModel):
    title: str
    checkedAt: str
    profile: str
    statement: str
    newApDefinition: str
    total: int
    schools: int
    newAp: int
    publicOpenings: int
    themes: list[str]
    policyLinks: list[PolicyLink]
    emailTemplate: str
    version: str
    added: int
    fitCounts: dict[str, int]
    researchAreas: list[str]
    identityNote: str
    fitNote: str

class Dataset(BaseModel):
    meta: Meta
    contacts: list[Contact] = Field(min_length=200, max_length=200)

class BrowseResult(BaseModel):
    total: int
    contacts: list[Contact]

class DirectionSummary(BaseModel):
    area: str
    total: int
    aiReal: int
    schools: list[str]
