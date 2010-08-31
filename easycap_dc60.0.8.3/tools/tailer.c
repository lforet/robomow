/*****************************************************************************
*                                                                            *
*  tailer.c                                                                  *
*                                                                            *
*                                                                            *
*                                                                            *
*  Usage:  tailer                                                            *
*                                                                            *
*         reads from   /var/log/kern.log                                     *
*                 or   /var/log/messages                                     *
*         writes to    /tmp/tail                                             *
*                                                                            *
*****************************************************************************/
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

#define BFSZ ( 512 * 1024 )
#define   OUTFNM  "/tmp/tail"
#define WHOLE_LOG
#if defined(WHOLE_LOG)
#define   TARGET  "====easycap===="
#else
#define   TARGET  "====OPEN===="
#endif /*WHOLE_LOG*/


char logfnm[8][64] = \
  {
  "/var/log/kern.log",
  "/var/log/messages",
  ""
  };

int main(int,char**);
/****************************************************************************/
/****************************************************************************/
/****************************************************************************/
int
main (int argc, char *argv[])
{
static size_t starget;
int i, otarget;
FILE *pfilog, *pfiout;
char bf[BFSZ + 2], *p1;

starget = strlen( TARGET );
otarget = (int) starget;

if ((FILE *)NULL == (pfiout = fopen( OUTFNM, "w" )))
  {
  fprintf(stderr, "ERROR: Cannot open initial output file: %s\n", OUTFNM );
  return(-1);
  }
pfilog = (FILE *)NULL;
for ( i = 0;  i < 8;  i++ )
  {
  p1 = &logfnm[i][0];  if ( ! *p1 ) break;
  if ((FILE *)NULL != (pfilog = fopen( &logfnm[i][0], "r" ))) break;
  }
if ((FILE *)NULL == pfilog )
  {
  fprintf(stderr, "ERROR: Could not open any log file for reading\n" );
  return(-1);
  }
/*---------------------------------------------------------------------------*/
bf[BFSZ - 2] = 0;
while ((char *)NULL != fgets( &bf[0], BFSZ, pfilog ))
  {
  if ( bf[BFSZ - 2] )
    {
    fprintf(stderr, "ERROR:  buffer overflow\n");
    return(-1);
    }

  p1 = &bf[0];
  while ( *p1 )
    {
    if ( &bf[ otarget ] <= p1 )
      {
      if ( ! memcmp( ( p1 - otarget ), TARGET, starget ) )
        {
        if ((FILE *)NULL == pfiout )
          {
          fprintf(stderr, "ERROR: Null pointer to old output file: %s\n", \
                                                                   OUTFNM );
          return(-1);
          }
        if ( fclose( pfiout ))
          {
          fprintf(stderr, "ERROR: Cannot close old output file: %s\n", OUTFNM);
          return(-1);
          }
        if ((FILE *)NULL == (pfiout = fopen( OUTFNM, "w" )))
          {
          fprintf(stderr, "ERROR: Cannot open new output file: %s\n", OUTFNM );
          return(-1);
          }
        break;
        }
      }
    p1++;
    }

  if ( EOF == fputs( &bf[0], pfiout ))
    {
    fprintf(stderr, "ERROR:  Failed to write to file: %s\n", OUTFNM );
    return(-1);
    }
  }
/*---------------------------------------------------------------------------*/
if ( ! feof( pfilog ))
  {
  fprintf(stderr, "ERROR: failed to read entire log file\n");
  }
if ((FILE *)NULL != pfilog )
  {
  if ( fclose( pfilog ))
    {
    fprintf(stderr, "ERROR: Cannot close log file\n");
    return(-1);
    }
  }
if ((FILE *)NULL != pfiout )
  {
  if ( fclose( pfiout ))
    {
    fprintf(stderr, "ERROR: Cannot close final output file: %s\n", OUTFNM );
    return(-1);
    }
  }
return(0);
}
/****************************************************************************/
