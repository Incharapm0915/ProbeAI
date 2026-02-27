"""
questions.py — ProbeAI Local Question Bank
Zero API calls. All questions are curated locally.
"""

QUESTION_BANK = {
    "python": [
        "How does Python's GIL affect multithreading, and when would you use multiprocessing instead?",
        "Explain the difference between a generator and a list comprehension with a real use case.",
        "What are Python decorators and how have you used them in a project?",
        "How do you manage memory in a Python app processing large datasets?",
        "Describe how you would design a REST API using FastAPI or Flask.",
    ],
    "javascript": [
        "Explain the event loop and how async/await works under the hood.",
        "What is the difference between == and === and why does it matter?",
        "How do closures work in JavaScript? Give a real-world example.",
        "How would you optimize a JavaScript app with slow rendering?",
        "Explain prototypal inheritance and how it differs from classical inheritance.",
    ],
    "react": [
        "Explain the difference between useEffect and useLayoutEffect.",
        "When would you use useCallback vs useMemo and why?",
        "How do you handle global state in a large React app without Redux?",
        "How would you optimize a component that re-renders too often?",
        "Describe how React's reconciliation algorithm works.",
    ],
    "nodejs": [
        "How does Node.js handle concurrent requests with a single thread?",
        "What is the difference between process.nextTick() and setImmediate()?",
        "How do you handle errors in async Node.js code?",
        "How would you scale a Node.js app to handle high traffic?",
        "Describe how you'd implement authentication in a Node.js REST API.",
    ],
    "java": [
        "Explain the difference between HashMap and ConcurrentHashMap.",
        "How does the JVM manage memory and what causes OutOfMemoryError?",
        "Describe a Spring Boot microservice you built — what patterns did you use?",
        "What is the difference between checked and unchecked exceptions?",
        "How does Java's garbage collector work and how can you tune it?",
    ],
    "sql": [
        "Explain INNER JOIN vs LEFT JOIN vs FULL OUTER JOIN.",
        "How do database indexes work and when would you avoid using them?",
        "Describe a slow query you diagnosed and how you fixed it.",
        "What is database normalization and when would you denormalize?",
        "How do you handle database migrations without downtime?",
    ],
    "mongodb": [
        "When would you choose MongoDB over a relational database?",
        "Explain how you designed a MongoDB schema for a real project.",
        "What is an aggregation pipeline and how have you used it?",
        "How does MongoDB handle transactions and what are their limitations?",
        "Describe a performance issue you faced with MongoDB and how you solved it.",
    ],
    "docker": [
        "What is the difference between a Docker image and a container?",
        "How do you reduce Docker image size in production?",
        "Describe a multi-container setup you built using Docker Compose.",
        "How do you manage secrets and environment variables in Docker?",
        "What happens when a Docker container runs out of memory?",
    ],
    "kubernetes": [
        "What is the difference between a Deployment and a StatefulSet?",
        "How do you configure horizontal pod autoscaling?",
        "Describe a production issue you debugged in a Kubernetes cluster.",
        "How do you implement zero-downtime deployments in Kubernetes?",
        "Explain how services, ingress, and DNS work together in K8s.",
    ],
    "aws": [
        "Describe an AWS architecture you designed and the trade-offs you made.",
        "How do you implement least-privilege IAM policies?",
        "Explain the difference between SQS and SNS and when to use each.",
        "How would you design a serverless API on AWS?",
        "What steps did you take to reduce costs in an AWS project?",
    ],
    "machine learning": [
        "Walk me through an end-to-end ML pipeline you built.",
        "How do you handle class imbalance in a classification problem?",
        "Explain the bias-variance tradeoff with an example from your work.",
        "How do you ensure your model is not overfitting?",
        "Describe how you deployed an ML model to production.",
    ],
    "devops": [
        "Describe a CI/CD pipeline you built from scratch.",
        "How do you monitor a production system and respond to incidents?",
        "What infrastructure-as-code tools have you used and how?",
        "How do you manage configuration across multiple environments?",
        "What is blue-green deployment and when would you use it?",
    ],
    "typescript": [
        "What are the differences between TypeScript interfaces and type aliases?",
        "How do generics improve type safety in TypeScript?",
        "How do you handle strict null checks and what problems do they prevent?",
        "How do you type third-party libraries without TypeScript definitions?",
        "Describe how TypeScript has improved a large-scale project you worked on.",
    ],
    "golang": [
        "How do goroutines differ from OS threads and why does that matter?",
        "Explain how channels work and how you've used them for concurrency.",
        "What are idiomatic patterns for error handling in Go?",
        "What made you choose Go for a project and what limitations did you hit?",
        "Explain Go interfaces and how they differ from OOP interfaces.",
    ],
    "django": [
        "Explain Django's ORM — when do you use select_related vs prefetch_related?",
        "How does Django's middleware work and when would you write custom middleware?",
        "How do you handle authentication and permissions in Django REST Framework?",
        "How would you fix N+1 query problems in a Django app?",
        "Explain Django signals — when are they useful and when should you avoid them?",
    ],
}

ALIASES = {
    "js": "javascript", "node": "nodejs", "node.js": "nodejs",
    "express": "nodejs", "ml": "machine learning", "ai": "machine learning",
    "deep learning": "machine learning", "tensorflow": "machine learning",
    "pytorch": "machine learning", "postgres": "sql", "postgresql": "sql",
    "mysql": "sql", "sqlite": "sql", "k8s": "kubernetes",
    "fastapi": "python", "flask": "python", "springboot": "java",
    "spring": "java", "spring boot": "java", "next.js": "react",
    "nextjs": "react", "vue": "javascript", "angular": "javascript",
    "gcp": "aws", "azure": "aws", "ci/cd": "devops", "jenkins": "devops",
    "github actions": "devops", "terraform": "devops", "mongo": "mongodb",
    "ts": "typescript", "go": "golang", "dl": "machine learning",
}

FALLBACK = [
    "Describe the most complex technical problem you've solved and your approach to it.",
    "Walk me through a system you designed — what architecture decisions did you make?",
    "Tell me about a production bug you fixed. How did you find and resolve it?",
    "How do you approach learning a new technology or framework quickly?",
]


def get_questions(tech_stack: str, n_per_tech: int = 2) -> list[dict]:
    """Return n_per_tech questions per detected technology. Zero API calls."""
    tokens = [t.strip().lower() for t in tech_stack.replace(",", " ").split()]
    phrases = [f"{tokens[i]} {tokens[i+1]}" for i in range(len(tokens) - 1)] + tokens

    matched = {}
    for p in phrases:
        key = ALIASES.get(p, p)
        if key in QUESTION_BANK and key not in matched:
            matched[key] = key.title()

    results = []
    for key, label in list(matched.items())[:5]:
        for q in QUESTION_BANK[key][:n_per_tech]:
            results.append({"tech": label, "question": q})

    if not results:
        for q in FALLBACK:
            results.append({"tech": "General", "question": q})

    return results