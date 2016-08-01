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
		 write(text,'(A,I5,A,A,A,F14.7,A,F14.7,A,A,A,A)') ' -b ',man(iman)%ind2,' -m ',trim(man(iman)%txt1),' -l ',man(iman)%val1,' -u ',man(iman)%val2,' -t ',trim(man(iman)%txt2),' -n ',trim(man(iman)%txt3)
		 cmd = trim(path(i_pat_python)%path1)//'pdf.py'
		 cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)
		 cmd = trim(cmd)//text

		 call system(cmd)

		 open(unit=201, file=trim(file_out), form='formatted')
		 do indx1 = 1,(man(iman)%ind2 + 2)
			read(unit=201, fmt='(A)') text
			write(unit=33,*) trim(text)
		 enddo
		 close(unit=201)

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
	write(unit=33,*) 'reformat date to GTN-P standard'
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
case('repl_text')
	write(unit=33,*) 'Replace text: '//trim(man(iman)%txt1)//' with '//trim(man(iman)%txt2)
	file_in = trim(path(i_pat_tmp)%path1)//'temp1'
	file_out = trim(path(i_pat_tmp)%path1)//'temp2'

	fmt = '(A)'

	!needs to be given indices of columns to read from
	open(unit=200, file=trim(file_in), form='formatted')
	do indx1 = 1,y_dim
		! ind1 is place
		write(unit=200, fmt=fmt) trim(temp1_char2(man(iman)%ind1, indx1))
	enddo
	close(unit=200)

	! -i <input file> -o <output file> -t <text to replace> -w <replacement>
	cmd = trim(path(i_pat_python)%path1)//'replace_text.py'
	cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)
	cmd = trim(cmd)//' -t '//trim(man(iman)%txt1)//' -w '//trim(man(iman)%txt2)

	call system(cmd)

	open(unit=201, file=trim(file_out), form='formatted')
	do indx1 = 1,y_dim
		read(unit=201, fmt=fmt) text
		temp1_char2(man(iman)%ind1, indx1) = text
		! temp1_char2(man(iman)%ind2, indx1) = temp
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
			write(unit=200,fmt=fmt) temp1_char2(man(iman)%ind1,iy), temp1_d2(man(iman)%ind2,iy), temp1_d2(man(iman)%ind3,iy)
		enddo
		close(unit=200)

		! Build the command, using all the arguments
		cmd = trim(path(i_pat_python)%path1)//'find_tz.py'
		cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)
		cmd = trim(cmd)//' -d '//'0'//' -t '//'1'//' -n '//'2'

		call system(cmd)

		open(unit=201, file=trim(file_out), form='formatted')
		do indx1 = 1, y_dim
			read(unit=201, fmt='f14.7,f14.7') temp1_d2(man(iman)%ind4, iy), temp1_d2(man(iman)%ind5, iy)
		enddo
		close(unit=201)

!----------------------------------------------------------
! remove a set of characters from character data
!----------------------------------------------------------
	case('rm_chars')
		write(unit=33,*) 'remove characters: '//trim(man(iman)%txt1)
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
		cmd = trim(cmd)//' -c '//man(iman)%txt1

		call system(cmd)

		open(unit=201, file=trim(file_out), form='formatted')
		do iy = 1, y_dim
			read(unit=201, fmt='(a10)') temp
			temp1_char2(indx1, iy) = trim(temp)
		enddo
		close(unit=201)

		!
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
		cmd = trim(cmd)//' -z '//'0'//' -e '//'1'//' -n '//'2'
		cmd = trim(cmd)//' -h '//man(iman)%txt1

		call system(cmd)

		open(unit=201, file=trim(file_out), form='formatted')
		do indx1 = 1, y_dim
			read(unit=201, fmt='f14.7,f14.7') temp1_d2(man(iman)%ind4, iy), temp1_d2(man(iman)%ind5, iy)
		enddo
		close(unit=201)

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
		cmd = trim(cmd)//' -t '//'0'//' -n '//'1'

		call system(cmd)

		open(unit=201, file=trim(file_out), form='formatted')
		do iy = 1, y_dim
			read(unit=201, fmt='f14.7,f14.7,a3') temp1_d2(man(iman)%ind4, iy), temp1_d2(man(iman)%ind5, iy), temp1_char2(man(iman)%ind6, iy)
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
		do indx1 = 1,7
			read(unit=201, fmt='(A)') text
			write(unit=33,*) trim(text)
		enddo
		close(unit=201)
!
! mean value, standard deviation, valid points, coverage frac!
!----------------------------------------------------------
! sort records in increasing order
!----------------------------------------------------------
! uses external python script
	  case('sort')		! TODO: copy sort
		if(man(iman)%num==1) then
		  write(unit=33,*) 'Sort input records in increasing order'
		  case='in_temp'
		endif
		if(man(iman)%num==2) then
		  write(unit=33,*) 'Sort output records in increasing order'
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
	  case('rem_dup')		! TODO: test rem_dup
		write(unit=33,*) 'Remove duplicate records'
		case = 'in_temp'
		call make_csv_data_file(ifil, case)

		file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		cmd = trim(path(i_pat_python)%path1)//'remove_duplicate.py'
		cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)

		call system(cmd)

		call read_csv_file(ifil, case)
!
!----------------------------------------------------------
! remove layers with no data from variable mapping file
!----------------------------------------------------------
	  case('rem_nodata')		! TODO: test rem_nodata
		write(unit=33,*) 'Remove null records'
		case = 'in_temp'
		call make_csv_data_file(ifil, case)

		file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		cmd = trim(path(i_pat_python)%path1)//'remove_null.py'
		cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)

		call system(cmd)

		call read_csv_file(ifil, case)
!
!----------------------------------------------------------
! count values per value
!----------------------------------------------------------
! counts the number of different values for a combination of 2 variables
! i.e. number of values for variable 2 per value of variable 1
! assumes the data is presorted first by var1 then by var2
	  case('count_2val')
		write(unit=33,*) 'Count values'
		indx1=man(iman)%ind1
		indx2=man(iman)%ind2
		file_in = trim(path(i_pat_tmp)%path1)//'temp1'
		file_out = trim(path(i_pat_tmp)%path1)//'temp2'

		open(unit=200, file=trim(file_in), form='formatted')
		do iy = 1, y_dim
			write(unit=200, fmt='(F14.7,A,F14.7)') temp1_d2(indx1, iy), ',',temp1_d2(indx2, iy)
		enddo
		close(unit=200)

		cmd = trim(path(i_pat_python)%path1)//'count_values.py'
		cmd = trim(cmd)//' -i '//trim(file_in)//' -o '//trim(file_out)
		cmd = trim(cmd)//' -m '//'double'

		call system(cmd)

	  open(unit=201, file=trim(file_out), form='formatted')
	  read(unit=201, fmt='(I7)') num
	  do iy = 1,num
		read(unit=201, fmt='(A)') temp
		write(unit=33, fmt='(A)') trim(temp)
	  enddo
	  close(unit=201)

!
!----------------------------------------------------------
! count values
!----------------------------------------------------------
! counts the number of different values of a single variable
! assumes the data is by the variable
!
	  case('count_val')
	  write(unit=33,*) 'Count unique, valid values'
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
		read(unit=201, fmt='(A)') temp
		write(unit=33, fmt=' (A)') trim(temp)
	  close(unit=201)

!
!----------------------------------------------------------
! count records
!----------------------------------------------------------
	  case('count_rec')
	  write(unit=33,*) 'Count the number of valid records'
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
			if(man(iman)%num==1) write(unit=33,*) 'Multiply ',trim(head_in(ix,1)), ' by ',man(iman)%val1
	    if(man(iman)%num==2) write(unit=33,*) 'Multiply ',trim(head_out(ix,1)), ' by ',man(iman)%val1
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
			if(man(iman)%num==1) write(unit=33,*) 'Divide ',trim(head_in(ix,1)), ' by ',man(iman)%val1
			if(man(iman)%num==2) write(unit=33,*) 'Divide ',trim(head_out(ix,1)), ' by ',man(iman)%val1
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
			if(man(iman)%num==1) write(unit=33,*) 'Add ',man(iman)%val1, ' to ',trim(head_in(ix,1))
			if(man(iman)%num==2) write(unit=33,*) 'Add ',man(iman)%val1, ' to ',trim(head_out(ix,1))
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
			if(man(iman)%num==1) write(unit=33,*) 'Subtract ',man(iman)%val1, ' from ',trim(head_in(ix,1))
			if(man(iman)%num==2) write(unit=33,*) 'Subtract ',man(iman)%val1, ' from ',trim(head_out(ix,1))
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

		 write(unit=33,*) 'Replace ',man(iman)%val1,' with ',man(iman)%val2

		 ! Build the command, including passing floats with the -n flags
		 write(text,'(A,F14.7,A,F14.7)') ' -t ',man(iman)%val1,' -v ',man(iman)%val2
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
		 write(text,'(A,F14.7,A,F14.7)') ' -t ',man(iman)%val1,' -v ',man(iman)%val2
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
		 write(text,'(A,F14.7,A,F14.7)') ' -t ',man(iman)%val1,' -v ',man(iman)%val2
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
		 write(text,'(A,F14.7,A,F14.7)') ' -t ',man(iman)%val1,' -v ',man(iman)%val2
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
		 write(text,'(A,F14.7,A,F14.7)') ' -t ',man(iman)%val1,' -v ',man(iman)%val2
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

	write(text, '(A,F14.7)') ' -l ', man(iman)%val1, ' -u ', man(iman)%val2, ' -v ', man(iman)%val3
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

	write(text, '(A,F14.7)') ' -l ', man(iman)%val1, ' -u ', man(iman)%val2, ' -v ', man(iman)%val3
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
		 write(text,'(A,F14.7)') ' -t ',man(iman)%val1
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
		 write(text,'(A,F14.7)') ' -t ',man(iman)%val1
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
		 cmd = trim(path(i_pat_python)%path1)//'create_gtnp_metadata_json.py'
		 cmd = trim(cmd)//' -t '//trim(path(i_pat_python)%path1)//'gtnp_metadata_template.json'
		 !cmd = trim(cmd)//' -c '//

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
	subroutine map_look_up(iman) ! TODO: Convert map_lookup
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
