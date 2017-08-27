!
!===================================================
    subroutine test_read_csv_file(idat)
!===================================================
! reads an ascii file of unknown length and saves only some records
! assumes the first variable is site ID and that the ID is the same as file name
!
    use dit_variables
    use netcdf
    use typeSizes
!
    implicit none
!
! input variables
    integer idat    ! input data file number to read
!
! internal variables
    integer itxt     ! character index
    integer icar     ! character index
    integer ipat     ! path number index
    integer irec     ! record number index
    integer ihed     ! header number index
    integer ivar     ! variable number index
    integer num      ! number characters
    integer status   ! read status variable
    double precision val1     ! temporary value 
    Character*250 Junk ! garbage variable for reading text
    Character*250 text ! garbage variable for reading text
    Character*250 fmt  ! text string format
!
! locate input data file
    ipat=file(idat)%npath1
    filename=trim(path(ipat)%path1)//trim(file(idat)%path1)
!
! check dimensions
    if(in%n_var/=file(idat)%ind1) then
      print*, 'Error: input file nvar does not match mapping file'
      print*, 'file nvar: ',in%n_var, 'mapvar nvar; ',file(idat)%ind1
      stop
    endif
    in%n_hed=file(idat)%ind2
!
! geric read format
    fmt='(a250)'
!
! count data records
    allocate(temp1_char1(in%n_var))
    open(unit=20, file=trim(filename), form='formatted', status='old')
!
! count records
    do ihed=1,in%n_hed
      read(unit=20,fmt=fmt) junk
    enddo
    in%n_rec=0
    do irec=1,10e26
      read(unit=20,fmt=fmt, iostat=status) junk
      if(status<0) exit
      in%n_rec=in%n_rec+1
    enddo
    close(unit=20)
!
! allocate data variables
    allocate(head_in(in%n_var,in%n_hed))
    allocate(data_in(in%n_var,in%n_rec))
    allocate(char_in(in%n_var,in%n_rec))
    char_in=miss_val_char
    head_in=miss_val_char
    data_in=miss_val_real
!
! reopen data file and read data values
    open(unit=20, file=trim(filename), form='formatted', status='old')
!
! read header
    do ihed=1,in%n_hed
      read(unit=20,*) head_in(:,ihed)
    enddo
!
! read data
    do irec=1,in%n_rec
!
! read Record as a text string
      read(unit=20,fmt=fmt, iostat=status) junk
!
! parse record into variables assuming comma deliminator
      junk=adjustl(junk)
      num=len(trim(junk))
      ivar=1
      icar=1
      text=''
      do itxt=1,num
        if(junk(itxt:itxt)/=',') then
	  text(icar:icar)=junk(itxt:itxt)
	  icar=icar+1
	else
	  char_in(ivar,irec)=trim(text)
	  text=''
	  ivar=ivar+1
	  icar=1
	endif
      enddo
      char_in(in%n_var,irec)=trim(text)
      do ivar=1,in%n_var
         if(var_in(ivar)%typ/='char') then
	   read(char_in(ivar,irec),*, iostat=status) val1
           if(status/=0) then
	     data_in(ivar,irec)=miss_val_real
	   else
	     data_in(ivar,irec)=val1
	   endif
	   char_in(ivar,irec)=trim(miss_val_char)
        endif
      enddo
    enddo
    close(unit=20)
!
! deallocate temporary variables
    deallocate(temp1_char1)
!
! set initial dimensions of output
    out%n_rec=in%n_rec
    out%n_hed=1
!
    end subroutine
!
!===================================================
    subroutine read_csv_file(ifil, case)
!===================================================
! reads in temporary CSV files
! assumes dimensions known already
!
    use dit_variables
    use netcdf
    use typeSizes
!
    implicit none
!
! input variables
    integer ifil      ! data file index
    Character*20 case ! what to write out as csv
!
! internal variables
    integer ipat    ! path numder index
    integer irec    ! record numder index
    integer ihed    ! header numder index
    integer ivar    ! header numder index
    integer status  ! read status variable
    Character*250 temp_file ! temporary file name
    Character*250 path_typ  ! path type
    Character*250 Junk      ! garbage variable for reading text
    double precision, allocatable :: data_read(:,:)          ! temp read data array
    Character*200, allocatable :: char_read(:,:) ! temp read character array
!
! read into local temporary arrays
    select case(case)
      case('in ')        ! read input arrays from original file
        x_dim=in%n_var
        y_dim=in%n_rec
        allocate(data_read(x_dim,y_dim))
        allocate(char_read(x_dim,y_dim))
        path_typ='input'
      case('in_temp')    ! read input arrays from temporary file
        x_dim=in%n_var
        y_dim=in%n_rec
        allocate(data_read(x_dim,y_dim))
        allocate(char_read(x_dim,y_dim))
        path_typ='temp'
	temp_file='temp2'
      case('out_temp')   ! read output arrays from temporary file
        x_dim=out%n_var
        y_dim=out%n_rec
        allocate(data_read(x_dim,y_dim))
        allocate(char_read(x_dim,y_dim))
        path_typ='temp'
	temp_file='temp2'
      case('shred_tmp')  ! read shredded output arrays from temporary file
        x_dim=tmp%n_var
        y_dim=tmp%n_rec
        allocate(data_read(x_dim,y_dim))
        allocate(char_read(x_dim,y_dim))
        path_typ='temp'
	temp_file='temp2'
    end select
!
! locate input data file
    if(trim(path_typ)=='temp') then
      filename=trim(path(i_pat_tmp)%path1)//trim(temp_file)
    else
      ipat=file(ifil)%npath1
      filename=trim(path(ipat)%path1)//trim(file(ifil)%path1)
    endif
    write(unit=33,*) '\t\tread: ',trim(filename)
!
! Open file and read header
    open(unit=20, file=trim(filename), form='formatted', status='old')
    read(unit=20,*) junk
!
! read data
    do irec=1,y_dim
      read(unit=20,*) data_read(:,irec)
    enddo
    close(unit=20)
!
! reopen data file and read header
    open(unit=20, file=trim(filename), form='formatted', status='old')
    read(unit=20,*) junk
!
! read character data
    do irec=1,y_dim
      read(unit=20,*) char_read(:,irec)
    enddo
    close(unit=20)
!
! move to correct internal dit array
    select case(case)
      case('in')       ! transfer to data_in arrays
        data_in=data_read
        char_in=char_read
      case('in_temp')  ! transfer to temp1 arrays
        temp1_d2=data_read
        temp1_char2=char_read
      case('out_temp') ! transfer to temp1 arrays
        temp1_d2=data_read
        temp1_char2=char_read
      case('shred_tmp')    ! transfer to temp2 arrays
        temp1_d2(1:tmp%n_var,1:tmp%n_rec)=data_read
        temp1_char1(1:tmp%n_rec)=char_read(1,:)
    end select
!
! deallocate local arrays
    deallocate(data_read)
    deallocate(char_read)

    end subroutine
!
!===================================================
    subroutine read_python_data(ifil)
!===================================================
!
    use dit_variables
    use netcdf
    use typeSizes
!
    implicit none
!
! input variables
    integer ifil    ! input data file number to read
!
! internal variables
    integer ipat    ! path numder index
    integer irec    ! record numder index
    integer ihed    ! header numder index
    integer ivar    ! header numder index
    integer status ! read status variable
    Character*45 Junk ! garbage variable for reading text
    Character*250 file_in  ! input file for python script
    Character*250 file_out ! output file from pythn script
    Character*250 cmd      ! command variable for system call
    logical temp_flag ! flag from read temporary file
!
! input/output data files for python script
    ipat=file(ifil)%npath1
    file_in=trim(path(ipat)%path1)//trim(file(ifil)%path1)
    file_out=trim(path(i_pat_tmp)%path1)//'temp2.csv'
!
! command to execute python script
    cmd=trim(path(i_pat_python)%path1)//'pull_ggd361_data.py -i'
    cmd=trim(cmd)//' '//trim(file_in)//' -o '//trim(file_out)
!
! call system command
    call system( trim(cmd) )
!
! read temporary file created by python script
    temp_flag=.true.
    call read_ascii_data(ifil,temp_flag)
!
    end subroutine
!
!===================================================
    subroutine read_ascii_filter(idat)
!===================================================
! reads an ascii file of unknown length and saves only some records
! assumes the first variable is site ID and that the ID is the same as file name
!
    use dit_variables
    use netcdf
    use typeSizes
!
    implicit none
!
! input variables
    integer idat    ! input data file number to read
!
! internal variables
    integer ipat     ! path numder index
    integer irec     ! record numder index
    integer ihed     ! header numder index
    integer ivar     ! header numder index
    integer status  ! read status variable
    Character*45 Junk ! garbage variable for reading text
!
! locate input data file
    ipat=file(idat)%npath1
    filename=trim(path(ipat)%path1)//trim(file(idat)%path1)
!
! check dimensions
    if(in%n_var/=file(idat)%ind1) then
      print*, 'Error: input file nvar does not match mapping file'
      print*, 'file nvar: ',in%n_var, 'mapvar nvar; ',file(idat)%ind1
      stop
    endif
    in%n_hed=file(idat)%ind2
!
! count data records
    allocate(temp1_char1(in%n_var))
    open(unit=20, file=trim(filename), form='formatted', status='old')
!
! count records
    do ihed=1,in%n_hed
      read(unit=20,*) junk
    enddo
    in%n_rec=0
    do irec=1,10e26
      read(unit=20,*, iostat=status) temp1_char1
      if(status<0) exit
      if(trim(temp1_char1(1))==trim(file(idat)%path1)) in%n_rec=in%n_rec+1
    enddo
    close(unit=20)
!
! allocate data variables
    allocate(head_in(in%n_var,in%n_hed))
    allocate(data_in(in%n_var,in%n_rec))
    allocate(char_in(in%n_var,in%n_rec))
    char_in=miss_val_char
    head_in=miss_val_char
    data_in=miss_val_real
!
! reopen data file and read real data values
    open(unit=20, file=trim(filename), form='formatted', status='old')
!
! read header
    do ihed=1,in%n_hed
      read(unit=20,*) head_in(:,ihed)
    enddo
!
! read data
    in%n_rec=0
    do irec=1,10e26
      read(unit=20,*, iostat=status) temp1_char1
      if(status<0) exit
      if(trim(temp1_char1(1))==trim(file(idat)%path1)) then
        in%n_rec=in%n_rec+1
	do ivar=1,in%n_var
	  if(var_in(ivar)%typ=='char') char_in(ivar,in%n_rec)=trim(temp1_char1(ivar))
	  if(var_in(ivar)%typ=='real') read(temp1_char1(ivar),*) data_in(ivar,in%n_rec)
	  if(var_in(ivar)%typ=='integer') read(temp1_char1(ivar),*) data_in(ivar,in%n_rec)
	enddo
      endif
    enddo
    close(unit=20)
!
! deallocate temporary variables
    deallocate(temp1_char1)
!
! set initial dimensions of output
    out%n_rec=in%n_rec
    out%n_hed=1
!
    end subroutine
!
!===================================================
    subroutine read_ascii_data(idat, temp_flag)
!===================================================
! assumes text fields surrounded by quotes
!
    use dit_variables
    use netcdf
    use typeSizes
!
    implicit none
!
! input variables
    integer idat    ! input data file number to read
    logical temp_flag ! flag from read temporary file
!
! internal variables
    integer ipat    ! path numder index
    integer irec    ! record numder index
    integer ihed    ! header numder index
    integer ivar    ! header numder index
    integer status  ! read status variable
    Character*45 Junk ! garbage variable for reading text
!
! locate input data file
    if(temp_flag) then
      filename=trim(path(i_pat_tmp)%path1)//'temp2.csv'
    else
      ipat=file(idat)%npath1
      filename=trim(path(ipat)%path1)//trim(file(idat)%path1)
    endif
!
! determine dimensions
    if(in%n_var/=file(idat)%ind1) then
      print*, 'Error: input file nvar does not match mapping file'
      print*, 'file nvar: ',in%n_var, 'mapvar nvar; ',file(idat)%ind1
      stop
    endif
    in%n_hed=file(idat)%ind2
!
! count data records
    allocate(temp1_d1(in%n_var))
    open(unit=20, file=trim(filename), form='formatted', status='old')
!
! count records
    do ihed=1,in%n_hed
      read(unit=20,*) junk
    enddo
    in%n_rec=0
    do irec=1,10e26
      read(unit=20,*, iostat=status) temp1_d1
      if(status<0) exit
      in%n_rec=in%n_rec+1
    enddo
    close(unit=20)
    deallocate(temp1_d1)
!
! allocate data variables
    allocate(head_in(in%n_var,in%n_hed))
    allocate(data_in(in%n_var,in%n_rec))
    allocate(char_in(in%n_var,in%n_rec))
!
! reopen data file and read real data values
    open(unit=20, file=trim(filename), form='formatted', status='old')
!
! read header
    do ihed=1,in%n_hed
      read(unit=20,*) head_in(:,ihed)
    enddo
!
! read data
    do irec=1,in%n_rec
      read(unit=20,*) data_in(:,irec)
    enddo
    close(unit=20)
!
! Set character data to missing value in real value data array
    do ivar=1,in%n_var
      if (var(ivar)%typ=='char') then
        data_in(ivar,:)=miss_val_real
      endif
    enddo
!
! reopen data file and read character data values
    open(unit=20, file=trim(filename), form='formatted', status='old')
!
! read header
    do ihed=1,in%n_hed
      read(unit=20,*) head_in(:,ihed)
    enddo
!
! read data
    do irec=1,in%n_rec
      read(unit=20,*) char_in(:,irec)
    enddo
    close(unit=20)
!
! set initial dimensions of output
    out%n_rec=in%n_rec
    out%n_hed=1
!
    end subroutine
!
!===================================================
      subroutine manipulate_data(ifil,iman)
!===================================================
!
    use dit_variables
    use netcdf
    use typeSizes
!
    implicit none
!
! i/o variables
    integer ifil ! data file index
    integer iman  ! manipulation index
!
! internal variables
    integer z_dim ! z dimension
    integer ix    ! x value index 
    integer iy    ! y value index
    integer ista  ! statistic index
    integer icnt  ! count index
    integer ivar  ! out variable index
    integer itxt  ! text index
    integer indx1 ! static record index 1
    integer indx2 ! static record index 2
    integer indx3 ! static record index 3
    integer indx4 ! static record index 4
    integer indx5 ! static record index 5
    integer indx6 ! static record index 6
    integer indx(6) ! array of indeces
    Character*20 typ(6) ! temp variable types
    integer irec  ! record index
    integer ipat  ! path index
    integer imap1, imap2, imap3, imap4
    integer idvar ! id number variable index
    integer n_stat ! number of statistics
    integer num   ! total count
    integer lim1  ! lower variable do loop limit
    integer lim2  ! upper variable do loop limit
    integer cnt1  ! count 1
    integer cnt2  ! count 2
    integer cnt3  ! count 3
    integer cnt4  ! count 4
    integer nval  ! number values
    integer status  ! read status variable
    integer imin  ! index of min value
    double precision val1     ! temporary value 
    double precision val2     ! temporary value
    double precision val3     ! temporary value
    double precision valmin   ! min value 
    double precision valmax   ! max value
    double precision dval     ! temporary delta value
    Character*200 tmp_text  ! text string
    Character*200 text      ! text string
    Character*200 temp      ! text string
    Character*200 temp1     ! text string 1
    Character*200 temp2     ! text string 2
    Character*200 fmt       ! text string format
    logical flag  ! generic flag
    integer year  ! year
    integer mon   ! month
    Character*250 junk     ! junk text
    Character*250 cmd      ! command variable for system call
    Character*250 file_in  ! input file for python script
    Character*250 file_out ! output file from pythn script
    Character*20 case ! what to write out as csv
!
! transfer data to local variable
    select case(man(iman)%num)
      case(1) ! input data
        x_dim=in%n_var
	y_dim=in%n_rec
	allocate(temp1_d2(x_dim,y_dim))
	allocate(temp1_char2(x_dim,y_dim))
	allocate(var_tmp(x_dim))
	allocate(head_tmp(x_dim))
	temp1_d2=data_in
	temp1_char2=char_in
	var_tmp=var_in
	head_tmp=head_in(:,1)
      case(2) ! output data
        x_dim=out%n_var
	y_dim=out%n_rec
	allocate(temp1_d2(x_dim,y_dim))
	allocate(temp1_char2(x_dim,y_dim))
	allocate(var_tmp(x_dim))
	allocate(head_tmp(x_dim))
	temp1_d2=data_out
	temp1_char2=char_out
	var_tmp=var_out
	head_tmp=head_out(:,1)
    end select
!
! set variable do loop limits
    if(man(iman)%ind1>0) then
      lim1=man(iman)%ind1
      lim2=man(iman)%ind1
    else
      lim1=1
      lim2=x_dim
    endif
!
! print manipulation
    print*, '\t',trim(man(iman)%typ)
    write(unit=33,*) trim(man(iman)%typ)
!
! scan through manipulations
    select case(man(iman)%typ)
!
!----------------------------------------------------------
! Convert to text
!----------------------------------------------------------
! convert either a real or integer value to a character string
      case('con_2_txt')
	indx1=man(iman)%ind1 ! variable number
        print*, '\tconvert variable ',indx1,' to text'
	write(unit=33,*) '\tconvert variable ',indx1,' to text'
	fmt=var_tmp(indx1)%fmt1
        if(trim(var_tmp(indx1)%typ)=='real') then
	  do irec=1,y_dim
	    write(junk,fmt=fmt) temp1_d2(indx1,irec)
	    junk=adjustl(junk)
	    temp1_char2(indx1,irec)=trim(junk)
	  enddo
	elseif(trim(var_tmp(indx1)%typ)=='integer') then
	  do irec=1,y_dim
	    nval=temp1_d2(indx1,irec)
	    write(junk,fmt=fmt) nval
	    junk=adjustl(junk)
	    temp1_char2(indx1,irec)=trim(junk)
	  enddo
	else
	  Print*, 'Error: incorrect variable type: ',trim(var_tmp(indx1)%typ)
	  stop
	endif
	var_tmp(indx1)%fmt1=trim(man(iman)%txt1)
	var_tmp(indx1)%typ='char'
!
!----------------------------------------------------------
! append text
!----------------------------------------------------------
! append character string
      case('app_txt')
	indx1=man(iman)%ind1 ! variable number
        print*, '\tappend ',trim(man(iman)%txt1),' to variable ',indx1
	write(unit=33,*) '\tappend ',trim(man(iman)%txt1),' to variable ',indx1
	junk=trim(man(iman)%txt1)
	do irec=1,y_dim
	  temp1_char2(indx1,irec)=temp1_char2(indx1,irec)//trim(junk)
        enddo
!
!----------------------------------------------------------
! prepend text
!----------------------------------------------------------
! append character string
      case('pre_txt')
	indx1=man(iman)%ind1 ! variable number
        print*, '\tprepend ',trim(man(iman)%txt1),' to variable ',indx1
	write(unit=33,*) '\tappend ',trim(man(iman)%txt1),' to variable ',indx1
	junk=trim(man(iman)%txt1)
	do irec=1,y_dim
	  temp1_char2(indx1,irec)=trim(junk)//temp1_char2(indx1,irec)
        enddo
!
!----------------------------------------------------------
! make a 2-D pdf of values
!----------------------------------------------------------
! make a pdf of the values
! Note: the median calculation assumes you have sorted the records by the y value
      case('make_2pdf')
	indx1=man(iman)%ind1 ! x variable number
	indx2=man(iman)%ind2 ! y variable number
	nval=man(iman)%ind3  ! number of bins
	write(unit=33,*) '\tmake a pdf x= ',trim(var_tmp(indx1)%txt1),' y= ',trim(var_tmp(indx2)%txt1)
!
! allocate variables
	allocate(temp2_d2(8,nval))     ! statistcs variable
	allocate(temp3_d2(y_dim,nval)) ! binned data
        allocate(temp_int2(2,nval))    ! counts per bin
	temp2_d2=0.
	temp3_d2=miss_val_real
	temp_int2=0
! temp2_d2(1,icnt)=x var bin values
! temp2_d2(2,icnt)=fraction tot pts in bin
! temp2_d2(3,icnt)=fraction valid points per bin
! temp2_d2(4,icnt)=mean value y var in bin
! temp2_d2(5,icnt)=standard deviation y var in bin
! temp2_d2(6,icnt)=min y var in bin
! temp2_d2(7,icnt)=median y var in bin
! temp2_d2(8,icnt)=max y var in bin
! temp_int2(1,icnt)=num points per bin
! temp_int2(2,icnt)=num valid points per bin
!
! min and max bin values
        if(trim(man(iman)%txt1)=='auto') then
	  do irec=1,y_dim
	    cnt1=irec
	    if(temp1_d2(indx1,irec)/=miss_val_real) then
	      valmin=temp1_d2(indx1,irec)
	      valmax=temp1_d2(indx1,irec)
	      exit
	    endif
	  enddo
	  do irec=cnt1,y_dim
	      if(temp1_d2(indx1,irec)/=miss_val_real) then
	        valmin=min(valmin,temp1_d2(indx1,irec))
	        valmax=max(valmax,temp1_d2(indx1,irec))
	      endif
	  enddo
	elseif(trim(man(iman)%txt1)=='man') then
          valmin=man(iman)%val1
          valmax=man(iman)%val2
	else
	  print*, 'Error: incorrect min/max option: ',trim(man(iman)%txt1)
	  stop
	endif
        dval=(valmax-valmin)/real(nval)
	write(unit=33,*) 'valmin: ',valmin
	write(unit=33,*) 'valmax: ',valmax
	write(unit=33,*) 'dval: ',dval
!
! bin values
	do icnt=1,nval
	  temp2_d2(1,icnt)=valmin+(real(icnt)-0.5)*dval
	enddo
!
! bin data
	do irec=1,y_dim
	  if(temp1_d2(indx1,irec)/=miss_val_real) then
	    icnt=int((temp1_d2(indx1,irec)-valmin)/dval)+1 ! bin index
            if(trim(man(iman)%txt2)=='include') then ! include point outside of x-range
	      if(icnt>nval) icnt=nval
              if(icnt<1) icnt=1
            endif
            if(icnt>=1.and.icnt<=nval) then
	      temp_int2(1,icnt)=temp_int2(1,icnt)+1
	      temp3_d2(temp_int2(1,icnt),icnt)=temp1_d2(indx2,irec)
	    endif
	  endif
	enddo
!
! Compress binned data by removing missing values
        allocate(temp1_d1(y_dim))  ! temp array for binned values
	do icnt=1,nval
	  temp1_d1=miss_val_real
	  do irec=1,y_dim
	    if(temp3_d2(irec,icnt)/=miss_val_real) then
	      temp_int2(2,icnt)=temp_int2(2,icnt)+1.
	      temp1_d1(temp_int2(2,icnt))=temp3_d2(irec,icnt)
	    endif
	  enddo
	  temp3_d2(:,icnt)=temp1_d1
	enddo
        deallocate(temp1_d1)  ! temp array for binned values
!
! calculate bin fractions
	cnt1=0.
	do icnt=1,nval
	  cnt1=cnt1+temp_int2(1,icnt)
	enddo
	do icnt=1,nval
	  temp2_d2(2,icnt)=real(temp_int2(1,icnt))/real(cnt1)*100.
	  if(real(temp_int2(1,icnt))>0) temp2_d2(3,icnt)=real(temp_int2(2,icnt))/real(temp_int2(1,icnt))*100.
	enddo
!
! calculate mean per bin
	do icnt=1,nval
	  do irec=1,temp_int2(2,icnt)
            temp2_d2(4,icnt)=temp2_d2(4,icnt)+temp3_d2(irec,icnt)
	  enddo
	  if(temp_int2(2,icnt)/=0) then
	    temp2_d2(4,icnt)=temp2_d2(4,icnt)/real(temp_int2(2,icnt))
	  else
	    temp2_d2(4,icnt)=miss_val_real
	  endif
	enddo
!
! calc standard deviation per bin
	do icnt=1,nval
	  do irec=1,temp_int2(2,icnt)
            val1=temp2_d2(4,icnt)-temp3_d2(irec,icnt)
	    temp2_d2(5,icnt)=temp2_d2(5,icnt)+val1*val1
	  enddo
	  if(temp_int2(2,icnt)/=0) then
	    temp2_d2(5,icnt)=sqrt(temp2_d2(5,icnt)/real(temp_int2(2,icnt)))
	  else
	    temp2_d2(5,icnt)=miss_val_real
	  endif
	enddo
!
! calc median per bin
	do icnt=1,nval
	  if(temp_int2(2,icnt)>0) then
	    temp2_d2(6,icnt)=temp3_d2(1,icnt)                 ! min
	    irec=temp_int2(2,icnt)/2
	    if(irec>0) temp2_d2(7,icnt)=temp3_d2(irec,icnt)   ! median	  
	    temp2_d2(8,icnt)=temp3_d2(temp_int2(2,icnt),icnt) ! max
	  else
	    temp2_d2(6,icnt)=miss_val_real   ! min
	    temp2_d2(7,icnt)=miss_val_real   ! median	  
	    temp2_d2(8,icnt)=miss_val_real   ! max
	  endif
	enddo
!
! write to processing file
        write(unit=33,*) 'Tot records: ', y_dim
        write(unit=33,*) 'Tot valid records: ', cnt2
        if(trim(man(iman)%txt1)/='include') write(unit=33,*) 'Tot records in range: ', cnt1
        fmt='(a5,1x,a12,1x,a5,1x,a12,1x,a5,1x,6(a12,1x))'
	write(unit=33, fmt=fmt) 'bin','x_mean','npts','nfrac(%)','valpts','val(%)','y_mean','std','min','med','max'
        fmt='(i5,1x,f12.4,1x,i5,1x,f12.4,1x,i5,1x,6(f12.4,1x))'
	do icnt=1,nval
	  write(unit=33, fmt=fmt) icnt, temp2_d2(1,icnt),temp_int2(1,icnt),temp2_d2(2,icnt),temp_int2(2,icnt),temp2_d2(3,icnt),temp2_d2(4,icnt),temp2_d2(5,icnt),temp2_d2(6,icnt),temp2_d2(7,icnt),temp2_d2(8,icnt)
	enddo
! temp2_d2(1,icnt)=x var bin values
! temp2_d2(2,icnt)=fraction tot pts in bin
! temp2_d2(3,icnt)=fraction valid points per bin
! temp2_d2(4,icnt)=mean value y var in bin
! temp2_d2(5,icnt)=standard deviation y var in bin
! temp2_d2(6,icnt)=min y var in bin
! temp2_d2(7,icnt)=median y var in bin
! temp2_d2(8,icnt)=max y var in bin
! temp_int2(1,icnt)=num points per bin
! temp_int2(2,icnt)=num valid points per bin
	deallocate(temp2_d2)
	deallocate(temp3_d2)
        deallocate(temp_int2)
!
!----------------------------------------------------------
! remove outlier values
!----------------------------------------------------------
! remove outlier values greater than two standard deviations from the mean
      case('rm_out_gt')
	indx1=man(iman)%ind1 ! variable number
	write(unit=33,*) '\tRemove outliers from ',indx1, ' ',trim(var_tmp(indx1)%txt1)
!
! calc mean and standard deviation
	cnt1=0
	val1=0. ! mean
	val2=0. ! standard deviation
	do irec=1,y_dim
	  if(temp1_d2(indx1,irec)/=miss_val_real) then
	    cnt1=cnt1+1 
	    val1=val1+temp1_d2(indx1,irec)
	  endif
	enddo
	if(icnt>0) val1=val1/real(cnt1)
	do irec=1,y_dim
          if(temp1_d2(indx1,irec)/=miss_val_real) val2=val2+(val1-temp1_d2(indx1,irec))**2.
        enddo
        if(cnt1/=0) then
          val2=sqrt(val2/real(cnt1))
        else
          val1=miss_val_real
          val2=miss_val_real
        endif
        write(unit=33,*) 'Mean: ',val1
        write(unit=33,*) 'STD: ',val2
!
! remove outliers
	cnt1=0
        fmt='(a12,1x,a12,1x,a12,1x,a12)'
	write(unit=33, fmt=fmt) 'count', 'record','criteria','value'
        fmt='(i12,1x,i12,1x,f12.4,1x,f12.4)'
	do irec=1,y_dim
	  if(temp1_d2(indx1,irec)/=miss_val_real) then
	    val3=abs((temp1_d2(indx1,irec)-val1)/(2.*val2))
	    if(val3>1) then
	      cnt1=cnt1+1
	      write(unit=33, fmt=fmt) cnt1, irec,val3,temp1_d2(indx1,irec)
              temp1_d2(indx1,irec)=miss_val_real
	    endif
	  endif
	enddo
        write(unit=33,*) 'Tot outliers: ',cnt1
!
!----------------------------------------------------------
! look up values from map
!----------------------------------------------------------
! right now this is restricted to commas and periods
      case('map_lookup')
        print*, '\tLook up values from a map'
	write(unit=33,*) '\tLook up values from a map'
	if(man(iman)%num==1) then
	  print*, 'Error: only do this to output array'
	  write(unit=33,*) 'Error: only do this to output array'
	  stop
	endif
        call map_look_up(iman)
!
!----------------------------------------------------------
! reformat date:time
!----------------------------------------------------------
! reformats the date to a standard format using a python script
! assumes in/out variables are both are character 
! File_in/file_out refer to the input and output files of the python script
      case('date_refmt')
	write(unit=33,*) '\treformat date to Std'
	indx1=man(iman)%ind1 ! output variable number
!
! input/output data files for python script
        file_in=trim(path(i_pat_tmp)%path1)//'temp1'
        file_out=trim(path(i_pat_tmp)%path1)//'temp2'
!
! write records to temporary file
        open(unit=22,file=trim(file_in),form='formatted')
	fmt=trim(var(indx1)%fmt1)
        do iy=1,y_dim
	  write(unit=22,fmt=fmt) temp1_char2(indx1,iy)
        enddo
        close(unit=22)
!
! command to execute python script
!  <date/time column file> -o <output file> -f <Python strptime format string>
!/usr/bin/python /sharehome/hwilcox/reformat_dates_to_gtnp.py -i date_time_column.csv -o reformatted_dt.csv -f '%Y%m%dT%H%M'
        cmd=trim(path(i_pat_python)%path1)//'reformat_dates_to_gtnp.py'
        cmd=trim(cmd)//' -i '//trim(file_in)
        cmd=trim(cmd)//' -o '//trim(file_out)
        cmd=trim(cmd)//' -f '//trim(man(iman)%txt1)
!
! call system command
        call system( trim(cmd) )
!
! read records from temporary file
        open(unit=22,file=trim(file_out),form='formatted')
	fmt=trim(var(indx1)%fmt1)
        do iy=1,y_dim
	  read(unit=22,fmt=fmt) temp
	  temp1_char2(indx1,iy)=trim(temp)
        enddo
        close(unit=22)
!
!----------------------------------------------------------
! create real date
!----------------------------------------------------------
! calculates a date date given year, month, and dom
! Assumes measurement taken at noon on dom
! accounts for leap year
      case('date_real')
	write(unit=33,*) '\tcreate date real'
	if(man(iman)%num==1) then
	  write(unit=33,*) 'Error: only do this to output data'
	  stop
	endif
	indx1=man(iman)%ind1 ! output variable number
	indx2=man(iman)%ind2 ! input year variable number
	indx3=man(iman)%ind3 ! input month variable number
	indx4=man(iman)%ind4 ! input day of month (dom) variable number
!
! loop through records
        do iy=1,y_dim
	  year=data_in(indx2,iy)
	  mon=data_in(indx3,iy)
!
! check for leap year; flag = .true. for leap year
          flag=.false.
          if(mod(year,4)==0) then
            if(mod(year,100)==0) then
              if(mod(year,400)==0) flag=.true.
            else
              flag=.true.
            endif
          endif
!
! calculate date
          if(flag) then ! leap year
	    temp1_d2(indx1,iy)=data_in(indx2,iy) + real(doy1_mon_leap(mon))/366. + (data_in(indx4,iy)-0.5)/366.
          else ! regular year
	    temp1_d2(indx1,iy)=data_in(indx2,iy) + real(doy1_mon(mon))/365. + (data_in(indx4,iy)-0.5)/365.
	  endif
        enddo
!
!----------------------------------------------------------
! convert to character
!----------------------------------------------------------
! converts a variable from real or integer to character string
! assumes not time of day given so assume noon
      case('conv_char')
	write(unit=33,*) '\tconvert to character'
	if(man(iman)%num==1) then
	  write(unit=33,*) 'Error: only do this to output data'
	  stop
	endif
	indx1=man(iman)%ind1 ! input variable number
	indx2=man(iman)%ind2 ! output variable number
!
! calculate date
	fmt=trim(var(indx1)%fmt1)
	if(trim(var(indx1)%typ)=='integer') then
          do iy=1,y_dim
	    num=data_in(indx1,iy)
	    write(text,fmt=fmt) num
	    temp1_char2(indx2,iy)=trim(text)
          enddo
	endif
	if(trim(var(indx1)%typ)=='real') then
          do iy=1,y_dim
	    write(text,fmt=fmt) data_in(indx1,iy)
	    temp1_char2(indx2,iy)=trim(text)
          enddo
	endif
!
! add prefix
        if(trim(man(iman)%txt1)/='na') then
          do iy=1,y_dim
	    temp1_char2(indx2,iy)=trim(man(iman)%txt1)//trim(temp1_char2(indx2,iy))
          enddo
	endif
!
!----------------------------------------------------------
! create character date
!----------------------------------------------------------
! calculates a character date given year, month, and dom
! assumes not time of day given so assume noon
      case('date_char')
	write(unit=33,*) '\tcreate date character (yyyy-mm-dd HH:MM)'
	if(man(iman)%num==1) then
	  write(unit=33,*) 'Error: only do this to output data'
	  stop
	endif
	indx1=man(iman)%ind1 ! output variable number
	indx2=man(iman)%ind2 ! input year variable number
	indx3=man(iman)%ind3 ! input month variable number
	indx4=man(iman)%ind4 ! input day of month (dom) variable number
!
! calculate date
        do iy=1,y_dim
!
! year
	  fmt=trim(var(indx2)%fmt1)
	  year=data_in(indx2,iy)
	  write(temp,fmt=fmt) year
	  text=trim(temp)//'-'
!
! month
	  fmt=trim(var(indx3)%fmt1)
	  mon=data_in(indx3,iy)
	  write(temp,fmt=fmt) mon
	  temp=adjustl(temp)
	  text=trim(text)//trim(temp)//'-'
!
! day-of-month
	  fmt=trim(var(indx4)%fmt1)
	  mon=data_in(indx4,iy)
	  write(temp,fmt=fmt) mon
	  temp=adjustl(temp)
	  text=trim(text)//trim(temp)
	  temp1_char2(indx1,iy)=trim(text)//' 12:00'
        enddo
!
!----------------------------------------------------------
! create character mid-month date
!----------------------------------------------------------
! calculates a mid-month character date given year and month
      case('mid_mon')
	write(unit=33,*) '\tcreate character mid-month date'
	if(man(iman)%num==1) then
	  write(unit=33,*) 'Error: only do this to output data'
	  stop
	endif
	indx1=man(iman)%ind1 ! output variable number
	indx2=man(iman)%ind2 ! input year variable number
	indx3=man(iman)%ind3 ! input month variable number
!
! locate inout variables
        do ivar=1, n_var
	  if(trim(head_tmp(indx2))==trim(var(ivar)%txt1)) imap2=ivar
	  if(trim(head_tmp(indx3))==trim(var(ivar)%txt1)) imap3=ivar
	enddo 
!
! calculate date
        do iy=1,y_dim
!
! year
	  fmt=trim(var(imap2)%fmt1)
	  year=data_in(indx2,iy)
	  write(temp,fmt=fmt) year
	  text=trim(temp)//'-'
!
! month
	  fmt=trim(var(imap3)%fmt1)
	  mon=data_in(indx3,iy)
	  write(temp,fmt=fmt) mon
	  text=trim(text)//trim(temp)
!
! day-of-month
          text=trim(text)//trim(mid_month(mon))
	  temp1_char2(indx1,iy)=trim(text)
        enddo
!
!----------------------------------------------------------
! calculate time zone
!----------------------------------------------------------
      case('timezone')
        print*, '\tcalculate time zone'
	write(unit=33,*) '\tcalculate time zone'
	if(man(iman)%num==1) then
	  print*, 'Error: only do this to output array'
	  write(unit=33,*) 'Error: only do this to output array'
	  stop
	endif
        call calc_time_zone(iman)
!
!----------------------------------------------------------
! calculate minimum distance to point
!----------------------------------------------------------
! spherical earth, straight distance
      case('min_dist')
	write(unit=33,*) '\tcalculate minimum distance'
	indx1=man(iman)%ind1 ! lon index
	indx2=man(iman)%ind2 ! lat index
	indx3=man(iman)%ind3 ! point path number
	indx4=man(iman)%ind4 ! display variable number
	indx5=man(iman)%ind5 ! display variable number
	indx6=man(iman)%ind6 ! filter flag (1=filter)
!
! count number of points
        allocate(temp1_d1(2))
	filename=trim(path(indx3)%path1)
	open(unit=44,file=trim(filename),form='formatted')
        read(unit=44,*) junk
        num=0
        do irec=1,10e26
          read(unit=44,*, iostat=status) temp1_d1
          if(status<0) exit
          num=num+1
        enddo
        close(unit=44)
        deallocate(temp1_d1)
!
! read in latitudes and longitudes
        allocate(temp2_d2(2,num))
	open(unit=44,file=trim(filename),form='formatted')
        read(unit=44,*) junk
        do irec=1,num
          read(unit=44,*) temp2_d2(:,irec)
        enddo
        close(unit=44)
!
! calculate distances
	do icnt=1,num
	  if(temp2_d2(1,icnt)/=miss_val_real) then
	    call distance(temp1_d2(indx1,1),temp1_d2(indx2,1),temp2_d2(1,icnt),temp2_d2(2,icnt),valmin)
	    imin=1
	    do irec=1,y_dim
	      call distance(temp1_d2(indx1,irec),temp1_d2(indx2,irec),temp2_d2(1,icnt),temp2_d2(2,icnt),val1)
	      if(val1<valmin) then
	        imin=irec
	        valmin=val1
	      endif
	    enddo
            fmt='(i3,2x,i6,2x,i6,3(2x,f15.8)'
	    if(indx6==1) then
	      if(valmin<man(iman)%val1) print(fmt), ifil,icnt,imin,valmin,temp1_d2(indx4,imin),temp1_d2(indx5,imin)
	    else
	      print(fmt), ifil, icnt,imin,valmin,temp1_d2(indx4,imin),temp1_d2(indx5,imin)
	    endif
	  endif
	enddo
!
!----------------------------------------------------------
! calculate distance to next point
!----------------------------------------------------------
! spherical earth, straight distance
      case('distance')
	write(unit=33,*) '\tcalculate distance'
	indx1=man(iman)%ind1 ! lon index
	indx2=man(iman)%ind2 ! lat index
	indx3=man(iman)%ind3 ! dist index
	do irec=1,y_dim-1
	  call distance(temp1_d2(indx1,irec),temp1_d2(indx2,irec),temp1_d2(indx1,irec+1),temp1_d2(indx2,irec+1),temp1_d2(indx3,irec))
	enddo
!
!----------------------------------------------------------
! calculate total distance
!----------------------------------------------------------
      case('dist_tot')
	write(unit=33,*) '\tcalculate total distance'
	indx1=man(iman)%ind1 ! distance index
	val1=0.
	do irec=1,y_dim
	  if(temp1_d2(indx1,irec)/=miss_val_real) val1=val1+temp1_d2(indx1,irec)
	enddo
	write(unit=33,*) '\tTotal distance: ',val1
!
!----------------------------------------------------------
! remove punctuation from character data
!----------------------------------------------------------
! right now this is restricted to commas and periods
      case('rm_punct')
	write(unit=33,*) '\tremove punctuation'
        fmt='(a4,2x,a4,2x,a4,2x,a50,2x,a50)'
	write(unit=33,fmt=fmt) 'rec','id','qc_flg','old text', 'new text'
        fmt='(i4,2x,i4,2x,i4,2x,a50,2x,a50)'
	indx1=man(iman)%ind1 ! variable index
	idvar=man(iman)%ind2 ! id index
	indx3=man(iman)%ind3 ! qc flag index
	do irec=1,y_dim
	  temp=trim(temp1_char2(indx1,irec))
	  temp=adjustl(temp)
	  num=len(temp)
	  cnt1=0
	  text=''
	  flag=.false.
	  do itxt=1,num
	    if(temp(itxt:itxt)=='.') then
	      flag=.true.
	      temp1_d2(indx3,irec)=1
	    elseif(temp(itxt:itxt)==',') then
	      flag=.true.
	      cnt1=cnt1+1
	      text(cnt1:cnt1)=';'
	      temp1_d2(indx3,irec)=1
	    else
	      cnt1=cnt1+1
	      text(cnt1:cnt1)=temp(itxt:itxt)
	    endif
	  enddo
	  if(flag) then
	    itxt=temp1_d2(idvar,irec)
	    ivar=temp1_d2(indx3,irec)
	    write(unit=33,fmt=fmt) irec,itxt,ivar,trim(temp1_char2(indx1,irec)),trim(text)
	  endif
	  temp1_char2(indx1,irec)=trim(text)
	enddo
!
!----------------------------------------------------------
! remove single character from text data
!----------------------------------------------------------
! remove a single character
      case('rm_char')
	write(unit=33,*) '\tremove ', trim(man(iman)%txt1), ' in variable ', trim(head_tmp(man(iman)%ind1))
        fmt='(a4,2x,a50,2x,a50)'
	if(trim(man(iman)%txt3)=='save') write(unit=33,fmt=fmt) 'rec','old text', 'new text'
        fmt='(i4,2x,a50,2x,a50)'
	indx1=man(iman)%ind1 ! variable index
	idvar=man(iman)%ind2 ! id index
	indx3=man(iman)%ind3 ! qc flag index
	cnt1=0
	do irec=1,y_dim
	  temp1=trim(temp1_char2(indx1,irec))
	  temp1=adjustl(temp1)
	  num=len(trim(temp1))
	  flag=.false.
	  temp2=''
	  do itxt=1,num
	    if(temp1(itxt:itxt)/=trim(man(iman)%txt1)) then
	      temp2=trim(temp2)//temp1(itxt:itxt)
	    else
	      flag=.true.
	      cnt1=cnt1+1
	    endif
	  enddo
	  temp1_char2(indx1,irec)=trim(temp2)
	  if(flag.and.trim(man(iman)%txt3)=='save') then
	    write(unit=33,fmt=fmt) irec,trim(temp1),trim(temp1_char2(indx1,irec))
	  endif
	enddo
	print*, cnt1, ' records changed'
	write(unit=33,*) cnt1, ' records changed'
!
!----------------------------------------------------------
! conditional if multiply
!----------------------------------------------------------
! remove a single character
      case('if_mult')
	indx1=man(iman)%ind1 ! target variable index
	indx2=man(iman)%ind2 ! conditional if variable index
	write(unit=33,*) '\tIf ',trim(head_tmp(indx1)),' has ', trim(man(iman)%txt1), ' mult ', trim(head_tmp(indx1)), ' by ',man(iman)%val1
        fmt='(a4,2x,a50,2x,a50)'
	if(trim(man(iman)%txt3)=='save') write(unit=33,fmt=fmt) 'rec','old text', 'new val'
        fmt='(i4,2x,a50,2x,f15.7)'
!
! length of search text string
	temp1=trim(man(iman)%txt1)
	temp1=adjustl(temp1)
        cnt2=len(trim(temp1))-1

	cnt1=0
	do irec=1,y_dim
	  temp1=trim(temp1_char2(indx2,irec))
	  temp1=adjustl(temp1)
	  num=len(trim(temp1))
	  flag=.false.
          if(num>=cnt2) then
	    do itxt=1,num-cnt2
	      if(temp1(itxt:itxt+cnt2)==trim(man(iman)%txt1)) flag=.true.
	    enddo
	  endif
	  if(flag) then
	    if(temp1_d2(indx1,irec)/=miss_val_real) temp1_d2(indx1,irec)=temp1_d2(indx1,irec)*man(iman)%val1
	    cnt1=cnt1+1
	    if(trim(man(iman)%txt3)=='save') write(unit=33,fmt=fmt) irec, trim(temp1), temp1_d2(indx1,irec)
	  endif
	enddo
	print*, cnt1, ' records changed'
	write(unit=33,*) cnt1, ' records changed'
!
!----------------------------------------------------------
! replace single character from text data
!----------------------------------------------------------
! replace a single character
      case('rep_char')
	write(unit=33,*) '\treplace ', trim(man(iman)%txt1), ' with ', trim(man(iman)%txt2),' in variable ', trim(head_tmp(man(iman)%ind1))
        fmt='(a4,2x,a50,2x,a50)'
	if(trim(man(iman)%txt3)=='save') write(unit=33,fmt=fmt) 'rec','old text', 'new text'
        fmt='(i4,2x,a50,2x,a50)'
	indx1=man(iman)%ind1 ! variable index
	idvar=man(iman)%ind2 ! id index
	indx3=man(iman)%ind3 ! qc flag index
	cnt1=0
	do irec=1,y_dim
	  temp1=trim(temp1_char2(indx1,irec))
	  temp1=adjustl(temp1)
	  num=len(trim(temp1))
	  flag=.false.
	  temp2=''
	  do itxt=1,num
	    if(temp1(itxt:itxt)/=trim(man(iman)%txt1)) then
	      temp2=trim(temp2)//temp1(itxt:itxt)
	    else
	      flag=.true.
	      temp2=trim(temp2)//trim(man(iman)%txt2)
	      cnt1=cnt1+1
	    endif
	  enddo
	  temp1_char2(indx1,irec)=trim(temp2)
	  if(flag.and.trim(man(iman)%txt3)=='save') then
	    write(unit=33,fmt=fmt) irec,trim(temp1),trim(temp1_char2(indx1,irec))
	  endif
	enddo
	print*, cnt1, ' records changed'
	write(unit=33,*) cnt1, ' records changed'
!
!----------------------------------------------------------
! Remove everything to left of character
!----------------------------------------------------------
! removes all characters to the left of a specific character
! assumes character occurs only once (or rather finds the first occurance)
      case('r_lt_char')
	write(unit=33,*) '\tRemove text left of ', trim(man(iman)%txt1), ' in variable ', trim(head_tmp(man(iman)%ind1))
        fmt='(a4,2x,a50,2x,a50,2x,a50)'
	if(trim(man(iman)%txt3)=='save') write(unit=33,fmt=fmt) 'rec','ID','old text', 'new text'
        fmt='(i4,2x,a50,2x,a50,2x,a50)'
	indx1=man(iman)%ind1 ! variable index
	indx2=man(iman)%ind2 ! id index
	cnt1=0
	do irec=1,y_dim
	  temp1=trim(temp1_char2(indx1,irec))
	  temp1=adjustl(temp1)
	  num=len(trim(temp1))
	  flag=.false.
	  indx6=1
	  do itxt=1,num
	    if(temp1(itxt:itxt)==trim(man(iman)%txt1)) then
	      indx6=itxt+1
	      cnt1=cnt1+1
	      flag=.true.
	      exit
	    endif
	  enddo
	  if(flag) then
	    if(indx6>num) then
	      temp1_char2(indx1,irec)=trim(man(iman)%txt2)
	    else
	      temp1_char2(indx1,irec)=trim(temp1(indx6:num))
	    endif
	    if(trim(man(iman)%txt3)=='save') write(unit=33,fmt=fmt) irec,trim(temp1_char2(indx2,irec)),trim(temp1),trim(temp1_char2(indx1,irec))
	  endif
	enddo
	print*, cnt1, ' records changed'
	write(unit=33,*) cnt1, ' records changed'
!
!----------------------------------------------------------
! Remove everything to right of character
!----------------------------------------------------------
! removes all characters to the left of a specific character
! assumes character occurs only once (or rather finds the first occurance)
      case('r_rt_char')
	write(unit=33,*) '\tRemove text right of ', trim(man(iman)%txt1), ' in variable ', trim(head_tmp(man(iman)%ind1))
        fmt='(a4,2x,a50,2x,a50,2x,a50)'
	if(trim(man(iman)%txt3)=='save') write(unit=33,fmt=fmt) 'rec','ID','old text', 'new text'
        fmt='(i4,2x,a50,2x,a50,2x,a50)'
	indx1=man(iman)%ind1 ! variable index
	indx2=man(iman)%ind2 ! id index
	cnt1=0
	do irec=1,y_dim
	  temp1=trim(temp1_char2(indx1,irec))
	  temp1=adjustl(temp1)
	  num=len(trim(temp1))
	  flag=.false.
	  indx6=1
	  do itxt=1,num
	    if(temp1(itxt:itxt)==trim(man(iman)%txt1)) then
	      indx6=itxt-1
	      cnt1=cnt1+1
	      flag=.true.
	      exit
	    endif
	  enddo
	  
	  if(flag) then
	    if(indx6<=0) then
	      temp1_char2(indx1,irec)=trim(man(iman)%txt2)
	    else
	      temp1_char2(indx1,irec)=trim(temp1(1:indx6))
	    endif
	    if(trim(man(iman)%txt3)=='save') write(unit=33,fmt=fmt) irec,trim(temp1_char2(indx2,irec)),trim(temp1),trim(temp1_char2(indx1,irec))
	  endif
	enddo
	print*, cnt1, ' records changed'
	write(unit=33,*) cnt1, ' records changed'
!
!----------------------------------------------------------
! replace single character from text data
!----------------------------------------------------------
! remove values containing a specific character
! assumes a number containing some character like '?'
! assumes a number treated as a text variable
      case('rep_marg')
	write(unit=33,*) '\treplace ', trim(head_tmp(man(iman)%ind1)), ' values containing ',trim(man(iman)%txt1), ' with ', trim(man(iman)%txt2) 
        fmt='(a4,2x,a50,2x,a50)'
	if(trim(man(iman)%txt3)=='save') write(unit=33,fmt=fmt) 'rec','old text', 'new text'
        fmt='(i4,2x,a50,2x,a50)'
	indx1=man(iman)%ind1 ! variable index
	idvar=man(iman)%ind2 ! id index
	indx3=man(iman)%ind3 ! qc flag index
	cnt1=0
	do irec=1,y_dim
	  temp1=trim(temp1_char2(indx1,irec))
	  temp1=adjustl(temp1)
	  num=len(trim(temp1))
	  flag=.false.
	  temp2=''
	  do itxt=1,num
	    if(temp1(itxt:itxt)==trim(man(iman)%txt1)) then
	      flag=.true.
	      cnt1=cnt1+1
	    endif
	  enddo
	  if(flag) then
	    temp1_char2(indx1,irec)=trim(man(iman)%txt2)
	    if(trim(man(iman)%txt3)=='save') write(unit=33,fmt=fmt) irec,trim(temp1),trim(temp1_char2(indx1,irec))
	  endif
	enddo
	print*, cnt1, ' records changed'
	write(unit=33,*) cnt1, ' records changed'
!
!----------------------------------------------------------
! replace text 
!----------------------------------------------------------
! replace entire text record
      case('r_eq_txt')
	write(unit=33,*) '\treplace ', trim(man(iman)%txt1), ' with ', trim(man(iman)%txt2), ' in variable ', trim(head_tmp(man(iman)%ind1))
        fmt='(a4,2x,a50,2x,a50)'
	if(trim(man(iman)%txt3)=='save') write(unit=33,fmt=fmt) 'rec','old text', 'new text'
        fmt='(i4,2x,a50,2x,a50)'
	indx1=man(iman)%ind1 ! variable index
	idvar=man(iman)%ind2 ! id index
	indx3=man(iman)%ind3 ! qc flag index
	cnt1=0
	do irec=1,y_dim
	  if(trim(temp1_char2(indx1,irec))==trim(man(iman)%txt1)) then
	    if(trim(man(iman)%txt3)=='save') then
	      write(unit=33,fmt=fmt) irec,trim(temp1_char2(indx1,irec)),trim(man(iman)%txt2)
	    endif
	    temp1_char2(indx1,irec)=trim(man(iman)%txt2)
	    cnt1=cnt1+1
	  endif
	enddo
	print*, cnt1, ' records changed'
	write(unit=33,*) cnt1, ' records changed'
!
!----------------------------------------------------------
! fill header
!----------------------------------------------------------
! fill an empty input header
      case('fil_head')
        if(man(iman)%num==1) then
	  write(unit=33,*) '\t\tfill input header'
	  deallocate(head_in)
	  in%n_hed=1
	  allocate(head_in(in%n_var,in%n_hed))
	  do ivar=1,in%n_var
	    head_in(ivar,1)=trim(var(ivar)%txt1)
	  enddo
	endif
        if(man(iman)%num==2) then
	  write(unit=33,*) '\t\tfill output header'
	  write(unit=33,*) 'already done automatically'
	endif
!
!----------------------------------------------------------
! convert utm coordinates to latitude and longitude
!----------------------------------------------------------
! exit to external python script to convert from utm coordinates to latitude and longitude
      case('conv_utm')
	write(unit=33,*) '\tconvert utm to lat/lon'
	write(unit=33,*) '\t\tuse standard python script'
	indx1=man(iman)%ind1 ! zone index
	indx2=man(iman)%ind2 ! east coordinate index
	indx3=man(iman)%ind3 ! north coordinate index
	if(trim(man(iman)%txt1)=='N') then
	  tmp_text=',N'
	elseif(trim(man(iman)%txt1)=='S') then
	  tmp_text=',S'
	else
	  print*, 'Error: zone code must be N or S'
	  Print*, 'Zone code is ',trim(man(iman)%txt1)
	  stop
	endif
!
! write utm coordinates to file
        filename=trim(path(i_pat_tmp)%path1)//'temp1'
	open(unit=44,file=trim(filename),form='formatted')
!
! loop through coordinates
	do irec=1,y_dim
!
! east coordinate
	  write(temp,*) temp1_d2(indx2,irec)
	  temp=adjustl(temp)
	  text=trim(temp)//','
!
! north coordinate
	  write(temp,*) temp1_d2(indx3,irec)
	  temp=adjustl(temp)
	  text=trim(text)//trim(temp)//','
!
! zone	  
	  itxt=temp1_d2(indx1,irec)
	  fmt='(i4)'
	  write(temp,fmt=fmt) itxt
	  temp=adjustl(temp)
	  text=trim(text)//trim(temp)//',N'
!
! write to file
	  write(unit=44,*) trim(text)
	enddo
	close(unit=44)
!
! execute python script
!
! input/output data files for python script 
        file_in=trim(path(i_pat_tmp)%path1)//'temp1'  ! input file to script
        file_out=trim(path(i_pat_tmp)%path1)//'temp2' ! output file from script
!
! command to execute python script
        cmd=trim(path(i_pat_python)%path1)//'utm_to_latlong.py'
        cmd=trim(cmd)//' -i '//trim(file_in)
        cmd=trim(cmd)//' -o '//trim(file_out)
!
! call system command
print*, trim(cmd)
        call system(trim(cmd))
!
! read in latitudes and longitudes
	open(unit=44,file=trim(file_out),form='formatted')
	do irec=1,y_dim
	  read(unit=44,*) temp1_d2(indx3,irec), temp1_d2(indx2,irec)
	enddo
	close(unit=44)

        fmt='(a4,2x,a4,2x,a20,2x,a15,2x,a15)'
	write(unit=33,fmt=fmt) 'rec','zone','East','North', 'lat','lon'
        fmt='(i4,2x,i4,2x,i4,2x,a50,2x,a50)'
!
!----------------------------------------------------------
! Probability density function
!----------------------------------------------------------
! convert either a real or integer value to a character string
      case('pdf_var')
	indx1=man(iman)%ind1 ! variable number
        print*, '\tPDF variable ',indx1
	write(unit=33,*) '\tPDF variable ',indx1
!
!----------------------------------------------------------
! variable statistics
!----------------------------------------------------------
! calculates min, max, mean, standard deviation
      case('stats_var')
	write(unit=33,*) '\tVariable statistics'
        if(man(iman)%num==1) write(unit=33,*) '\t\tInput Variable Statistics'
        if(man(iman)%num==2) write(unit=33,*) '\t\tOutput Variable Statistics'
!
! allocate Stats variables
	n_stat=8
	allocate(temp2_d2(x_dim,n_stat))
!
! print Header
	fmt='(9(a14,1x))'
        write(unit=33,fmt=fmt) 'Variable','min','max','mean','std','totpts','valid_pts','pts_frac','n_outlier'
!
! loop through variables
	do ix=1,x_dim
!
! min and max value
!
! find first valid point
	  do iy=1,y_dim
	    cnt1=iy
	    if(temp1_d2(ix,iy)/=miss_val_real) then
	      val1=temp1_d2(ix,iy)
	      val2=temp1_d2(ix,iy)
	      exit
	    endif
	  enddo
!
! go through rest of points
	  if(cnt1<=y_dim) then
	    do iy=cnt1,y_dim
	      if(temp1_d2(ix,iy)/=miss_val_real) then
	        val1=min(val1,temp1_d2(ix,iy))
	        val2=max(val2,temp1_d2(ix,iy))
	      endif
	    enddo
	  endif
	  temp2_d2(ix,1)=val1
	  temp2_d2(ix,2)=val2
!
! mean value, standard deviation, valid points, coverage frac
          val1=0. 
          val2=0. 
	  cnt1=0
	  do iy=1,y_dim
	    if(temp1_d2(ix,iy)/=miss_val_real) then
	      val1=val1+temp1_d2(ix,iy)
	      cnt1=cnt1+1
	    endif
	  enddo
	  if(cnt1/=0) val1=val1/real(cnt1)
	  do iy=1,y_dim
	    if(temp1_d2(ix,iy)/=miss_val_real) val2=val2+(val1-temp1_d2(ix,iy))**2.
	  enddo
	  if(cnt1/=0) then
	    val2=sqrt(val2/real(cnt1))
	  else
	    val1=miss_val_real
	    val2=miss_val_real
	  endif
	  temp2_d2(ix,3)=val1
	  temp2_d2(ix,4)=val2
	  temp2_d2(ix,5)=real(y_dim)
	  temp2_d2(ix,6)=real(cnt1)
	  temp2_d2(ix,7)=real(cnt1)/real(y_dim)
!
! outliers
	  cnt1=0
	  do iy=1,y_dim
	    if(temp1_d2(ix,iy)/=miss_val_real) then
              val1=abs((temp1_d2(ix,iy)-temp2_d2(ix,4))/(2.*temp2_d2(ix,4))) 
	      if(val1>1) then
	        cnt1=cnt1+1
	      endif
	    endif
	  enddo
	  temp2_d2(ix,8)=cnt1
!
! write statistics
	  fmt='(a15)'
	  write(temp,fmt=fmt) trim(head_tmp(ix))
	  text=temp
	  fmt='(f14.3)'
	  do ivar=1,n_stat
	    write(temp,fmt=fmt) temp2_d2(ix,ivar)
	    text=trim(text)//' '//trim(temp)
	  enddo
          write(unit=33,*) trim(text)
	enddo
!
!----------------------------------------------------------
! variable median
!----------------------------------------------------------
! calculates median and quatiles for one variable
! assumes sorted by the variable first
      case('med_var')
	write(unit=33,*) '\tVariable median'
	indx1=man(iman)%ind1
!
! allocate Stats variables
	n_stat=7
	allocate(temp1_d1(n_stat))
!
! print Header
	fmt='(9(a14,1x))'
        write(unit=33,fmt=fmt) 'Variable','min','2.5%','25%','Median','75%','97.5%','max'
!
! find first valid point
	  do iy=1,y_dim
	    cnt1=iy
	    if(temp1_d2(indx1,iy)/=miss_val_real) exit
	  enddo
	  cnt2=y_dim-cnt1
!
! quartiles and median
          temp1_d1(1)=temp1_d2(indx1,cnt1) ! Min Value
          irec=cnt1+cnt2*0.025
	  if(irec==0) irec=1
          temp1_d1(2)=temp1_d2(indx1,irec) ! 2.5% Value
          irec=cnt1+cnt2*0.25
	  if(irec==0) irec=1
          temp1_d1(3)=temp1_d2(indx1,irec) ! 25% Value
          irec=cnt1+cnt2*0.5
	  if(irec==0) irec=1
	  temp1_d1(4)=temp1_d2(indx1,irec) ! median Value
          irec=cnt1+cnt2*0.75
	  if(irec==0) irec=1
          temp1_d1(5)=temp1_d2(indx1,irec) ! 75% Value
          irec=cnt1+cnt2*0.975
	  if(irec==0) irec=1
          temp1_d1(6)=temp1_d2(indx1,irec) ! 97.5% Value
          temp1_d1(7)=temp1_d2(indx1,y_dim) ! Max Value
!
! write statistics
	  fmt='(a15)'
	  write(temp,fmt=fmt) trim(head_tmp(indx1))
	  text=temp
	  fmt='(f14.3)'
	  do ivar=1,n_stat
	    write(temp,fmt=fmt) temp1_d1(ivar)
	    text=trim(text)//' '//trim(temp)
	  enddo
          write(unit=33,*) trim(text)
!
! deallocate Stats variables
	deallocate(temp1_d1)
!
!----------------------------------------------------------
! sort records in increasing order
!----------------------------------------------------------
! uses external python script
      case('sort')
        if(man(iman)%num==1) then
	  write(unit=33,*) '\tSort input records in increasing order'
	  case='in_temp'
        endif
	if(man(iman)%num==2) then
	  write(unit=33,*) '\tSort output records in increasing order'
	  case='out_temp'
	endif
        call make_csv_data_file(ifil,case)
!
! local sort variable numbers
	indx(1)=man(iman)%ind1
	indx(2)=man(iman)%ind2
	indx(3)=man(iman)%ind3
	indx(4)=man(iman)%ind4
	indx(5)=man(iman)%ind5
	indx(6)=man(iman)%ind6
	cnt1=0
	do icnt=1,6
	  if(indx(icnt)/=0) cnt1=cnt1+1
	enddo
!
! variable type mapping between DIT and python sort routine
	indx2=man(iman)%val1
	do ivar=1,cnt1
	  indx1=indx(ivar)
	  typ(ivar)=var_tmp(indx1)%typ
	  if(indx(ivar)==indx2) typ(ivar)='dt'
	enddo
!
! input/output data files for python script 
        file_in=trim(path(i_pat_tmp)%path1)//'temp1'  ! input file to script
        file_out=trim(path(i_pat_tmp)%path1)//'temp2' ! output file from script
!
! command to execute python script
        cmd=trim(path(i_pat_python)%path1)//'sort_by_columns.py'
        cmd=trim(cmd)//' -i '//trim(file_in)
        cmd=trim(cmd)//' -o '//trim(file_out)
!
! variables to sort
        text=qd//'['
	do ivar=1,cnt1
	  if(indx(ivar)/=0) then
	    fmt='(i2)'
	    write(temp, fmt=fmt) indx(ivar)-1
	    temp=adjustl(temp)
	    text=trim(text)//'('//trim(temp)//', '//qs//trim(typ(ivar))//qs//')'
	    if(ivar<cnt1) text=trim(text)//','
	  endif
	enddo
	text=trim(text)//']'//qd

        cmd=trim(cmd)//' -l '//trim(text)
	write(unit=33,*) 'sort cmd: ', trim(cmd)
!
! call system command
        call system( trim(cmd) )
!
! Read back in
        call read_csv_file(ifil, case)
!
!----------------------------------------------------------
! remove duplicate records
!----------------------------------------------------------
      case('rem_dup')
        write(unit=33,*) '\tRemove duplicate records'
	if(man(iman)%num==2) then
	  write(unit=33,*) 'Error: only do this to input array'
	  print*, 'Error: only do this to input array'
	  stop
	endif
!
! identify duplicate records
	allocate(temp_int1(y_dim))
	temp_int1=0
	indx1=man(iman)%ind1
	indx2=man(iman)%ind2
	num=0
	do irec=1,y_dim-1
	  do iy=irec+1,y_dim
	    if(temp_int1(irec)==0) then
	      if(temp1_d2(indx1,irec)==temp1_d2(indx1,iy).and.temp1_d2(indx2,irec)==temp1_d2(indx2,iy)) then
	        num=num+1
	        temp_int1(iy)=1
	      endif
	    endif
	  enddo
	enddo
!
! compress data file
        write(unit=33,*) '\t\tNum duplicate records: ',num
	if(num>0) then
	  allocate(temp2_d2(x_dim,y_dim))
	  temp2_d2=miss_val_real
	  in%n_rec=in%n_rec-num
	  out%n_rec=out%n_rec-num
	  irec=0
	  do iy=1,y_dim
	    if(temp_int1(iy)==0) then
	      irec=irec+1
	      temp2_d2(:,irec)=temp1_d2(:,iy)
	    elseif(trim(man(iman)%txt1)=='print') then
	      write(unit=33,*) '\t\tDelete ',iy, temp1_d2(indx1,iy),temp1_d2(indx2,iy)
	    endif
	  enddo
	  temp1_d2=temp2_d2
	  deallocate(temp2_d2)
	  deallocate(temp_int1)
	endif
!
!----------------------------------------------------------
! remove layers with no data from variable mapping file
!----------------------------------------------------------
      case('rem_nodata')
        write(unit=33,*) '\tRemove layers with no data'
	if(man(iman)%num==2) then
	  write(unit=33,*) 'Error: only do this to input array'
	  stop
	endif
!
! identify layers with no data and turn off copy flags
! treat empty layers like other extraneous variables
	num=0
        do ivar=1,n_var
          if(var(ivar)%flg2.and.var(ivar)%map=='copy') then
            do ix=1, in%n_var
	      if(trim(var(ivar)%txt1)==trim(head_tmp(ix))) exit
            enddo
	    if(maxval(temp1_d2(ix,:))==miss_val_real) then
	      if(var(ivar)%map=='copy') then
	        num=num+1
	        var(ivar)%flg2=.false.
	        var(ivar)%map='na'
	        write(unit=33,*) num,ivar,trim(var(ivar)%txt1)
	      endif
	    endif
          endif
        enddo
!
!----------------------------------------------------------
! count values per value
!----------------------------------------------------------
! counts the number of different values for a combination of 2 variables
! i.e. number of values for variable 2 per value of variable 1
! assumes the data is presorted first by var1 then by var2
      case('count_2val') 
	indx1=man(iman)%ind1
	indx2=man(iman)%ind2
	write(unit=33,*) '\tcount ',trim(head_tmp(indx2)),' values per ',trim(head_tmp(indx1))
	if(man(iman)%txt1=='all') then
	  write(unit=33,*) '\t\tsave everything in processing file'
	  fmt='(5(a15,2x))'
	  write(unit=33,fmt) 'Val1','val2','numval2','numrec','lastrec'
	  fmt='(f15.7,2x,f15.7,2x,i15,2x,i15,2x,i15)'
	endif
	if(man(iman)%txt1=='sum') then
	  write(unit=33,*) '\t\tsave only summary data in processing file'
	  fmt='(5(a15,2x))'
	  write(unit=33,fmt) trim(head_tmp(indx1)),'num '//trim(head_tmp(indx2)), 'totrec','firstrec','lastrec'
	  fmt='(f15.7,2x,i15,2x,i15,2x,i15,2x,i15)'
	endif
!
! set counting variables
	val1=temp1_d2(indx1,1)
	val2=temp1_d2(indx2,1)
	cnt1=1 ! number different values for val1
	cnt2=1 ! number different values for val2 for each val1
	cnt3=0 ! total number records for val2
	cnt4=0 ! total number records for val1
!
! loop through all records
	do iy=1,y_dim
!
! start counting with first record
	  if(temp1_d2(indx1,iy)==val1.and.temp1_d2(indx2,iy)==val2) then
	    cnt3=cnt3+1
	    cnt4=cnt4+1
!
! var2 changes, but not var1: cnt2 increases by 1, reset cnt3
	  elseif(temp1_d2(indx1,iy)==val1.and.temp1_d2(indx2,iy)/=val2) then
	    if(man(iman)%txt1=='all') write(unit=33,fmt) val1, val2, cnt2,cnt3, iy-1
	    cnt2=cnt2+1
	    cnt3=1
	    cnt4=cnt4+1
	    val2=temp1_d2(indx2,iy)
!
! var1 changes: cnt1 increases by 1, reset cnt2 and cnt3
	  elseif(temp1_d2(indx1,iy)/=val1.and.temp1_d2(indx2,iy)/=val2) then
	    if(man(iman)%txt1=='all') write(unit=33,fmt) val1, val2, cnt2, cnt3, iy-1
	    if(man(iman)%txt1=='sum') write(unit=33,fmt) val1, cnt2, cnt4, iy-cnt4,iy-1
	    cnt1=cnt1+1
	    cnt2=1
	    cnt3=1
	    cnt4=1
	    val1=temp1_d2(indx1,iy)
	    val2=temp1_d2(indx2,iy)
	  endif
	enddo
!
! save last set of values 
	if(man(iman)%txt1=='all') write(unit=33,fmt) val1, val2, cnt2, cnt3, iy-1
	if(man(iman)%txt1=='sum') write(unit=33,fmt) val1, cnt2, cnt4, iy-cnt4,iy-1
!
! write totals
	write(unit=33,*) '\t\t',trim(head_tmp(indx1))//' has ',cnt1, ' different values'
!
!----------------------------------------------------------
! count values
!----------------------------------------------------------
! counts the number of different values of a single variable
! assumes the data is sorted by the variable
!
      case('count_val') 
	indx1=man(iman)%ind1
	write(unit=33,*) '\tcount values for ',trim(head_tmp(indx1))
	fmt='(3(a15,2x))'
	write(unit=33,fmt) 'Value','numrec','lastrec'
	fmt='(f15.7,2x,i15,2x,i15)'
!
! count records per value
	val1=temp1_d2(indx1,1)
	cnt1=1 ! number different values
	cnt2=0 ! number records per value
	do iy=1,y_dim
	  if(temp1_d2(indx1,iy)==val1) then
	    cnt2=cnt2+1
	  else
	    write(unit=33,fmt) val1, cnt2, iy-1
	    cnt1=cnt1+1
	    cnt2=1
	    val1=temp1_d2(indx1,iy)
	  endif
	enddo
!
! save last set of values
	write(unit=33,fmt) val1, cnt2, iy-1
!
! write totals
	write(unit=33,*) '\t\t',trim(head_tmp(indx1))//' has ',cnt1, ' different values'
!
!----------------------------------------------------------
! count records
!----------------------------------------------------------
      case('count_rec') 
	do ix=lim1,lim2
	  write(unit=33,*) '\tcount records'
!
! count valid records
	  cnt1=0
	  do iy=1,y_dim
	    if(temp1_d2(ix,iy)/=miss_val_real) then
	      cnt1=cnt1+1
	    endif
	  enddo
	  write(unit=33,*) '\t\t',trim(head_tmp(ix))//': ',cnt1, ' valid values'
	  write(unit=33,*) '\t\t','total number records: ',y_dim
	enddo
!
!----------------------------------------------------------
! check for non-integer values in integer variable
!----------------------------------------------------------
      case('chk_int')
	do ix=lim1,lim2
	  write(unit=33,*) '\tCheck ',trim(head_tmp(ix)), ' for non-integer values'
	  val1=man(iman)%val1
	  cnt1=0
	  do iy=1,y_dim
	    val1=mod(temp1_d2(ix,iy),1.)
	    if(val1/=0.) then
	      cnt1=cnt1+1
	      print*, cnt1,iy,temp1_d2(ix,iy)
	    endif
	  enddo
	enddo
!
!----------------------------------------------------------
! count non-real values in variable
!----------------------------------------------------------
! assumes variable is mix of text and number values
! assumes variable is treated as a text variable
      case('chk_real')
	indx1=man(iman)%ind1 ! variable index
	idvar=man(iman)%ind2 ! id index
	indx3=man(iman)%ind3 ! qc flag index
	write(unit=33,*) '\tCheck ',trim(head_tmp(indx1)), ' for non-number values'
        fmt='(a4,2x,a50)'
	if(trim(man(iman)%txt3)=='save') write(unit=33,fmt=fmt) 'rec','text'
        fmt='(i4,2x,a50)'
	cnt1=0
	do irec=1,y_dim
	  temp1=trim(temp1_char2(indx1,irec))
	  temp1=adjustl(temp1)
	  read(temp1,*, iostat=status) val1
          if(status/=0) then
	    cnt1=cnt1+1
	    if(trim(man(iman)%txt3)=='save')write(unit=33,fmt=fmt) irec,trim(temp1)
	  endif
	enddo
	print*, cnt1, ' non-number values'
	write(unit=33,*) cnt1, ' non-number values'
!
!----------------------------------------------------------
! convert variables from text to real numbers
!----------------------------------------------------------
      case('txt_2_real')
	lim1=man(iman)%ind1 ! start variable index
	lim2=man(iman)%ind2 ! end variabler index
	do ivar=lim1,lim2
!
! reset variable mapping
          var_tmp(ivar)%typ='real'
          var_tmp(ivar)%fmt1=trim(man(iman)%txt1)
!
! write to processing file
	  write(unit=33,*) '\tConvert ',trim(head_tmp(ivar)), ' from character to real'
	  if(trim(man(iman)%txt3)=='save') then
            fmt='(a4,2x,a50)'
	    write(unit=33,*) '\tBad numbers'
	    write(unit=33,fmt=fmt) 'rec','value'
            fmt='(i4,2x,a50)'
	  endif
!
! convert to real
	  cnt1=0
	  do irec=1,y_dim
	    temp1=trim(temp1_char2(ivar,irec))
	    temp1=adjustl(temp1)
	    read(temp1,*, iostat=status) val1
            if(status/=0) then
	      cnt1=cnt1+1
	      if(trim(man(iman)%txt3)=='save') write(unit=33,fmt=fmt) irec,trim(temp1)
	      temp1_d2(ivar,irec)=miss_val_real
	    else
	      temp1_d2(ivar,irec)=val1
	    endif
	  enddo
	  print*, cnt1, ' non-number values'
	  write(unit=33,*) cnt1, ' non-number values'
	enddo
!
!----------------------------------------------------------
! convert variables from text to real numbers
!----------------------------------------------------------
      case('txt_2_int')
	lim1=man(iman)%ind1 ! start variable index
	lim2=man(iman)%ind2 ! end variabler index
	do ivar=lim1,lim2
!
! reset variable mapping
          var_tmp(ivar)%typ='integer'
          var_tmp(ivar)%fmt1=trim(man(iman)%txt1)
!
! write to processing file
	  write(unit=33,*) '\tConvert ',trim(head_tmp(ivar)), ' from character to integer'
	  if(trim(man(iman)%txt3)=='save') then
            fmt='(a4,2x,a50)'
	    write(unit=33,*) '\tBad numbers'
	    write(unit=33,fmt=fmt) 'rec','value'
            fmt='(i4,2x,a50)'
	  endif
!
! convert to integer
	  cnt1=0
	  do irec=1,y_dim
	    temp1=trim(temp1_char2(ivar,irec))
	    temp1=adjustl(temp1)
	    read(temp1,*, iostat=status) val1
            if(status/=0) then
	      cnt1=cnt1+1
	      if(trim(man(iman)%txt3)=='save') write(unit=33,fmt=fmt) irec,trim(temp1)
	      temp1_d2(ivar,irec)=miss_val_real
	    else
	      temp1_d2(ivar,irec)=val1
	    endif
	  enddo
	  print*, cnt1, ' non-number values'
	  write(unit=33,*) cnt1, ' non-number values'
	enddo
!
!----------------------------------------------------------
! copy variable
!----------------------------------------------------------
! assumes variables all real
! returns missing if any are missing
      case('copy_var')
	indx1=man(iman)%ind1 ! target variable index
	indx2=man(iman)%ind2 ! first variable index
	write(unit=33,*) '\tCopy ',trim(head_tmp(indx1)), ' = ',trim(head_tmp(indx2))
	temp1_d2(indx1,:)=temp1_d2(indx2,:)
	temp1_char2(indx1,:)=temp1_char2(indx2,:)
!
!----------------------------------------------------------
! conditional if based on file number for character variables
!----------------------------------------------------------
! Assigns value to variable based on file number
! assumes character variable
      case('if_file_c')
	indx1=man(iman)%ind1 ! target variable index
	indx2=man(iman)%ind2 ! start file number
	indx3=man(iman)%ind3 ! end file number
	write(unit=33,*) '\tIf file=',indx2,'-',indx3, ', ',trim(head_tmp(indx1)),' is ', trim(man(iman)%txt1)
        if(ifil>=indx2.and.ifil<=indx3) temp1_char2(indx1,:)=trim(man(iman)%txt1)
!
!----------------------------------------------------------
! index records each file
!----------------------------------------------------------
! Assigns index number to each record
! assumes integer variable
      case('indx_file')
	indx1=man(iman)%ind1 ! target variable index
	write(unit=33,*) '\tIndex records for ',trim(head_tmp(indx1))
	do irec=1,y_dim
	  temp1_d2(indx1,irec)=real(irec)
	enddo
!
!----------------------------------------------------------
! conditional if based on file number for real/integer variables
!----------------------------------------------------------
! Assigns value to variable based on file number
! assumes real variable
      case('if_file')
	indx1=man(iman)%ind1 ! target variable index
	indx2=man(iman)%ind2 ! start file number
	indx3=man(iman)%ind3 ! end file number
	write(unit=33,*) '\tIf file=',indx2,'-',indx3, ', ',trim(head_tmp(indx1)),' is ', man(iman)%val1
        if(ifil>=indx2.and.ifil<=indx3) temp1_d2(indx1,:)=man(iman)%val1
!
!----------------------------------------------------------
! calculate average two variables
!----------------------------------------------------------
! assumes variables all real
! returns missing if any are missing
      case('cal_ave')
	indx1=man(iman)%ind1 ! target variable index
	indx2=man(iman)%ind2 ! first variable index
	indx3=man(iman)%ind3 ! second variable index
	write(unit=33,*) '\tCalculate average ',trim(head_tmp(indx1)), '=ave(',trim(head_tmp(indx2)),',',trim(head_tmp(indx3)),')'
	cnt1=0
	do irec=1,y_dim
	  flag=.true.
	  if(temp1_d2(indx2,irec)==miss_val_real) flag=.false.
	  if(temp1_d2(indx3,irec)==miss_val_real) flag=.false.
	  if(flag) then
	    temp1_d2(indx1,irec)=(temp1_d2(indx2,irec)+temp1_d2(indx3,irec))*.5
	    cnt1=cnt1+1
	  endif
	enddo
	print*, cnt1, ' values out of ',y_dim, ' records'
	write(unit=33,*) cnt1, ' values out of ',y_dim, ' records'
!
!----------------------------------------------------------
! calculate ratio of two variables
!----------------------------------------------------------
! assumes variables all real
! returns missing if any are missing
      case('cal_ratio')
	indx1=man(iman)%ind1 ! target variable index
	indx2=man(iman)%ind2 ! first variable index
	indx3=man(iman)%ind3 ! second variable index
	write(unit=33,*) '\tCalculate ratio ',trim(head_tmp(indx1)), '=',trim(head_tmp(indx2)),'/',trim(head_tmp(indx3))
	cnt1=0
	do irec=1,y_dim
	  flag=.true.
	  if(temp1_d2(indx2,irec)==miss_val_real) flag=.false.
	  if(temp1_d2(indx3,irec)==miss_val_real) flag=.false.
	  if(temp1_d2(indx3,irec)==0.) flag=.false.
	  if(flag) then
	    temp1_d2(indx1,irec)=temp1_d2(indx2,irec)/temp1_d2(indx3,irec)
	    cnt1=cnt1+1
	  endif
	enddo
	print*, cnt1, ' values out of ',y_dim, ' records'
	write(unit=33,*) cnt1, ' values out of ',y_dim, ' records'
!
!----------------------------------------------------------
! calculate scalar of variable
!----------------------------------------------------------
! assumes variables all real
! returns missing if any are missing
      case('cal_scale')
	indx1=man(iman)%ind1 ! target variable index
	indx2=man(iman)%ind2 ! first variable index
	write(unit=33,*) '\tCalculate ',trim(head_tmp(indx1)), '=',trim(head_tmp(indx2)),'*',man(iman)%val1
	cnt1=0
	do irec=1,y_dim
	  flag=.true.
	  if(temp1_d2(indx2,irec)==miss_val_real) flag=.false.
	  if(flag) then
	    temp1_d2(indx1,irec)=temp1_d2(indx2,irec)*man(iman)%val1
	    cnt1=cnt1+1
	  endif
	enddo
	print*, cnt1, ' values out of ',y_dim, ' records'
	write(unit=33,*) cnt1, ' values out of ',y_dim, ' records'
!
!----------------------------------------------------------
! fill text
!----------------------------------------------------------
      case('fill_txt')
	do ix=lim1,lim2
          if(trim(man(iman)%txt1)=='all') then
	    temp1_char2(ix,:)=trim(man(iman)%txt1)
	  else
	    write(unit=33,*) '\tFill valid ',trim(head_tmp(ix)), ' with ',trim(man(iman)%txt1)
	    do iy=1,y_dim
	      if(temp1_char2(ix,iy)/=miss_val_char) temp1_char2(ix,iy)=trim(man(iman)%txt1)
	    enddo
	  endif
	enddo
!
!----------------------------------------------------------
! fill constant
!----------------------------------------------------------
      case('fill_con')
	do ix=lim1,lim2
          if(trim(man(iman)%txt1)=='all') then
	    temp1_d2(ix,:)=man(iman)%val1
	  else
	    write(unit=33,*) '\tFill ',trim(head_tmp(ix)), ' withy ',man(iman)%val1
	    do iy=1,y_dim
	      if(temp1_d2(ix,iy)/=miss_val_real) temp1_d2(ix,iy)=man(iman)%val1
	    enddo
	  endif
	enddo
!
!----------------------------------------------------------
! multiply by constant
!----------------------------------------------------------
      case('mult_con')
	do ix=lim1,lim2
	  write(unit=33,*) '\tMultiply ',trim(head_tmp(ix)), ' by ',man(iman)%val1
	  val1=man(iman)%val1
	  do iy=1,y_dim
	    if(temp1_d2(ix,iy)/=miss_val_real) temp1_d2(ix,iy)=temp1_d2(ix,iy)*val1
	  enddo
	enddo
!
!----------------------------------------------------------
! divide by constant
!----------------------------------------------------------
      case('div_con')
	do ix=lim1,lim2
	  write(unit=33,*) '\tDivide ',trim(head_tmp(ix)), ' by ',man(iman)%val1
	  val1=man(iman)%val1
	  if(val1==0.) then
	    print*, 'Error: cannot divide by zero'
	    print*, 'manipulation: ', iman, ' value: ',val1
	    stop
	  endif
	  do iy=1,y_dim
	    if(temp1_d2(ix,iy)/=miss_val_real) temp1_d2(ix,iy)=temp1_d2(ix,iy)/val1
	  enddo
	enddo
!
!----------------------------------------------------------
! add constant
!----------------------------------------------------------
      case('add_con')
	do ix=lim1,lim2
	  write(unit=33,*) '\tAdd ',man(iman)%val1, ' to ',trim(head_tmp(ix))
	  val1=man(iman)%val1
	  do iy=1,y_dim
	    if(temp1_d2(ix,iy)/=miss_val_real) temp1_d2(ix,iy)=temp1_d2(ix,iy)+val1
	  enddo
	enddo
!
!----------------------------------------------------------
! subtract constant
!----------------------------------------------------------
      case('sub_con')
	do ix=lim1,lim2
	  write(unit=33,*) '\tSubtract ',man(iman)%val1, ' from ',trim(head_tmp(ix))
	  val1=man(iman)%val1
	  do iy=1,y_dim
	    if(temp1_d2(ix,iy)/=miss_val_real) temp1_d2(ix,iy)=temp1_d2(ix,iy)-val1
	  enddo
	enddo
!
!----------------------------------------------------------
! replace values equal
!----------------------------------------------------------
      case('replace_eq')
	do ix=lim1,lim2
	  write(unit=33,*) '\treplace values for ',trim(head_tmp(ix))
	  val1=man(iman)%val1
	  val2=man(iman)%val2
	  write(unit=33,*) '\t\treplace ',val1, ' with ', val2
!
! replace values
	  cnt1=0 ! number of values replaced
	  do iy=1,y_dim
	    if(temp1_d2(ix,iy)==val1) then
	      cnt1=cnt1+1
	      temp1_d2(ix,iy)=val2
	    endif
	  enddo
	  write(unit=33,*) '\t\t',cnt1, ' values replaced'
	  write(unit=33,*) '\t\t','total number records: ',y_dim
	enddo
!
!----------------------------------------------------------
! print values greater than
!----------------------------------------------------------
      case('print_gt') 
	  write(unit=33,*) '\tPrint values > ', man(iman)%val1
	  val1=man(iman)%val1
	  indx1=man(iman)%ind1
!
! find first valid point
	  do iy=1,y_dim
	    if(temp1_d2(indx1,iy)/=miss_val_real.and.temp1_d2(indx1,iy)>val1) then
	      print*, iy,temp1_d2(indx1,iy)
	    endif
	  enddo
!
!----------------------------------------------------------
! print values less than
!----------------------------------------------------------
      case('print_lt') 
	  write(unit=33,*) '\tPrint values < ', man(iman)%val1
	  val1=man(iman)%val1
	  indx1=man(iman)%ind1
!
! find first valid point
	  do iy=1,y_dim
	    if(temp1_d2(indx1,iy)/=miss_val_real.and.temp1_d2(indx1,iy)<val1) then
	      print*, iy,temp1_d2(indx1,iy)
	    endif
	  enddo
!
!----------------------------------------------------------
! print max and min values
!----------------------------------------------------------
      case('print_max') 
	do ix=lim1,lim2
	  write(unit=33,*) '\tPrint Min and Max'
!
! find first valid point
	  do iy=1,y_dim
	    if(temp1_d2(ix,iy)/=miss_val_real) then
	      val1=temp1_d2(ix,iy)
	      val2=temp1_d2(ix,iy)
	      exit
	    endif
	  enddo
!
! go through rest of points
	  if(iy<=y_dim) then
	    do iy=1,y_dim
	      val1=max(val1,temp1_d2(ix,iy))
	      val2=min(val2,temp1_d2(ix,iy))
	    enddo
	    write(unit=33,*) '\t\t',trim(head_tmp(ix))//' max: ',val1, ' min: ',val2
	  else
	    write(unit=33,*) '\t\t',trim(head_tmp(ix))//' min/max: no valid points'
	  endif
	enddo
!
!----------------------------------------------------------
! print mean and standard deviation
!----------------------------------------------------------
      case('print_mean')
	write(unit=33,*) '\tPrint mean and standard deviation'
	do ix=lim1,lim2
          val1=0. 
          val2=0. 
	  cnt1=0.
	  do iy=1,y_dim
	    if(temp1_d2(ix,iy)/=miss_val_real) then
	      val1=val1+temp1_d2(ix,iy)
	      cnt1=cnt1+1
	    endif
	  enddo
	  if(cnt1/=0.) val1=val1/cnt1
	  do iy=1,y_dim
	    if(temp1_d2(ix,iy)/=miss_val_real) val2=val2+(val1-temp1_d2(ix,iy))**2.
	  enddo
	  if(cnt1/=0.) then
	    val2=sqrt(val2/cnt1)
	    write(unit=33,*) '\t\t',trim(head_tmp(ix))//' mean:',val1, ' std: ',val2,' pts:',cnt1
	  else
	    write(unit=33,*) '\t\t',trim(head_tmp(ix))//' mean/std: no valid points'
	  endif
	enddo
!
!----------------------------------------------------------
! print negative values
!----------------------------------------------------------
      case('print_neg')
	write(unit=33,*) '\tPrint negative values'
	do ix=lim1,lim2
          cnt1=0
	  do iy=1,y_dim
	    if(temp1_d2(ix,iy)/=miss_val_real.and.temp1_d2(ix,iy)<0.) then
	      write(unit=33,*) iy,temp1_d2(ix,iy)
	      cnt1=cnt1+1
	    endif
	  enddo
	  write(unit=33,*) '\t\t',trim(head_tmp(ix))//' neg:',cnt1
	enddo
!
! end manipulations
    end select
!
! transfer data back to data variable
    select case(man(iman)%num)
      case(1) ! input data
	data_in=temp1_d2
	char_in=temp1_char2
	var_in=var_tmp
      case(2) ! output data
	data_out=temp1_d2
	char_out=temp1_char2
	var_out=var_tmp
    end select
!
! deallocate local variable
    deallocate(temp1_d2)
    deallocate(temp1_char2)
    deallocate(var_tmp)
    deallocate(head_tmp)
!
    end subroutine
!
!===================================================
    subroutine map_look_up(iman)
!===================================================
!
    use dit_variables
    use netcdf
    use typeSizes
!
    implicit none
!
! input variables
    integer iman    ! input data file number to read
!
! internal variables
    integer ipat    ! path numder index
    integer irec    ! record numder index
    integer ihed    ! header numder index
    integer ivar    ! header numder index
    integer icls    ! class numder index
    integer status  ! read status variable
    integer n_grid  ! number grid
    integer n_class ! number classes
    integer igrd    ! grid index
    integer indx_varlat   ! latitude variable index
    integer indx_varlon   ! longitude variable index
    integer indx_latmap   ! latitude index for map
    integer indx_lonmap   ! longitude index for map
    Character*20  varname  ! generic variable name
    Character*45 Junk ! garbage variable for reading text
    double precision, allocatable :: class_num(:)         ! temporary class number
    Character*45, allocatable :: class_name(:)         ! temporary class name
    logical flag  ! generic flag
    real, allocatable :: temp_map(:,:)       ! temporary map
!
! grid definition file
    ipat=man(iman)%ind3
    filename=trim(path(ipat)%path1)
    print*, '\t\tGrid def file: ', trim(filename)
    write(unit=33,*) '\t\tGrid def file: ', trim(filename)
    open(unit=9,file=trim(filename),form='formatted', status='old')
    read (9,11) junk,n_grid ! read number of grids defined in file
    read (9,10) junk
    do igrd=1,n_grid
      read (9,*) grid_r%name, grid_r%type, grid_r%lonmin, grid_r%latmin, grid_r%Dlon, grid_r%Dlat, grid_r%lon_offset, grid_r%lat_offset, grid_r%nlon, grid_r%nlat
      if(trim(grid_r%name)==trim(path(ipat)%txt2)) exit
    enddo
    close(unit=9)
    print*, '\t\tgrid name: ',trim(grid_r%name)
    write(unit=33,*) '\t\tgrid name: ',trim(grid_r%name)
!
! standard formats for input
10    Format (a45)
11    Format (a45, I4)
!
! read map
    allocate(temp_map(grid_r%nlon,grid_r%nlat))
    ipat=man(iman)%ind1
    filename=trim(path(ipat)%path1)
    varname=trim(path(ipat)%txt2)
    print*, '\t\tmap: ',trim(filename)
    write(unit=33,*) '\t\tmap: ',trim(filename)
    print*, '\t\tvariable: ', trim(varname)
    write(unit=33,*) '\t\tvariable: ', trim(varname)
    call read_single_netcdf_c(filename,varname,grid_r%nlon,grid_r%nlat,temp_map)
!
! locate latitude and longitude variable index
    indx_varlon=man(iman)%ind4
    indx_varlat=man(iman)%ind5
!
! nearest neighbor matching
    allocate(temp1_d1(y_dim))
    allocate(temp1_char1(y_dim))
    do irec=1,y_dim
      indx_lonmap=(data_out(indx_varlon,irec)-grid_r%lonmin)/grid_r%dlon+1
      indx_latmap=(data_out(indx_varlat,irec)-grid_r%latmin)/grid_r%dlat+1
      temp1_d1(irec)=temp_map(indx_lonmap,indx_latmap)
    enddo
!
! read in number to text matching file
    ipat=man(iman)%ind2
    filename=trim(path(ipat)%path1)
    print*, '\t\tcode: ', trim(filename)
    open(unit=9,file=trim(filename),form='formatted', status='old')
    read (9,*) n_class
    allocate(class_num(n_class))
    allocate(class_name(n_class))
    read (9,*) junk
    do icls=1,n_class
      read (9,*) class_num(icls),class_name(icls)
    enddo
    close(unit=9)
!
! match map value to text class
    do irec=1,y_dim
      do icls=1,n_class
	if(temp1_d1(irec)==class_num(icls)) then
	  temp1_char1(irec)=trim(class_name(icls))
	  exit
	endif
      enddo
      write(unit=33,*) irec,temp1_d1(irec),trim(temp1_char1(irec))
    enddo
!
! put into data array
    do irec=1,y_dim
      temp1_char2(man(iman)%ind6,irec)=trim(temp1_char1(irec))
    enddo
!
! deallocate local files
    deallocate(class_num)
    deallocate(class_name)

    end subroutine
!
!===================================================
    subroutine calc_time_zone(iman)
!===================================================
! calculates time zone based on site longitude
!
! Modifications:
!  Kevin schaefer created subroutine (6/30/15)
!---------------------------------------------------
    use dit_variables
    use netcdf
    use typeSizes
!
    implicit none
!
! input variables
    integer iman    ! input data file number to read
!
! internal variables
    integer irec    ! record numder index
    integer ivar    ! header numder index
    integer icls    ! class numder index
    integer indx_varlon   ! longitude variable index
    integer indx_varzon   ! time zone variable index
    double precision dlon       ! (deg) delta longitude of time zone
    double precision lonmin     ! (deg) minimumlongitude of GMT time zone
!
! locate longitude variable index
    do ivar=1,n_var
      if(trim(man(iman)%txt1)==trim(var(ivar)%txt2)) indx_varlon=var(ivar)%ind2
      if(trim(man(iman)%txt2)==trim(var(ivar)%txt2)) indx_varzon=var(ivar)%ind2
    enddo
    print*,'\t\tlon index: ', indx_varlon,trim(head_out(indx_varlon,1))
    print*,'\t\tzone index: ',indx_varzon,trim(head_out(indx_varzon,1))
!
! calculate time zone
    allocate(temp_int1(y_dim))
    dlon=15.
    lonmin=7.5
    do irec=1,y_dim
      temp_int1(irec)=(abs(data_out(indx_varlon,irec))-lonmin)/dlon+1
      if(temp1_d2(indx_varlon,irec)<0.)  temp_int1(irec)=-1.* temp_int1(irec)
    enddo
!
! put into output data array
    do irec=1,y_dim
      temp1_d2(indx_varzon,irec)=temp_int1(irec)
    enddo
!
! deallocate files
    deallocate(temp_int1)
!
    end subroutine
!
!--------------------------------------------------------------------------
      subroutine distance(lon1,lat1,lon2,lat2,dist)
!--------------------------------------------------------------------------
! Calculates distance between two points on the Earth
!
! Modifications:
!  Kevin Schaefer created routine from vectorCorrelation routine (11/9/16)
    IMPLICIT NONE
!
! begin input variables
    double precision lon1 ! (deg) longitude first point
    double precision lat1 ! (deg) latitude first point
    double precision lon2 ! (deg) longitude second point
    double precision lat2 ! (deg) latitude second point
!
! begin output variables
    double precision dist ! (m) distance between points
!
! begin internal variables
    double precision x1,y1,z1  ! (m) x, y, z, coordinates
    double precision x2,y2,z2  ! (m) x, y, z, coordinates
    double precision x3,y3,z3  ! (m) x, y, z, coordinates
    double precision pi180     ! (1/deg) pi divided by 180
    double precision earth_rad ! (m) earth radius
    double precision delta     ! (m) temp distance
!
! constants
    pi180=3.14159/180. ! pi divided by 180
    earth_rad=6356752. ! earth radius
!
! coordinates first point
    x1=earth_rad*cos(pi180*lat1)*cos(pi180*lon1)
    y1=earth_rad*cos(pi180*lat1)*sin(pi180*lon1)
    z1=earth_rad*sin(pi180*lat1)
!
! coordinates second point
    x2=earth_rad*cos(pi180*lat2)*cos(pi180*lon2)
    y2=earth_rad*cos(pi180*lat2)*sin(pi180*lon2)
    z2=earth_rad*sin(pi180*lat2)
!
! distance between points
    delta=x2-x1
    dist=delta**2.
    delta=y2-y1
    dist=dist+delta**2.
    delta=z2-z1
    dist=dist+delta**2.
    dist=dsqrt(dist)
!
    return
    end
!
