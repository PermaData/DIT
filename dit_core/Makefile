SHELL=/bin/sh
# 
# List of Source objects for each main calling sequence 
# (main first, subroutines second)

dit= dit_mod.o dit_main.o dit_read_input.o dit_read.o dit_write.o netcdf_util.o


# Tunable parameters
#
# FC		Name of the fortran compiling system to use
# FFLAGS	Flags to the compiler
#               -O optimize
#               -o output specified
#               -g use debugger
# LDFLAGS	Flags to the loader
# LIBS		List of libraries
# CMD		Name of the executable
#
# SGI unique
#FC =		f90
#FFLAGS =	-g -I/usr/local/netcdf/include
#LDFLAGS =       	
#LIBS =		-L/usr/local/lib -lpgplot -lX11 -lnetcdf

# Linux unique
FC =		pgf90
#FFLAGS =	-g -I/usr/include -Mbounds
FFLAGS =	-g -I/usr/local/netcdf-3.6.2_64_pgi/include -I/usr/include -Mbounds
LDFLAGS =       	
#LIBS =		-L/usr/X11R6/lib -L/usr/lib -L/home/schaefek/schaefer_lib/pgplot \
 -lpgplot -lX11 -lnetcdf -lg2c -lpng -llapack -lblas
LIBS =		-L/usr/lib -lX11 -lnetcdf -lpng -llapack -lblas
#
# end machine unique
CMD =		a.out
.f:
	$(FC) $(FFLAGS) $(LDFLAGS) -o $@ $<

# Object list for each subroutine(s) in a separate file
dit_read.o: dit_read.f90
	$(FC) $(FFLAGS) -c dit_read.f90
dit_write.o: dit_write.f90
	$(FC) $(FFLAGS) -c dit_write.f90
dit_main.o: dit_main.f90
	$(FC) $(FFLAGS) -c dit_main.f90
dit_mod.o: dit_mod.f90
	$(FC) $(FFLAGS) -c dit_mod.f90
dit_read_input.o: dit_read_input.f90
	$(FC) $(FFLAGS) -c dit_read_input.f90
netcdf_util.o: netcdf_util.f90
	$(FC) $(FFLAGS) -c netcdf_util.f90
netcdf_routines.o: netcdf_routines.f90
	$(FC) $(FFLAGS) -c netcdf_routines.f90


# make command list

dit: $(dit)
	$(FC) $(FFLAGS) $(dit) $(LIBS) -o dit.out

# Cleanup stuff
clean:
	-rm -f *.o *.out *.mod *.stb core

