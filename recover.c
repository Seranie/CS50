#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if(argc != 2)
    {
        printf("Use as such: ./recover file_name");
        return 1;
    }

    char *filename = argv[1];

    FILE *file = fopen(filename, "r");

    if(file == NULL)
    {
        printf("Invalid File");
        return 1;
    }

    int BLOCK_SIZE = 512;
    BYTE BUFFER[BLOCK_SIZE];
    int counter = 0;
    char *string_buffer = malloc(sizeof(char) * 8);
    FILE *output = NULL;

    while(fread(BUFFER, sizeof(BYTE), 512, file) == 512)
    {
            if(BUFFER[0] == 0xff && BUFFER[1] == 0xd8 && BUFFER[2] == 0xff && (BUFFER[3] & 0xf0) == 0xe0)
            {
                if(output != NULL)
                {
                    fclose(output);
                }
                sprintf(string_buffer, "%03i.jpg", counter);
                output = fopen(string_buffer, "w");
                if(output == NULL)
                {
                    printf("File error\n");
                    return 1;
                }
                fwrite(BUFFER, sizeof(BUFFER), 1, output);
                counter++;
            }
            else if(output != NULL)
            {
                fwrite(BUFFER, sizeof(BUFFER), 1, output);
            }
            else
            {
                continue;
            }

    }

    fclose(output);
    fclose(file);
    free(string_buffer);
}