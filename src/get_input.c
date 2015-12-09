#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*************************************************************************/
/*                                                                       */
/*  File:         get_input.c                                            */
/*                                                                       */
/*  Date:         November 2015                                          */
/*                                                                       */
/*  Description:  Read in user inputs                                    */
/*                                                                       */
/*  Inputs:       ptr_file_name  memory address of input file name       */
/*                ptr_lthr       memory address of threshold HR          */
/*                                                                       */
/*************************************************************************/

void get_input(char *ptr_file_name, float *ptr_lthr, int argc, char **argv)
{
   int r;
   int lthr_flag;
   char is_string_buffer[30];
   char *ptr_conv;
   //
   if(argc == 1)
   {
      printf("\nEnter file name : ");
      fgets(ptr_file_name, 255, stdin);

      printf("\nEnter LTHR [bpm]:");
      scanf("%f", ptr_lthr);
   }

   if(argc == 2)
   // the user entered one argument. Find out if it is digits
   {
      if(strspn(argv[1], "0123456789.") == strlen(argv[1]))
      {
         printf("string only numbers\n");
         lthr_flag = 1;
      }      
      else
      {
         printf("string has characters that are not numbers\n ");
         lthr_flag = 0;
      }
      if(lthr_flag == 0)
      {
         printf("\nEnter LTHR [bpm]:");
         scanf("%f", ptr_lthr);
         //
         strcpy(ptr_file_name, argv[1]);
      }
      else
      {
         printf("\nEnter file name : ");
         fgets(ptr_file_name, 255, stdin);
         //
         *ptr_lthr = strtol(argv[1], &ptr_conv, 10);
      }
   }
   lthr_flag = 0;
   if(argc == 3)
   // the user entered both arguments. Find out which is which
   {
      if(strspn(argv[1], "0123456789.") == strlen(argv[1]))
      {
         printf("string only numbers\n");
         lthr_flag = 1;
      }      
      if(lthr_flag == 0)
      {
         strcpy(ptr_file_name, argv[1]);
         *ptr_lthr = strtol(argv[2], &ptr_conv, 10);
      }
      if(lthr_flag == 1)
      {
         *ptr_lthr = strtol(argv[1], &ptr_conv, 10);
         strcpy(ptr_file_name, argv[2]);
      }
   } 

   printf("File name: %s\n", ptr_file_name);
   printf("LTHR     : %f\n", *ptr_lthr);


   printf("argc value in get_input: %d\n",argc);

   if(argc != 2)
   {
      // Echo the instructions for specifying a file from cmd line
      printf("To calculate stress for a file, use: '%s filename'\n", argv[0]);
      printf("For testing purposes, we will load 'TestGPX.gpx' anyway.\n");
      // *** HACK FOR TESTING *** 
      // If you run the program w/o supplying a file name, the following line
      // sets it to the test *.gpx file automatically.
      strcpy(ptr_file_name, "TestGPX.gpx");      
   }
   else
   { 
      FILE *file = fopen( argv[1], "r");
      if(file == 0) 
      {
         // If the file pointer is null, terminate the program
         printf("File not found. Terminating...\n");
        // fclose(file);
         exit(EXIT_SUCCESS);
      }
      else
      {
         strcpy(ptr_file_name,argv[1]);
      }
   } 

   printf("input file name before exiting get_input: %s\n",ptr_file_name);
/*   int input_check = 0;
    
   while (input_check == 0)
   {
      // fix this with input checking
      printf("\nEnter file name: ");
      fgets(ptr_file_name, 255, stdin);
      printf("\nFile name echo: %s", ptr_file_name);
      input_check = 1;
   }
  
   
   //
   input_check = 0;
   while (input_check == 0)
   {  
      printf("\nEnter threshold heart rate in BPM: ");
      if(scanf("%f", ptr_lthr))
      {
        //
      	if (*ptr_lthr < 50 || *ptr_lthr > 215)
      	{
      	   printf("\n!!! Please enter a reasonable LTHR !!!\n\n");
	   input_check = 0;
      	}
        else 
        {
           input_check = 1;
        }
      }
      else
      {
	printf("enter a number yo");
        input_check = 0;
        *ptr_lthr = 0;
      }
   }
*/
}

