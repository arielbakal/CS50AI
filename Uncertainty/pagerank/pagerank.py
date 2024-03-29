import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    res = {}

    # Calculate the probability for choosing a random page
    random_prob = (1 / len(corpus)) * (1 - damping_factor)

    # Assign the probability for the current page
    res[page] = random_prob

    # Calculate the probability for choosing a linked page
    if len(corpus[page]) == 0:
        linked_prob = 0
    else:
        linked_prob = (1 / len(corpus[page])) * damping_factor

    # Assign the probability for each linked page
    for linked_page in corpus[page]:
        res[linked_page] = linked_prob + random_prob

    # Assign the probability for all other pages
    for other_page in corpus:
        if other_page not in corpus[page]:
            res[other_page] = random_prob

    # prob_sum = sum([res[i] for i in res])
    # print(res)
    # print("prob sum =",prob_sum)

    return res

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize return var copying corpus keys with 0 as values
    res = {page: 0 for page in corpus}

    # First sampling
    sample = random.choice(list(corpus.keys()))
    res[sample] += 1

    # Remaining n-1 samples
    for _ in range(n-1):
        model = transition_model(corpus, sample, damping_factor)
        model_keys = list(model.keys())
        model_weights = [model[i] for i in model]
        sample = random.choices(model_keys, model_weights, k=1)[0]

        res[sample] += 1

    # Normalize the values
    for item in res:
        res[item] /= n

    # prob_sum = sum([res[i] for i in res])
    # print(res)
    # print("prob sum =", prob_sum)

    return res

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize pagerank values with 1/n
    res = {page: 1/len(corpus) for page in corpus}
    
    # Initialize differences of pagerank_n with pagerank_n+1
    differences = {page: 1/len(corpus) for page in corpus}

    # Iterate formula
    while max(differences.values()) >= 0.001: 
        for p in res.keys():
            temp_diff = res[p] 

            pages_linked_to_p = pages_linked_to(corpus, p)

            linked_pages_sum = 0

            for i in pages_linked_to_p:
                if len(corpus[i]) == 0:
                    linked_pages_sum += res[i] / len(corpus) 
                else:
                    linked_pages_sum += res[i] / len(corpus[i])
                
            res[p] = ( (1-damping_factor) / len(corpus) ) + (damping_factor * linked_pages_sum)

            differences[p] = abs(temp_diff - res[p]) 
        # print("diff =", max(differences.values()))

    # prob_sum = sum([res[i] for i in res])
    # print(res)
    # print("prob sum =", prob_sum)

    return res

def pages_linked_to(corpus, page):

    res = corpus[page]

    if not res:  
        res = list(corpus.keys())  
    else:
        res = [p for p in corpus if page in corpus[p]]

    return res

if __name__ == "__main__":
    main()
