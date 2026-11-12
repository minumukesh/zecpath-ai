# ============================================================
# ZECPATH AI - DAY 9
# MASTER SKILL DICTIONARY
# ============================================================

SKILL_DICTIONARY = {

    # ========================================================
    # TECHNICAL
    # ========================================================

    "technical": {

        "python": [
            "python"
        ],

        "javascript": [
            "javascript",
            "js",
            "java script"
        ],

        "java": [
            "java"
        ],

        "sql": [
            "sql"
        ],

        "excel": [
            "excel",
            "microsoft excel"
        ],

        "power bi": [
            "power bi",
            "powerbi",
            "microsoft power bi"
        ],

        "scikit-learn": [
            "scikit-learn",
            "scikit learn",
            "sklearn"
        ],

        "react": [
            "react",
            "reactjs",
            "react.js"
        ],

        "node.js": [
            "nodejs",
            "node js",
            "node.js"
        ],

        "express.js": [
            "express",
            "expressjs",
            "express.js"
        ],

        "angular": [
            "angular",
            "angularjs"
        ],

        "vue.js": [
            "vue",
            "vuejs",
            "vue.js"
        ],

        "mongodb": [
            "mongodb",
            "mongo db"
        ],

        "mysql": [
            "mysql",
            "my sql"
        ],

        "docker": [
            "docker"
        ],

        "git": [
            "git"
        ],

        "github": [
            "github",
            "git hub"
        ],

        "aws": [
            "aws",
            "amazon web services"
        ],

        "machine learning": [
            "machine learning",
            "ml"
        ],

        "deep learning": [
            "deep learning",
            "dl"
        ],

        "artificial intelligence": [
            "artificial intelligence",
            "ai"
        ],

        "data science": [
            "data science"
        ],

        "data analysis": [
            "data analysis",
            "data analytics"
        ]
    },


    # ========================================================
    # BUSINESS / NON-TECHNICAL
    # ========================================================

    "business": {

        "project management": [
            "project management"
        ],

        "communication": [
            "communication",
            "communication skills"
        ],

        "teamwork": [
            "teamwork",
            "team work"
        ],

        "problem solving": [
            "problem solving",
            "problem-solving"
        ],

        "time management": [
            "time management"
        ],

        "customer service": [
            "customer service",
            "customer support"
        ],

        "sales": [
            "sales"
        ],

        "marketing": [
            "marketing"
        ],

        "hospitality": [
            "hospitality"
        ],

        "supervision": [
            "supervision"
        ],

        "accounting": [
            "accounting"
        ],

        "revenue management": [
            "revenue management"
        ],

        "customer satisfaction": [
            "customer satisfaction"
        ],

        "data entry": [
            "data entry"
        ],

        "inventory management": [
            "inventory management"
        ],

        "auditing": [
            "auditing"
        ],

        "staffing": [
            "staffing"
        ],

        "business intelligence": [
            "business intelligence",
            "bi"
        ]
    },


    # ========================================================
    # CREATIVE
    # ========================================================

    "creative": {

        "canva": [
            "canva"
        ],

        "figma": [
            "figma"
        ],

        "graphic design": [
            "graphic design"
        ],

        "ui design": [
            "ui design",
            "user interface design"
        ],

        "ux design": [
            "ux design",
            "user experience design"
        ],

        "video editing": [
            "video editing"
        ],

        "content creation": [
            "content creation"
        ]
    }
}


# ============================================================
# TECHNOLOGY STACKS
# ============================================================

SKILL_STACKS = {

    "mern": [
        "mongodb",
        "express.js",
        "react",
        "node.js"
    ],

    "mean": [
        "mongodb",
        "express.js",
        "angular",
        "node.js"
    ],

    "lamp": [
        "linux",
        "apache",
        "mysql",
        "php"
    ],

    "mevn": [
        "mongodb",
        "express.js",
        "vue.js",
        "node.js"
    ]
}


# ============================================================
# NORMALIZATION MAP
# ============================================================

NORMALIZATION_MAP = {}

for category, skills in SKILL_DICTIONARY.items():

    for canonical_skill, aliases in skills.items():

        NORMALIZATION_MAP[
            canonical_skill.lower()
        ] = canonical_skill

        for alias in aliases:

            NORMALIZATION_MAP[
                alias.lower()
            ] = canonical_skill