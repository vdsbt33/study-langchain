from langchain_typesafe import Choice, Noul, Score, TypeSafeClassifier, classifier

classifier = TypeSafeClassifier()

response = classifier.invoke(
    {
        "state": (
            "The deploy failed twice and customers are seeing 500 errors."
            "Can someone look now?"
        ),
        "questions": {
            "urgent": Noul(instructions="Does this need attention right now?"),
            "team": Choice(
                instructions="Which team should pick this up?",
                criteria={
                    "infra": "Deploys, availability and on-call incidents.",
                    "billing": "Payments, invoices and subscriptions.",
                },
            ),
            "severity": Score(
                instructions="How severe is the impact?",
                criteria=["Cosmetic", "Degraded for some users", "Full outage"]
            ),
        },
    }
)

print(response)
