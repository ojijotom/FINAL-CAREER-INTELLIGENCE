# CAREER INTELLIGENCE PLATFORM
## SYSTEM ARCHITECTURE, DEVELOPMENT AND ACCESSIBILITY BLUEPRINT

**Document Type:** Software Development and System Architecture Report  
**Project Name:** Career Intelligence  
**Development Approach:** Local-first, modular and scalable development  
**Frontend:** React, TypeScript and Vite  
**Backend:** Python and Django REST Framework  
**Database:** MariaDB  
**Intelligence Approach:** Hybrid deterministic algorithms and Artificial Intelligence  
**Initial Development Environment:** Windows 11  
**Document Status:** Official Project Development Blueprint

---

# 1. INTRODUCTION

The Career Intelligence Platform is a technology-based system designed to connect students, universities and employers through intelligent career guidance, employment opportunities and labour-market analysis.

The system will help students understand their abilities, identify suitable career paths, discover employment opportunities and develop the skills required by the job market.

It will also enable employers to identify suitable candidates and universities to understand how their academic programmes and students align with industry requirements.

The platform will use a combination of deterministic algorithms, structured data analysis and Artificial Intelligence to provide meaningful, explainable and personalised results.

A major objective of this project is to ensure that the platform is inclusive and accessible to people with different physical, sensory and technological abilities.

The system must not be designed exclusively for people who can see clearly, hear audio, use a mouse, type quickly or navigate conventional interfaces.

Accessibility, usability, data protection, reliability and explainability must remain fundamental principles throughout development.

# 2. PROJECT VISION

To develop an intelligent, inclusive and reliable career development platform that connects education, individual abilities and employment opportunities through data-driven career guidance and labour-market intelligence.

# 3. PROJECT MISSION

To empower students, universities and employers through intelligent career analysis, skills assessment, employment matching and accessible digital services.

# 4. PROJECT OBJECTIVES

The platform shall:

1. Help students identify careers that align with their education, skills, interests and abilities.
2. Match students with actual employment opportunities posted by employers.
3. Analyse job-market requirements and identify the skills employers demand.
4. Identify differences between student capabilities and industry requirements.
5. Generate personalised learning and career development recommendations.
6. Enable employers to publish vacancies, identify candidates and manage applications.
7. Enable universities to monitor student development and graduate readiness.
8. Provide universities with insights into the relationship between academic programmes and labour-market demand.
9. Use Artificial Intelligence to explain results and provide guidance without inventing calculated results.
10. Provide accessible interfaces and alternative ways of interacting with the system.
11. Protect personal information, academic records, employment information and uploaded documents.
12. Support future expansion without requiring a complete redesign of the system.

# 5. SYSTEM USERS AND PORTALS

The platform shall have three principal user portals.

## 5.1 STUDENT PORTAL

The student portal will provide students with tools to understand their career potential, improve their skills and access employment opportunities.

### Main functionalities

- Student registration and authentication.
- Personal profile management.
- Academic information and education history.
- CV upload and management.
- Academic transcript upload.
- Skill identification and assessment.
- Skill verification and evidence management.
- Career compatibility analysis.
- Career recommendations and explanations.
- Job search and job suitability analysis.
- Job application management.
- Skill-gap analysis.
- Personalised learning recommendations.
- Career development plans.
- Progress tracking.
- Notifications and alerts.
- Accessibility settings.
- Help centre and guided assistance.

### Expected outcomes

Students should be able to understand:

- Which careers align with their profiles.
- Why particular careers are recommended.
- Which skills they currently possess.
- Which skills require improvement.
- Which available vacancies match their qualifications.
- What employers expect from candidates.
- What actions they can take to improve their employment readiness.

## 5.2 EMPLOYER PORTAL

The employer portal will connect employers with students and other candidates whose capabilities align with advertised vacancies.

### Main functionalities

- Employer registration and authentication.
- Company profile management.
- Vacancy creation and management.
- Job descriptions.
- Required academic qualifications.
- Required technical and professional skills.
- Experience requirements.
- Job categories and industry classification.
- Vacancy availability and status management.
- Candidate search.
- Candidate profile viewing, subject to permissions.
- Job suitability analysis.
- Application management.
- Candidate shortlisting.
- Recruitment status updates.
- Employer demand insights.
- Notifications and alerts.
- Accessibility settings.
- Help centre and guided assistance.

### Expected outcomes

Employers should be able to:

- Advertise employment opportunities.
- Identify candidates who meet vacancy requirements.
- Compare candidate skills against job requirements.
- Understand skill availability among candidates.
- Manage applications and recruitment processes.
- Identify recurring skills gaps in the available talent pool.

The system must not automatically make discriminatory employment decisions. Employers must retain appropriate human oversight over recruitment decisions.

## 5.3 UNIVERSITY PORTAL

The university portal will help educational institutions monitor student development and understand how their programmes align with employment requirements.

### Main functionalities

- University registration and authentication.
- University profile management.
- Academic programme management.
- Department and course information.
- Student management.
- Student academic progress monitoring.
- Skills development monitoring.
- Career readiness analysis.
- Graduate readiness reports.
- Industry demand analysis.
- Skills-gap reports.
- Programme-to-industry alignment.
- Employment trend reports.
- Graduate employment tracking where appropriate and lawfully obtained.
- Notifications and alerts.
- Accessibility settings.
- Help centre and guided assistance.

### Expected outcomes

Universities should be able to understand:

- The career readiness of their students.
- The skills students possess.
- The skills employers are demanding.
- Areas where students need additional development.
- Whether academic programmes align with employment requirements.
- Which skills may require greater attention in teaching and practical training.

University users must only access student information they are authorised to view.

# 6. CORE INTELLIGENCE ENGINE

The Career Intelligence Engine is the central analytical component of the platform.

It will be developed as a collection of independent but interconnected modules.

The engine shall initially contain the following components.

## 6.1 CAREER MATCHING ENGINE

Purpose:

To determine how well a student's profile aligns with a particular career.

Inputs:

- Student skills.
- Academic qualifications.
- Education level.
- Interests.
- Verified evidence.
- Career requirements.

Outputs:

- Career compatibility score.
- Individual scoring components.
- Explanation of compatibility.
- Strengths.
- Missing information.
- Relevant skills gaps.

The compatibility score must be calculated using deterministic Python algorithms.

Missing information must not automatically be interpreted as a zero score.

The system must disclose when a result is based on incomplete student information.

## 6.2 JOB MATCHING ENGINE

Purpose:

To compare a student's profile against an actual employment vacancy.

Inputs:

- Student qualifications.
- Student skills.
- Verified evidence.
- Experience, where available.
- Vacancy description.
- Required qualifications.
- Required skills.
- Experience requirements.
- Vacancy status.

Outputs:

- Job suitability score.
- Matched requirements.
- Missing requirements.
- Skill gaps.
- Qualification alignment.
- Explanation of suitability.

Job suitability must be calculated separately from general career compatibility.

A student may be suitable for a career but not yet meet the requirements of a particular vacancy.

The system must distinguish between mandatory requirements and preferred requirements.

A student must not be incorrectly presented as meeting a mandatory qualification simply because other scoring components are strong.

## 6.3 SKILL-GAP ANALYSIS ENGINE

Purpose:

To identify the differences between existing student capabilities and required skill levels.

Inputs:

- Current student skills.
- Current skill levels.
- Required career skills.
- Required job skills.
- Target skill levels.
- Skill importance or weighting.

Outputs:

- Existing skills.
- Missing skills.
- Skills requiring improvement.
- Current skill levels.
- Target skill levels.
- Gap measurements.
- Skill development priorities.

The engine must support different skill requirements for different careers and vacancies.

## 6.4 LABOUR-MARKET INTELLIGENCE ENGINE

Purpose:

To analyse employment demand and compare employer requirements with the skills available among students and candidates.

Initial data sources:

- Vacancies published by employers on the platform.
- Employer job descriptions.
- Required qualifications.
- Required technical skills.
- Required professional skills.
- Industry classifications.
- Job categories.
- Vacancy locations.
- Vacancy status and publication dates.

Future data sources:

- External employment platforms where authorised access is available.
- Public labour-market datasets.
- Government employment reports.
- Industry research and workforce reports.

The system shall analyse:

- Frequently demanded skills.
- Skills demanded by different industries.
- Qualification requirements.
- Emerging and declining demand patterns where sufficient historical data exists.
- Skills gaps among registered students.
- Differences between employer demand and available talent.
- Industry-specific requirements.
- Geographic employment patterns where reliable location data exists.

### Important measurement rules

The system must distinguish between:

- Number of active vacancies.
- Number of employers requesting a particular skill.
- Number of vacancy records mentioning a skill.
- Number of students possessing a skill.
- Number of verified students possessing a skill.

These measurements must not be presented as interchangeable.

For example, the system must not claim that a skill is the most demanded skill in the entire country based only on a small collection of vacancies posted on the platform.

Reports must disclose the dataset size, source, geographical scope and date range.

Expired, closed and inactive vacancies must not be counted as active opportunities.

## 6.5 LEARNING RECOMMENDATION ENGINE

Purpose:

To recommend practical learning activities based on identified skill gaps and career objectives.

Inputs:

- Student's existing skills.
- Career requirements.
- Job requirements.
- Skill-gap analysis.
- Student learning progress.
- Available learning resources.

Outputs:

- Priority skills to improve.
- Suggested learning activities.
- Practical exercises.
- Suggested projects.
- Learning sequence.
- Progress indicators.

Recommendations should be realistic and related to actual requirements.

The system should distinguish between verified learning resources and general learning suggestions.

## 6.6 AI GUIDANCE ENGINE

Purpose:

To provide understandable explanations and personalised guidance using Artificial Intelligence.

AI may:

- Explain career compatibility results.
- Explain job suitability results.
- Interpret skill-gap reports.
- Suggest learning approaches.
- Explain labour-market trends.
- Help students understand career options.
- Provide conversational career guidance.
- Assist users in navigating the platform.

AI must not:

- Invent student qualifications.
- Invent student skills or achievements.
- Change deterministic compatibility scores.
- Manufacture job vacancies.
- Claim that an inactive vacancy is available.
- Guarantee employment.
- Make unsupported claims about labour-market demand.
- Override mandatory job requirements.
- Make final recruitment decisions.

AI-generated guidance must be grounded in information supplied by the backend intelligence engine.

The AI provider must be accessed through the backend. API keys must never be exposed in frontend code.

If the AI provider is unavailable, core deterministic calculations and essential portal functions should continue working.

# 7. ACCESSIBILITY AND INCLUSIVE DESIGN

Accessibility is a mandatory system requirement.

The platform must be designed to support users with visual, hearing, physical, motor and other accessibility needs.

The target is WCAG 2.2 Level AA conformance, with practical testing using assistive technologies and real users where possible.

Accessibility must be considered during component design, implementation and testing rather than added after the system is complete.

## 7.1 USERS WITH LOW VISION

The platform must support users who have difficulty reading small text or distinguishing interface elements.

Required features:

- Adjustable text sizes.
- Browser zoom support.
- High-contrast display option.
- Clear text and background contrast.
- Readable fonts.
- Adjustable spacing where practical.
- Clearly visible buttons and controls.
- Avoidance of information communicated through colour alone.
- Support for screen magnification.
- Properly labelled images and icons.
- Consistent page layouts.
- Clear focus indicators.

The interface must remain usable when enlarged without hiding essential content or forcing unnecessary horizontal scrolling.

## 7.2 BLIND USERS

The system must support users who rely on screen readers and keyboard navigation.

Required features:

- Semantic HTML.
- Proper heading hierarchy.
- Accessible form labels.
- Descriptive button names.
- Alternative text for meaningful images.
- Screen-reader-friendly notifications.
- Accessible tables and data reports.
- Keyboard navigation across all essential functions.
- Logical reading and focus order.
- Accessible menus and dialogs.
- Properly labelled form errors.
- Accessible charts with equivalent textual data descriptions.

Important information must not be available only through images, icons, charts or visual animations.

All important actions must be possible without using a mouse.

## 7.3 DEAF AND HARD-OF-HEARING USERS

The system must not depend exclusively on audio communication.

Required features:

- Captions for instructional and tutorial videos.
- Written alternatives for audio instructions.
- Text-based notifications.
- Visual alerts for important events.
- Text-based support and help options.
- Transcripts for audio-based learning content.
- Avoidance of audio-only warnings.
- Support for sign-language instructional resources where feasible.

If voice interaction is introduced, every essential voice function must have a text-based alternative.

## 7.4 USERS WITH PHYSICAL AND MOTOR DISABILITIES

The system must accommodate users who have difficulty using a mouse, keyboard, touchscreen or other conventional input devices.

Required features:

- Complete keyboard accessibility.
- Large and sufficiently spaced interactive controls.
- Clear focus indicators.
- Reduced dependence on drag-and-drop interactions.
- Alternatives to complex gestures.
- Accessible forms.
- Sufficient time to complete tasks.
- Ability to pause or extend timed interactions where appropriate.
- Compatibility with assistive input devices.
- Simple navigation.
- Avoidance of unnecessary repeated actions.

The system should support switch navigation and other assistive technologies where browser and device capabilities permit.

## 7.5 USERS WITH COGNITIVE OR LEARNING DIFFICULTIES

The platform should provide:

- Simple and understandable language.
- Clear instructions.
- Consistent page layouts.
- Step-by-step forms.
- Progress indicators.
- Explanations of technical terms.
- Clear error messages.
- Avoidance of unnecessary visual distractions.
- Ability to review information before submitting it.
- Confirmation before important or irreversible actions.

Complex career and labour-market results should be explained in understandable language.

## 7.6 ACCESSIBILITY SETTINGS

A dedicated accessibility settings area should be available across the portals.

Where practical, user preferences should include:

- Text size.
- High-contrast mode.
- Reduced motion.
- Display preferences.
- Keyboard navigation guidance.
- Screen-reader assistance instructions.
- Caption preferences for supported media.
- Simplified interface options.

Accessibility preferences should be saved for the user when authenticated and applied consistently across the platform.

Users must not be forced to disclose a disability to access accessibility features.

# 8. HELP AND GUIDED ASSISTANCE SYSTEM

The platform must support users who may not know how to operate certain features independently.

Help must be available from all three portals.

The system shall provide two main forms of assistance.

## 8.1 MANUAL HELP AND GUIDES

The platform must include a help centre containing:

- Registration instructions.
- Login instructions.
- Profile completion guides.
- CV upload instructions.
- Transcript upload instructions.
- Career analysis instructions.
- Job search instructions.
- Job application instructions.
- Employer vacancy publication instructions.
- University reporting instructions.
- Accessibility instructions.
- Account and security guidance.

Guides should use simple language, illustrations where helpful and clear step-by-step instructions.

Where videos are provided, they must include captions and text alternatives.

Guides should be searchable and organised according to the user's portal.

## 8.2 AUTOMATED ON-SCREEN GUIDANCE

The platform should include an interactive guidance system.

Examples:

- A first-time user walkthrough.
- Guided profile completion.
- Step-by-step CV upload assistance.
- Guided career analysis.
- Guided job application.
- Guided employer vacancy creation.
- Guided university reporting.

The system should explain what each important section does and what information the user needs to provide.

Guided instructions must:

- Be dismissible.
- Allow users to move backwards and forwards.
- Allow users to pause and resume where practical.
- Avoid blocking screen-reader navigation.
- Provide keyboard-accessible controls.
- Avoid relying on colour or visual highlighting alone.
- Provide a way to restart a walkthrough.
- Respect reduced-motion settings.

## 8.3 CONTEXTUAL HELP

Each major page should provide help relevant to the task currently being performed.

For example:

- The CV upload page should explain supported formats and file-size limits.
- The career results page should explain how compatibility scores are calculated.
- The job matching page should explain mandatory and preferred requirements.
- The employer vacancy form should explain how to describe skills and qualifications.
- The university reports page should explain the meaning of its indicators.

## 8.4 FUTURE ASSISTIVE HELP FEATURES

The platform may later support:

- An accessible conversational help assistant.
- Text-to-speech assistance.
- Speech-to-text input.
- Multilingual guidance.
- Sign-language learning resources.
- Human support escalation where available.

These features must supplement, not replace, accessible manual navigation and written instructions.

# 9. TECHNICAL ARCHITECTURE

The platform shall use a modular architecture.

## 9.1 FRONTEND

Technology:

- React.
- TypeScript.
- Vite.
- React Router.
- Accessible reusable interface components.

Responsibilities:

- Display the three user portals.
- Handle navigation.
- Present forms and dashboards.
- Display intelligence results.
- Provide accessibility controls.
- Present help and guided assistance.
- Communicate with backend APIs.
- Handle authentication state appropriately.

The frontend must not contain private AI API keys, database credentials or privileged administrative secrets.

## 9.2 BACKEND

Technology:

- Python.
- Django.
- Django REST Framework.

Responsibilities:

- Authentication and authorisation.
- User and role management.
- Business logic.
- Database operations.
- Document processing.
- Intelligence engine integration.
- AI provider integration.
- Job and application management.
- University reporting.
- Notifications.
- Data validation.
- Security and audit logging.

The backend must enforce permissions independently of frontend restrictions.

## 9.3 DATABASE

Technology:

- MariaDB.

The database will store structured platform information.

Expected data domains include:

- Users and roles.
- Student profiles.
- Employer profiles.
- University profiles.
- Academic programmes.
- Qualifications.
- Skills.
- Career catalogue.
- Career skill requirements.
- Job vacancies.
- Job skill requirements.
- Applications.
- Document records.
- Verified student evidence.
- Career analysis history.
- Job matching history.
- Learning recommendations.
- Labour-market analysis.
- Notifications.
- Accessibility preferences.
- Help content and guidance progress.
- Audit records.

Actual database models must be designed carefully to avoid unnecessary duplication.

Relationships, ownership and permissions must be established before implementation.

## 9.4 INTELLIGENCE ENGINE

The intelligence engine shall remain modular and independent from presentation code.

Its calculations should be testable without requiring a running React frontend or external AI service.

The engine should use structured inputs and outputs so that different Django API endpoints can reuse the same calculations.

## 9.5 AI PROVIDER

The AI provider will be accessed through a backend service.

The provider should be replaceable without rewriting the entire intelligence engine.

Provider selection, API usage, cost management, rate limits and error handling must be considered before production integration.

# 10. DOCUMENT PROCESSING

The platform will support CV and academic transcript uploads.

The processing workflow shall be:

1. User uploads a document.
2. Backend validates file size, extension and actual file content.
3. Backend checks file ownership and permissions.
4. Document is processed using an appropriate extraction method.
5. Extracted information is presented to the student.
6. Student reviews and corrects extracted information.
7. Student confirms the information.
8. Verified information becomes available to the intelligence engine.

The system must not automatically treat extracted information as confirmed academic or professional evidence.

Document storage must be private and access-controlled.

Sensitive documents must not be publicly accessible through predictable URLs.

# 11. SECURITY AND DATA PROTECTION

Security must be incorporated into every major component.

Required principles:

- Secure authentication.
- Role-based access control.
- Backend permission enforcement.
- Secure password handling.
- Protected API endpoints.
- Input validation.
- File upload security.
- Secure database credentials.
- Environment variables for secrets.
- Protection against common web vulnerabilities.
- HTTPS in production.
- Rate limiting where appropriate.
- Audit logging for sensitive actions.
- Secure session and token management.
- Appropriate backup and recovery procedures.

Student academic records and personal documents must only be accessible to authorised users.

Employers must not gain unrestricted access to all student records.

Universities must not gain unrestricted access to information outside their authorised institutional scope.

AI services must receive only the information necessary for the requested task.

Data retention, deletion, consent and access policies must be considered in accordance with applicable data protection requirements, including Kenya's Data Protection Act.

# 12. DATA QUALITY AND INTELLIGENCE RELIABILITY

All analytical results must be traceable to their underlying data.

The system must:

- Distinguish missing data from zero values.
- Handle duplicate skills consistently.
- Validate numerical skill levels.
- Record analysis dates.
- Track data completeness.
- Distinguish verified from unverified information.
- Handle expired and inactive vacancies.
- Preserve the source of labour-market information.
- Avoid misleading conclusions from small datasets.
- Make scoring methods understandable.
- Allow analysis results to be recalculated when relevant data changes.

Scores must be presented as indicators rather than guarantees of career success or employment.

# 13. API ARCHITECTURE

The following endpoints are proposed as the initial API structure. They must be reconciled with the actual Django models and existing URL structure before implementation.

### Student APIs

- GET /api/profile/
- PUT /api/profile/
- POST /api/documents/cv/
- POST /api/documents/transcript/
- GET /api/intelligence/careers/
- POST /api/intelligence/analyze/
- GET /api/intelligence/skill-gaps/
- GET /api/intelligence/learning-plan/
- GET /api/jobs/
- GET /api/jobs/{id}/
- POST /api/jobs/{id}/apply/

### Employer APIs

- GET /api/employer/profile/
- POST /api/employer/jobs/
- GET /api/employer/jobs/
- PUT /api/employer/jobs/{id}/
- GET /api/employer/applications/
- GET /api/employer/candidates/
- POST /api/employer/candidates/match/

### University APIs

- GET /api/university/profile/
- GET /api/university/students/
- GET /api/university/programmes/
- GET /api/university/reports/readiness/
- GET /api/university/reports/skills/
- GET /api/university/reports/labour-market/

### Labour-Market APIs

- GET /api/intelligence/market/overview/
- GET /api/intelligence/market/skills/
- GET /api/intelligence/market/industries/
- GET /api/intelligence/market/qualifications/
- GET /api/intelligence/market/trends/

### Help and Accessibility APIs

Where user-specific preferences or progress require persistence:

- GET /api/accessibility/preferences/
- PUT /api/accessibility/preferences/
- GET /api/help/
- GET /api/help/{id}/
- POST /api/help/progress/

These are proposed routes, not a requirement to create duplicate endpoints if equivalent functionality already exists.

# 14. DEVELOPMENT PHASES

Development shall follow a controlled sequence.

### Phase 1: Architecture and existing project review

- Confirm project structure.
- Confirm active Django settings and URL configuration.
- Confirm React frontend architecture.
- Identify existing database models.
- Establish data contracts.
- Document module responsibilities.

### Phase 2: Intelligence engine development

- Improve existing scoring functions.
- Improve missing-data handling.
- Handle duplicate and invalid inputs.
- Add automated tests.
- Add job matching.
- Add labour-market intelligence.
- Add learning recommendations.
- Validate all calculation outputs.

### Phase 3: Database and backend integration

- Design and implement the required models.
- Establish model relationships.
- Create migrations.
- Implement serializers.
- Implement API views and permissions.
- Connect the intelligence engine to the backend.
- Test APIs independently.

### Phase 4: Document processing

- Implement secure uploads.
- Implement extraction.
- Implement student review and verification.
- Connect verified information to the intelligence engine.

### Phase 5: AI integration

- Select and configure the provider.
- Secure the API key.
- Implement controlled prompt generation.
- Integrate grounded explanations.
- Add error handling and usage controls.
- Test AI outputs against calculated results.

### Phase 6: Frontend integration

- Connect the student portal.
- Connect the employer portal.
- Connect the university portal.
- Replace prototype data with backend data.
- Implement real authentication and permissions.
- Display analytical results.

### Phase 7: Accessibility and help implementation

Accessibility is developed throughout all phases, but this phase ensures full verification of:

- Screen-reader compatibility.
- Keyboard navigation.
- Visual accessibility.
- Hearing accessibility.
- Motor accessibility.
- Guided walkthroughs.
- Manual help guides.
- Contextual assistance.

### Phase 8: System testing and deployment

- Backend testing.
- Frontend testing.
- Database testing.
- API integration testing.
- Security testing.
- Accessibility testing.
- Intelligence accuracy testing.
- Cross-browser testing.
- Performance testing.
- Production deployment preparation.

# 15. TESTING AND QUALITY ASSURANCE

Every major feature must be tested before integration into the next phase.

Testing shall include:

### Functional testing

Confirm that each portal performs its intended functions.

### Intelligence testing

Confirm that career scores, job suitability scores, skill gaps and labour-market indicators are calculated correctly.

### Data validation testing

Test missing, duplicated, malformed and inconsistent information.

### Security testing

Confirm that users cannot access information outside their permissions.

### Accessibility testing

Test with:

- Keyboard-only navigation.
- Screen readers.
- Browser zoom.
- High-contrast settings.
- Reduced-motion settings.
- Captions and transcripts.
- Assistive input methods where available.

### Usability testing

Confirm that users can complete important tasks without unnecessary complexity.

Testing must include representative users with different accessibility needs wherever possible.

# 16. NON-FUNCTIONAL REQUIREMENTS

The system must aim to be:

- Accessible.
- Secure.
- Reliable.
- Maintainable.
- Scalable.
- Responsive.
- Understandable.
- Efficient.
- Modular.
- Testable.

The application should remain usable on common desktop, tablet and mobile devices.

The architecture should allow future additions without requiring a complete redesign.

# 17. STRICT ARCHITECTURAL RULES

The following rules will guide all future development.

1. The platform must retain its three main portals: Student, Employer and University.
2. Career matching, job matching and labour-market intelligence must remain distinct analytical functions.
3. Deterministic Python algorithms must calculate compatibility, suitability and analytical indicators.
4. AI must explain and support calculated results, not invent or overwrite them.
5. MariaDB remains the primary structured database unless a formally approved architectural change is made.
6. Django REST Framework remains the central backend API layer.
7. React and TypeScript remain the frontend foundation.
8. Sensitive credentials must never be placed in frontend code.
9. Existing project files and working configurations must not be overwritten without inspection.
10. Existing models must be reused where appropriate rather than duplicated.
11. Missing information must not silently become zero or be treated as verified.
12. Job-market reports must identify their sources and data coverage.
13. Expired vacancies must not be treated as active opportunities.
14. Student information must be protected by appropriate permissions.
15. Accessibility must be included in every portal and major workflow.
16. Essential operations must have accessible alternatives to mouse, audio and visual-only interaction.
17. Manual help and automated guidance must be available.
18. Core deterministic functionality must not depend entirely on an external AI service.
19. Every major component must have appropriate tests.
20. No new feature should be implemented without understanding how it affects the existing architecture.

# 18. CHANGE MANAGEMENT AND FUTURE ADDITIONS

The project is allowed to evolve.

New features, improvements and integrations may be proposed as development progresses.

However, every addition must first be evaluated against the following questions:

1. Does it support the project's main objectives?
2. Which portal or engine component does it affect?
3. Does it require new database models or fields?
4. Does it duplicate existing functionality?
5. Does it introduce security or privacy risks?
6. Does it affect accessibility?
7. Does it affect existing API contracts?
8. Does it introduce additional infrastructure or costs?
9. Can it be implemented without breaking existing functionality?
10. Can it be tested independently?

If an addition is appropriate, it should be documented and incorporated into the architecture before implementation.

If an addition changes an existing architectural decision, the relevant section of this report must be updated.

The original architecture must not be abandoned casually or changed simply because a new technology or feature becomes available.

# 19. PROJECT SUCCESS CRITERIA

The platform will be considered functionally successful when:

- Students can register and manage their profiles.
- Students can upload and verify academic and career documents.
- Students can receive explainable career recommendations.
- Students can identify their skill gaps.
- Students can find and match with actual available vacancies.
- Employers can publish and manage vacancies.
- Employers can identify and assess suitable candidates.
- Universities can monitor student career readiness.
- Universities can analyse alignment between student skills and employer demand.
- The labour-market engine can analyse platform vacancy data reliably.
- AI can explain analytical results without changing their calculated values.
- Users with visual, hearing and physical disabilities can use essential platform functions.
- Users can obtain manual or automated help when needed.
- Data is protected through appropriate authentication and authorisation.
- The system can operate locally and can be prepared for future production deployment.

# 20. CONCLUSION

The Career Intelligence Platform is intended to be more than a job portal or a career recommendation application.

It is an integrated platform connecting education, individual capabilities and employment demand.

Its success will depend on the quality of its intelligence, the reliability of its data, the usefulness of its recommendations, the security of its information and its ability to serve people with different abilities.

The development process shall therefore remain modular, structured, test-driven and aligned with this blueprint.

Every implementation decision should contribute to the same overall objective: creating an intelligent, inclusive and reliable platform that helps students develop, helps employers find talent and helps universities prepare graduates for the realities of the employment market.

**END OF PROJECT ARCHITECTURE AND DEVELOPMENT BLUEPRINT**
