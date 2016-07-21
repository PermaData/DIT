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
	real, allocatable :: data_read(:,:)          ! temp read data array
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
	real val1     ! temporary value
	real val2     ! temporary value
	real valmin   ! min value
	real valmax   ! max value
	real dval     ! temporary delta value
	Character*200 text  ! text string
	Character*200 temp   ! text string
	Character*200 fmt    ! text string format
	logical flag  ! generic flag
	integer year  ! year
	integer mon   ! month
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
	allocate(var_tmp(in%n_var))
	temp1_d2=data_in
	temp1_char2=char_in
	var_tmp=var_in
	  case(2) ! output data
		x_dim=out%n_var
	y_dim=out%n_rec
	allocate(temp1_d2(x_dim,y_dim))
	allocate(temp1_char2(x_dim,y_dim))
	allocate(var_tmp(out%n_var))
	temp1_d2=data_out
	temp1_char2=char_out
	var_tmp=var_out
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
! scan through manipulations
	select case(man(iman)%typ)
!
!----------------------------------------------------------
! make a pdf of values
!----------------------------------------------------------
	  case('make_pdf')
		 indx1=man(iman)%ind1
		 file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		 file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		 write(unit=33,*) 'Make a pdf'

		 open(unit=200, file=trim(file_in), form='formatted')
		 fmt = '(F14.7)'
		 do iy = 1, y_dim
			write(unit=200,fmt=fmt) temp1_d2(indx1,iy)
		 enddo
		 close(unit=200)

		 ! Build the command, using all the arguments
		 write(text,'(A,I5,A,A,A,F14.7,A,F14.7,A,A,A,A)') ' -n ',man(iman)%ind2,' -f ',trim(man(iman)%txt1),' -n ',man(iman)%val1,' -n ',man(iman)%val2,' -f ',trim(man(iman)%txt2),' -f ',trim(man(iman)%txt3)
		 cmd = trim(path(i_pat_python)%path1)//'pdf.py'
		 cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)
		 cmd = trim(cmd)//text

		 call system(cmd)

		 open(unit=201, file=trim(file_out), form='formatted')
		 do indx1 = 1,(man(iman)%ind2 - 1)
			read(unit=201, fmt='(A)') text
			write(unit=33,*) trim(text)
		 enddo
		 close(unit=201)

!!$	indx1=man(iman)%ind1 ! x variable number
!!$	indx2=man(iman)%ind2 ! y variable number
!!$	nval=man(iman)%ind3  ! number of bins
!!$	write(unit=33,*) '\tmake a pdf x= ',trim(var_tmp(indx1)%txt1),' y= ',trim(var_tmp(indx2)%txt1)
!!$	allocate(temp2_d2(5,nval))
!!$	temp2_d2=0.
!!$!
!!$! min and max bin values
!!$        if(trim(man(iman)%txt1)=='auto') then
!!$	  do irec=1,y_dim
!!$	    cnt1=irec
!!$	    if(temp1_d2(indx1,irec)/=miss_val_real) then
!!$	      valmin=temp1_d2(indx1,irec)
!!$	      valmax=temp1_d2(indx1,irec)
!!$	      exit
!!$	    endif
!!$	  enddo
!!$	  do irec=cnt1,y_dim
!!$	      if(temp1_d2(indx1,irec)/=miss_val_real) then
!!$	        valmin=min(valmin,temp1_d2(indx1,irec))
!!$	        valmax=max(valmax,temp1_d2(indx1,irec))
!!$	      endif
!!$	  enddo
!!$	elseif(trim(man(iman)%txt1)=='man') then
!!$          valmin=man(iman)%val1
!!$          valmax=man(iman)%val2
!!$	else
!!$	  print*, 'Error: incorrect min/max option: ',trim(man(iman)%txt1)
!!$	  stop
!!$	endif
!!$        dval=(valmax-valmin)/real(nval)
!!$	write(unit=33,*) 'valmin: ',valmin
!!$	write(unit=33,*) 'valmax: ',valmax
!!$	write(unit=33,*) 'dval: ',dval
!!$!
!!$! bin values
!!$	do icnt=1,nval
!!$	  temp2_d2(1,icnt)=valmin+(real(icnt)-0.5)*dval
!!$	enddo
!!$!
!!$! bin data: count points and calc mean
!!$	cnt1=0
!!$	cnt2=0
!!$	do irec=1,y_dim
!!$	  if(temp1_d2(indx1,irec)/=miss_val_real) then
!!$	    cnt2=cnt2+1
!!$	    icnt=int((temp1_d2(indx1,irec)-valmin)/dval)+1 ! bin index
!!$            if(trim(man(iman)%txt2)=='include') then ! include point outside of x-range
!!$	      cnt1=cnt1+1
!!$	      if(icnt>nval) icnt=nval
!!$              if(icnt<1) icnt=1
!!$              temp2_d2(2,icnt)=temp2_d2(2,icnt)+1.
!!$              if(temp1_d2(indx2,irec)/=miss_val_real) then
!!$	        temp2_d2(3,icnt)=temp2_d2(3,icnt)+1.
!!$	        temp2_d2(4,icnt)=temp2_d2(4,icnt)+temp1_d2(indx2,irec)
!!$	      endif
!!$            else ! exclude points outside range
!!$              if(icnt>=1.and.icnt<=nval) then
!!$	        cnt1=cnt1+1
!!$		temp2_d2(2,icnt)=temp2_d2(2,icnt)+1.
!!$                if(temp1_d2(indx2,irec)/=miss_val_real) then
!!$	          temp2_d2(3,icnt)=temp2_d2(3,icnt)+1.
!!$	          temp2_d2(4,icnt)=temp2_d2(4,icnt)+temp1_d2(indx2,irec)
!!$	        endif
!!$	      endif
!!$            endif
!!$	  endif
!!$	enddo
!!$!
!!$! cal mean
!!$	do icnt=1,nval
!!$	  if(temp2_d2(3,icnt)/=0.) temp2_d2(4,icnt)=temp2_d2(4,icnt)/temp2_d2(3,icnt)
!!$	enddo
!!$!
!!$! bin data: calc standard deviation
!!$	do irec=1,y_dim
!!$	  if(temp1_d2(indx1,irec)/=miss_val_real) then
!!$	    icnt=int((temp1_d2(indx1,irec)-valmin)/dval)+1 ! bin index
!!$            if(trim(man(iman)%txt2)=='include') then ! include point outside of x-range
!!$	      if(icnt>nval) icnt=nval
!!$              if(icnt<1) icnt=1
!!$              if(temp1_d2(indx2,irec)/=miss_val_real) then
!!$	        val1=(temp2_d2(4,icnt)-temp1_d2(indx2,irec))
!!$		temp2_d2(5,icnt)=temp2_d2(5,icnt)+val1*val1
!!$	      endif
!!$            else ! exclude points outside range
!!$              if(icnt>=1.and.icnt<=nval) then
!!$                if(temp1_d2(indx2,irec)/=miss_val_real) then
!!$	          val1=(temp2_d2(4,icnt)-temp1_d2(indx2,irec))
!!$		  temp2_d2(5,icnt)=temp2_d2(5,icnt)+val1*val1
!!$	        endif
!!$	      endif
!!$            endif
!!$	  endif
!!$	enddo
!!$!
!!$! Normalize
!!$	do icnt=1,nval
!!$	  if(temp2_d2(3,icnt)/=0.) temp2_d2(5,icnt)=sqrt(temp2_d2(5,icnt)/temp2_d2(3,icnt))
!!$	  if(temp2_d2(2,icnt)/=0.) temp2_d2(3,icnt)=temp2_d2(3,icnt)/temp2_d2(2,icnt)*100.
!!$	  temp2_d2(2,icnt)=temp2_d2(2,icnt)/real(cnt1)*100.
!!$	enddo
!!$!
!!$! write to processing file
!!$        write(unit=33,*) 'Tot records: ', y_dim
!!$        write(unit=33,*) 'Tot valid records: ', cnt2
!!$        if(trim(man(iman)%txt1)/='include') write(unit=33,*) 'Tot records in range: ', cnt1
!!$        fmt='(a5,1x,a15,1x,a6,1x,a15,,1x,a15,1x,a6)'
!!$	write(unit=33, fmt=fmt) 'bin', trim(var_tmp(indx1)%txt1),'num(%)',trim(var_tmp(indx2)%txt1),'std','val(%)'
!!$        fmt='(i5,1x,f15.7,1x,f6.2,1x,f15.7,1x,f15.7,1x,f6.2)'
!!$	do icnt=1,nval
!!$	  write(unit=33, fmt=fmt) icnt, temp2_d2(1,icnt),temp2_d2(2,icnt),temp2_d2(4,icnt),temp2_d2(5,icnt),temp2_d2(3,icnt)
!!$	enddo
!!$	deallocate(temp2_d2)
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
! command to execute pythonm script
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
! Move specified text between columns
!----------------------------------------------------------
case('move_text')		! TODO: Test move_text
	write(unit=33,*) 'Move text from one column to another'
	file_in = path(i_pat_tmp)%path1//'temp1'
	file_out = path(i_pat_tmp)%path1//'temp2'

	fmt = '(A,A)'

	! needs to be given indices of columns to read from
	open(unit=200, file=trim(file_in), form='formatted')
	do indx1 = 1,y_dim
		write(unit=200, fmt=fmt) temp1_char2(man(iman)%ind1, indx1),temp1_char2(man(iman)%ind2, indx1)
	enddo
	close(unit=200)

	! -i <input file> -o <output file> -f <regex to move> -t <regex to move to>
	cmd = path(i_pat_python)%path1//'move_text.py'
	cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)
	cmd = trim(cmd)//' -f '//trim(man(iman)%txt1)//' -t '//trim(man(iman)%txt2)

	call system(cmd)

	open(unit=201, file=trim(file_out), form='formatted')
	do indx1 = 1,y_dim
		read(unit=201, fmt=fmt) text, temp
		temp1_char2(man(iman)%ind1, indx1) = text
		temp1_char2(man(iman)%ind2, indx1) = temp
	enddo
	close(unit=201)

!
!----------------------------------------------------------
! Replace text in a column
!----------------------------------------------------------
case('repl_text')		! TODO: Test replace_text
	write(unit=33,*) 'Replace text in records'
	file_in = trim(path(i_pat_tmp)%path1)//'temp1'
	file_out = trim(path(i_pat_tmp)%path1)//'temp2'

	fmt = '(A,A)'

	!needs to be given indices of columns to read from
	open(unit=200, file=trim(file_in), form='formatted')
	do indx1 = 1,y_dim
		! ind1 is place
		write(unit=200, fmt=fmt) temp1_char2(man(iman)%ind1, indx1)
	enddo
	close(unit=200)

	! -i <input file> -o <output file> -t <text to replace> -w <replacement>
	cmd = trim(path(i_pat_python)%path1)//'replace_text.py'
	cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)
	cmd = trim(cmd)//' -t '//trim(man(iman)%txt1)//' -w '//trim(man(iman)%txt2)
	print*,cmd

	call system(cmd)

	open(unit=201, file=trim(file_out), form='formatted')
	do indx1 = 1,y_dim
		read(unit=201, fmt=fmt) text, temp
		temp1_char2(man(iman)%ind1, indx1) = text
		temp1_char2(man(iman)%ind2, indx1) = temp
	enddo
	close(unit=201)


!
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
	  case('mid_mon')		! TODO: Test mid_mon
		indx1=man(iman)%ind1 ! output variable number
		indx2=man(iman)%ind2 ! input year variable number
		indx3=man(iman)%ind3 ! input month variable number
		file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		open(unit=200, file=trim(file_in), form='formatted')
		do iy = 1, y_dim
			write(unit=200, fmt='(I4.4,I2.2)') temp1_d2(indx2, iy), temp1_d2(indx3, iy)
		enddo
		close(unit=200)

		cmd = trim(path(i_pat_python)%path1)//'mid_month.py'
		cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)
		cmd = trim(cmd)//' -f '//trim(man(iman)%txt1)

		call system(cmd)

	  open(unit=201, file=trim(file_out), form='formatted')
	  do iy = 1,y_dim
		read(unit=201, fmt='(A16)') temp
		temp1_char2(indx1, iy) = temp
	  enddo
	  close(unit=201)

	! write(unit=33,*) '\tcreate character mid-month date'
	! if(man(iman)%num==1) then
	  ! write(unit=33,*) 'Error: only do this to output data'
	  ! stop
	! endif
	! indx1=man(iman)%ind1 ! output variable number
	! indx2=man(iman)%ind2 ! input year variable number
	! indx3=man(iman)%ind3 ! input month variable number
! !
! ! locate inout variables
		! do ivar=1, n_var
	  ! if(trim(head_in(indx2,1))==trim(var(ivar)%txt1)) imap2=ivar
	  ! if(trim(head_in(indx3,1))==trim(var(ivar)%txt1)) imap3=ivar
	! enddo
! !
! ! calculate date
		! do iy=1,y_dim
! !
! ! year
	  ! fmt=trim(var(imap2)%fmt1)
	  ! year=data_in(indx2,iy)
	  ! write(temp,fmt=fmt) year
	  ! text=trim(temp)//'-'
! !
! ! month
	  ! fmt=trim(var(imap3)%fmt1)
	  ! mon=data_in(indx3,iy)
	  ! write(temp,fmt=fmt) mon
	  ! text=trim(text)//trim(temp)
! !
! ! day-of-month
		  ! text=trim(text)//trim(mid_month(mon))
	  ! temp1_char2(indx1,iy)=trim(text)
		! enddo
!
!----------------------------------------------------------
! calculate time zone
!----------------------------------------------------------
! right now this is restricted to commas and periods
	  case('timezone')		! TODO: complete timezone
	  write(unit=33,*) '\tcalculate time zone'
	   file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		open(unit=200, file=trim(file_in), form='formatted')
		fmt = 'A16,F14.7,F14.7'
		do iy = 1, y_dim
			write(unit=200,fmt=fmt) temp2_d2(man(iman)%ind1,iy), temp2_d2(man(iman)%ind2,iy), temp1_d2(man(iman)%ind3,iy)
		enddo
		close(unit=200)

		! Build the command, using all the arguments
		cmd = trim(path(i_pat_python)%path1)//'utm_to_latlong.py'
		cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)
		cmd = trim(cmd)//' -n '//'0'//' -n '//'1'//' -n '//'2'
		cmd = trim(cmd)//' -f '//man(iman)%txt1

		call system(cmd)

		open(unit=201, file=trim(file_out), form='formatted')
		do indx1 = 1, y_dim
			read(unit=201, fmt='f14.7,f14.7') temp1_d2(man(iman)%ind4, iy), temp1_d2(man(iman)%ind5, iy)
		enddo
		close(unit=201)
		! print*, '\tcalculate time zone'
	! write(unit=33,*) '\tcalculate time zone'
	! if(man(iman)%num==1) then
	  ! print*, 'Error: only do this to output array'
	  ! write(unit=33,*) 'Error: only do this to output array'
	  ! stop
	! endif
		! call calc_time_zone(iman)

!----------------------------------------------------------
! remove a set of characters from character data
!----------------------------------------------------------
	case('rm_chars')		! TODO: Test rm_chars
		write(unit=33,*) '\tremove characters'
		indx1 = man(iman)%ind1
		file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		open(unit=200, file=trim(file_in), form='formatted')
		do iy = 1, y_dim
			write(unit=200,fmt='(a)') trim(temp1_char2(indx1, iy))
		enddo
		close(unit=200)

		! Build the command, using all the arguments
		cmd = trim(path(i_pat_python)%path1)//'remove_chars.py'
		cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)
		cmd = trim(cmd)//' -f '//man(iman)%txt1

		call system(cmd)

		open(unit=201, file=trim(file_out), form='formatted')
		do indx1 = 1, y_dim
			read(unit=201, fmt='(a)') temp 
			print*,trim(temp)
			temp1_char2(indx1, iy) = trim(temp)
		enddo
		close(unit=201)



		!
!----------------------------------------------------------
! remove punctuation from character data
!----------------------------------------------------------
! right now this is restricted to commas and periods
	  ! case('rm_punct')
	! write(unit=33,*) '\tremove punctuation'
		! fmt='(a4,2x,a4,2x,a4,2x,a50,2x,a50)'
	! write(unit=33,fmt=fmt) 'rec','id','qc_flg','old text', 'new text'
		! fmt='(i4,2x,i4,2x,i4,2x,a50,2x,a50)'
	! indx1=man(iman)%ind1 ! variable index
	! idvar=man(iman)%ind2 ! id index
	! indx3=man(iman)%ind3 ! qc flag index
	! do irec=1,y_dim
	  ! temp=trim(temp1_char2(indx1,irec))
	  ! temp=adjustl(temp)
	  ! num=len(temp)
	  ! cnt1=0
	  ! text=''
	  ! flag=.false.
	  ! do itxt=1,num
	    ! if(temp(itxt:itxt)=='.') then
	      ! flag=.true.
	      ! temp1_d2(indx3,irec)=1
	    ! elseif(temp(itxt:itxt)==',') then
	      ! flag=.true.
	      ! cnt1=cnt1+1
	      ! text(cnt1:cnt1)=';'
	      ! temp1_d2(indx3,irec)=1
	    ! else
	      ! cnt1=cnt1+1
	      ! text(cnt1:cnt1)=temp(itxt:itxt)
	    ! endif
	  ! enddo
	  ! if(flag) then
	    ! itxt=temp1_d2(idvar,irec)
	    ! ivar=temp1_d2(indx3,irec)
	    ! write(unit=33,fmt=fmt) irec,itxt,ivar,trim(temp1_char2(indx1,irec)),trim(text)
	  ! endif
	  ! temp1_char2(indx1,irec)=trim(text)
	! enddo
!
!----------------------------------------------------------
! convert utm coordinates to latitude and longitude
!----------------------------------------------------------
! exit to external python script to convert from utm coordinates to latitude and longitude
	  case('conv_utm')		! TODO: Test conv_utm
		write(unit=33,*) 'convert utm to lat/lon'
		file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		open(unit=200, file=trim(file_in), form='formatted')
		fmt = 'F14.7,F14.7,F14.7'
		do iy = 1, y_dim
			write(unit=200,fmt=fmt) temp1_d2(man(iman)%ind1,iy), temp1_d2(man(iman)%ind2,iy), temp1_d2(man(iman)%ind3,iy)
		enddo
		close(unit=200)

		! Build the command, using all the arguments
		cmd = trim(path(i_pat_python)%path1)//'utm_to_latlong.py'
		cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)
		cmd = trim(cmd)//' -n '//'0'//' -n '//'1'//' -n '//'2'
		cmd = trim(cmd)//' -f '//man(iman)%txt1

		call system(cmd)

		open(unit=201, file=trim(file_out), form='formatted')
		do indx1 = 1, y_dim
			read(unit=201, fmt='f14.7,f14.7') temp1_d2(man(iman)%ind4, iy), temp1_d2(man(iman)%ind5, iy)
		enddo
		close(unit=201)
	! write(unit=33,*) '\tconvert utm to lat/lon'
	! write(unit=33,*) '\t\tuse standard python script'
	! indx1=man(iman)%ind1 ! zone index
	! indx2=man(iman)%ind2 ! east coordinate index
	! indx3=man(iman)%ind3 ! north coordinate index
	! indx4=man(iman)%ind4 ! latitude index
	! indx5=man(iman)%ind5 ! longitude index
	! idvar=man(iman)%ind6 ! record id number
! !
! ! write utm coordinates to file
		! do ipat = 1, n_path
		  ! if(path(ipat)%typ=='outpath')exit
		! enddo
		! filename='temp.dat'
		! open(unit=44,file=trim(filename),form='formatted')

	! do irec=1,y_dim
	  ! print*, indx1,irec,data_in(indx1,irec)
! !
! ! zone
	  ! fmt='(f4.1)'
	  ! write(temp,fmt=fmt) data_in(indx1,irec)
	  ! temp=adjustl(temp)
	  ! text=trim(temp)//','
! !
! ! east coordinate
	  ! write(temp,*) data_in(indx2,irec)
	  ! temp=adjustl(temp)
	  ! text=trim(text)//trim(temp)//','
! !
! ! north coordinate
	  ! write(temp,*) data_in(indx3,irec)
	  ! temp=adjustl(temp)
	  ! text=trim(text)//trim(temp)
	  ! write(unit=44,*) trim(text)
	! enddo
! !
! ! read
	! close(unit=44)
		! fmt='(a4,2x,a4,2x,a20,2x,a15,2x,a15)'
	! write(unit=33,fmt=fmt) 'rec','zone','East','North', 'lat','lon'
		! fmt='(i4,2x,i4,2x,i4,2x,a50,2x,a50)'

!----------------------------------------------------------
! convert latitude/longitude coordinates to utm
!----------------------------------------------------------
	  case('conv_latlon')		! TODO: Test conv_latlon
		write(unit=33,*) 'convert lat/lon to utm'
		file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		open(unit=200, file=trim(file_in), form='formatted')
		fmt = 'F14.7,F14.7'
		do iy = 1, y_dim
			write(unit=200,fmt=fmt) temp1_d2(man(iman)%ind1,iy), temp1_d2(man(iman)%ind2,iy)
		enddo
		close(unit=200)

		! Build the command, using all the arguments
		cmd = trim(path(i_pat_python)%path1)//'latlong_to_utm.py'
		cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)
		cmd = trim(cmd)//' -n '//'0'//' -n '//'1'
		cmd = trim(cmd)//' -f '//man(iman)%txt1

		call system(cmd)

		open(unit=201, file=trim(file_out), form='formatted')
		do indx1 = 1, y_dim

		enddo
		close(unit=201)
!
!----------------------------------------------------------
! variable statistics
!----------------------------------------------------------
	  case('stats_var')
		write(unit=33,*) 'Variable statistics'
		indx1=man(iman)%ind1
		file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		open(unit=200, file=trim(file_in), form='formatted')
		fmt = '(F14.7)'
		do iy = 1, y_dim
			write(unit=200,fmt=fmt) temp1_d2(indx1,iy)
		enddo
		close(unit=200)

		! Build the command, using all the arguments
		cmd = trim(path(i_pat_python)%path1)//'statistics.py'
		cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)

		call system(cmd)

		open(unit=201, file=trim(file_out), form='formatted')
		do indx1 = 1,2
			read(unit=201, fmt='(A)') text
			write(unit=33,*) trim(text)
		enddo
		close(unit=201)

!!$        if(man(iman)%num==1) write(unit=33,*) '\t\tInput Variable Statistics'
!!$        if(man(iman)%num==2) write(unit=33,*) '\t\tOutput Variable Statistics'
!!$!
!!$! allocate Stats variables
!!$	n_stat=7
!!$	allocate(temp2_d2(x_dim,n_stat))
!!$	allocate(head_tmp(n_stat))
!!$!
!!$! set header
!!$        head_tmp(1)='min'
!!$        head_tmp(2)='max'
!!$        head_tmp(3)='mean'
!!$        head_tmp(4)='std'
!!$        head_tmp(5)='totpts'
!!$        head_tmp(6)='valid_pts'
!!$        head_tmp(7)='pts_frac'
!!$!
!!$! print Header
!!$	fmt='(8(a14,1x))'
!!$        write(unit=33,fmt=fmt) 'Variable','min','max','mean','std','totpts','valid_pts','pts_frac'
!!$!
!!$! loop through variables
!!$	do ix=1,x_dim
!!$!
!!$! min and max value
!!$!
!!$! find first valid point
!!$	  do iy=1,y_dim
!!$	    cnt1=iy
!!$	    if(temp1_d2(ix,iy)/=miss_val_real) then
!!$	      val1=temp1_d2(ix,iy)
!!$	      val2=temp1_d2(ix,iy)
!!$	      exit
!!$	    endif
!!$	  enddo
!!$!
!!$! go through rest of points
!!$	  if(cnt1<=y_dim) then
!!$	    do iy=cnt1,y_dim
!!$	      if(temp1_d2(ix,iy)/=miss_val_real) then
!!$	        val1=min(val1,temp1_d2(ix,iy))
!!$	        val2=max(val2,temp1_d2(ix,iy))
!!$	      endif
!!$	    enddo
!!$	  endif
!!$	  temp2_d2(ix,1)=val1
!!$	  temp2_d2(ix,2)=val2
!
! mean value, standard deviation, valid points, coverage frac
!!$          val1=0.
!!$          val2=0.
!!$	  cnt1=0
!!$	  do iy=1,y_dim
!!$	    if(temp1_d2(ix,iy)/=miss_val_real) then
!!$	      val1=val1+temp1_d2(ix,iy)
!!$	      cnt1=cnt1+1
!!$	    endif
!!$	  enddo
!!$	  if(cnt1/=0) val1=val1/real(cnt1)
!!$	  do iy=1,y_dim
!!$	    if(temp1_d2(ix,iy)/=miss_val_real) val2=val2+(val1-temp1_d2(ix,iy))**2.
!!$	  enddo
!!$	  if(cnt1/=0) then
!!$	    val2=sqrt(val2/real(cnt1))
!!$	  else
!!$	    val1=miss_val_real
!!$	    val2=miss_val_real
!!$	  endif
!!$	  temp2_d2(ix,3)=val1
!!$	  temp2_d2(ix,4)=val2
!!$	  temp2_d2(ix,5)=real(y_dim)
!!$	  temp2_d2(ix,6)=real(cnt1)
!!$	  temp2_d2(ix,7)=real(cnt1)/real(y_dim)
!!$!
!!$! write statistics
!!$	  fmt='(a15)'
!!$	  if(man(iman)%num==1) write(temp,fmt=fmt) trim(head_in(ix,1))
!!$	  if(man(iman)%num==2) write(temp,fmt=fmt) trim(head_out(ix,1))
!!$	  text=temp
!!$	  fmt='(f14.3)'
!!$	  do ivar=1,n_stat
!!$	    write(temp,fmt=fmt) temp2_d2(ix,ivar)
!!$	    text=trim(text)//' '//trim(temp)
!!$	  enddo
!!$          write(unit=33,*) trim(text)
!!$	enddo
!!$!
!!$! deallocate Stats variables
!!$	deallocate(head_tmp)
!!$	deallocate(temp2_d2)
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
	  case('rem_dup')		! TODO: Write and complete and test rem_dup
		write(unit=33,*) '\tRemove duplicate records'
	if(man(iman)%num==2) then
	  write(unit=33,*) 'Error: only do this to input array'
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
	    if(temp1_d2(indx1,irec)==temp1_d2(indx1,iy).and.temp1_d2(indx2,irec)==temp1_d2(indx2,iy)) then
	      num=num+1
	      temp_int1(iy)=1
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
	    else
	      write(unit=33,*) '\t\tDelete duplicate record ',iy, temp1_d2(indx1,iy),temp1_d2(indx2,iy)
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
	  case('rem_nodata')		! TODO: Write and complete and test rem_nodata
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
	      if(trim(var(ivar)%txt1)==trim(head_in(ix,1))) exit
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
	  case('count_2val')		! TODO: Write and complete and test count_2val
	indx1=man(iman)%ind1
	indx2=man(iman)%ind2
	write(unit=33,*) '\tcount ',trim(head_in(indx2,1)),' values per ',trim(head_in(indx1,1))
	if(man(iman)%txt1=='all') then
	  write(unit=33,*) '\t\tsave everything in processing file'
	  fmt='(5(a15,2x))'
	  write(unit=33,fmt) 'Val1','val2','numval2','numrec','lastrec'
	  fmt='(f15.7,2x,f15.7,2x,i15,2x,i15,2x,i15)'
	endif
	if(man(iman)%txt1=='sum') then
	  write(unit=33,*) '\t\tsave only summary data in processing file'
	  fmt='(5(a15,2x))'
	  write(unit=33,fmt) trim(head_in(indx1,1)),'num '//trim(head_in(indx2,1)), 'totrec','firstrec','lastrec'
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
	write(unit=33,*) '\t\t',trim(head_in(indx1,1))//' has ',cnt1, ' different values'
!
!----------------------------------------------------------
! count values
!----------------------------------------------------------
! counts the number of different values of a single variable
! assumes the data is by the variable
!
	  case('count_val')		! TODO: Test count_val
	  write(unit=33,*) 'Count values'
		indx1=man(iman)%ind1
		file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		open(unit=200, file=trim(file_in), form='formatted')
		do iy = 1, y_dim
			write(unit=200, fmt='(F14.7)') temp1_d2(indx1, iy)
		enddo
		close(unit=200)

		cmd = trim(path(i_pat_python)%path1)//'count_values.py'
		cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)

		call system(cmd)

	  open(unit=201, file=trim(file_out), form='formatted')
	  do iy = 1,y_dim
		read(unit=201, fmt='(A)') temp
		write(unit=33, fmt='(A)') trim(temp)
	  enddo
	  close(unit=201)
	! indx1=man(iman)%ind1
	! write(unit=33,*) '\tcount values for ',trim(head_in(indx1,1))
	! fmt='(3(a15,2x))'
	! write(unit=33,fmt) 'Value','numrec','lastrec'
	! fmt='(f15.7,2x,i15,2x,i15)'

! !
! ! count valid records
	! val1=temp1_d2(indx1,1)
	! cnt1=1 ! number different values
	! cnt2=0 ! number valid records per value
	! cnt3=0 ! total valid values
	! do iy=1,y_dim
	  ! if(temp1_d2(indx1,iy)==miss_val_real) print*, indx1,iy,temp1_d2(indx1,iy)
	  ! if(temp1_d2(indx1,iy)/=miss_val_real.and.temp1_d2(indx1,iy)==val1) then
	    ! cnt2=cnt2+1
	    ! cnt3=cnt3+1
	  ! else
	    ! write(unit=33,fmt) val1, cnt2, iy-1
	    ! cnt1=cnt1+1
	    ! cnt2=1
	    ! cnt3=cnt3+1
	    ! val1=temp1_d2(indx1,iy)
	  ! endif
	! enddo
! !
! ! save last set of values
	! write(unit=33,fmt) val1, cnt2, iy-1
! !
! ! write totals
	! write(unit=33,*) '\t\t',trim(head_in(indx1,1))//' has ',cnt1, ' different values'
	! write(unit=33,*) '\t\t','Total valid values: ',cnt3
	! write(unit=33,*) '\t\t','total number records: ',y_dim
!
!----------------------------------------------------------
! count records
!----------------------------------------------------------
	  case('count_rec')		! TODO: test count_rec
	  write(unit=33,*) 'count the number of valid records'
		indx1=man(iman)%ind1
		file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		open(unit=200, file=trim(file_in), form='formatted')
		do iy = 1, y_dim
			write(unit=200, fmt='(F14.7)') temp1_d2(indx1, iy)
		enddo
		close(unit=200)

		cmd = trim(path(i_pat_python)%path1)//'count_records.py'
		cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)

		call system(cmd)

	  open(unit=201, file=trim(file_out), form='formatted')
		read(unit=201, fmt='(A)') temp
		write(unit=33, fmt='(A)') trim(temp)
	  close(unit=201)
	! do ix=lim1,lim2
	  ! write(unit=33,*) '\tcount records'
! !
! ! count valid records
	  ! cnt1=0
	  ! do iy=1,y_dim
	    ! if(temp1_d2(ix,iy)/=miss_val_real) then
	      ! cnt1=cnt1+1
	    ! endif
	  ! enddo
	  ! write(unit=33,*) '\t\t',trim(head_in(ix,1))//': ',cnt1, ' valid values'
	  ! write(unit=33,*) '\t\t','total number records: ',y_dim
	! enddo
!
!----------------------------------------------------------
! check for non-integer values
!----------------------------------------------------------
	  case('chk_int')		! TODO: test chk_int
	  write(unit=33,*) 'check for non-integer values'
		indx1=man(iman)%ind1
		file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		open(unit=200, file=trim(file_in), form='formatted')
		do iy = 1, y_dim
			write(unit=200, fmt='(F14.7)') temp1_d2(indx1, iy)
		enddo
		close(unit=200)

		cmd = trim(path(i_pat_python)%path1)//'check_int.py'
		cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)

		call system(cmd)

	  open(unit=201, file=trim(file_out), form='formatted')
	  do iy = 1,y_dim
		read(unit=201, fmt='(A)') temp
		write(unit=33, fmt='(A)') trim(temp)
	  enddo
	  close(unit=201)

	! do ix=lim1,lim2
	  ! write(unit=33,*) '\tCheck ',trim(head_in(ix,1)), ' for non-integer values'
	  ! val1=man(iman)%val1
	  ! cnt1=0
	  ! do iy=1,y_dim
	    ! val1=mod(temp1_d2(ix,iy),1.)
	    ! if(val1/=0.) then
	      ! cnt1=cnt1+1
	      ! print*, cnt1,iy,temp1_d2(ix,iy)
	    ! endif
	  ! enddo
	! enddo
!
!----------------------------------------------------------
! multiply by constant
!----------------------------------------------------------
	  case('mult_con')
		 file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		 file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		 open(unit=200, file=trim(file_in), form='formatted')
		 fmt = '(F14.7)'
		 do ix=lim1,lim2
			if(man(iman)%num==1) write(unit=33,*) '\tMultiply ',trim(head_in(ix,1)), ' by ',man(iman)%val1
	    if(man(iman)%num==2) write(unit=33,*) '\tMultiply ',trim(head_out(ix,1)), ' by ',man(iman)%val1
			do iy = 1, y_dim
			   write(unit=200,fmt=fmt) temp1_d2(ix,iy)
			enddo
		 enddo
		 close(unit=200)

		 ! Build the command, including passing a float with the -n
		 write(text,'(A,F14.7)') ' -n ',man(iman)%val1
		 cmd = trim(path(i_pat_python)%path1)//'mult_const.py'
		 cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)
		 cmd = trim(cmd)//text

		 call system( cmd )

		 open(unit=201, file=trim(file_out), form='formatted')
		 do indx1 = 1,(lim2-lim1+1)*y_dim
			ix = indx1/(y_dim+1) + lim1
			iy = mod(indx1, y_dim+1)
			read(unit=201, fmt) val1
			temp1_d2(ix,iy) = val1
		 enddo
		 close(unit=201)

!!$	do ix=lim1,lim2
!!$	  if(man(iman)%num==1) write(unit=33,*) '\tMultiply ',trim(head_in(ix,1)), ' by ',man(iman)%val1
!!$	  if(man(iman)%num==2) write(unit=33,*) '\tMultiply ',trim(head_out(ix,1)), ' by ',man(iman)%val1
!!$	  val1=man(iman)%val1
!!$	  do iy=1,y_dim
!!$	    if(temp1_d2(ix,iy)/=miss_val_real) temp1_d2(ix,iy)=temp1_d2(ix,iy)*val1
!!$	  enddo
!!$	enddo
!
!----------------------------------------------------------
! divide by constant
!----------------------------------------------------------
	  case('div_con')
		 file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		 file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		 open(unit=200, file=trim(file_in), form='formatted')
		 fmt = '(F14.7)'
		 do ix=lim1,lim2
			if(man(iman)%num==1) write(unit=33,*) '\tDivide ',trim(head_in(ix,1)), ' by ',man(iman)%val1
			if(man(iman)%num==2) write(unit=33,*) '\tDivide ',trim(head_out(ix,1)), ' by ',man(iman)%val1
			do iy = 1, y_dim
			   write(unit=200,fmt=fmt) temp1_d2(ix,iy)
			enddo
		 enddo
		 close(unit=200)

		 ! Build the command, including passing a float with the -n
		 write(text,'(A,F14.7)') ' -n ',man(iman)%val1
		 cmd = trim(path(i_pat_python)%path1)//'div_const.py'
		 cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)
		 cmd = trim(cmd)//text

		 call system( cmd )

		 open(unit=201, file=trim(file_out), form='formatted')
		 do indx1 = 1,(lim2-lim1+1)*y_dim
			ix = indx1/(y_dim+1) + lim1
			iy = mod(indx1, y_dim+1)
			read(unit=201, fmt) val1
			temp1_d2(ix,iy) = val1
		 enddo
		 close(unit=201)
!!$	do ix=lim1,lim2
!!$	  if(man(iman)%num==1) write(unit=33,*) '\tDivide ',trim(head_in(ix,1)), ' by ',man(iman)%val1
!!$	  if(man(iman)%num==2) write(unit=33,*) '\tDivide ',trim(head_out(ix,1)), ' by ',man(iman)%val1
!!$	  val1=man(iman)%val1
!!$	  if(val1==0.) then
!!$	    print*, 'Error: cannot divide by zero'
!!$	    print*, 'manipulation: ', iman, ' value: ',val1
!!$	    stop
!!$	  endif
!!$	  do iy=1,y_dim
!!$	    if(temp1_d2(ix,iy)/=miss_val_real) temp1_d2(ix,iy)=temp1_d2(ix,iy)*val1
!!$	  enddo
!!$	enddo
!
!----------------------------------------------------------
! add constant
!----------------------------------------------------------
	  case('add_con')
		 file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		 file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		 open(unit=200, file=trim(file_in), form='formatted')
		 fmt = '(F14.7)'
		 do ix=lim1,lim2
			if(man(iman)%num==1) write(unit=33,*) '\tAdd ',man(iman)%val1, ' to ',trim(head_in(ix,1))
			if(man(iman)%num==2) write(unit=33,*) '\tAdd ',man(iman)%val1, ' to ',trim(head_out(ix,1))
			do iy = 1, y_dim
			   write(unit=200,fmt=fmt) temp1_d2(ix,iy)
			enddo
		 enddo
		 close(unit=200)

		 ! Build the command, including passing a float with the -n
		 write(text,'(A,F14.7)') ' -n ',man(iman)%val1
		 cmd = trim(path(i_pat_python)%path1)//'add_const.py'
		 cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)
		 cmd = trim(cmd)//text

		 call system( cmd )

		 open(unit=201, file=trim(file_out), form='formatted')
		 do indx1 = 1,(lim2-lim1+1)*y_dim
			ix = indx1/(y_dim+1) + lim1
			iy = mod(indx1, y_dim+1)
			read(unit=201, fmt) val1
			temp1_d2(ix,iy) = val1
		 enddo
		 close(unit=201)
!!$	do ix=lim1,lim2
!!$	  if(man(iman)%num==1) write(unit=33,*) '\tAdd ',man(iman)%val1, ' to ',trim(head_in(ix,1))
!!$	  if(man(iman)%num==2) write(unit=33,*) '\tAdd ',man(iman)%val1, ' to ',trim(head_out(ix,1))
!!$	  val1=man(iman)%val1
!!$	  do iy=1,y_dim
!!$	    if(temp1_d2(ix,iy)/=miss_val_real) temp1_d2(ix,iy)=temp1_d2(ix,iy)+val1
!!$	  enddo
!!$	enddo
!
!----------------------------------------------------------
! subtract constant
!----------------------------------------------------------
	  case('sub_con')
		 file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		 file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		 open(unit=200, file=trim(file_in), form='formatted')
		 fmt = '(F14.7)'
		 do ix=lim1,lim2
			if(man(iman)%num==1) write(unit=33,*) '\tSubtract ',man(iman)%val1, ' from ',trim(head_in(ix,1))
			if(man(iman)%num==2) write(unit=33,*) '\tSubtract ',man(iman)%val1, ' from ',trim(head_out(ix,1))
			do iy = 1, y_dim
			   write(unit=200,fmt=fmt) temp1_d2(ix,iy)
			enddo
		 enddo
		 close(unit=200)

		 ! Build the command, including passing a float with the -n
		 write(text,'(A,F14.7)') ' -n ',man(iman)%val1
		 cmd = trim(path(i_pat_python)%path1)//'sub_const.py'
		 cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)
		 cmd = trim(cmd)//text

		 call system( cmd )

		 open(unit=201, file=trim(file_out), form='formatted')
		 do indx1 = 1,(lim2-lim1+1)*y_dim
			ix = indx1/(y_dim+1) + lim1
			iy = mod(indx1, y_dim+1)
			read(unit=201, fmt) val1
			temp1_d2(ix,iy) = val1
		 enddo
		 close(unit=201)
!!$	do ix=lim1,lim2

!!$	  val1=man(iman)%val1
!!$	  do iy=1,y_dim
!!$	    if(temp1_d2(ix,iy)/=miss_val_real) temp1_d2(ix,iy)=temp1_d2(ix,iy)-val1
!!$	  enddo
!!$	enddo
!
!----------------------------------------------------------
! replace values equal
!----------------------------------------------------------
	  case('replace_eq')
		 file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		 file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		 open(unit=200, file=trim(file_in), form='formatted')
		 fmt = '(F14.7)'
		 do ix=lim1,lim2
			do iy = 1, y_dim
			   write(unit=200,fmt=fmt) temp1_d2(ix,iy)
			enddo
		 enddo
		 close(unit=200)

		 write(unit=33,*) 'replace ',man(iman)%val1,' with ',man(iman)%val2

		 ! Build the command, including passing floats with the -n flags
		 write(text,'(A,F14.7,A,F14.7)') ' -n ',man(iman)%val1,' -n ',man(iman)%val2
		 cmd = trim(path(i_pat_python)%path1)//'replace_eq.py'
		 cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)
		 cmd = trim(cmd)//text

		 call system( cmd )

		 ! The first line in file_out will be the number of values replaced
		 open(unit=201, file=trim(file_out), form='formatted')
		 do indx1 = 1,(lim2-lim1+1)*y_dim
			read(unit=201, fmt) val1
			if(indx1 == 1) then
			   write(unit=33,*) 'Made ',val1,' replacements'
			else
			   ix = (indx1-1)/(y_dim+1) + lim1
			   iy = mod((indx1-1), y_dim+1)
			   temp1_d2(ix,iy) = val1
			endif
		 enddo
		 close(unit=201)
!!$	do ix=lim1,lim2
!!$	  if(man(iman)%num==1) write(unit=33,*) '\treplace values for ',trim(head_in(ix,1))
!!$	  if(man(iman)%num==2) write(unit=33,*) '\treplace values for ',trim(head_out(ix,1))
!!$	  val1=man(iman)%val1
!!$	  val2=man(iman)%val2
!!$	  write(unit=33,*) '\t\treplace ',val1, ' with ', val2
!!$!
!!$! replace values
!!$	  cnt1=0 ! number of values replaced
!!$	  do iy=1,y_dim
!!$	    if(temp1_d2(ix,iy)==val1) then
!!$	      cnt1=cnt1+1
!!$	      temp1_d2(ix,iy)=val2
!!$	    endif
!!$	  enddo
!!$	  write(unit=33,*) '\t\t',cnt1, ' values replaced'
!!$	  write(unit=33,*) '\t\t','total number records: ',y_dim
!!$	enddo
!
!----------------------------------------------------------
! replace values greater than
!----------------------------------------------------------
	  case('replace_gt')
		 file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		 file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		 write(unit=33,*) 'Replace values > ', man(iman)%val1, ' with ', man(iman)%val2

		 open(unit=200, file=trim(file_in), form='formatted')
		 fmt = '(F14.7)'
		 do ix=lim1,lim2
			do iy = 1, y_dim
			   write(unit=200,fmt=fmt) temp1_d2(ix,iy)
			enddo
		 enddo
		 close(unit=200)

		 ! Build the command, including passing floats with the -n flags
		 write(text,'(A,F14.7,A,F14.7)') ' -n ',man(iman)%val1,' -n ',man(iman)%val2
		 cmd = trim(path(i_pat_python)%path1)//'replace_gt.py'
		 cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)
		 cmd = trim(cmd)//text

		 call system( cmd )

		 ! The first line in file_out will be the number of values replaced
		 open(unit=201, file=trim(file_out), form='formatted')
		 do indx1 = 1,(lim2-lim1+1)*y_dim
			read(unit=201, fmt) val1
			if(indx1 == 1) then
			   write(unit=33,*) 'Made ',val1,' replacements'
			else
			   ix = (indx1-1)/(y_dim+1) + lim1
			   iy = mod((indx1-1), y_dim+1)
			   temp1_d2(ix,iy) = val1
			endif
		 enddo
		 close(unit=201)

!
!----------------------------------------------------------
! replace values greater than or equal to
!----------------------------------------------------------
	  case('replace_ge')
		 file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		 file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		 write(unit=33,*) 'Replace values >= ', man(iman)%val1, ' with ', man(iman)%val2

		 open(unit=200, file=trim(file_in), form='formatted')
		 fmt = '(F14.7)'
		 do ix=lim1,lim2
			do iy = 1, y_dim
			   write(unit=200,fmt=fmt) temp1_d2(ix,iy)
			enddo
		 enddo
		 close(unit=200)

		 ! Build the command, including passing floats with the -n flags
		 write(text,'(A,F14.7,A,F14.7)') ' -n ',man(iman)%val1,' -n ',man(iman)%val2
		 cmd = trim(path(i_pat_python)%path1)//'replace_ge.py'
		 cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)
		 cmd = trim(cmd)//text

		 call system( cmd )

		 open(unit=201, file=trim(file_out), form='formatted')
		 do indx1 = 1,(lim2-lim1+1)*y_dim
			read(unit=201, fmt) val1
			if(indx1 == 1) then
			   write(unit=33,*) 'Made ',val1,' replacements'
			else
			   ix = (indx1-1)/(y_dim+1) + lim1
			   iy = mod((indx1-1), y_dim+1)
			   temp1_d2(ix,iy) = val1
			endif
		 enddo
		 close(unit=201)

!
!----------------------------------------------------------
! replace values less than
!----------------------------------------------------------
	  case('replace_lt')
		 file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		 file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		 write(unit=33,*) 'Replace values < ', man(iman)%val1, ' with ', man(iman)%val2

		 open(unit=200, file=trim(file_in), form='formatted')
		 fmt = '(F14.7)'
		 do ix=lim1,lim2
			do iy = 1, y_dim
			   write(unit=200,fmt=fmt) temp1_d2(ix,iy)
			enddo
		 enddo
		 close(unit=200)

		 ! Build the command, including passing floats with the -n flags
		 write(text,'(A,F14.7,A,F14.7)') ' -n ',man(iman)%val1,' -n ',man(iman)%val2
		 cmd = trim(path(i_pat_python)%path1)//'replace_lt.py'
		 cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)
		 cmd = trim(cmd)//text

		 call system( cmd )

		 open(unit=201, file=trim(file_out), form='formatted')
		 do indx1 = 1,(lim2-lim1+1)*y_dim
			read(unit=201, fmt) val1
			if(indx1 == 1) then
			   write(unit=33,*) 'Made ',val1,' replacements'
			else
			   ix = (indx1-1)/(y_dim+1) + lim1
			   iy = mod((indx1-1), y_dim+1)
			   temp1_d2(ix,iy) = val1
			endif
		 enddo
		 close(unit=201)

!
!----------------------------------------------------------
! replace values less than or equal to
!----------------------------------------------------------
	  case('replace_le')
		 file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		 file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		 write(unit=33,*) 'Replace values <= ', man(iman)%val1, ' with ', man(iman)%val2

		 open(unit=200, file=trim(file_in), form='formatted')
		 fmt = '(F14.7)'
		 do ix=lim1,lim2
			do iy = 1, y_dim
			   write(unit=200,fmt=fmt) temp1_d2(ix,iy)
			enddo
		 enddo
		 close(unit=200)

		 ! Build the command, including passing floats with the -n flags
		 write(text,'(A,F14.7,A,F14.7)') ' -n ',man(iman)%val1,' -n ',man(iman)%val2
		 cmd = trim(path(i_pat_python)%path1)//'replace_le.py'
		 cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)
		 cmd = trim(cmd)//text

		 call system( cmd )

		 open(unit=201, file=trim(file_out), form='formatted')
		 do indx1 = 1,(lim2-lim1+1)*y_dim
			read(unit=201, fmt) val1
			if(indx1 == 1) then
			   write(unit=33,*) 'Made ',val1,' replacements'
			else
			   ix = (indx1-1)/(y_dim+1) + lim1
			   iy = mod((indx1-1), y_dim+1)
			   temp1_d2(ix,iy) = val1
			endif
		 enddo
		 close(unit=201)

 !
!----------------------------------------------------------
! replace values not in a range
!----------------------------------------------------------
case('replace_notin_range')
	write(unit=33,*) 'Replace values outside the range ', man(iman)%val1, '-', man(iman)%val2, ' with ', man(iman)%val3

	file_in = trim(path(i_pat_tmp)%path1)//'temp1'
	file_out = trim(path(i_pat_tmp)%path2)//'temp2'

	open(unit=200, file=trim(file_in), form='formatted')
	do ix = man(iman)%ind1,man(iman)%ind2
		do iy = 1,y_dim
			write(unit=200,fmt='(f14.7)') temp1_d2(ix,iy)
		enddo
	enddo
	close(unit=200)

	write(text, '(A,F14.7)') ' -n ', man(iman)%val1, ' -n ', man(iman)%val2, ' -n ', man(iman)%val3
	cmd = path(i_pat_python)%path1//'replace_notin_rangex.py'
	cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)
	cmd = trim(cmd)//trim(text)

	open(unit=201, file=trim(file_out), form='formatted')
	do indx1 = 1,(lim2-lim1+1)*y_dim
		ix = indx1/(y_dim+1) + lim1
		iy = mod(indx1, y_dim+1)
		read(unit=201,fmt='(f14.7)') val1
		temp1_d2(ix, iy) = val1
	enddo
	close(unit=201)

!
!----------------------------------------------------------
! replace values in a range
!----------------------------------------------------------
case('replace_range')
	write(unit=33,*) 'Replace values outside the range ', man(iman)%val1, '-', man(iman)%val2, ' with ', man(iman)%val3
	file_in = trim(path(i_pat_tmp)%path1)//'temp1'
	file_out = trim(path(i_pat_tmp)%path2)//'temp2'

	open(unit=200, file=trim(file_in), form='formatted')
	do ix = man(iman)%ind1,man(iman)%ind2
		do iy = 1,y_dim
			write(unit=200,fmt='(f14.7)') temp1_d2(ix,iy)
		enddo
	enddo
	close(unit=200)

	write(text, '(A,F14.7)') ' -n ', man(iman)%val1, ' -n ', man(iman)%val2, ' -n ', man(iman)%val3
	cmd = path(i_pat_python)%path1//'replace_rangex.py'
	cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)
	cmd = trim(cmd)//trim(text)

	open(unit=201, file=trim(file_out), form='formatted')
	do indx1 = 1,(lim2-lim1+1)*y_dim
		ix = indx1/(y_dim+1) + lim1
		iy = mod(indx1, y_dim+1)
		read(unit=201,fmt='(f14.7)') val1
		temp1_d2(ix, iy) = val1
	enddo
	close(unit=201)

!
!----------------------------------------------------------
! print values greater than
!----------------------------------------------------------
	  case('print_gt')
		 write(unit=33,*) 'Print values > ', man(iman)%val1
		 file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		 file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		 open(unit=200, file=trim(file_in), form='formatted')
		 fmt = '(F14.7)'
		 do ix=lim1,lim2
			do iy = 1, y_dim
			   write(unit=200,fmt=fmt) temp1_d2(ix,iy)
			enddo
		 enddo
		 close(unit=200)

		 ! Build the command, including passing a float with the -n flag
		 write(text,'(A,F14.7)') ' -n ',man(iman)%val1
		 cmd = trim(path(i_pat_python)%path1)//'print_gt.py'
		 cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)
		 cmd = trim(cmd)//text

		 call system( cmd )

		 open(unit=201, file=trim(file_out), form='formatted')
		 read(unit=201, fmt=fmt) val1
		 do indx1 = 1,int(val1)
			read(unit=201,fmt='(A)') text
			write(unit=33,*) trim(text)
		 enddo
		 close(unit=201)
!!$	  write(unit=33,*) '\tPrint values > ', man(iman)%val1
!!$	  val1=man(iman)%val1
!!$	  indx1=man(iman)%ind1
!!$!
!!$! find first valid point
!!$	  do iy=1,y_dim
!!$	    if(temp1_d2(indx1,iy)/=miss_val_real.and.temp1_d2(indx1,iy)>val1) then
!!$	      print*, iy,temp1_d2(indx1,iy)
!!$	    endif
!!$	  enddo
!
!----------------------------------------------------------
! print values less than
!----------------------------------------------------------
	  case('print_lt')
		 write(unit=33,*) 'Print values < ', man(iman)%val1
		 file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		 file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		 open(unit=200, file=trim(file_in), form='formatted')
		 fmt = '(F14.7)'
		 do ix=lim1,lim2
			do iy = 1, y_dim
			   write(unit=200,fmt=fmt) temp1_d2(ix,iy)
			enddo
		 enddo
		 close(unit=200)

		 ! Build the command, including passing a float with the -n flag
		 write(text,'(A,F14.7)') ' -n ',man(iman)%val1
		 cmd = trim(path(i_pat_python)%path1)//'print_lt.py'
		 cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)
		 cmd = trim(cmd)//text

		 call system( cmd )

		 open(unit=201, file=trim(file_out), form='formatted')
		 read(unit=201, fmt=fmt) val1
		 do indx1 = 1,int(val1)
			read(unit=201,fmt='(A)') text
			write(unit=33,*) trim(text)
		 enddo
		 close(unit=201)
!!$	  write(unit=33,*) '\tPrint values < ', man(iman)%val1
!!$	  val1=man(iman)%val1
!!$	  indx1=man(iman)%ind1
!!$!
!!$! find first valid point
!!$	  do iy=1,y_dim
!!$	    if(temp1_d2(indx1,iy)/=miss_val_real.and.temp1_d2(indx1,iy)<val1) then
!!$	      print*, iy,temp1_d2(indx1,iy)
!!$	    endif
!!$	  enddo
!
!----------------------------------------------------------
! print max and min values
!----------------------------------------------------------
	  case('print_max')
		 write(unit=33,*) 'Print max and min '
		 file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		 file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		 open(unit=200, file=trim(file_in), form='formatted')
		 fmt = '(F14.7)'
		 do ix=lim1,lim2
			do iy = 1, y_dim
			   write(unit=200,fmt=fmt) temp1_d2(ix,iy)
			enddo
		 enddo
		 close(unit=200)

		 cmd = trim(path(i_pat_python)%path1)//'print_max.py'
		 cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)

		 call system( cmd )

		 open(unit=201, file=trim(file_out), form='formatted')
		 read(unit=201, fmt=fmt) val1
		 do indx1 = 1,int(val1)
			read(unit=201,fmt='(A)') text
			write(unit=33,*) trim(text)
		 enddo
		 close(unit=201)
!!$	do ix=lim1,lim2
!!$	  write(unit=33,*) '\tPrint Min and Max'
!!$!
!!$! find first valid point
!!$	  do iy=1,y_dim
!!$	    if(temp1_d2(ix,iy)/=miss_val_real) then
!!$	      val1=temp1_d2(ix,iy)
!!$	      val2=temp1_d2(ix,iy)
!!$	      exit
!!$	    endif
!!$	  enddo
!!$!
!!$! go through rest of points
!!$	  if(iy<=y_dim) then
!!$	    do iy=1,y_dim
!!$	      val1=max(val1,temp1_d2(ix,iy))
!!$	      val2=min(val2,temp1_d2(ix,iy))
!!$	    enddo
!!$	    write(unit=33,*) '\t\t',trim(head_in(ix,1))//' max: ',val1, ' min: ',val2
!!$	  else
!!$	    write(unit=33,*) '\t\t',trim(head_in(ix,1))//' min/max: no valid points'
!!$	  endif
!!$	enddo
!
!----------------------------------------------------------
! print mean and standard deviation
!----------------------------------------------------------
	  case('print_mean')
		 file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		 file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		 write(unit=33,*) 'Print mean and standard deviation'

		 open(unit=200, file=trim(file_in), form='formatted')
		 fmt = '(F14.7)'
		 do ix=lim1,lim2
			do iy = 1, y_dim
			   write(unit=200,fmt=fmt) temp1_d2(ix,iy)
			enddo
		 enddo
		 close(unit=200)

		 ! Build the command
		 cmd = trim(path(i_pat_python)%path1)//'print_mean.py'
		 cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)

		 call system( cmd )

		 open(unit=201, file=trim(file_out), form='formatted')
		 do indx1=1,4
			read(unit=201,*) text
			write(unit=33,*) trim(text)
		 enddo
		 close(unit=201)

!!$	write(unit=33,*) '\tPrint mean and standard deviation'
!!$	do ix=lim1,lim2
!!$          val1=0.
!!$          val2=0.
!!$	  cnt1=0.
!!$	  do iy=1,y_dim
!!$	    if(temp1_d2(ix,iy)/=miss_val_real) then
!!$	      val1=val1+temp1_d2(ix,iy)
!!$	      cnt1=cnt1+1
!!$	    endif
!!$	  enddo
!!$	  if(cnt1/=0.) val1=val1/cnt1
!!$	  do iy=1,y_dim
!!$	    if(temp1_d2(ix,iy)/=miss_val_real) val2=val2+(val1-temp1_d2(ix,iy))**2.
!!$	  enddo
!!$	  if(cnt1/=0.) then
!!$	    val2=sqrt(val2/cnt1)
!!$	    write(unit=33,*) '\t\t',trim(head_in(ix,1))//' mean:',val1, ' std: ',val2,' pts:',cnt1
!!$	  else
!!$	    write(unit=33,*) '\t\t',trim(head_in(ix,1))//' mean/std: no valid points'
!!$	  endif
!!$	enddo
!
!----------------------------------------------------------
! create JSON metadata file
!----------------------------------------------------------
		 case('metadata')
		 file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		 file_out = trim(path(i_pat_out)%path1)//'metadata.json'

		 open(unit=200, file=trim(file_in), form='formatted')
		 fmt = '(F14.7)'
		 do ix=lim1,lim2
			do iy = 1, y_dim
			   write(unit=200,fmt=fmt) temp1_d2(ix,iy)
			enddo
		 enddo
		 close(unit=200)

		 ! Build the command
		 ! TODO: Complete this expression
		 cmd = path(i_pat_python)%path1//'create_gtnp_metadata_json.py'
		 cmd = trim(cmd)//' -t /sharehome/hwilcox/DIT/template.json'
		 cmd = trim(cmd)//' -c '

		 call system( cmd )

		 open(unit=201, file=trim(file_out), form='formatted')
		 do indx1=1,4
			read(unit=201,*) text
			write(unit=33,*) trim(text)
		 enddo
		 close(unit=201)

!
!----------------------------------------------------------
! move text from one column to another
!----------------------------------------------------------
		 ! case('move_text')
		 ! file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		 ! file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		 ! open(unit=200, file=trim(file_in), form='formatted')
		 ! fmt = '(F14.7)'
		 ! do ix=lim1,lim2
			! do iy = 1, y_dim
			   ! write(unit=200,fmt=fmt) temp1_d2(ix,iy)
			! enddo
		 ! enddo
		 ! close(unit=200)

		 ! ! Build the command
		 ! cmd = '/usr/bin/python/ /sharehome/hwilcox/DIT/move_text.py'
		 ! cmd = trim(cmd)//' -i '//file_in
		 ! cmd = trim(cmd)//' -o '//file_out
		 ! cmd = trim(cmd)//' -f '//man(iman)%txt1
		 ! cmd = trim(cmd)//' -t '//man(iman)%txt2

		 ! call system( cmd )

		 ! open(unit=201, file=trim(file_out), form='formatted')
		 ! do indx1=1,4
			! read(unit=201,*) text
			! write(unit=33,*) trim(text)
		 ! enddo
		 ! close(unit=201)

!
! end manipulations
	end select
!
! transfer data back to data variable
	select case(man(iman)%num)
	  case(1) ! input data
	data_in=temp1_d2
	char_in=temp1_char2
	  case(2) ! output data
	data_out=temp1_d2
	char_out=temp1_char2
	end select
!
! deallocate local variable
	deallocate(temp1_d2)
	deallocate(temp1_char2)
	deallocate(var_tmp)
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
	real, allocatable :: class_num(:)         ! temporary class number
	Character*45, allocatable :: class_name(:)         ! temporary class name
	logical flag  ! generic flag
!
! grid definition file
	do ipat=1,n_path
	  if(trim(path(ipat)%typ)=='grid_def') filename=trim(path(ipat)%path1)
	enddo
	print*, '\t\tGrid def file: ', trim(filename)
	write(unit=33,*) '\t\tGrid def file: ', trim(filename)
	open(unit=9,file=trim(filename),form='formatted', status='old')

	read (9,11) junk,n_grid ! read number of grids defined in file
	read (9,10) junk
	do igrd=1,n_grid
	  read (9,*) grid_r%name, grid_r%type, grid_r%lonmin, grid_r%latmin, grid_r%Dlon, grid_r%Dlat, grid_r%lon_offset, grid_r%lat_offset, grid_r%nlon, grid_r%nlat
	  if(trim(grid_r%name)==trim(man(iman)%txt1)) exit
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
	allocate(temp2_d2(grid_r%nlon,grid_r%nlat))
	ipat=man(iman)%ind1
	filename=trim(path(ipat)%path1)
	varname=trim(path(ipat)%txt2)
	print*, '\t\tmap: ',trim(filename)
	write(unit=33,*) '\t\tmap: ',trim(filename)
	print*, '\t\tvariable: ', trim(varname)
	write(unit=33,*) '\t\tvariable: ', trim(varname)
	call read_single_netcdf_c(filename,varname,grid_r%nlon,grid_r%nlat,temp2_d2)
!
! locate latitude and longitude variable index
	do ivar=1,n_var
	  if(trim(man(iman)%txt2)==trim(var(ivar)%txt1)) indx_varlon=var(ivar)%ind1
	  if(trim(man(iman)%txt3)==trim(var(ivar)%txt1)) indx_varlat=var(ivar)%ind1
	enddo
!
! nearest neighbor matching
	allocate(temp1_d1(y_dim))
	allocate(temp1_char1(y_dim))
	do irec=1,y_dim
	  indx_lonmap=(data_in(indx_varlon,irec)-grid_r%lonmin)/grid_r%dlon+1
	  indx_latmap=(data_in(indx_varlat,irec)-grid_r%latmin)/grid_r%dlat+1
	  temp1_d1(irec)=temp2_d2(indx_lonmap,indx_latmap)
	enddo
!
! read in number to text matching file
	ipat=man(iman)%ind2
	filename=trim(path(ipat)%path1)
	print*, trim(filename)
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
!      print*, irec,temp1_d1(irec),trim(temp1_char1(irec))
	  write(unit=33,*) irec,temp1_d1(irec),trim(temp1_char1(irec))
	enddo
!
! put into data array
	do irec=1,y_dim
	  temp1_char2(man(iman)%ind3,irec)=trim(temp1_char1(irec))
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
	real dlon       ! (deg) delta longitude of time zone
	real lonmin     ! (deg) minimumlongitude of GMT time zone
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
