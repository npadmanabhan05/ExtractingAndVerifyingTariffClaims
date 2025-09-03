from db.db_utils import fetch_unchecked_articles, set_assumptions, set_supported_claims, declare_as_fact_checked, fetch_economic_info
from db.vector_db import get_relevant_info
from fact_checker.embedding_creation import get_embedding
from fact_checker.assumption_verification import get_validity
import ast
import time

articles = fetch_unchecked_articles()
for article in articles:
    assumptions = []
    facts = []
    claims = article[1]
    # converts the string to an actual list
    claim_list = ast.literal_eval(claims)
    # checks each claim
    for claim in claim_list:
        embedding = get_embedding(claim)
        # gets the economic info that is most relevant to the claim
        matches = get_relevant_info(embedding)
        num_evidence = 1
        evidence = ""
        # based on ids, adds the actual text for each match to a list of evidence
        for match in matches:
            text = fetch_economic_info(match.get('id'))
            evidence += f"Source {num_evidence}: \n\n" + text + "\n\n"
            num_evidence += 1
        validity = get_validity(claim, evidence)
        if (validity == "yes"):
            facts.append(claim)
        else:
            assumptions.append(claim)
        time.sleep(5)
    num_assumptions = len(assumptions)
    num_supported_claims = len(facts)
    set_assumptions(article[0], str(assumptions), num_assumptions)
    set_supported_claims(article[0], str(facts), num_supported_claims)
    declare_as_fact_checked(article[0])
        
        




