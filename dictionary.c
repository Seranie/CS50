// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

//function prototype
void hashDictionary(void);
void deleteHash(node *tmp);
unsigned int size(void);

// TODO: Choose number of buckets in hash table
int N;
FILE* dic;

// Hash table
node** table;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    //hash word
    long tmp_hash_key = hash(word);
    //look at hashed dictionary for existnece of word
    if(table[tmp_hash_key] != 0)
    {
        node* tmp_ptr = table[tmp_hash_key];
        while(tmp_ptr != NULL)
        {
            if(strcasecmp(tmp_ptr->word, word) == 0)
            {
                return true;
            }
            else
            {
                tmp_ptr = tmp_ptr->next;
            }
        }
        return false;
    }
    else
    {
        return false;
    }
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int hash_base = 5381;
    int hash_key = 0;
    for(int i = 0; i < strlen(word); i++)
    {
        if(isalpha(word[i]) != 0)
        {
            hash_key += (hash_base << 5) + hash_base + tolower(word[i]);
        }
    }
    hash_key %= N;
    return hash_key;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    dic = fopen(dictionary, "r");
    if(dic == NULL)
    {
        return false;
    }
    else
    {
        N = size();
        table = calloc(N, sizeof(table));
        if(table == NULL)
        {
            return false;
        }
        hashDictionary();
        return true;
    }
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    int no_of_words = 0;
    //read file char by char into arr, while also counting no of words
    char wordBuffer[LENGTH + 2];
    while(fgets(wordBuffer, (LENGTH + 2), dic) != NULL)
    {
        no_of_words++;
    }
    fseek(dic, 0, SEEK_SET);
    return no_of_words;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    if(fclose(dic) == 0)
    {
        for (int k = 0; k < N; k++)
        {
            deleteHash(table[k]);
        }
        free(table);
        return true;
    }
    else
    {
        for (int k = 0; k < N; k++)
        {
            deleteHash(table[k]);
        }
        free(table);
        return false;
    }
}


void hashDictionary(void)
{
    char wordBuffer[LENGTH + 2] = {0};
    while(fgets(wordBuffer, (LENGTH + 2), dic) != NULL)
    {
        node* tmp = malloc(sizeof(node));
        if(tmp == NULL)
        {
            return;
        }
        int tmpHashKey = hash(wordBuffer);
        int len = strlen(wordBuffer);
        if(len > 0 && wordBuffer[(len - 1)] == '\n')
        {
            wordBuffer[len - 1] = '\0';
        }
        strcpy(tmp->word, wordBuffer);
        memset(wordBuffer, 0, sizeof(char) * (LENGTH + 1));
        if(table[tmpHashKey] == 0)
        {
            tmp->next = NULL;
            table[tmpHashKey] = tmp;
        }
        else
        {
            tmp->next = table[tmpHashKey];
            table[tmpHashKey] = tmp;
        }
    }
    fseek(dic, 0, SEEK_SET);
}


void deleteHash(node* tmp)
{
    node* test_Ptr = NULL;
    test_Ptr = tmp;
    if(test_Ptr == 0 || test_Ptr == NULL)
    {
        return;
    }
    else
    {
        if(test_Ptr->next == NULL)
        {
            free(test_Ptr);
        }
        else
        {
            deleteHash(test_Ptr->next);
            free(test_Ptr);
        }
        return;
    }
}