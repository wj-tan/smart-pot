#include <stdlib.h>
#include <string.h>
#include <stdio.h>

char * get_string() {

        char theString[]= "Last updated at ";

        char *myString = malloc ( sizeof(char) * (strlen(theString)) +1 );

        strcpy(myString, theString);

        return myString;
}
