import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    SUM = 0
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
        SUM += ranks[page]
    print(SUM)
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    SUM = 0
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
        SUM += ranks[page]
    print(SUM)


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

    newPR = dict()

    # if multiple links on page
    if len(corpus[page]) == 0:
        # no links on page
        probability = 1 / len(corpus)
        for page in corpus:
            newPR[page] = probability

        return newPR
    
    elif len(corpus[page]) != 1:
        links = list(corpus[page])
        probability = damping_factor / len(links)
        for link in links:
            newPR[link] = probability
        
    elif len(corpus[page]) == 1:
        # if only 1 link on page
        for links in corpus[page]:
            newPR[links] = damping_factor


    randomProbability = (1 - damping_factor) / len(corpus)
    # assigns 1 - damping_factor probability across all pages
    for page in corpus:
        if page not in newPR:
            newPR[page] = randomProbability
        else:
            newPR[page] = newPR[page] + randomProbability

    return newPR

    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # create new dict 
    random.seed(123)

    newDict = dict()
    for page in corpus.keys():
        newDict[page] = 0

    nextPage = None
    for i in range(n):
        if i == 0:
            allPages = list(corpus.keys())
            nextPage = random.choice(allPages)
            newDict[nextPage] += 1
        else:
            # pick next page
            links = transition_model(corpus, nextPage, damping_factor)
            pages = list(links.keys())
            probabilities = list(links.values())
            nextPage = random.choices(pages, probabilities)
            nextPage = nextPage[0]
            newDict[nextPage] += 1

    # converts number of sample that landed on that page to decimal / sample size
    for page in newDict:
        newDict[page] = (newDict[page] / n)

    return newDict

    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pageRank = dict()
    # populate dict with all sites in corpus
    # start by assigning all key values to 1/N, N being no of sites in corpus
    probability = 1 / len(corpus)
    for page in corpus.keys():
        pageRank[page] = probability

    DIFFERENCE = 0.001
    while True:
        toContinue = False
        copyPageRank = copy.deepcopy(pageRank)
        for page in pageRank:
            firstCondition = (1 - damping_factor) / len(corpus)
            sum = 0
            # check all websites in corpus for links to current page
            for links in corpus:
                if page in corpus[links]:
                    sum += copyPageRank[links] / len(corpus[links])
                elif len(corpus[links]) == 0:
                    sum += copyPageRank[links] / len(corpus)
            sum = sum * damping_factor
            newPageRank = sum + firstCondition

            # check for difference
            checkDifference = pageRank[page] - newPageRank
            if abs(checkDifference) > DIFFERENCE:
                toContinue = True

            # update pagerank value for current page
            pageRank[page] = newPageRank
        # if difference is bigger than 0.001 loop again across all pages.
        if toContinue == False:
            break

    return pageRank
    raise NotImplementedError


if __name__ == "__main__":
    main()
