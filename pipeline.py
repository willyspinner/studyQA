from transformers import pipeline

from search import search

nlp = pipeline('question-answering')
def simple_qa_pipeline(question_string):
    """
    Similar to facebook's drQA, we use a document search engine (in this case ,using Okapi BM25)
    that narrows the search space to a few documents using the search query. Then, we use the document
    as the context to feed into our extractive QA model (in this case, pretrained on SQuaD).

    """
    results = search(question_string)
    if len(results) == 0:
        print("No results")
        return
    with open(results[0]['filepath']) as f:
        context = f.read()
    qa_result = nlp(question=question_string, context=context)
    return qa_result




