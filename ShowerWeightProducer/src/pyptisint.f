C*********************************************************************
 
C...PYPTIS
C...Generates pT-ordered spacelike initial-state parton showers and
C...trial joinings.
C...MODE=-1: Initialize ISR from scratch, starting from the hardest
C...         interaction initiators at PT2NOW.
C...MODE= 0: Generate a trial branching on interaction MINT(36), side
C...         MINT(30). Start evolution at PT2NOW, solve Sudakov for PT2.
C...         Store in /PYISMX/ if PT2 is largest so far. Abort if PT2
C...         is below PT2CUT.
C...         (Also generate test joinings if MSTP(96)=1.)
C...MODE= 1: Accept stored shower branching. Update event record etc.
C...PT2NOW : Starting (max) PT2 scale for evolution.
C...PT2CUT : Lower limit for evolution.
C...PT2    : Result of evolution. Generated PT2 for trial emission.
C...IFAIL  : Status return code. IFAIL=0 when all is well.
 
      SUBROUTINE PYPTISINT(MODE,PT2NOW,PT2CUT,PT2,IFAIL)
 
C...Double precision and integer declarations.
c      IMPLICIT DOUBLE PRECISION(A-H, O-Z)
c      IMPLICIT INTEGER(I-N)
      IMPLICIT NONE
      INTEGER MODE,IFAIL
      REAL*8 PT2NOW,PT2CUT,PT2
      INTEGER PYCOMP
      REAL*8 PYR,PYMASS,PYANGL
C...Parameter statement for maximum size of showers.
c      PARAMETER (MAXNUR=1000)
C...Commonblocks.
C...User process event common block.
      INTEGER MAXNUP
      PARAMETER (MAXNUP=500)
      INTEGER NUP,IDPRUP,IDUP,ISTUP,MOTHUP,ICOLUP
      DOUBLE PRECISION XWGTUP,SCALUP,AQEDUP,AQCDUP,PUP,VTIMUP,SPINUP
      COMMON/HEPEUP/NUP,IDPRUP,XWGTUP,SCALUP,AQEDUP,AQCDUP,IDUP(MAXNUP),
     &ISTUP(MAXNUP),MOTHUP(2,MAXNUP),ICOLUP(2,MAXNUP),PUP(5,MAXNUP),
     &VTIMUP(MAXNUP),SPINUP(MAXNUP)
      SAVE /HEPEUP/

C...User process initialization commonblock.
      INTEGER MAXPUP
      PARAMETER (MAXPUP=100)
      INTEGER IDBMUP,PDFGUP,PDFSUP,IDWTUP,NPRUP,LPRUP
      DOUBLE PRECISION EBMUP,XSECUP,XERRUP,XMAXUP
      COMMON/HEPRUP/IDBMUP(2),EBMUP(2),PDFGUP(2),PDFSUP(2),
     &IDWTUP,NPRUP,XSECUP(MAXPUP),XERRUP(MAXPUP),XMAXUP(MAXPUP),
     &LPRUP(MAXPUP)
      SAVE /HEPRUP/

c      COMMON/PYPART/NPART,NPARTD,IPART(MAXNUR),PTPART(MAXNUR)
      INTEGER N,NPAD,K
      REAL*8 P,V
      COMMON/PYJETS/N,NPAD,K(4000,5),P(4000,5),V(4000,5)
      INTEGER MSTU,MSTJ
      REAL*8 PARU,PARJ
      COMMON/PYDAT1/MSTU(200),PARU(200),MSTJ(200),PARJ(200)
      INTEGER KCHG
      REAL*8 PMAS,PARF,VCKM
      COMMON/PYDAT2/KCHG(500,4),PMAS(500,4),PARF(2000),VCKM(4,4)
      INTEGER MSTP,MSTI
      REAL*8 PARP,PARI
      COMMON/PYPARS/MSTP(200),PARP(200),MSTI(200),PARI(200)
      INTEGER MINT
      REAL*8 VINT
      COMMON/PYINT1/MINT(400),VINT(400)

c      COMMON/PYINT2/ISET(500),KFPR(500,2),COEF(500,20),ICOL(40,4,2)
      INTEGER KFIVAL,NMI,IMI,NVC,IMISEP
      REAL*8 XASSOC,XPSVC,PVCTOT,XMI,PT2MI
      COMMON/PYINTM/KFIVAL(2,3),NMI(2),IMI(2,800,2),NVC(2,-6:6),
     &     XASSOC(2,-6:6,240),XPSVC(-6:6,-1:240),PVCTOT(2,-1:1),
     &     XMI(2,240),PT2MI(240),IMISEP(0:240)
      INTEGER MIMX,JSMX,KFLAMX,KFLCMX,KFBEAM,NISGEN
      REAL*8 PT2MX,PT2AMX,ZMX,RM2CMX,Q2BMX,PHIMX
      COMMON/PYISMX/MIMX,JSMX,KFLAMX,KFLCMX,KFBEAM(2),NISGEN(2,240),
     &     PT2MX,PT2AMX,ZMX,RM2CMX,Q2BMX,PHIMX
c      COMMON/PYCTAG/NCT,MCT(4000,2)
c      COMMON/PYISJN/MJN1MX,MJN2MX,MJOIND(2,240)
c      SAVE /PYPART/,/PYJETS/,/PYDAT1/,/PYDAT2/,/PYPARS/,/PYINT1/,
      SAVE /PYJETS/,/PYDAT1/,/PYDAT2/,/PYPARS/,/PYINT1/,
     &     /PYINTM/,/PYISMX/
C...Local variables

      REAL*8 WTDERIV(-2:2),VALINT(-2:2,0:1),VALILO(-2:2,0:1)
      REAL*8 VALIHI(-2:2,0:1),VALILU(-2:2,0:1),VALILD(-2:2,0:1)
      REAL*8 VALINTS(-2:2),VALILOS(-2:2)
      REAL*8 VALIHIS(-2:2),VALILUS(-2:2),VALILDS(-2:2)
      REAL*8 FR(2)
      REAL*8 RNUMDRV5,FAC,PTCUTR0,PTSTEP0
      REAL*8 RMB,RMB2,RMC,RMC2,ALAM3,ALAM4,ALAM5,ALAM2,RM2C,PT2ADJ
      REAL*8 TMIN,PTEMAX,WTEMAX,XMXC,FMQ,ZMXCR,SHAT
      REAL*8 RMQ2,XFSUM,PT20,XQ0,XG0,TPM0
      REAL*8 PTCUTR,PT2CUTR,PT2MNE,B0,PTSTEP,ZMIN,ZMAX
      REAL*8 RMIN,RMAX,WPDF0,WTAPE,WTFF,WTGF,WTAPQ,WTGG,WTFG
      REAL*8 RML,TPL,TPM,TML,WN,XFBO
      REAL*8 WTSUM,WTSUMS,PT2RAT,PT2JAC,ALF,WTRAN,WTZ
      REAL*8 WTZP,ZJACOBP,XFANP,WTPDF1,WTPDF2
      REAL*8 ZJACOB,Z,ZFAC,Q2B,SIDE,BETAX,BETAZ,SDIP,PTCHK,WTEXTRA
      REAL*8 TEMP,PTTMP,XFBN,XFAN,XA,XB,XFBNV,XFANV
      REAL*8 WTDIP,WTTOT,WTTOTV,WTDIPHI,WTDIPLO,WTLAMU,WTLAMD
      REAL*8 THETA
      INTEGER IDIP,IFS,I1,IM,IMAX,IMIN,IR,IS,ISUB,IT,II,JDIP,JS,JJ
      INTEGER KFL,KFLA,KFLAA,KFLB,KFLBA,KFLC,KFLCB,KSVCB,MCRQQ,MCTAG
      INTEGER MECOR,MI,MJOIN,MJOIND,MQMASS,MSIDE,MSTP67,NDIP,NJN,NPASS
      INTEGER NTRY
      INTEGER IKNT
      INTEGER IPTINT,IZINT,IZ
      REAL*8 XX(20),WW(20)
      REAL*8 PTRAND,WTI,ZRAND,WTIZ,DELZ
      DATA IKNT/0/
      SAVE IKNT
      LOGICAL IWRITE
      DATA IWRITE/.FALSE./
      SAVE IWRITE
      

      REAL*8 ZSAV(2,240),PT2SAV(2,240),
     &     XFB(-25:25),XFA(-25:25),XFN(-25:25),
     &     WTAP(-25:25),WTPDF(-25:25),SHTNOW(240)
      SAVE ZSAV,PT2SAV,XFB,XFA,XFN,WTAP,WTPDF,XMXC,SHTNOW,
     &     RMB2,RMC2,ALAM3,ALAM4,ALAM5,TMIN,PTEMAX,WTEMAX
      SAVE XX,WW
C...For check on excessive weights.
c      CHARACTER CHWT*12
 
C...Only give errors for very large weights, otherwise just warnings
      DATA WTEMAX /1.5D0/
C...Only give errors for large pT, otherwise just warnings
      DATA PTEMAX /5D0/
 
      IFAIL=-1
  
C----------------------------------------------------------------------
C...MODE=-1: Initialize initial state showers from scratch, i.e.
C...starting from the hardest interaction initiators.
      IF (MODE.EQ.-1) THEN
        IF(IKNT.EQ.0) THEN
          CALL GAULEG(0D0,1D0,XX,WW,20)
        ENDIF
        IKNT=IKNT+1
C...Set hard scattering SHAT.
        VINT(44)=(PUP(4,1)+PUP(4,2))**2-(PUP(3,1)+PUP(3,2))**2-
     $    (PUP(2,1)+PUP(2,2))**2-(PUP(1,1)+PUP(1,2))**2
        SHTNOW(1)=VINT(44)
C...Mass thresholds and Lambda for QCD evolution.
c        AEM2PI=PARU(101)/PARU(2)
        RMB=PMAS(5,1)
        RMC=PMAS(4,1)
        ALAM4=PARP(61)
        IF(MSTU(112).LT.4) ALAM4=PARP(61)*(PARP(61)/RMC)**(2D0/25D0)
        IF(MSTU(112).GT.4) ALAM4=PARP(61)*(RMB/PARP(61))**(2D0/25D0)
        ALAM5=ALAM4*(ALAM4/RMB)**(2D0/23D0)
        ALAM3=ALAM4*(RMC/ALAM4)**(2D0/27D0)
C...Optionally use Lambda_MC = Lambda_CMW 
        IF (MSTP(64).EQ.3) THEN
          ALAM5 = ALAM5 * 1.569D0
          ALAM4 = ALAM4 * 1.618D0
          ALAM3 = ALAM3 * 1.661D0 
        ENDIF
        RMB2=RMB**2
        RMC2=RMC**2
C...Massive quark forced creation threshold (in M**2).
        TMIN=1.01D0
C...Set upper limit for X (ensures some X left for beam remnant).
        VINT(1)=EBMUP(1)+EBMUP(2)
        MINT(1)=-1
        XMXC=1D0-2D0*PARP(111)/VINT(1)
        VINT(143)=1D0
        VINT(144)=1D0
        VINT(41)=PUP(4,1)/EBMUP(1)
        VINT(42)=PUP(4,2)/EBMUP(2)
c        VINT(55)=SCALUP
c        VINT(56)=VINT(55)**2
        MINT(103)=IDUP(1)
        MINT(104)=IDUP(2)
        KFBEAM(1)=2212
        KFBEAM(2)=2212
 
        IF (MSTP(61).GE.1) THEN
C...Initial values: flavours, momenta, virtualities.
          DO 100 JS=1,2
            NISGEN(JS,1)=0
            NMI(JS)=0
C...Special kinematics check for c/b quarks (that g -> c cbar or
C...b bbar kinematically possible).
            IMI(JS,1,1)=JS
            KFLB=IDUP(JS)
            IF(ABS(KFLB).LE.6) THEN
              NVC(JS,KFLB)=0
            ELSE
              NVC(JS,0)=0
            ENDIF
            DO II=-5,5
              IF(II.NE.0) NVC(JS,II)=0
            ENDDO
            XMI(JS,1)=VINT(40+JS)
            KFLCB=IABS(KFLB)
            IF(KFBEAM(JS).NE.22.AND.(KFLCB.EQ.4.OR.KFLCB.EQ.5)) THEN
C...Check PT2MAX > mQ^2
              IF (VINT(56).LT.1.05D0*PMAS(PYCOMP(KFLCB),1)**2) THEN
                CALL PYERRM(9,'(PYPTIS:) PT2MAX < 1.05 * MQ**2. '//
     &               'No Q creation possible.')
                MINT(51)=1
                RETURN
              ELSE
C...Check for physical z values (m == MQ / sqrt(s))
C...For creation diagram, x < z < (1-m)/(1+m(1-m))
                FMQ=PMAS(KFLCB,1)/SQRT(SHTNOW(1))
                ZMXCR=(1D0-FMQ)/(1D0+FMQ*(1D0-FMQ))
                IF (XMI(JS,1).GT.0.9D0*ZMXCR) THEN
                  CALL PYERRM(9,'(PYPTIS:) No physical z value for '//
     &                 'Q creation.')
                  MINT(51)=1
                  RETURN
                ENDIF
              ENDIF
            ENDIF
  100     CONTINUE
        ENDIF
 
        MINT(354)=0
        MINT(35)=1
 
C----------------------------------------------------------------------
C...MODE= 0: Generate a trial branching on interaction MINT(36) side
C...MINT(30). Store if emission PT2 scale is largest so far.
C...Also generate test joinings if MSTP(96)=1.
      ELSEIF(MODE.EQ.0) THEN
        IFAIL=-1
        MECOR=0
        ISUB=MINT(1)
        JS=MINT(30)
C...No shower for structureless beam
        IF (MINT(44+JS).EQ.1) RETURN
        MI=MINT(36)
        SHAT=VINT(44)
C...Absolute shower max scale = VINT(56)
        IF (MSTP(67).NE.0) THEN
          PT2 = MIN(PT2NOW,VINT(56))
        ELSE
C...For MSTP(67)=0, adjust starting scale by PARP(67)
          PT2=MIN(PT2NOW,PARP(67)*VINT(56))
        ENDIF
        IF (NISGEN(1,MI).EQ.0.AND.NISGEN(2,MI).EQ.0) SHTNOW(MI)=SHAT
C...Define for which processes ME corrections have been implemented.
        IF(MSTP(68).EQ.1.OR.MSTP(68).EQ.3) THEN
          IF(ISUB.EQ.1.OR.ISUB.EQ.2.OR.ISUB.EQ.141.OR.ISUB.EQ
     &         .142.OR.ISUB.EQ.144) MECOR=1
          IF(ISUB.EQ.102.OR.ISUB.EQ.152.OR.ISUB.EQ.157) MECOR=2
          IF(ISUB.EQ.3.OR.ISUB.EQ.151.OR.ISUB.EQ.156) MECOR=3
C...Calculate preweighting factor for ME-corrected processes.
          IF(MECOR.GE.1) CALL PYMEMX(MECOR,WTFF,WTGF,WTFG,WTGG)
        ENDIF
C...Basic info on daughter for which to find mother.
        KFLB=IDUP(JS)
        KFLBA=IABS(KFLB)
C...KSVCB: -1 for sea or first companion, 0 for valence or gluon, >1 for
C...second companion.
CCCC        KSVCB=MAX(-1,IMI(JS,MI,2))


C...Treat "first" companion of a pair like an ordinary sea quark
C...(except that creation diagram is not allowed)
c        IF(IMI(JS,MI,2).GT.IMISEP(MI)) KSVCB=-1
C...X (rescaled to [0,1])
        XB=XMI(JS,MI)/VINT(142+JS)
C...Massive quarks (use physical masses.)
        RMQ2=0D0
        MQMASS=0
c$$$        IF (KFLBA.EQ.4.OR.KFLBA.EQ.5) THEN
c$$$          RMQ2=RMC2
c$$$          IF (KFLBA.EQ.5) RMQ2=RMB2
c$$$C...Special threshold treatment for non-photon beams
c$$$          IF (KFBEAM(JS).NE.22) MQMASS=KFLBA
c$$$C...Check that not below mass threshold.
c$$$          IF(MQMASS.GT.0.AND.PT2.LT.TMIN*RMQ2) THEN
c$$$            CALL PYERRM(9,'(PYPTIS:) PT2 < 1.01 * MQ**2. '//
c$$$     &        'No Q creation possible.')
c$$$            MINT(51)=1
c$$$C...Special return code if failing before any evolution at all: bad event
c$$$            IF (NISGEN(1,MI).EQ.0.AND.NISGEN(2,MI).EQ.0) MINT(51)=2
c$$$            RETURN
c$$$          ENDIF
c$$$
c$$$        ENDIF
 
C...Flags for parton distribution calls.
        MINT(105)=MINT(102+JS)
        MINT(109)=MINT(106+JS)
        VINT(120)=VINT(2+JS)

C.......Okay, assume p-p collisions
        IF(KFLB.EQ.1.OR.KFLB.EQ.2) THEN
          KSVCB=0
        ELSEIF(KFLBA.NE.21) THEN
          KSVCB=-1
        ELSE
          KSVCB=0
        ENDIF

C...Calculate initial parton distribution weights.
        IF(XB.GE.XMXC) THEN
          RETURN
        ELSEIF(MQMASS.EQ.0) THEN
          CALL PYPDFU(KFBEAM(JS),XB,PT2,XFB)
          IF( KFLB.EQ.1 .OR. KFLB.EQ.2 ) THEN
            XFSUM=XPSVC(KFLB,0)+XPSVC(KFLB,-1)
            KSVCB=0
            IF(PYR(0)*XFSUM.GT.XPSVC(KFLB,0)) KSVCB=-1
CMRENNA...TEMP
            KSVCB=0
c            WTFRAC=XFSUM/XPSVC(KFLB,KSVCB)
          ENDIF

        ELSE
C...Initialize massive quark PT2 dependent pdf underestimate.
          PT20=PT2
          CALL PYPDFU(KFBEAM(JS),XB,PT20,XFB)
          IF( KFLB.EQ.1 .OR. KFLB.EQ.2 ) THEN
            XFSUM=XPSVC(KFLB,0)+XPSVC(KFLB,-1)
            KSVCB=0
            IF(PYR(0)*XFSUM.GT.XPSVC(KFLB,0)) KSVCB=-1
          ENDIF
C.!.Tentative treatment of massive valence quarks.
          XQ0=MAX(1D-10,XPSVC(KFLB,KSVCB))
          XG0=XFB(21)
          TPM0=LOG(PT20/RMQ2)
          WPDF0=TPM0*XG0/XQ0
        ENDIF
cc        IF (KFLBA.LE.6) THEN
C...For quarks, only include respective sea, val, or cmp part.
C
cc          IF (KSVCB.LE.0) THEN
cc            XFB(KFLB)=XPSVC(KFLB,KSVCB)
cc          ELSE
C...Find companion's companion
C             MISEA=0
C   120       MISEA=MISEA+1
C             IF (IMI(JS,MISEA,2).NE.IMI(JS,MI,1)) GOTO 120
C             XS=XMI(JS,MISEA)
C             XREM=VINT(142+JS)
C             YS=XS/(XREM+XS)
C C...Momentum fraction of the companion quark.
C C...Rescale from XB = x/XREM to YB = x/(1-Sum_rest) -> factor (1-YS).
C             YB=XB*(1D0-YS)
C             XFB(KFLB)=PYFCMP(YB/VINT(140),YS/VINT(140),MSTP(87))
cc          ENDIF
cc        ENDIF


        PT2CUTR=PT2CUT
        PTCUTR=SQRT(PT2CUTR)
C.......make this a formula to handle larger pT?
        PTSTEP=2D0
        PT2CUT=MAX((PTCUTR-3D0*PTSTEP)**2,PT2CUTR/4D0)

C...Determine overestimated z range: switch at c and b masses.
  130   IF (PT2.GT.TMIN*RMB2) THEN
c          IZRG=3
          PT2MNE=MAX(TMIN*RMB2,PT2CUT)
          B0=23D0/6D0
          ALAM2=ALAM5**2
        ELSEIF(PT2.GT.TMIN*RMC2) THEN
c          IZRG=2
          PT2MNE=MAX(TMIN*RMC2,PT2CUT)
          B0=25D0/6D0
          ALAM2=ALAM4**2
        ELSE
c          IZRG=1
          PT2MNE=PT2CUT
          B0=27D0/6D0
          ALAM2=ALAM3**2
        ENDIF
C...Divide Lambda by PARP(64) (equivalent to mult pT2 by PARP(64))
        ALAM2=ALAM2/PARP(64)
C...Overestimated ZMAX:
        IF (MQMASS.EQ.0) THEN
C...Massless
          ZMAX=1D0-0.5D0*(PT2MNE/SHTNOW(MI))*(SQRT(1D0+4D0*SHTNOW(MI)
     &         /PT2MNE)-1D0)
        ELSE
C...Massive (limit for bremsstrahlung diagram > creation)
          FMQ=SQRT(RMQ2/SHTNOW(MI))
          ZMAX=1D0/(1D0+FMQ)
        ENDIF
        ZMIN=XB/XMXC
 
C...If kinematically impossible then do not evolve.
        IF(PT2.LT.PT2CUT.OR.ZMAX.LE.ZMIN) THEN
          DO II=391,400
            VINT(II)=1D0
          ENDDO
          RETURN
        ENDIF
 
C...Reset Altarelli-Parisi and PDF weights.
        DO 140 KFL=-5,5
          WTAP(KFL)=0D0
          WTPDF(KFL)=0D0
  140   CONTINUE
        WTAP(21)=0D0
        WTPDF(21)=0D0
C...Zero joining weights and compute X(partner) and X(mother) values.
        NJN=0
        IF (MSTP(96).NE.0) THEN
          print*,' did not expect to get here '
        ENDIF
 
C...Approximate Altarelli-Parisi weights (integrated AP dz).
C...q -> q, g -> q or q -> q + gamma (already set which).
        IF(KFLBA.LE.5) THEN
C...Val and cmp quarks get an extra sqrt(z) to smooth their bumps.
          IF (KSVCB.LT.0) THEN
            WTAP(KFLB)=(8D0/3D0)*LOG((1D0-ZMIN)/(1D0-ZMAX))
          ELSE
            RMIN=(1+SQRT(ZMIN))/(1-SQRT(ZMIN))
            RMAX=(1+SQRT(ZMAX))/(1-SQRT(ZMAX))
            WTAP(KFLB)=(8D0/3D0)*LOG(RMAX/RMIN)
          ENDIF
          WTAP(21)=0.5D0*(ZMAX-ZMIN)
          WTAPE=(2D0/9D0)*LOG((1D0-ZMIN)/(1D0-ZMAX))
          IF(MOD(KFLBA,2).EQ.0) WTAPE=4D0*WTAPE
          IF(MECOR.GE.1.AND.NISGEN(JS,MI).EQ.0) THEN
            WTAP(KFLB)=WTFF*WTAP(KFLB)
            WTAP(21)=WTGF*WTAP(21)
            WTAPE=WTFF*WTAPE
          ENDIF
          IF(MSTP(61).EQ.1) WTAPE=0D0
          IF (KSVCB.GE.1) THEN
C...Kill normal creation but add joining diagrams for cmp quark.
            WTAP(21)=0D0
            IF (KFLBA.EQ.4.OR.KFLBA.EQ.5) THEN
              CALL PYERRM(9,'(PYPTIS:) Sorry, I got a heavy companion'//
     &             " quark here. Not handled yet, giving up!")
              PT2=0D0
              MINT(51)=1
              RETURN
            ENDIF
C...Check for possible joinings
c            IF (MSTP(96).NE.0.AND.MJOIND(JS,MI).EQ.0) THEN
C...Find companion's companion.
c              print*,'did not expect to get here '
c            ENDIF
          ELSEIF (KSVCB.EQ.0) THEN
C...Kill creation diagram for val quarks and sea quarks with companions.
            WTAP(21)=0D0
          ELSEIF (MQMASS.EQ.0) THEN
C...Extra safety factor for massless sea quark creation.
            WTAP(21)=WTAP(21)*1.25D0
          ENDIF
 
C...  q -> g, g -> g.
        ELSEIF(KFLB.EQ.21) THEN
C...Here we decide later whether a quark picked up is valence or
C...sea, so we maintain the extra factor sqrt(z) since we deal
C...with the *sum* of sea and valence in this context.
          WTAPQ=(16D0/3D0)*(SQRT(1D0/ZMIN)-SQRT(1D0/ZMAX))
C...new: do not allow backwards evol to pick up heavy flavour.
          DO 180 KFL=1,MIN(3,MSTP(58))
            WTAP(KFL)=WTAPQ
            WTAP(-KFL)=WTAPQ
  180     CONTINUE
          WTAP(21)=6D0*LOG(ZMAX*(1D0-ZMIN)/(ZMIN*(1D0-ZMAX)))
          IF(MECOR.GE.1.AND.NISGEN(JS,MI).EQ.0) THEN
            WTAPQ=WTFG*WTAPQ
            WTAP(21)=WTGG*WTAP(21)
          ENDIF
C...Check for possible joinings (companions handled separately above)
c          IF (MSTP(96).NE.0.AND.MINT(31).GE.2.AND.MJOIND(JS,MI).EQ.0)
c     &         THEN
c            print*,'did not expect to get here '
c          ENDIF
        ENDIF
 
C...Initialize massive quark evolution
        IF (MQMASS.NE.0) THEN
          RML=(RMQ2+VINT(18))/ALAM2
          TML=LOG(RML)
          TPL=LOG((PT2+VINT(18))/ALAM2)
          TPM=LOG((PT2+VINT(18))/RMQ2)
          WN=WTAP(21)*WPDF0/B0
        ENDIF
 

 
C...  Calculate PDF weights and sum for evolution rate.
        WTSUM=0D0
        XFBO=MAX(1D-10,XFB(KFLB))
        DO 210 KFL=-5,5
          WTPDF(KFL)=XFB(KFL)/XFBO
          WTSUM=WTSUM+WTAP(KFL)*WTPDF(KFL)
  210   CONTINUE
C...Only add gluon mother diagram for massless KFLB.
        IF(MQMASS.EQ.0) THEN
          WTPDF(21)=XFB(21)/XFBO
          WTSUM=WTSUM+WTAP(21)*WTPDF(21)
        ENDIF
        WTSUM=MAX(0.0001D0,WTSUM)
        WTSUMS=WTSUM
C...Add joining diagrams where applicable.
c        WTJOIN=0D0
        IF (MSTP(96).NE.0.AND.NJN.NE.0) THEN
          print*,' did not expect to get here '
        ENDIF
C.......
        IF(KFLB.NE.1.AND.KFLB.NE.2) THEN
          FR(1)=1D0
          FR(2)=0D0
        ELSE
          FR(1)=MIN(XFB(-KFLB)/XFB(KFLB),1D0)
          FR(2)=1D0-FR(1)
        ENDIF
C    XPSVC(KFLB,-1)/(XPSVC(KFLB,-1)+XPSVC(KFLB,0))
C        FR(2)=XPSVC(KFLB,0)/(XPSVC(KFLB,-1)+XPSVC(KFLB,0))

c        PT2CUTR=PT2CUT
c        PT2CUT=0.5D0*PT2CUTR

        DO II=-2,2
          WTDERIV(II)=0D0
          VALINT(II,0) = 0D0
          VALINT(II,1) = 00D0
          VALILO(II,0) = 0D0
          VALILO(II,1) = 0D0
          VALIHI(II,0) = 0D0
          VALIHI(II,1) = 0D0
          VALILU(II,0) = 0D0
          VALILU(II,1) = 0D0
          VALILD(II,0) = 0D0
          VALILD(II,1) = 0D0
        ENDDO

C.......value of the integral


        PT2RAT = LOG(PT2/ALAM2)/LOG(PT2CUT/ALAM2)
        PT2JAC = LOG(PT2RAT)

c        PT2RAT = PT2/PT2CUT
        PT2JAC = LOG(PT2RAT)



cc        print*,zmin,zmax,pt2jac,pt2,pt2cut
cc        IF(IKNT.GE.6) IWRITE=.TRUE.
        IF (IWRITE) WRITE(*,*) "KSVCB = ",
     $    KSVCB,KFLB,XPSVC(KFLB,0),XPSVC(KFLB,-1),XB,XMXC
        IF(IWRITE) WRITE(*,*) NMI(JS),NVC(JS,1),NVC(JS,2)
C...Loopback point for iteration


        DO 200 IPTINT=0,40

        WTTOT = 0D0
        WTLAMU = 0D0
        WTLAMD = 0D0
        WTDIP = 0D0
        WTDIPLO = 0D0
        WTDIPHI = 0D0

        WTI=1D0
cc        IPTINT=IPTINT+1
        IF(IPTINT.EQ.0 .OR.IPTINT.EQ.40) WTI=0.5D0
        PTRAND=IPTINT*.025D0

        WTSUM=WTSUMS
C        PT2=ALAM2*((PT2+VINT(18))/ALAM2)**(PYR(0)**(B0/WTSUM))-VINT(18)
        ALF=PT2RAT**PTRAND
        PT2=ALAM2*(PT2CUT/ALAM2)**ALF

c        PT2=PT2CUT*(PT2RAT)**PYR(0)

        WTLAMU=LOG(PT2/ALAM2)/LOG(0.25D0*PT2/ALAM2)
        WTLAMD=LOG(PT2/ALAM2)/LOG(4D0*PT2/ALAM2)
        PT2MX=0D0
        KFLC=21
 
C...  Evolve massive quark creation separately.
        MCRQQ=0 
C...Evolve joining separately
        MJOIN=0

C...Parton distributions at new pT2 but old x.
        MINT(30)=JS
        CALL PYPDFU(KFBEAM(JS),XB,PT2,XFN)
C...Treat val and cmp separately
ccc        IF (KFLBA.LE.6.AND.KSVCB.LE.0) XFN(KFLB)=XPSVC(KFLB,KSVCB)
ccc        IF(IWRITE) WRITE(*,*) '*',KFLB,XB,PT2,
ccc     $    XPSVC(KFLB,0),XPSVC(KFLB,-1)
c        IF (KSVCB.GE.1)
c     &       XFN(KFLB)=PYFCMP(YB/VINT(140),YS/VINT(140),MSTP(87))
        XFBN=XFN(KFLB)
        IF(XFBN.LT.1D-20) THEN
          IF(KFLA.EQ.KFLB) THEN
            WTAP(KFLB)=0D0
            GOTO 200
          ELSE
            XFBN=1D-10
            XFN(KFLB)=XFBN
          ENDIF
        ENDIF
        DO 270 KFL=-5,5
          XFB(KFL)=XFN(KFL)
  270   CONTINUE
        XFB(21)=XFN(21)
        XFBNV=0D0
        IF(KFLB.EQ.1 .OR. KFLB.EQ.2 ) THEN
          XFBN=MAX(XFN(-KFLB),1D-10)
          XFBNV=MAX(XFN(KFLB)-XFBN,1D-10)
        ELSE
          XFBN=MAX(XFN(KFLB),1D-10)
          XFBNV=0D0
        ENDIF

        NTRY=40
        DELZ=1D0/DBLE(NTRY)
        DELZ=0.5D0
C...Pick normal pT2 (in overestimated z range).
        DO 230 IZINT=0,NTRY-1
        WTTOT=0D0
        WTIZ=1D0
        IZ=IZINT/2+1

c        IF(IZINT.EQ.0.OR.IZINT.EQ.NTRY) WTIZ=0.5D0
c        ZRAND=IZINT*DELZ
        WTIZ=WW(IZ)
        IF(MOD(IZINT,2).EQ.0) THEN
          ZRAND=0.5D0*(1D0-XX(IZ))
        ELSE
          ZRAND=0.5D0*(1D0+XX(IZ))
        ENDIF


c        IF (MSTP(96).NE.0.AND.NJN.NE.0) THEN
c
c        ENDIF
 
C...Loopback if crossed c/b mass thresholds.
c        IF(IZRG.EQ.3.AND.PT2.LT.RMB2) THEN
c          PT2=RMB2
c         GOTO 130
c        ELSEIF(IZRG.EQ.2.AND.PT2.LT.RMC2) THEN
c          PT2=RMC2
c          GOTO 130
c        ENDIF
 
C...Speed up shower. Skip if higher-PT acceptable branching
C...already found somewhere else.
C...Also finish if below lower cutoff.
 
cc        IF ((PT2-PT2MX).LT.-0.001.OR.PT2.LT.PT2CUT) RETURN
 
C...Select parton A flavour (massive Q handled above.)
        WTEXTRA=1D0
c$$$        IF (MQMASS.EQ.0.AND.KFLC.NE.22.AND.MJOIN.EQ.0) THEN
c$$$          WTRAN=PYR(0)*WTSUM
c$$$          KFLA=-6
c$$$  240     KFLA=KFLA+1
c$$$          WTRAN=WTRAN-WTAP(KFLA)*WTPDF(KFLA)
c$$$          IF(KFLA.LE.5.AND.WTRAN.GT.0D0) GOTO 240
c$$$          IF(KFLA.EQ.6) KFLA=21
c$$$          WTEXTRA=WTSUM/(WTAP(KFLA)*WTPDF(KFLA))
c$$$        ENDIF
CMRENNA...
        KFLA=KFLB		       
        KFLAA=IABS(KFLA)
        

C...Choose z value (still in overestimated range) and corrective weight.
C...Unphysical z will be rejected below when Q2 has is computed.
        WTZ=0D0
        WTZP=0D0
        ZJACOB = -1D0
        ZJACOBP = -1D0

        KSVCB=-1

C...Note: ME and MQ>0 give corrections to overall weights, not shapes.
C...q -> q + g or q -> q + gamma (already set which).
        Z=ZMIN
        IF (KFLAA.LE.5.AND.KFLBA.LE.5) THEN
          IF (KSVCB.LT.0) THEN
C            Z=1D0-(1D0-ZMIN)*((1D0-ZMAX)/(1D0-ZMIN))**PYR(0)
            Z=1D0-(1D0-ZMIN)*((1D0-ZMAX)/(1D0-ZMIN))**ZRAND
            ZJACOB = LOG((1D0-ZMIN)/(1D0-ZMAX))
          ELSE
            ZFAC=RMIN*(RMAX/RMIN)**PYR(0)
            Z=((1-ZFAC)/(1+ZFAC))**2
            ZJACOB = LOG(RMAX/RMIN)
          ENDIF
          WTZ=0.5D0*(1D0+Z**2)
          WTZP=(Z**2+(1D0-Z)**2)*(1D0-Z)
C...Massive weight correction.
          IF (KFLBA.GE.4) WTZ=WTZ-Z*(1D0-Z)**2*RMQ2/PT2
C...Valence quark weight correction (extra sqrt)
          IF (KSVCB.GE.0) WTZ=WTZ*SQRT(Z)
 
          ZJACOBP = 0.5D0*ZJACOB
          ZJACOB = ZJACOB*8D0/3D0

C...q -> g + q.
C...NB: MQ>0 not yet implemented. Forced absent above.
        ELSEIF (KFLAA.LE.5.AND.KFLB.EQ.21) THEN
          KFLC=KFLA
c          Z=ZMAX/(1D0+PYR(0)*(SQRT(ZMAX/ZMIN)-1D0))**2
c          WTZ=0.5D0*(1D0+(1D0-Z)**2)*SQRT(Z)
c          ZJACOB = 2D0*(1D0/SQRT(ZMIN)-1D0/SQRT(ZMAX))
          Z=ZMIN*(ZMAX/ZMIN)**PYR(0)
          WTZ=0.5D0*(1D0+(1D0-Z)**2)
          ZJACOB = LOG(ZMAX/ZMIN)

          ZJACOB = ZJACOB*8D0/3D0
 
C...g -> q + qbar.
        ELSEIF (KFLA.EQ.21.AND.KFLBA.LE.5) THEN
          KFLC=-KFLB
          Z=ZMIN+PYR(0)*(ZMAX-ZMIN)
          WTZ=Z**2+(1D0-Z)**2
C...Massive correction
          IF (MQMASS.NE.0) THEN
            WTZ=WTZ+2D0*Z*(1D0-Z)*RMQ2/PT2
C...Extra safety margin for light sea quark creation
          ELSEIF (KSVCB.LT.0) THEN 
            WTZ=WTZ/1.25D0
          ENDIF
          ZJACOB = ZMAX-ZMIN

          ZJACOB = 0.5D0*ZJACOB
 
C...g -> g + g.
        ELSEIF (KFLA.EQ.21.AND.KFLB.EQ.21) THEN
          KFLC=21
          Z=1D0/(1D0+((1D0-ZMIN)/ZMIN)*((1D0-ZMAX)*ZMIN/
     &         (ZMAX*(1D0-ZMIN)))**ZRAND)
C     &         (ZMAX*(1D0-ZMIN)))**PYR(0))

          WTZ=(1D0-Z*(1D0-Z))**2
          ZJACOB = LOG(ZMAX*(1D0-ZMIN)/(ZMIN*(1D0-ZMAX)))

          WTZP=0.5D0*(1D0+(1D0-Z)**2)*(1D0-Z)
	      ZJACOBP = ZJACOB*8D0/3D0
          ZJACOB = ZJACOB * 6D0
        ENDIF
 
C...Derive Q2 from pT2.
        Q2B=PT2/(1D0-Z)
        IF (KFLBA.GE.4) Q2B=Q2B-RMQ2
 
C...Loopback if outside allowed z range for given pT2.
        RM2C=PYMASS(KFLC)**2
        PT2ADJ=Q2B-Z*(SHTNOW(MI)+Q2B)*(Q2B+RM2C)/SHTNOW(MI)
        IF (PT2ADJ.LT.1D-6) GOTO 230


C...Loop back if trial emission fails.
cc        IF(WTTOT.GE.0D0.AND.WTTOT.LT.PYR(0)) GOTO 200
C...Save acceptable branching.
        IF(PT2.GT.PT2MX) THEN
          MIMX=MINT(36)
          JSMX=JS
c          PT2MX=PT2
          KFLAMX=KFLA
          KFLCMX=KFLC
          RM2CMX=RM2C
          Q2BMX=Q2B
          ZMX=Z
          PT2AMX=PT2ADJ
C          PHIMX=PHI
          PHIMX=0D0
C...Boost recoiling parton to compensate for Q2 scale.
          SIDE=3D0-2D0*JS
          SHAT=SHTNOW(MI)
          BETAZ=SIDE*(1D0-(1D0+Q2BMX/SHAT)**2)/
     &         (1D0+(1D0+Q2BMX/SHAT)**2)
          IR=3997
          K(IR,1)=1
          IM=3998
          K(IM,1)=1
          IT=3999
          K(IT,1)=1
          IS=4000
          K(IS,1)=1
          IMIN=IR
          IMAX=IS
          P(IR,1)=0D0
          P(IR,2)=0D0
          P(IR,3)=0.5D0*SQRT(SHAT)*(-SIDE)
          P(IR,4)=0.5D0*SQRT(SHAT)
          CALL PYROBO(IR,IR,0D0,0D0,0D0,0D0,BETAZ)
         
C...Define kinematics of new partons in old frame.

          P(IM,1)=SQRT(PT2AMX)*SHAT/(ZMX*(SHAT+Q2BMX))
          P(IM,2)=0D0
          P(IM,3)=0.5D0*SQRT(SHAT)*((SHAT-Q2BMX)/((SHAT
     &         +Q2BMX)*ZMX)+(Q2BMX+RM2CMX)/SHAT)*SIDE
          P(IM,4)=SQRT(P(IM,1)**2+P(IM,3)**2)
          P(IT,1)=P(IM,1)
          P(IT,2)=P(IM,2)
          P(IT,3)=P(IM,3)-0.5D0*(SHAT+Q2BMX)/SQRT(SHAT)*SIDE
          P(IT,4)=SQRT(P(IT,1)**2+P(IT,3)**2+RM2CMX)
          P(IT,5)=SQRT(RM2CMX)
 
C...Update internal line, now spacelike
          P(IS,1)=P(IM,1)-P(IT,1)
          P(IS,2)=P(IM,2)-P(IT,2)
          P(IS,3)=P(IM,3)-P(IT,3)
          P(IS,4)=P(IM,4)-P(IT,4)
          P(IS,5)=P(IS,4)**2-P(IS,1)**2-P(IS,2)**2-P(IS,3)**2
C...Represent spacelike virtualities as -sqrt(abs(Q2)) .
          IF (P(IS,5).LT.0D0) THEN
             P(IS,5)=-SQRT(ABS(P(IS,5)))
          ELSE
             P(IS,5)=SQRT(P(IS,5))
          ENDIF
 
C...Boost entire system and rotate to new frame.
C...(including docu lines)
          BETAX=(P(IM,1)+P(IR,1))/(P(IM,4)+P(IR,4))
          BETAZ=(P(IM,3)+P(IR,3))/(P(IM,4)+P(IR,4))
          CALL PYROBO(IMIN,IMAX,0D0,0D0,-BETAX,0D0,-BETAZ)
          I1=IM
          THETA=PYANGL(P(I1,3),P(I1,1))
          CALL PYROBO(IMIN,IMAX,-THETA,PHIMX,0D0,0D0,0D0)
C          IF( P(IT,1)**2+P(IT,2)**2 .LT. PT2CUTR ) WTTOT=0D0
          PTCHK = SQRT(P(IT,1)**2+P(IT,2)**2)
          DO II=-2,2
            WTDERIV(II)=0D0
            PTTMP=PTCUTR+PTSTEP*DBLE(II)
            IF(PTCHK.GE.PTTMP) WTDERIV(II)=1D0
          ENDDO
          IF(WTDERIV(-2).EQ.0) GOTO 230

        ENDIF


C...Size of phase space and coherence suppression: MSTP(67) and MSTP(62)
C...No modification for very first emission if using ME correction
        MSTP67 = MSTP(67)
        IF (MECOR.GE.1.AND.NISGEN(1,MI).EQ.0.AND.NISGEN(2,MI).EQ.0) THEN
          MSTP67 = 0
        ENDIF
 
C...For 1st branching, limit phase space by s-hat with color-partner
        IF (MSTP67.GE.1.AND.NISGEN(JS,MI).EQ.0) THEN
          MSIDE=1
          IDIP=JS
          NPASS=1
C...Use anticolor tag for antiquark, or for gluon half the time
          IF (KFLB.LT.0.AND.KFLBA.LT.10) MSIDE=2
C...Use anticolor tag for antiquark, or for gluon half the time
          IF (KFLB.EQ.21) NPASS=2
C...Tag
          WTDIPHI=0D0
          WTDIP=0D0
          WTDIPLO=0D0
 265      MCTAG=ICOLUP(MSIDE,IDIP)
C...Default is to set up phase space using the opposite incoming parton
          JDIP=3-JS
          NDIP=0

C...Alternatively, look for final-state color partner (pick first if several)
          DO 260 IFS=3,NUP
            IF (ICOLUP(MSIDE,IFS).EQ.MCTAG.AND.NDIP.EQ.0) THEN
              JDIP=IFS
              NDIP=NDIP+1
            ENDIF
  260     CONTINUE
C...Compute momentum transfer: sdip = -t = - (p1 - p2)^2
C...(also works for annihilation since incoming massless, so shat = -(p1 - p2)^2)
          SDIP=ABS(((PUP(4,IDIP)-PUP(4,JDIP))**2
     &        -(PUP(3,IDIP)-PUP(3,JDIP))**2
     &        -(PUP(2,IDIP)-PUP(2,JDIP))**2
     &        -(PUP(1,IDIP)-PUP(1,JDIP))**2))
          IF (MSTP67.EQ.1) THEN
C...1 Option to completely kill radiation above s_dip * PARP(67)
            IF (4D0*PT2.GT.PARP(67)*SDIP) GOTO 230
          ELSE IF (MSTP67.EQ.2) THEN
C...2 Option to allow suppressed unordered radiation above s_dip * PARP(67)
C...  (-> improved power showers?)
CCCC            IF (4D0*PT2*PYR(0).GT.PARP(67)*SDIP) GOTO 230
            IF(NPASS.EQ.1) THEN
              WTDIP   = MIN(1D0, PARP(67)*SDIP/4D0/PT2 )
              WTDIPLO = MIN(1D0, PARP(67)*SDIP/4D0/PT2/4D0 )
              WTDIPHI = MIN(1D0, PARP(67)*SDIP/4D0/PT2*4D0 )
            ELSE
              WTDIP = WTDIP+0.5D0*MIN(1D0, PARP(67)*SDIP/4D0/PT2 )
              WTDIPLO = WTDIPLO+0.5D0*MIN(1D0,PARP(67)*SDIP/4D0/PT2/4D0)
              WTDIPHI = WTDIPHI+0.5D0*MIN(1D0,PARP(67)*SDIP/4D0/PT2*4D0)
              MSIDE=MSIDE+1
            ENDIF
            IF(NPASS.EQ.2.AND.MSIDE.EQ.2) GOTO 265
          ENDIF

cccc          ZJACOB = ZJACOB * WTDIP
 
C...For subsequent branchings, loopback if nonordered in angle/rapidity
        ELSE IF (MSTP(62).GE.3.AND.NISGEN(JS,MI).GE.1) THEN
          IF(PT2.GT.((1D0-Z)/(Z*(1D0-ZSAV(JS,MI))))**2*PT2SAV(JS,MI))
     &         GOTO 230
        ENDIF
 
C...Select phi angle of branching at random.

 
 
C...Parton distributions at new pT2 and new x.
        XA=XB/Z
        MINT(30)=JS
        CALL PYPDFU(KFBEAM(JS),XA,PT2,XFA)
ccc        IF (KFLBA.LE.5.AND.KFLAA.LE.5) THEN
C...q -> q + g: only consider respective sea, val, or cmp content.
ccc          IF (KSVCB.LE.0) THEN
ccc            XFA(KFLA)=XPSVC(KFLA,KSVCB)
ccc          ELSE
c            YA=XA*(1D0-YS)
c            XFA(KFLB)=PYFCMP(YA/VINT(140),YS/VINT(140),MSTP(87))
ccc          ENDIF
ccc        ENDIF
        IF(KFLB.EQ.1 .OR. KFLB.EQ.2 ) THEN
          XFAN=MAX(XFA(-KFLA),1D-10)
          XFANV=MAX(XFA(KFLA)-XFAN,1D-10)
        ELSE
          XFAN=MAX(XFA(KFLA),1D-10)
          XFANV=0D0
        ENDIF

	    XFANP=0D0
        IF(KFLB.EQ.21) THEN
        DO 271 KFL=-5,5
          IF(KFL.EQ.KFLB) GOTO 271
          XFANP=XFANP+XFA(KFL)
 271    CONTINUE
        ELSE
          XFANP=XFA(21)
        ENDIF


 
C...If weighting fails continue evolution.
        WTTOT=0D0
        WTTOTV=0D0
        IF (MCRQQ.EQ.0) THEN
c          WTPDFA=1D0/WTPDF(KFLA)
c          WTTOT=WTZ*XFAN/XFBN*WTPDFA
          IF(KFLB.EQ.1.OR.KFLB.EQ.2) THEN
            IF(XFBN.GE.1D-10)  WTTOT=WTTOT+ WTZ*XFAN/XFBN*ZJACOB
            IF(XFBNV.GE.1D-10) WTTOTV=WTTOTV+ WTZ*XFANV/XFBNV*ZJACOB
            WTTOT=WTTOT + WTZP*XFANP/XFBN*ZJACOBP
          ELSE
            WTTOT=(WTZP*XFANP/XFBN*ZJACOBP + WTZ*XFAN/XFBN*ZJACOB)
          ENDIF
          WTTOT=WTTOT*WTEXTRA
          WTTOTV=WTTOTV*WTEXTRA
          IF(IWRITE) write(*,*) wtz,xfan,xfbn,zjacob,wtextra
        ELSEIF(MCRQQ.EQ.1) THEN
          print*,' mcrqq = 1 '
c          WTPDFA=TPM/WPDF0
c          WTTOT=WTCRQQ*WTZ*XFAN/XFBN*WTPDFA*ZJACOB*WTEXTRA*WTFRAC
c          XBEST=TPM/TPM0*XQ0
        ELSEIF(MCRQQ.EQ.2) THEN
          print*,' massive quark creation '
C...Force massive quark creation.
          WTTOT=1D0
        ENDIF
        WTTOT=WTTOT*WTIZ
        WTTOTV=WTTOTV*WTIZ

        DO II=-2,2
          VALINT(II,0) = VALINT(II,0) + WTI*WTTOT*WTDIP*WTDERIV(II)
          VALILO(II,0) = VALILO(II,0) + WTI*WTTOT*WTDIPLO*WTDERIV(II)
          VALIHI(II,0) = VALIHI(II,0) + WTI*WTTOT*WTDIPHI*WTDERIV(II)
          VALILU(II,0)=VALILU(II,0) + WTI*WTTOT*WTDIP*WTLAMU*WTDERIV(II)
          VALILD(II,0)=VALILD(II,0) + WTI*WTTOT*WTDIP*WTLAMD*WTDERIV(II)
          VALINT(II,1) = VALINT(II,1) + WTI*WTTOTV*WTDIP*WTDERIV(II)
          VALILO(II,1) = VALILO(II,1) + WTI*WTTOTV*WTDIPLO*WTDERIV(II)
          VALIHI(II,1) = VALIHI(II,1) + WTI*WTTOTV*WTDIPHI*WTDERIV(II)
          VALILU(II,1)=VALILU(II,1)+WTI*WTTOTV*WTDIP*WTLAMU*WTDERIV(II)
          VALILD(II,1)=VALILD(II,1)+WTI*WTTOTV*WTDIP*WTLAMD*WTDERIV(II)
        ENDDO


 230    CONTINUE
 200    CONTINUE


cc        NTRY=40
C        FAC=PT2JAC/DBLE(NTRY)/B0*.025D0
        FAC=PT2JAC/B0*.025D0*DELZ
        DO II=-2,2
          DO JJ=0,1
          VALINT(II,JJ) = VALINT(II,JJ)*FAC
          VALILO(II,JJ) = VALILO(II,JJ)*FAC
          VALIHI(II,JJ) = VALIHI(II,JJ)*FAC
          VALILU(II,JJ) = VALILU(II,JJ)*FAC
          VALILD(II,JJ) = VALILD(II,JJ)*FAC          
          ENDDO
        ENDDO
        DO II=-2,2
          VALINTS(II)=FR(1)*EXP(-VALINT(II,0))+FR(2)*EXP(-VALINT(II,1)) 
          VALILOS(II)=FR(1)*EXP(-VALILO(II,0))+FR(2)*EXP(-VALILO(II,1)) 
          VALIHIS(II)=FR(1)*EXP(-VALIHI(II,0))+FR(2)*EXP(-VALIHI(II,1)) 
          VALILUS(II)=FR(1)*EXP(-VALILU(II,0))+FR(2)*EXP(-VALILU(II,1)) 
          VALILDS(II)=FR(1)*EXP(-VALILD(II,0))+FR(2)*EXP(-VALILD(II,1)) 
        ENDDO
        VINT(400) = VALINTS(0)
        VINT(399) = VALILOS(0)
        VINT(398) = VALIHIS(0)
        VINT(397) = VALILUS(0)
        VINT(396) = VALILDS(0)

        PTCUTR0=PTCUTR
        PTSTEP0=PTSTEP
        VINT(395) = RNUMDRV5(VALINTS,PTCUTR0,PTSTEP0)
        VINT(394) = RNUMDRV5(VALILOS,PTCUTR0,PTSTEP0)
        VINT(393) = RNUMDRV5(VALIHIS,PTCUTR0,PTSTEP0)
        VINT(392) = RNUMDRV5(VALILUS,PTCUTR0,PTSTEP0)
        VINT(391) = RNUMDRV5(VALILDS,PTCUTR0,PTSTEP0)
        
        PT2CUT = PT2CUTR

C----------------------------------------------------------------------
C...MODE= 1: Accept stored shower branching. Update event record etc.

      ENDIF
 
C...If reached this point, normal exit.
  390 IFAIL=0
 
      RETURN
      END
C.......four point numerical derivative formula
C.......assume evenly spaced for now
      FUNCTION RNUMDRV5(FUNC,PTCUTR0,PTSTEP0)
      IMPLICIT NONE
      DOUBLE PRECISION RNUMDRV5,FUNC(-2:2),PTCUTR0,PTSTEP0,PTTMP,TEMP
      TEMP=PTCUTR0+PTSTEP0
      PTTMP=TEMP-PTCUTR0
      RNUMDRV5=((FUNC(-2)-FUNC(2))-8D0*(FUNC(-1)-FUNC(1)))/12D0/PTTMP
      RETURN
      END

      SUBROUTINE gauleg(x1,x2,x,w,n)
      INTEGER n
      REAL*8 x1,x2,x(20),w(20)
      DOUBLE PRECISION EPS
      PARAMETER (EPS=3.d-14)
      INTEGER i,j,m
      DOUBLE PRECISION p1,p2,p3,pp,xl,xm,z,z1,pi
      PI=4D0*DATAN(1D0)
      m=(n+1)/2
      xm=0.5d0*(x2+x1)
      xl=0.5d0*(x2-x1)
      do 12 i=1,m
c        z=cos(3.141592654d0*(i-.25d0)/(n+.5d0))
        z=cos(PI*(DBLE(i)-.25d0)/(dble(n)+.5d0))
1       continue
          p1=1.d0
          p2=0.d0
          do 11 j=1,n
            p3=p2
            p2=p1
            p1=((2.d0*dble(j)-1.d0)*z*p2-(dble(j)-1.d0)*p3)/dble(j)
11        continue
          pp=n*(z*p1-p2)/(z*z-1.d0)
          z1=z
          z=z1-p1/pp
        if(abs(z-z1).gt.EPS)goto 1
        x(i)=xm-xl*z
        x(n+1-i)=xm+xl*z
        w(i)=2.d0*xl/((1.d0-z*z)*pp*pp)
        w(n+1-i)=w(i)
12    continue
      return
      END
C  (C) Copr. 1986-92 Numerical Recipes Software v%1jw#<0(9p#3.
