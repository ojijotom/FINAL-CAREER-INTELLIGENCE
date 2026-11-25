
import re


SKILL_ALIASES = {
    "C Programming": ["c programming", "c language", "programming in c"],
    "C++": ["c++", "cpp"],
    "Cloud Computing": ["cloud computing", "cloud services", "aws", "azure", "gcp"],
    "Communication": ["communication", "communication skills", "verbal communication"],
    "Critical Thinking": ["critical thinking", "analytical thinking"],
    "CSS": ["css", "css3"],
    "Cybersecurity": ["cybersecurity", "cyber security", "information security"],
    "Data Analysis": ["data analysis", "data analytics", "analysing data", "analyzing data"],
    "Data Visualization": ["data visualization", "data visualisation", "visualization"],
    "Database Design": ["database design", "database modelling", "database modeling"],
    "Django": ["django"],
    "Git": ["git", "version control"],
    "HTML": ["html", "html5"],
    "Java": ["java", "java programming", "java language"],
    "JavaScript": ["javascript", "js programming"],
    "Linux": ["linux", "ubuntu", "unix"],
    "Machine Learning": ["machine learning", "ml models"],
    "MySQL": ["mysql"],
    "Networking": ["networking", "computer networks", "network administration"],
    "PHP": ["php"],
    "Problem Solving": ["problem solving", "problem-solving"],
    "Python": ["python", "python programming"],
    "React": ["react", "react.js", "reactjs"],
    "SQL": ["sql", "structured query language"],
    "Teamwork": ["teamwork", "team work", "collaboration"],
}


def _find_evidence(text, start, end, window=100):
    """Return a short excerpt surrounding a detected skill."""
    left = max(0, start - window)
    right = min(len(text), end + window)

    excerpt = text[left:right].strip()
    excerpt = re.sub(r"\s+", " ", excerpt)

    return excerpt[:250]


def extract_skills(text, catalogue):
    """
    Match document text against the existing skills catalogue.

    Only catalogue skills are returned.
    Proficiency and verification are not assigned.
    """
    if not text:
        return []

    normalized_text = text.lower()
    results = []

    for skill in catalogue:
        aliases = SKILL_ALIASES.get(
            skill.name,
            [skill.name.lower()],
        )

        matches = []

        for alias in aliases:
            alias = alias.lower().strip()

            pattern = (
                r"(?<!\w)"
                + re.escape(alias)
                + r"(?!\w)"
            )

            match = re.search(pattern, normalized_text)

            if match:
                matches.append(
                    (match.start(), match.end(), alias)
                )

        if matches:
            start, end, matched_alias = min(
                matches,
                key=lambda item: item[0],
            )

            results.append({
                "skill": skill,
                "matched_alias": matched_alias,
                "evidence": _find_evidence(text, start, end),
            })

    return results
