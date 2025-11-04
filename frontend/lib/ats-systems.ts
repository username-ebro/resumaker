// ATS System Profiles - Comprehensive data about major ATS platforms
// Research compiled: 2025-11-03

export interface ATSSystem {
  id: string
  name: string
  marketShare: string
  difficulty: 'easy' | 'medium' | 'hard' | 'very-hard'
  formatPreference: 'docx' | 'pdf' | 'both'
  urlPattern: string
  exampleURL: string
  parsingQuality: 'none' | 'poor' | 'fair' | 'good' | 'excellent'
  allowsCreativeFormatting: boolean
  keywordMatching: 'exact' | 'fuzzy' | 'ai-powered' | 'manual'
  uniqueQuirks: string[]
  optimizationTips: string[]
  commonComplaints: string[]
  bestFor: string
  emoji: string
}

export const ATS_SYSTEMS: Record<string, ATSSystem> = {
  workday: {
    id: 'workday',
    name: 'Workday',
    marketShare: '39%+ of Fortune 500',
    difficulty: 'hard',
    formatPreference: 'docx',
    urlPattern: 'wd5.myworkdayjobs.com',
    exampleURL: 'company.wd5.myworkdayjobs.com/careers',
    parsingQuality: 'fair',
    allowsCreativeFormatting: false,
    keywordMatching: 'exact',
    emoji: '🏢',
    uniqueQuirks: [
      'Extremely sensitive to formatting consistency',
      'Cannot properly read headers and footers 25% of the time',
      'Requires manual input if parsing fails',
      'Forces users to create new account for every application',
      'Biased toward standard section headings - creative headings = automatic rejection'
    ],
    optimizationTips: [
      'Use DOCX format (strongly preferred over PDF)',
      'Use standard fonts: Arial, Times New Roman, or Calibri (11-12 pt)',
      'Standard section headers REQUIRED: "Education," "Experience," "Skills"',
      '8-12 core keywords from job description (15+ looks spammy)',
      'Mirror exact language from job posting',
      'Avoid headers/footers for contact information',
      'Provide examples of skills - don\'t just list them',
      'Keep formatting simple: No columns, no tables, no graphics'
    ],
    commonComplaints: [
      'Issues with resume parsing, requiring manual data entry multiple times',
      'Requiring users to create a new account for every job application',
      'Complicated, time-consuming application process',
      'System times out frequently'
    ],
    bestFor: 'Large enterprise applications'
  },

  greenhouse: {
    id: 'greenhouse',
    name: 'Greenhouse',
    marketShare: 'Growing (+5 pts since 2019)',
    difficulty: 'medium',
    formatPreference: 'both',
    urlPattern: 'boards.greenhouse.io',
    exampleURL: 'job-boards.greenhouse.io/company',
    parsingQuality: 'good',
    allowsCreativeFormatting: true,
    keywordMatching: 'fuzzy',
    emoji: '🌱',
    uniqueQuirks: [
      'DOES NOT USE TRADITIONAL RESUME PARSING (Major differentiator)',
      'Hiring managers see full image of your resume exactly as submitted',
      'No algorithmic scoring or automated ranking',
      'Human review-focused rather than algorithm-focused',
      'Uses scorecards where hiring managers manually rate qualifications'
    ],
    optimizationTips: [
      'PDF or Word both work equally well',
      'Keywords still critical - hiring managers search by job titles, skills, experience',
      'Visual clarity matters for human reviewers',
      'Customize for job description - scorecards rate alignment with requirements',
      'Creative formatting allowed but keep it professional and readable',
      'Focus on content quality over ATS gaming',
      'Word stemming in search ("manage" matches "management")'
    ],
    commonComplaints: [
      'Some confusion about whether formatting matters (it does for readability, not parsing)',
      'Fewer complaints overall - human review provides better candidate experience'
    ],
    bestFor: 'Tech/growth companies that value human review'
  },

  taleo: {
    id: 'taleo',
    name: 'Taleo (Oracle)',
    marketShare: '13.2% of Fortune 500 (declining)',
    difficulty: 'very-hard',
    formatPreference: 'docx',
    urlPattern: 'taleo.net/careersection',
    exampleURL: 'company.taleo.net/careersection/jobsearch',
    parsingQuality: 'poor',
    allowsCreativeFormatting: false,
    keywordMatching: 'fuzzy',
    emoji: '⚠️',
    uniqueQuirks: [
      'Proprietary parsing algorithm strips HTML tags, special characters, certain fonts',
      'Cannot handle tables, columns, headers, footers, excessive styling',
      '4-criteria scoring system: Profile, Education, Experience, Skills (0-3 stars each)',
      'Automatic candidate scoring visible to recruiters (not candidates)',
      '"Invisible scoring" is major complaint',
      'Legacy system with outdated UX'
    ],
    optimizationTips: [
      'DOCX strongly recommended (PDF only if text-based)',
      'Clean, structured formatting REQUIRED - no tables, columns, headers, footers',
      'Mirror exact job description language for keywords',
      '10-15 high-impact keywords from job description',
      'Personalize resume for each job - CRITICAL for Taleo success',
      'Tailor Professional Summary and Skills to each posting',
      'Clear section headings with bullet points',
      'Consistent date formats',
      'Avoid creative formatting entirely'
    ],
    commonComplaints: [
      'Rigid and outdated user experience',
      'Invisible scoring system feels unfair',
      'Rejects qualified candidates for formatting reasons',
      'Most frustrating ATS to work with',
      '75%+ rejection rate even for qualified candidates'
    ],
    bestFor: 'Legacy enterprise systems (avoid if possible)'
  },

  icims: {
    id: 'icims',
    name: 'iCIMS',
    marketShare: '10.7% overall market share',
    difficulty: 'medium',
    formatPreference: 'both',
    urlPattern: 'icims.com/jobs',
    exampleURL: 'company.icims.com/jobs',
    parsingQuality: 'excellent',
    allowsCreativeFormatting: false,
    keywordMatching: 'ai-powered',
    emoji: '🤖',
    uniqueQuirks: [
      'Advanced AI capabilities (more sophisticated than many competitors)',
      'Automatically profiles candidates by skill matching from resumes',
      'Autogenerates skills lists for each candidate',
      'Intelligent scoring system adjusts parameters per job',
      '90% of CVs can be processed without human intervention',
      'Strong CRM capabilities for high-volume recruitment'
    ],
    optimizationTips: [
      'Word or PDF documents both work well',
      'Use standard formatting for best results',
      'Keyword optimization critical - uses keyword matching to identify candidates',
      'Skills-focused resume benefits from autogenerated skills detection',
      'Clean PDF or DOCX format',
      'Benefits from ATS-optimized resume builders (98% parsing success rate)'
    ],
    commonComplaints: [
      'High-volume recruitment can feel impersonal',
      'Generally positive feedback on parsing accuracy (fewer complaints than others)'
    ],
    bestFor: 'High-volume hiring at scale'
  },

  lever: {
    id: 'lever',
    name: 'Lever',
    marketShare: 'Growing (+11 pts since 2019)',
    difficulty: 'medium',
    formatPreference: 'both',
    urlPattern: 'jobs.lever.co',
    exampleURL: 'jobs.lever.co/company',
    parsingQuality: 'good',
    allowsCreativeFormatting: false,
    keywordMatching: 'fuzzy',
    emoji: '🔄',
    uniqueQuirks: [
      'Combines ATS + CRM capabilities (unified platform)',
      'Parsing feeds integrated CRM for long-term candidate nurturing',
      'Higher accuracy with keyword searches due to word stemming',
      'Structures resume data into rich candidate profiles',
      'Ideal for proactive pipeline building'
    ],
    optimizationTips: [
      'PDF or Word both supported',
      'Keep formatting simple and readable (tables/columns can affect format)',
      'Avoid image-based content entirely',
      'Use keywords strategically - benefits from word stemming',
      'Standard fonts and structure recommended',
      'Optimized for long-term candidate relationship building'
    ],
    commonComplaints: [
      'Browser capability requirements can be confusing',
      'Formatting can be affected in columns/tables',
      'Generally positive user feedback on functionality'
    ],
    bestFor: 'Relationship building and talent pipeline development'
  },

  smartrecruiters: {
    id: 'smartrecruiters',
    name: 'SmartRecruiters',
    marketShare: 'Growing market presence',
    difficulty: 'medium',
    formatPreference: 'both',
    urlPattern: 'jobs.smartrecruiters.com',
    exampleURL: 'jobs.smartrecruiters.com/company',
    parsingQuality: 'good',
    allowsCreativeFormatting: false,
    keywordMatching: 'ai-powered',
    emoji: '🧠',
    uniqueQuirks: [
      'Built-in AI resume screening with candidate ranking',
      'Cloud-based ATS with strong screening features',
      'Designed for high-volume hiring',
      'Processes resumes to establish candidate rankings automatically',
      'Saves recruiters significant time with automation'
    ],
    optimizationTips: [
      'PDF or Word both supported',
      'Keyword optimization critical - AI ranks candidates',
      'Standard formatting for best AI interpretation',
      'Align with job description requirements',
      'Quantify achievements for better ranking',
      'Clean, professional structure'
    ],
    commonComplaints: [
      'Some concerns about AI bias in ranking',
      'Relatively fewer complaints (newer, more modern system)'
    ],
    bestFor: 'Companies hiring at scale with AI-powered screening'
  },

  successfactors: {
    id: 'successfactors',
    name: 'SAP SuccessFactors',
    marketShare: '13.2% of Fortune 500',
    difficulty: 'hard',
    formatPreference: 'both',
    urlPattern: 'successfactors.com/career',
    exampleURL: 'career.successfactors.com/company',
    parsingQuality: 'good',
    allowsCreativeFormatting: false,
    keywordMatching: 'exact',
    emoji: '💼',
    uniqueQuirks: [
      'Uses third-party TextKernel for parsing',
      'Complex configuration requirements',
      'Picklist fields don\'t work with resume parsing',
      'Won\'t parse API-submitted or agency candidate resumes',
      'Mobile Apply limitation: Only parses when background fields are empty',
      'Pre-populates work experience, current employer, contact address'
    ],
    optimizationTips: [
      'PDF or Word both supported',
      'Standard formatting essential due to TextKernel parsing',
      'Complete profile before application for best results',
      'Avoid mobile apply if possible (parsing limitations)',
      'Simple structure works best',
      'Not ideal for agency-submitted candidates'
    ],
    commonComplaints: [
      'Complex configuration requirements',
      'Mobile apply parsing doesn\'t work well',
      'Won\'t parse certain candidate types (agency, API-submitted)',
      'Picklist field limitations'
    ],
    bestFor: 'Large enterprise with SAP ecosystem'
  },

  bamboohr: {
    id: 'bamboohr',
    name: 'BambooHR',
    marketShare: 'Small to mid-sized businesses',
    difficulty: 'easy',
    formatPreference: 'both',
    urlPattern: 'bamboohr.com/careers',
    exampleURL: 'company.bamboohr.com/careers',
    parsingQuality: 'none',
    allowsCreativeFormatting: true,
    keywordMatching: 'manual',
    emoji: '🎋',
    uniqueQuirks: [
      'NO NATIVE RESUME PARSING (major limitation)',
      'Requires manual data input for candidate information',
      'Third-party integrations required for parsing',
      'ATS without automated parsing (unusual for modern systems)',
      'Focused on applicant tracking and interview scheduling',
      'Better suited for low-to-moderate application volumes'
    ],
    optimizationTips: [
      'Format matters less than content clarity',
      'Make information easy to find for manual data entry',
      'Standard resume structure helps recruiters input data quickly',
      'Clear contact information prominently displayed',
      'Focus on readability for human review'
    ],
    commonComplaints: [
      'Lack of automatic parsing is a notable limitation',
      'Manual data entry is time-consuming for recruiters',
      'Not suitable for high application volumes'
    ],
    bestFor: 'Small businesses with lower application volumes'
  },

  jazzhr: {
    id: 'jazzhr',
    name: 'JazzHR',
    marketShare: 'Small to mid-sized businesses',
    difficulty: 'medium',
    formatPreference: 'both',
    urlPattern: 'applytojob.com/apply',
    exampleURL: 'company.applytojob.com/apply',
    parsingQuality: 'fair',
    allowsCreativeFormatting: false,
    keywordMatching: 'exact',
    emoji: '🎵',
    uniqueQuirks: [
      'Works best with LinkedIn/Indeed integration',
      'Resume parsing extracts and populates data fields',
      'Manual correction often needed for file attachment uploads',
      'Flaws when fetching from file attachments - fields not appropriated correctly',
      'Lacks advanced AI-powered parsing',
      'Recognized as Top Performer in 2025 Hackett Group rankings'
    ],
    optimizationTips: [
      'Apply through LinkedIn/Indeed when possible for better auto-fill',
      'Standard formatting for file uploads',
      'Double-check auto-populated fields for accuracy',
      'Simple, clean resume structure',
      'PDF or Word both work'
    ],
    commonComplaints: [
      'Auto-fill doesn\'t work well with file attachments',
      'Fields not mapped correctly from resumes',
      'Lacks advanced automation features'
    ],
    bestFor: 'Small to mid-sized companies with basic needs'
  },

  phenom: {
    id: 'phenom',
    name: 'Phenom People',
    marketShare: '8.7% of Fortune 500 (fastest growing)',
    difficulty: 'medium',
    formatPreference: 'both',
    urlPattern: 'phenompeople.com/careers',
    exampleURL: 'company.phenompeople.com/careers',
    parsingQuality: 'good',
    allowsCreativeFormatting: false,
    keywordMatching: 'ai-powered',
    emoji: '🚀',
    uniqueQuirks: [
      'Fastest-growing ATS among Fortune 500 (usage nearly doubled)',
      'Focus on talent experience and AI-powered personalization',
      'Modern platform with advanced features',
      'Strong candidate experience focus'
    ],
    optimizationTips: [
      'Standard ATS best practices apply',
      'Modern AI likely means better semantic understanding',
      'Clean formatting recommended',
      'PDF or Word both work',
      'Keyword optimization important'
    ],
    commonComplaints: [
      'Newer system with limited user feedback available'
    ],
    bestFor: 'Modern companies focused on candidate experience'
  }
}

export const detectATSFromURL = (url: string): ATSSystem | null => {
  const lowercaseURL = url.toLowerCase()

  for (const system of Object.values(ATS_SYSTEMS)) {
    if (lowercaseURL.includes(system.urlPattern.toLowerCase())) {
      return system
    }
  }

  return null
}

export const getATSRecommendation = (atsId?: string): {
  format: 'pdf' | 'docx'
  reasoning: string
  tips: string[]
} => {
  if (!atsId) {
    return {
      format: 'docx',
      reasoning: 'DOCX is the safest choice when the ATS system is unknown. It works with 98% of systems.',
      tips: [
        'Use standard fonts (Arial, Calibri, Times New Roman)',
        'Simple, single-column layout',
        'Standard section headings',
        'Include both PDF and DOCX versions for flexibility'
      ]
    }
  }

  const system = ATS_SYSTEMS[atsId]

  if (!system) {
    return getATSRecommendation()
  }

  const format = system.formatPreference === 'both' ? 'pdf' : system.formatPreference

  return {
    format,
    reasoning: `${system.name} ${
      system.formatPreference === 'docx'
        ? 'strongly prefers DOCX format for best parsing results'
        : system.formatPreference === 'pdf'
        ? 'works well with PDF format'
        : 'accepts both PDF and DOCX equally well'
    }.`,
    tips: system.optimizationTips.slice(0, 4) // Top 4 tips
  }
}

export const getDifficultyColor = (difficulty: ATSSystem['difficulty']): string => {
  switch (difficulty) {
    case 'easy': return 'text-green-600'
    case 'medium': return 'text-yellow-600'
    case 'hard': return 'text-orange-600'
    case 'very-hard': return 'text-red-600'
  }
}

export const getDifficultyLabel = (difficulty: ATSSystem['difficulty']): string => {
  switch (difficulty) {
    case 'easy': return 'Easy'
    case 'medium': return 'Medium'
    case 'hard': return 'Hard'
    case 'very-hard': return 'Very Hard'
  }
}
