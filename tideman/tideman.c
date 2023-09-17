#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);
bool recursionshit(int initialWinner, int loser);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);


            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for(int i = 0; i < candidate_count; i++)
    {
        //Checks if candidates name exists
        if(strcmp(name, candidates[i]) == 0)
        {
            //add candidates index to rank chart
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for(int i = 0; i < candidate_count; i++)
    {
        for(int k = i; k < candidate_count; k++)
        {
            if(i != k)
            {
            preferences[ranks[i]][ranks[k]] = preferences[ranks[i]][ranks[k]] + 1;
            }
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    int counter = 0;
    for(int i = 0; i < candidate_count; i++)
    {
        for(int k = candidate_count - 1; k > i; k--)
        {
            if(preferences[i][k] > preferences[k][i])
            {
                pairs[counter].winner = i;
                pairs[counter].loser = k;
                counter++;
            }
            else if (preferences[k][i] > preferences[i][k])
            {
                pairs[counter].winner = k;
                pairs[counter].loser = i;
                counter++;
            }
        }
    }
    pair_count = counter;
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    int x = 0;
    int y = 0;
    int strength[pair_count];
    for(int i = 0; i < pair_count; i++)
    {
        x = pairs[i].winner;
        y = pairs[i].loser;
        strength[i] = preferences[x][y] - preferences[y][x];
    }
    int counter = 0;
    for(int j = 0; j < pair_count - 1; j++)
    {
        int highest = j;
        for(int k = 0 + j; k < pair_count; k++)
        {
            if(strength[k] > strength[highest])
            {
                highest = k;
            }
        }
        if(highest != j)
        {
            int swap = strength[counter];
            strength[counter] = strength[highest];
            strength[highest] = swap;

            pair swapForPairs = pairs[counter];
            pairs[counter] = pairs[highest];
            pairs[highest] = swapForPairs;
            counter++;
        }
    }
    return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
   for(int i = 0; i < pair_count; i++)
   {
    //goes through each pair, checking if they create cycle, if they dont, execute the locked function.
        if(recursionshit(pairs[i].winner, pairs[i].loser) == false)
        {
            locked[pairs[i].winner][pairs[i].loser] = true;
        }
   }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    bool loser[candidate_count];
    int counter = 0;
    for(int k = 0; k < candidate_count; k++)
    {
        for(int j = 0; j < candidate_count; j++)
        {
            if(locked[j][k] == true)
            {
                loser[k] = true;
                counter++;
            }
        }
    }
    for(int i = 0; i < candidate_count; i++)
    {
        if(loser[i] == false)
        {
            printf("%s\n", candidates[i]);
        }
    }
    return;
}


bool recursionshit(int initialWinner, int loser)
{
    //if winner of the pair that is being checked is == to the loser in the recursion, return true;
    if(loser == initialWinner)
    {
        return true;
    }
    else
    {
        bool result = false;
        for(int i = 0; i < candidate_count; i++)
        {
            //check if loser has won over anybody before
            if(locked[loser][i] == true)
            {
                //check if loser has won over the initial winner before.
                if(i == initialWinner)
                {
                    return true;
                }
                //else check the loser of this losing pair...until it finds a pair where loser has won over initial winner.
                //if not then return false
                if(recursionshit(initialWinner, i) == true)
                {
                    result = true;
                }
            }
        }
        return result;
    }
}