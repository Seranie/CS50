#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int average = 0;
    RGBTRIPLE result;
    for(int i = 0; i < height; i++)
    {
        for(int k = 0; k < width; k++)
        {
            average = round((float)(image[i][k].rgbtRed + image[i][k].rgbtGreen + image[i][k].rgbtBlue) / 3);
            if(average != image[i][k].rgbtRed || average != image[i][k].rgbtBlue || average != image[i][k].rgbtGreen)
            {
                result.rgbtRed = average;
                result.rgbtGreen = average;
                result.rgbtBlue = average;
                image[i][k] = result;
            }

        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp;
        for(int i = 0; i < height; i++)
        {
            if(width % 2 != 0)
            {
                for(int k = 0; k < (width - 1)  / 2; k++)
                {
                    if(k != (width- 1 / 2))
                    {
                        temp = image[i][k];
                        image[i][k] = image[i][width - 1 - k];
                        image[i][width - 1 - k] = temp;
                    }
                }
            }
            else
            {
                for(int j = 0; j < width / 2; j++)
                {
                    temp = image[i][j];
                    image[i][j] = image[i][width - 1 - j];
                    image[i][width - 1 - j] = temp;
                }
            }
        }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height * width];
    int temp_counter = 0;
    for(int i = 0; i < height; i++)
    {
        for(int k = 0; k < width; k++)
        {
            RGBTRIPLE sum;
            float red = 0, green = 0, blue = 0;
            int counter = 0;
            for(int j = i - 1; j <= i + 1; j++)
            {
                for(int l = k - 1; l <= k + 1; l++)
                {
                    if((j >= 0 && j < height) && (l >= 0 && l < width))
                    {
                        red += image[j][l].rgbtRed;
                        blue += image[j][l].rgbtBlue;
                        green += image[j][l].rgbtGreen;
                        counter++;
                    }
                }
            }
            sum.rgbtRed = round(red / counter);
            sum.rgbtBlue = round(blue / counter);
            sum.rgbtGreen = round(green / counter);
            temp[temp_counter] = sum;
            temp_counter++;
        }
    }
    int anotherCounter = 0;
    for(int a = 0; a < height; a++)
    {
        for(int x = 0; x < width; x++)
        {
            image[a][x] = temp[anotherCounter];
            anotherCounter++;
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    int gy[9] = {-1, -2, -1, 0, 0, 0, 1, 2, 1};
    int gx[9] = {-1, 0, 1, -2, 0, 2, -1, 0, 1};
    RGBTRIPLE temp[height * width];
    int temp_counter = 0;
    //target initial pixel
    for(int i = 0; i < height; i++)
    {
        for(int k = 0; k < width; k++)
        {
            int redGx = 0, blueGx = 0, greenGx = 0;
            int redGy = 0, blueGy = 0, greenGy = 0;
            int counter = 0;
            //target surrounding 3x3 pixels
            for(int j = i - 1; j <= i + 1; j++)
            {
                for(int l = k - 1; l <= k + 1; l++)
                {
                    //check if within boundary
                    if((j >= 0 && j < height) && (l >=0 && l < width))
                    {
                        //assign matrix to channel values
                        redGx += image[j][l].rgbtRed * gx[counter];
                        blueGx += image[j][l].rgbtBlue * gx[counter];
                        greenGx += image[j][l].rgbtGreen * gx[counter];
                        redGy += image[j][l].rgbtRed * gy[counter];
                        blueGy += image[j][l].rgbtBlue * gy[counter];
                        greenGy += image[j][l].rgbtGreen * gy[counter];
                        counter++;
                    }
                    else
                    {
                        counter++;
                    }
                }
            }
            //adds both matrix values
            int newRed = round(sqrt((float)(redGx * redGx) + (redGy * redGy)));
            int newBlue = round(sqrt((float)(blueGx * blueGx) + (blueGy * blueGy)));
            int newGreen = round(sqrt((float)(greenGx * greenGx) + (greenGy * greenGy)));
            //checks if sum give more than 255 and caps it
            if(newRed > 255)
            {
                newRed = 255;
            }
            if(newBlue > 255)
            {
                newBlue = 255;
            }
            if(newGreen > 255)
            {
                newGreen = 255;
            }
            temp[temp_counter].rgbtRed = newRed;
            temp[temp_counter].rgbtBlue = newBlue;
            temp[temp_counter].rgbtGreen = newGreen;
            temp_counter++;
        }
    }
    int anotherCounter = 0;
    for(int a = 0; a < height; a++)
    {
        for(int z = 0; z < width; z++)
        {
            image[a][z] = temp[anotherCounter];
            anotherCounter++;
        }
    }


    return;
}
