import csv
import itertools
import sys
import random

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    def passGene(person):
                probability = None
                match person:
                    case 0:
                        probability = PROBS["mutation"]
                    case 1:
                        probability = 0.5 - PROBS["mutation"]
                    case 2:
                        probability = 1 - PROBS["mutation"]
                return probability

    def doesntPassGene(person):
        probability = None
        match person:
            case 0:
                probability = 1 - PROBS["mutation"]
            case 1:
                probability = 0.5 - PROBS["mutation"]
            case 2:
                probability = PROBS["mutation"]
        return probability

    Probabilites = dict()

    for person in people:
        mother = people[person]['mother']
        father = people[person]['father']
        parents = dict()
        parents[mother] = None
        parents[father] = None
        # number of genes parents have
        for parent in parents:
            if parent in two_genes:
                parents[parent] = 2
            elif parent in one_gene:
                parents[parent] = 1
            else:
                parents[parent] = 0

        # NO GENES
        if person not in one_gene and person not in two_genes:
            # if no parents
            if people[person]['mother'] == None:
                probability = PROBS["gene"][0]
                if person not in have_trait:
                    Probabilites[person] = probability * PROBS["trait"][0][False]
                elif person in have_trait:
                    Probabilites[person] = probability * PROBS['trait'][0][True]
            else:
                # if have parents
                motherProbability = doesntPassGene(parents[mother])
                fatherProbability = doesntPassGene(parents[father])
                probability = fatherProbability * motherProbability
                if person not in have_trait:
                    Probabilites[person] = probability * PROBS["trait"][0][False]
                else:
                    Probabilites[person] = probability * PROBS["trait"][0][True]

        # ONE GENE
        if person in one_gene:
            if people[person]['mother'] == None:
                probability = PROBS["gene"][1]
                if person not in have_trait:
                    Probabilites[person] = probability * PROBS["trait"][1][False]
                elif person in have_trait:
                    Probabilites[person] = probability * PROBS['trait'][1][True]
            else:
                # if have parents
                motherProbability = passGene(parents[mother])
                fatherProbability = doesntPassGene(parents[father])
                probability = fatherProbability * motherProbability
                motherProbability = doesntPassGene(parents[mother])
                fatherProbability = passGene(parents[father])
                probability += motherProbability * fatherProbability
                if person not in have_trait:
                    Probabilites[person] = probability * PROBS["trait"][1][False]
                else:
                    Probabilites[person] = probability * PROBS["trait"][1][True]


        if person in two_genes:
            if people[person]['mother'] == None:
                probability = PROBS["gene"][2]
                if person not in have_trait:
                    Probabilites[person] = probability * PROBS["trait"][2][False]
                elif person in have_trait:
                    Probabilites[person] = probability * PROBS['trait'][2][True]
            else:
                # if have parents
                motherProbability = passGene(parents[mother])
                fatherProbability = passGene(parents[father])
                probability = fatherProbability * motherProbability
                if person not in have_trait:
                    Probabilites[person] = probability * PROBS["trait"][2][False]
                else:
                    Probabilites[person] = probability * PROBS["trait"][2][True]
    joint = 1
    for probability in Probabilites.values():
        joint *= probability

    return joint
    raise NotImplementedError


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in two_genes:
            probabilities[person]['gene'][2] += p
        elif person in one_gene:
            probabilities[person]['gene'][1] += p
        else:
            probabilities[person]['gene'][0] += p
        
        if person in have_trait:
            probabilities[person]['trait'][True] += p
        else:
            probabilities[person]['trait'][False] += p
    
    return

    raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for person in probabilities:
        Sum1 = sum(probabilities[person]['gene'].values())
        Sum2 = sum(probabilities[person]['trait'].values())
        for key in probabilities[person]['gene']:
            if probabilities[person]['gene'][key] != 0:
                probabilities[person]['gene'][key] /= Sum1
        for key in probabilities[person]['trait']:
            if probabilities[person]['trait'][key] != 0:
                probabilities[person]['trait'][key] /= Sum2

    return
    raise NotImplementedError


if __name__ == "__main__":
    main()
