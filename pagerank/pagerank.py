import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000
MARGIN = 0.001


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
    # initialize probability distribution dictionary
    distribution = {}
    # store the number of links for the page
    num_links = len(corpus[page])
    # total number of pages
    n = len(corpus)
    # calculate probability if the page has links by adding
    if num_links:  
        # probability of choosing the same page or random page         
        for p in corpus:
            distribution[p] = (1 - damping_factor) / n
        # and probability of choosing a link from the page
        for link in corpus[page]:
            distribution[link] += damping_factor / num_links
    else:
        # if the page has no links, the probability is the same to choose any other page
        for p in corpus:
            distribution[p] = 1 / n
    
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    """
    corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
    damping_factor = .85
    n = 15

    transition_model_1 = {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}
    """
    page_ranks = {page: 0 for page in corpus}
    # The first sample should be generated by choosing from a page at random
    curr_page = random.choice(list(corpus))
    page_ranks[curr_page] += 1/n

    # collect n - 1 (remaining) samples
    num_samples = n - 1
    while num_samples:
        # For each of the remaining samples, the next sample should be generated from 
        # the previous sample based on the previous sample’s transition model
        model = transition_model(corpus, curr_page, damping_factor)
        pages = list(model.keys())
        probabilities = list(model.values())
        # pick next page based on the transition model probabilities
        random_choice = random.choices(pages, probabilities)[0]
        curr_page = random_choice
        # increment the random choice
        page_ranks[curr_page] += 1/n
        num_samples -= 1
    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    n = len(corpus)
    # Begin by assigning each page a rank of 1 / N, where N is the total number of pages in the corpus.
    page_ranks = {page: 1/n for page in corpus}
    # Repeatedly calculate new rank values based on all of the current rank values
    # (i.e., calculating a page’s PageRank based on the PageRanks of all pages that link to it).
    
    def calculate_ranks(p_ranks):
        new_ranks = {}
        total_diff = 0
        for page in corpus:
            rank = (1 - damping_factor) / n
            for p, links in corpus.items():
                if page in links:
                    rank += damping_factor * p_ranks[p] / len(links)
                elif not corpus[p]:
                    # A page that has no links at all should be interpreted as having one link 
                    # for every page in the corpus (including itself).
                    rank += damping_factor * p_ranks[p] / n
            new_ranks[page] = rank
            total_diff += abs(p_ranks[page] - rank)

        if total_diff <= 0.001:
            return new_ranks
        
        return calculate_ranks(new_ranks)

    return calculate_ranks(page_ranks)


if __name__ == "__main__":
    main()
