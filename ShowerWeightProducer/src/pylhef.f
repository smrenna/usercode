

C*********************************************************************

C...Combine the two old-style Pythia initialization and event files
C...into a single Les Houches Event File.

      SUBROUTINE PYLHEF
 
C...Double precision and integer declarations.
      IMPLICIT DOUBLE PRECISION(A-H, O-Z)
      IMPLICIT INTEGER(I-N)
 
C...PYTHIA commonblock: only used to provide read/write units and version.
      COMMON/PYPARS/MSTP(200),PARP(200),MSTI(200),PARI(200)
      SAVE /PYPARS/
 
C...User process initialization commonblock.
      INTEGER MAXPUP
      PARAMETER (MAXPUP=100)
      INTEGER IDBMUP,PDFGUP,PDFSUP,IDWTUP,NPRUP,LPRUP
      DOUBLE PRECISION EBMUP,XSECUP,XERRUP,XMAXUP
      COMMON/HEPRUP/IDBMUP(2),EBMUP(2),PDFGUP(2),PDFSUP(2),
     &IDWTUP,NPRUP,XSECUP(MAXPUP),XERRUP(MAXPUP),XMAXUP(MAXPUP),
     &LPRUP(MAXPUP)
      SAVE /HEPRUP/
 
C...User process event common block.
      INTEGER MAXNUP
      PARAMETER (MAXNUP=500)
      INTEGER NUP,IDPRUP,IDUP,ISTUP,MOTHUP,ICOLUP
      DOUBLE PRECISION XWGTUP,SCALUP,AQEDUP,AQCDUP,PUP,VTIMUP,SPINUP
      COMMON/HEPEUP/NUP,IDPRUP,XWGTUP,SCALUP,AQEDUP,AQCDUP,IDUP(MAXNUP),
     &ISTUP(MAXNUP),MOTHUP(2,MAXNUP),ICOLUP(2,MAXNUP),PUP(5,MAXNUP),
     &VTIMUP(MAXNUP),SPINUP(MAXNUP)
      SAVE /HEPEUP/

      INTEGER IEVENT
      DATA IEVENT/0/
      SAVE IEVENT

C...Lines to read in assumed never longer than 200 characters. 
      PARAMETER (MAXLEN=200)
      CHARACTER*(MAXLEN) STRING

C...Format for reading lines.
      CHARACTER*6 STRFMT
      STRFMT='(A000)'
      WRITE(STRFMT(3:5),'(I3)') MAXLEN

C...Rewind initialization and event files. 
c      REWIND MSTP(161)
c      REWIND MSTP(162)

 51   format(i9,5i5,5e19.11,f3.0,f4.0)
 52   format(2i5,2e19.11,6i5)

C...Write header info.
      IF(IEVENT.EQ.0) THEN
      WRITE(MSTP(163),'(A)') '<LesHouchesEvents version="1.0">'
      WRITE(MSTP(163),'(A)') '<!--'
      WRITE(MSTP(163),'(A,I1,A1,I3)') 'File generated with PYTHIA ',
     &MSTP(181),'.',MSTP(182)
      WRITE(MSTP(163),'(A)') '-->'       

C...Read first line of initialization info and get number of processes.
c      READ(MSTP(161),'(A)',END=400,ERR=400) STRING                  
c      READ(STRING,*,ERR=400) IDBMUP(1),IDBMUP(2),EBMUP(1),
c     &EBMUP(2),PDFGUP(1),PDFGUP(2),PDFSUP(1),PDFSUP(2),IDWTUP,NPRUP

C...Copy initialization lines, omitting trailing blanks. 
C...Embed in <init> ... </init> block.
      WRITE(MSTP(163),'(A)') '<init>' 
C...Read first line of initialization info.
      WRITE(MSTP(163),52) IDBMUP(1),IDBMUP(2),EBMUP(1),
     &EBMUP(2),PDFGUP(1),PDFGUP(2),PDFSUP(1),PDFSUP(2),IDWTUP,NPRUP

C...Read NPRUP subsequent lines with information on each process.
      DO 120 IPR=1,NPRUP
        WRITE(MSTP(163),*) XSECUP(IPR),XERRUP(IPR),
     &  XMAXUP(IPR),LPRUP(IPR)
  120 CONTINUE
      WRITE(MSTP(163),'(A)') '</init>' 
      ELSE
        BACKSPACE(MSTP(163))
      ENDIF
C...Begin event loop. Read first line of event info or already done.
c      READ(MSTP(162),'(A)',END=320,ERR=400) STRING    
c  200 CONTINUE

C...Look at first line to know number of particles in event.
c      READ(STRING,*,ERR=400) NUP,IDPRUP,XWGTUP,SCALUP,AQEDUP,AQCDUP

C...Begin an <event> block. Copy event lines, omitting trailing blanks. 
      WRITE(MSTP(163),'(A)') '<event>' 
      WRITE(MSTP(163),*) NUP,IDPRUP,XWGTUP,SCALUP,AQEDUP,AQCDUP
      DO 240 I=1,NUP
        WRITE(MSTP(163),51) IDUP(I),ISTUP(I),
     &  MOTHUP(1,I),MOTHUP(2,I),ICOLUP(1,I),ICOLUP(2,I),
     &  (PUP(J,I),J=1,5),VTIMUP(I),SPINUP(I)
  240 CONTINUE
              

C..End the <event> block. Loop back to look for next event.
      WRITE(MSTP(163),'(A)') '</event>' 
      IEVENT=IEVENT+1
  320 WRITE(MSTP(163),'(A)') '</LesHouchesEvents>' 
      RETURN

C...Error exit.
  400 WRITE(*,*) ' PYLHEF file joining failed!'

      RETURN
      END
