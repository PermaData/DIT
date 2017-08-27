!
!===================================================
      subroutine read_inputs
!===================================================
! reads in all inputs to the Data Integration Tool (dit) program
!
! Modifications:
!  Kevin Schaefer created routine (1/10/15)
!---------------------------------------------------
!
      use dit_variables
!
      implicit none
!
! internal variables
      integer iman      ! manipulation index
      integer ipat      ! path index
      integer idat      ! data file index
      integer ivar      ! variable index
      Character*45 Junk ! garbage variable for reading input descriptors
      character*20 typ   ! path type
      logical find ! flag if path is found
      double precision test
!
! read input file
      open(unit=100,file='Dit.in',form='formatted')
!
! read standard missing values
      read (unit=100,10) junk
      read (unit=100,14) junk, miss_val_real
      read (unit=100,17) junk, miss_val_char
!
! data manipulations
      read (unit=100,10) junk
      read (unit=100,11) junk,n_man
      allocate(man(n_man))
      read (unit=100,10) junk
      do iman = 1, n_man
        read (unit=100,*) man(iman)%doit, man(iman)%typ, man(iman)%num, man(iman)%ind1, man(iman)%ind2, &
	man(iman)%ind3, man(iman)%ind4, man(iman)%ind5, man(iman)%ind6, man(iman)%val1, man(iman)%val2, man(iman)%val3, man(iman)%txt1, man(iman)%txt2, man(iman)%txt3
      enddo
!
! paths and control filenames
      read (unit=100,10) junk
      read (unit=100,11) junk,n_path
      allocate(path(n_path))
      read (unit=100,10) junk
      do ipat = 1, n_path
        read (unit=100,*) path(ipat)%num, path(ipat)%cat,path(ipat)%typ, path(ipat)%txt1, path(ipat)%txt2,path(ipat)%path1
      enddo
!
! data filenames
      read (unit=100,10) junk
      read (unit=100,11) junk,n_file
      allocate(file(n_file))
      read (unit=100,10) junk
      do idat = 1, n_file
        read (unit=100,*) file(idat)%num, file(idat)%typ, file(idat)%path1,file(idat)%path2, file(idat)%npath1, file(idat)%npath2,file(idat)%npath3, &
	                file(idat)%npath4,file(idat)%ind1,file(idat)%ind2
      enddo
!
! close inputs file
      close(unit=100)
!
! assign time variables
      day_per_yr=365.
      day_per_yr_leap=366.
      day_per_mon(:)      = (/31,28,31,30,31,30,31,31,30,31,30,31/)
      day_per_mon_leap(:) = (/31,29,31,30,31,30,31,31,30,31,30,31/)
      doy1_mon(:)         = (/1,32,60,91,121,152,182,213,244,274,305,335/)
      doy1_mon_leap(:)    = (/1,32,61,92,122,153,183,214,245,276,306,336/)  
      mid_mon_doy(:)      = (/15.5,45.,74.5,105.,135.5,166.,196.5,227.5,258.,288.5,319.,349.5/)
      mid_mon_doy_leap(:) = (/15.5,45.5,75.5,106.,136.5,167.,197.5,228.5,259.,289.5,320.,350.5/)
      mid_month(1)='-15 12:00'
      mid_month(2)='-14 00:00'
      mid_month(3)='-15 12:00'
      mid_month(4)='-15 00:00'
      mid_month(5)='-15 12:00'
      mid_month(6)='-15 00:00'
      mid_month(7)='-15 12:00'
      mid_month(8)='-15 12:00'
      mid_month(9)='-15 00:00'
      mid_month(10)='-15 12:00'
      mid_month(11)='-15 00:00'
      mid_month(12)='-15 12:00'
!
! find and open output processing data file
      do ipat = 1, n_path
        if(path(ipat)%typ=='propath')exit
      enddo
      filename=trim(path(ipat)%path1)
      open(unit=33,file=trim(filename),form='formatted')
!
! find path indeces
      do ipat = 1, n_path
        if(path(ipat)%typ=='temp') i_pat_tmp=ipat
        if(path(ipat)%typ=='python') i_pat_python=ipat
        if(path(ipat)%typ=='outpath') i_pat_out=ipat
      enddo
!
! integer missing value
      miss_val_int=miss_val_real
!
! standard character string variables
      qd='"'
      qs="'"
!
! standard formats for input
10    Format (a45)
11    Format (a45, I4)
12    Format (a45, a2)
13    Format (a45, E15.8)
14    Format (a45, f8.4)
16    Format (a45, a200)
17    Format (a45, a20)
21    Format (a45, a8)
22    Format (i2,2x,a100)
!
      end subroutine
!
!===================================================
      subroutine read_variable_mapping_file (idat)
!===================================================
! reads input to output variable mapping file
! set dimensions of output variable
! executed once for each input data file
!
! Modifications:
!  Kevin Schaefer created routine (1/10/15)
!---------------------------------------------------
!
      use dit_variables
!
      implicit none
!
! internal variables
      integer ipat      ! path index
      integer idat      ! data file index
      integer ivar      ! variable index
      integer imap      ! variable map index
      Character*45 Junk ! garbage variable for reading input descriptors
      character*20 typ   ! path type
      logical find ! flag if path is found
      logical flg  ! generic flag
!
! variable mapping key
! var(ivar)%num   ! num
! var(ivar)%txt1  ! In_var
! var(ivar)%txt2  ! Out_var
! var(ivar)%flg1  ! in
! var(ivar)%flg2  ! out
! var(ivar)%ind1  ! o_in
! var(ivar)%ind2  ! o_out
! var(ivar)%map   ! map_typ
! var(ivar)%typ   ! typ
! var(ivar)%fmt1  ! fmt
! var(ivar)%txt3  ! units
! var(ivar)%txt4  ! Description
!
! locate variable mapping file
      ipat=file(idat)%npath3
      if(trim(path(ipat)%typ)/='varmap') then
        print*, 'Error: incorrect variable mapping file'
	print*, 'Data File: ', idat
	print*, 'type: ', trim(path(ipat)%typ)
	stop
      endif
      filename=trim(path(ipat)%path1)
!
! read variable mapping file
      open(unit=100, File=trim(filename), form='formatted', status='old')
      read(unit=100, *) n_var
      allocate(var(n_var))
      read(unit=100, *) junk
      do ivar=1,n_var
         read(unit=100,*) var(ivar)%num, var(ivar)%txt1, var(ivar)%txt2, var(ivar)%flg1, var(ivar)%flg2, var(ivar)%ind1, var(ivar)%ind2, var(ivar)%map, &
	 var(ivar)%typ,var(ivar)%fmt1,var(ivar)%txt3, var(ivar)%txt4
      enddo
      close(unit=100)
!
! check some values
      do ivar=1,n_var
         flg=.false.
	 if(trim(var(ivar)%typ)=='char') flg=.true.
	 if(trim(var(ivar)%typ)=='real') flg=.true.
	 if(trim(var(ivar)%typ)=='integer') flg=.true.
	 if(.not.flg) then
	   print*, 'Error: incorrect variable type'
	   print*, ivar, trim(var(ivar)%typ)
	   stop
	 endif
      enddo
!
! count number of input and output variables
      in%n_var=0
      out%n_var=0
      do ivar=1,n_var
         if(var(ivar)%flg1) in%n_var=in%n_var+1
         if(var(ivar)%flg2) out%n_var=out%n_var+1
      enddo
!
! input array variable specifications
      allocate(var_in(in%n_var))
      do imap=1,in%n_var
        do ivar=1,n_var
	  if(var(ivar)%ind1==imap) var_in(imap)=var(ivar)
	enddo
      enddo
!
! output array variable specifications
      allocate(var_out(out%n_var))
      do imap=1,out%n_var
        do ivar=1,n_var
	  if(var(ivar)%ind2==imap) var_out(imap)=var(ivar)
	enddo
      enddo
!
! standard formats for input
10    Format (a45)
11    Format (a45, I4)
12    Format (a45, a2)
13    Format (a45, E15.8)
14    Format (a45, f8.4)
16    Format (a45, a200)
17    Format (a45, a20)
21    Format (a45, a8)
22    Format (i2,2x,a100)
!
      end subroutine
