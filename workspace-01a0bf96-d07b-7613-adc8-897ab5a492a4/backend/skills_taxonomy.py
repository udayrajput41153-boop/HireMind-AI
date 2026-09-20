"""
Curated skill taxonomy: canonical skill -> aliases + category.
Used by the offline extraction path and to NORMALIZE the output of the
LLM-based Resume/Job agents so matching is consistent either way.
"""

SKILLS = {
    # --- Languages ---
    "python":      {"aliases": ["py", "python3"], "category": "Language"},
    "java":        {"aliases": ["java 8", "java 11", "java 17", "jdk"], "category": "Language"},
    "javascript":  {"aliases": ["js", "es6", "ecmascript", "vanilla js"], "category": "Language"},
    "typescript":  {"aliases": ["ts"], "category": "Language"},
    "c++":         {"aliases": ["cpp", "c plus plus"], "category": "Language"},
    "c":           {"aliases": ["c language", "c programming"], "category": "Language"},
    "c#":          {"aliases": ["csharp", "c-sharp", "c sharp", ".net c#"], "category": "Language"},
    "go":          {"aliases": ["golang"], "category": "Language"},
    "rust":        {"aliases": [], "category": "Language"},
    "kotlin":      {"aliases": [], "category": "Language"},
    "swift":       {"aliases": [], "category": "Language"},
    "r":           {"aliases": ["r lang", "r programming", "r studio"], "category": "Language"},
    "scala":       {"aliases": [], "category": "Language"},
    "php":         {"aliases": [], "category": "Language"},
    "ruby":        {"aliases": ["ruby on rails", "rails"], "category": "Language"},
    "sql":         {"aliases": ["mysql queries", "t-sql", "pl/sql", "structured query language"], "category": "Language"},
    "bash":        {"aliases": ["shell scripting", "shell", "linux scripting"], "category": "Language"},

    # --- Frontend ---
    "react":         {"aliases": ["react.js", "reactjs", "react js"], "category": "Frontend"},
    "next.js":       {"aliases": ["nextjs", "next js"], "category": "Frontend"},
    "angular":       {"aliases": ["angularjs", "angular.js"], "category": "Frontend"},
    "vue":           {"aliases": ["vue.js", "vuejs"], "category": "Frontend"},
    "svelte":        {"aliases": ["sveltekit"], "category": "Frontend"},
    "html":          {"aliases": ["html5"], "category": "Frontend"},
    "css":           {"aliases": ["css3"], "category": "Frontend"},
    "tailwind":      {"aliases": ["tailwind css", "tailwindcss"], "category": "Frontend"},
    "bootstrap":     {"aliases": [], "category": "Frontend"},
    "redux":         {"aliases": ["redux toolkit", "react redux"], "category": "Frontend"},
    "sass":          {"aliases": ["scss"], "category": "Frontend"},
    "material ui":   {"aliases": ["mui", "material-ui"], "category": "Frontend"},
    "webpack":       {"aliases": [], "category": "Frontend"},
    "vite":          {"aliases": [], "category": "Frontend"},

    # --- Backend ---
    "node.js":       {"aliases": ["node", "nodejs", "node js"], "category": "Backend"},
    "express":       {"aliases": ["express.js", "expressjs"], "category": "Backend"},
    "django":        {"aliases": [], "category": "Backend"},
    "flask":         {"aliases": [], "category": "Backend"},
    "fastapi":       {"aliases": ["fast api"], "category": "Backend"},
    "spring boot":   {"aliases": ["springboot", "spring", "spring framework"], "category": "Backend"},
    "graphql":       {"aliases": [], "category": "Backend"},
    "rest api":      {"aliases": ["rest", "rest apis", "restful", "restful api", "restful apis", "rest api design", "api development"], "category": "Backend"},
    "microservices": {"aliases": ["microservice", "micro-services", "microservice architecture"], "category": "Backend"},
    "grpc":          {"aliases": [], "category": "Backend"},
    "celery":        {"aliases": [], "category": "Backend"},
    "django rest framework": {"aliases": ["drf"], "category": "Backend"},

    # --- Data / ML / AI ---
    "machine learning":   {"aliases": ["ml", "classical ml", "ml algorithms", "statistical learning"], "category": "Data & ML"},
    "deep learning":      {"aliases": ["dl", "neural networks", "neural network", "deep neural networks"], "category": "Data & ML"},
    "pytorch":            {"aliases": ["torch"], "category": "Data & ML"},
    "tensorflow":         {"aliases": ["tf", "tf 2", "tensorflow 2"], "category": "Data & ML"},
    "keras":              {"aliases": [], "category": "Data & ML"},
    "scikit-learn":       {"aliases": ["sklearn", "scikit learn", "scikitlearn"], "category": "Data & ML"},
    "xgboost":            {"aliases": ["xgb"], "category": "Data & ML"},
    "lightgbm":           {"aliases": [], "category": "Data & ML"},
    "nlp":                {"aliases": ["natural language processing", "text analytics", "natural-language-processing"], "category": "Data & ML"},
    "computer vision":    {"aliases": ["cv", "opencv", "image processing"], "category": "Data & ML"},
    "llm":                {"aliases": ["llms", "large language models", "large language model", "genai", "generative ai", "generativeai", "prompt engineering", "langchain", "rag"], "category": "Data & ML"},
    "transformers":       {"aliases": ["hugging face", "huggingface", "bert", "attention models"], "category": "Data & ML"},
    "pandas":             {"aliases": ["pandas dataframe"], "category": "Data & ML"},
    "numpy":              {"aliases": [], "category": "Data & ML"},
    "data analysis":      {"aliases": ["data analytics", "exploratory data analysis", "eda", "data wrangling"], "category": "Data & ML"},
    "data visualization": {"aliases": ["data viz", "dataviz", "visualisation"], "category": "Data & ML"},
    "statistics":         {"aliases": ["statistical analysis", "statistical modeling", "statistical modelling", "hypothesis testing", "probability"], "category": "Data & ML"},
    "a/b testing":        {"aliases": ["ab testing", "a b testing", "experimentation"], "category": "Data & ML"},
    "feature engineering":{"aliases": [], "category": "Data & ML"},
    "spark":              {"aliases": ["apache spark", "pyspark"], "category": "Data & ML"},
    "hadoop":             {"aliases": [], "category": "Data & ML"},
    "airflow":            {"aliases": ["apache airflow"], "category": "Data & ML"},
    "etl":                {"aliases": ["data pipelines", "data pipeline", "elt"], "category": "Data & ML"},
    "data engineering":   {"aliases": ["data warehouse", "data warehousing", "data modeling"], "category": "Data & ML"},
    "recommendation systems": {"aliases": ["recommender systems", "collaborative filtering"], "category": "Data & ML"},

    # --- BI tools ---
    "tableau":   {"aliases": ["tableau dashboards"], "category": "BI & Analytics"},
    "power bi":  {"aliases": ["powerbi", "power-bi"], "category": "BI & Analytics"},
    "looker":    {"aliases": [], "category": "BI & Analytics"},
    "excel":     {"aliases": ["ms excel", "microsoft excel", "advanced excel", "spreadsheets", "excel macros", "vba"], "category": "BI & Analytics"},
    "google analytics": {"aliases": ["ga4"], "category": "BI & Analytics"},

    # --- Databases ---
    "postgresql": {"aliases": ["postgres", "postgre sql"], "category": "Database"},
    "mysql":      {"aliases": ["mariadb"], "category": "Database"},
    "mongodb":    {"aliases": ["mongo", "mongo db"], "category": "Database"},
    "redis":      {"aliases": [], "category": "Database"},
    "elasticsearch": {"aliases": ["elastic search", "elastic"], "category": "Database"},
    "sqlite":     {"aliases": [], "category": "Database"},
    "snowflake":  {"aliases": [], "category": "Database"},
    "bigquery":   {"aliases": ["big query"], "category": "Database"},
    "cassandra":  {"aliases": [], "category": "Database"},
    "dynamodb":   {"aliases": ["dynamo db"], "category": "Database"},
    "oracle":     {"aliases": ["oracle db"], "category": "Database"},

    # --- DevOps / Cloud ---
    "aws":            {"aliases": ["amazon web services", "amazon aws"], "category": "Cloud & DevOps"},
    "azure":          {"aliases": ["microsoft azure"], "category": "Cloud & DevOps"},
    "gcp":            {"aliases": ["google cloud", "google cloud platform"], "category": "Cloud & DevOps"},
    "docker":         {"aliases": ["docker containers", "containerization", "containerisation"], "category": "Cloud & DevOps"},
    "kubernetes":     {"aliases": ["k8s"], "category": "Cloud & DevOps"},
    "terraform":      {"aliases": ["terraform iac", "iac"], "category": "Cloud & DevOps"},
    "ansible":        {"aliases": [], "category": "Cloud & DevOps"},
    "jenkins":        {"aliases": [], "category": "Cloud & DevOps"},
    "ci/cd":          {"aliases": ["cicd", "ci cd", "continuous integration", "continuous deployment", "continuous delivery", "github actions", "gitlab ci"], "category": "Cloud & DevOps"},
    "linux":          {"aliases": ["ubuntu", "unix", "debian", "centos"], "category": "Cloud & DevOps"},
    "git":            {"aliases": ["github", "gitlab", "bitbucket", "version control"], "category": "Cloud & DevOps"},
    "nginx":          {"aliases": [], "category": "Cloud & DevOps"},
    "prometheus":     {"aliases": ["grafana", "monitoring"], "category": "Cloud & DevOps"},
    "serverless":     {"aliases": ["lambda", "aws lambda", "cloud functions"], "category": "Cloud & DevOps"},
    "sagemaker":      {"aliases": ["aws sagemaker"], "category": "Cloud & DevOps"},
    "kafka":          {"aliases": ["apache kafka"], "category": "Cloud & DevOps"},
    "rabbitmq":       {"aliases": [], "category": "Cloud & DevOps"},

    # --- Mobile ---
    "android":    {"aliases": ["android sdk", "android development", "android studio"], "category": "Mobile"},
    "ios":        {"aliases": ["ios development", "xcode"], "category": "Mobile"},
    "flutter":    {"aliases": ["dart"], "category": "Mobile"},
    "react native": {"aliases": ["react-native"], "category": "Mobile"},

    # --- Testing / QA ---
    "selenium":   {"aliases": ["selenium webdriver"], "category": "Testing"},
    "cypress":    {"aliases": [], "category": "Testing"},
    "jest":       {"aliases": [], "category": "Testing"},
    "junit":      {"aliases": ["testng"], "category": "Testing"},
    "postman":    {"aliases": ["api testing"], "category": "Testing"},
    "playwright": {"aliases": [], "category": "Testing"},
    "manual testing": {"aliases": ["qa", "quality assurance", "test cases"], "category": "Testing"},

    # --- Tools & practices ---
    "agile":          {"aliases": ["scrum", "kanban", "agile methodologies", "sprint planning"], "category": "Practice"},
    "jira":           {"aliases": [], "category": "Practice"},
    "system design":  {"aliases": ["distributed systems", "scalable systems", "architecture design", "high level design"], "category": "Practice"},
    "object oriented programming": {"aliases": ["oop", "oops", "object-oriented programming", "object oriented design"], "category": "Practice"},
    "data structures": {"aliases": ["dsa", "algorithms", "data structures and algorithms"], "category": "Practice"},
    "communication":  {"aliases": ["communication skills", "stakeholder management", "presentation skills"], "category": "Soft skill"},
    "leadership":     {"aliases": ["team leadership", "mentoring", "team management", "people management"], "category": "Soft skill"},
    "problem solving": {"aliases": ["analytical skills", "critical thinking", "analytical thinking"], "category": "Soft skill"},
    "project management": {"aliases": ["program management", "delivery management"], "category": "Practice"},
}

# Build alias -> canonical lookup (built once)
_ALIAS_MAP = {}
for canon, meta in SKILLS.items():
    _ALIAS_MAP[canon.lower()] = canon
    for a in meta["aliases"]:
        _ALIAS_MAP[a.lower()] = canon


def canonicalize(term):
    """Return canonical skill name for a term, or None if unknown."""
    if not term:
        return None
    t = term.strip().lower()
    if t in _ALIAS_MAP:
        return _ALIAS_MAP[t]
    return None


def all_terms():
    """All known terms (canonical + aliases) for substring scanning."""
    return _ALIAS_MAP


def category_of(canon):
    return SKILLS.get(canon, {}).get("category", "Other")
