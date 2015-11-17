#include <stdio.h>
#include <string.h>

char* strip_leading_spaces(char *input);

/*************************************************************************/
/*                                                                       */
/*  File:         parse_file_line.c                                      */
/*                                                                       */
/*  Date:         November 2015                                          */
/*                                                                       */
/*  Description:  Parse the input *.gpx file, looking for HR data after  */
/*                each <time> tag.                                       */
/*                                                                       */
/*  Inputs:       ptr_lthr        memory address of threshold HR         */
/*                                                                       */
/*************************************************************************/

int parse_file_line(char *ptr_file_name)
{
   FILE *fp;
   char individual_line;
   char buffer[256];
   size_t len;
   char *ptr_b;
   int counter = 1;
   char buffer_nw[256];

   // Open the *test* input file
   fp = fopen("./TestGPX.gpx", "r");
   
   printf("Reading file...\n");
//   while(fgets(buffer, 256, fp))
   while(counter < 200)
   {
      // Read the first string into the buffer, echo result
      fgets(buffer, 256, fp);
      printf("Line: %d, %s",counter,buffer);

      // Strip leading spaces, echo result
      strip_leading_spaces(buffer);
      printf("Line: %d, %s\n",counter,buffer);

      counter++;
   }
   fclose(fp);

   return(0);
}

char* strip_leading_spaces(char *input)
{
   int i,j;

   i = 0;
   j = 0;

   while(input[i] != '\0')
   {
      if(input[i] != ' ')
      {
         input[j++] = input[i];
      }
      i++;
   }
   input[j] = '\0';
   return(input);
}
