!======================================================================
! Export Monte Carlo Optical Dataset
!
! Zemax 2011 EE
!
! Purpose
! -------
! Export representative Monte Carlo trials into a directory structure
! compatible with the Python Optical Analysis Toolkit.
!
! Output Structure
! ----------------
!
! monte_carlo/
!     representative_case/
!         wavelength_nm/
!
!             spot.txt
!
!             field_1/
!                 psf.txt
!                 mtf.txt
!                 wavefront.txt
!
!             field_2/
!                 ...
!
!             field_N/
!
!----------------------------------------------------------------------
! IMPORTANT (Zemax 2011 EE)
!
! Each analysis uses its own CFG file.
!
!     psf.CFG
!     mtf.CFG
!     spot.CFG
!     wavefront.CFG
!
! Sharing CFG files between analyses causes MODIFYSETTINGS() to overwrite
! unrelated settings.
!
!----------------------------------------------------------------------
! NOTE
!
! This file is generated from a template.
!
! Python expands representative trials into one complete export block for every representative trial.
!
!======================================================================

FORMAT 0

!======================================================================
! Export Mode
!
! 1 = PSF only
! 2 = FFT MTF only
! 3 = Spot Diagram only
! 4 = Wavefront only
! 5 = Everything
!======================================================================

EXPORT_MODE = 5

!======================================================================
! Project Paths
!======================================================================

ROOT$ = "C:\archive\manthan\projects\uv-vis-instrument\"

DEV$ = ROOT$ + "development\optical-engineering-toolkit\"

OPTICS$ = ROOT$ + "optical_designs\"

MCROOT$ = OPTICS$ + "05-nominal-optical-design\monte-carlo-trials\"

CFGROOT$ = OPTICS$ + "05-nominal-optical-design\"

OUTPUT$ = DEV$ + "input\monte-carlo\"

PSFCFG$ = CFGROOT$ + "psf.CFG"

MTFCFG$ = CFGROOT$ + "mtf.CFG"

SPTCFG$ = CFGROOT$ + "spot.CFG"

WFMCFG$ = CFGROOT$ + "wavefront.CFG"

PRINT "=============================================================="
PRINT "Representative Monte Carlo Export"
PRINT "=============================================================="
PRINT ""

PRINT "Analysis Settings"
PRINT "------------------------------"
PRINT "PSF        : ", PSFCFG$
PRINT "MTF        : ", MTFCFG$
PRINT "Spot       : ", SPTCFG$
PRINT "Wavefront  : ", WFMCFG$
PRINT ""

PRINT "Beginning representative trial export..."
PRINT ""

!======================================================================
! AUTO-GENERATED REPRESENTATIVE TRIAL EXPORTS
!
! Everything below is generated automatically by Python.
!
! Each generated block:
!
!     • loads one representative Monte Carlo lens
!     • determines dataset dimensions
!     • exports every wavelength
!     • exports spot diagrams
!     • exports every field
!         • PSF
!         • FFT MTF
!         • Wavefront
!
!======================================================================

{{REPRESENTATIVE_TRIALS}}

PRINT ""

PRINT "=============================================================="
PRINT "Representative Monte Carlo export completed successfully."
PRINT "=============================================================="

END