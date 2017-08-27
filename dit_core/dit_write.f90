!
!===================================================
  subroutine kml_point(ifil,iman)
!===================================================
! Creates a single kml point file containing all files
!
    use dit_variables
!
    implicit none
!
! input variables
    integer ifil ! data file index
    integer iman ! manipulation number
!
! internal variables
    integer irec  ! output record index
    Character*250 text ! text string
    Character*60 fmt   ! text string format
    Character*250 kml(100)   ! kml file
    Character*60 txt_lon ! longitude text version
    Character*60 txt_lat ! latitude text version
    Character*60 txt_alt ! alt text version
!
! save message
    write(unit=33,*) '\tCreate output kml line file'
! ind1 = pathnum reference kml file
! ind2 = pathnum output kml
! ind3 = varnum longitude
! ind4 = varnum latitude
! ind5 = varnum point label
!
! read reference kml file
    filename=trim(path(man(iman)%ind1)%path1)
    open(Unit=60, file=trim(filename), form='formatted')
    do irec=1,10
        read(unit=60,fmt='(a180)') kml(irec)
    enddo
    close(60)
!
! open output kml file
    if(ifil==1) then
      filename=trim(path(man(iman)%ind2)%path1)
      open(Unit=611, file=trim(filename), form='formatted')
      fmt='(a250)'
      do irec=1,3
        write(unit=611,fmt) kml(irec)
      enddo
    endif
!
! write file header
    text='	<name>'//trim(file(ifil)%path1)//'</name>'
    fmt='(a250)'
    write(unit=611,fmt) text
!
! write points to kml file
    fmt='(a250)'
    do irec=1,out%n_rec
      write(unit=611,fmt) kml(5)

      text='      <name>'//trim(char_out(man(iman)%ind5,irec))//'</name>'
      write(unit=611,fmt) text

      write(txt_lon,*) data_out(man(iman)%ind3,irec)
      write(txt_lat,*) data_out(man(iman)%ind4,irec)
      txt_lon=adjustl(txt_lon)
      txt_lat=adjustl(txt_lat)
      text='      <Point><coordinates>'//trim(txt_lon)//','//trim(txt_lat)//'</coordinates></Point>'
      write(unit=611,*) trim(text)

      write(unit=611,fmt) kml(8)

    enddo
!
! close filename and kml file
    if (ifil==n_file) then
      write(unit=611,fmt) kml(9)
      write(unit=611,fmt) kml(10)
      close(unit=611)
    endif

    end subroutine
!
!===================================================
  subroutine kml_sqr(ifil,iman)
!===================================================
! Creates a single kml line file containing all files
!
    use dit_variables
!
    implicit none
!
! input variables
    integer ifil ! data file index
    integer iman ! manipulation number
!
! internal variables
    integer ilin  ! kml ref line index
    integer irec  ! output record index
    integer ipt   ! point index
    double precision box(2,5)   ! point index
    Character*250 text ! text string
    Character*60 fmt   ! text string format
    Character*250 kml(100)   ! kml file
    Character*60 txt_lon ! longitude text version
    Character*60 txt_lat ! latitude text version
    Character*60 txt_alt ! alt text version
!
! save message
    write(unit=33,*) '\tCreate output kml line file'
! ind1 = pathnum reference kml file
! ind2 = pathnum output kml
! ind3 = varnum longitude
! ind4 = varnum latitude
! ind5 = polygon name
!
! read reference kml file
    filename=trim(path(man(iman)%ind1)%path1)
    open(Unit=60, file=trim(filename), form='formatted')
    do ilin=1,36
        read(unit=60,fmt='(a200)') kml(ilin)
    enddo
    close(60)
!
! open output kml file
    filename=trim(path(man(iman)%ind2)%path1)
    print*, '\tfilename: ', trim(filename)
    open(Unit=611, file=trim(filename), form='formatted')
    fmt='(a250)'
    do ilin=1,3
      write(unit=611,fmt) kml(ilin)
    enddo
    text='	<name>'//trim(man(iman)%txt1)//'</name>'
    write(unit=611,fmt) text
    do ilin=5,19
      write(unit=611,fmt) kml(ilin)
    enddo
!
! write polygons
    fmt='(a250)'
    do irec=1,out%n_rec
!
! write placemark header to kml file
      write(unit=611,fmt) kml(20)
      text='               <name>'//trim(char_out(man(iman)%ind5,irec))//'</name>'
      write(unit=611,fmt) text
      text='               <description>'//trim(char_out(man(iman)%ind5,irec))//'</description>'
      write(unit=611,fmt) text
      do ilin=23,28
        write(unit=611,fmt) kml(ilin)
      enddo
!
! write line elements(points) to kml file
! box(1,:) lon
! box(2,:) lat
      box(1,1)=data_out(man(iman)%ind3,irec)-man(iman)%val1
      box(2,1)=data_out(man(iman)%ind4,irec)-man(iman)%val2

      box(1,2)=data_out(man(iman)%ind3,irec)+man(iman)%val1
      box(2,2)=data_out(man(iman)%ind4,irec)-man(iman)%val2

      box(1,3)=data_out(man(iman)%ind3,irec)+man(iman)%val1
      box(2,3)=data_out(man(iman)%ind4,irec)+man(iman)%val2

      box(1,4)=data_out(man(iman)%ind3,irec)-man(iman)%val1
      box(2,4)=data_out(man(iman)%ind4,irec)+man(iman)%val2

      box(1,5)=box(1,1)
      box(2,5)=box(2,1)
      
      do ipt=1,5
        write(txt_lon,*) box(1,ipt)
        write(txt_lat,*) box(2,ipt)
        txt_lon=adjustl(txt_lon)
        txt_lat=adjustl(txt_lat)
	
        text=trim(txt_lon)//','//trim(txt_lat)
        text=adjustl(text)
        write(unit=611,*) trim(text)
      enddo
!
! write placemark footer to kml file
      do ilin=30,34
        write(unit=611,fmt) kml(ilin)
      enddo
    enddo
!
! close filename and kml file
    write(unit=611,fmt) kml(35)
    write(unit=611,fmt) kml(36)
    close(unit=611)

    end subroutine
!
!===================================================
  subroutine kml_line(ifil,iman)
!===================================================
! Creates a single kml line file containing all files
!
    use dit_variables
!
    implicit none
!
! input variables
    integer ifil ! data file index
    integer iman ! manipulation number
!
! internal variables
    integer irec  ! output record index
    Character*250 text ! text string
    Character*60 fmt   ! text string format
    Character*250 kml(100)   ! kml file
    Character*60 txt_lon ! longitude text version
    Character*60 txt_lat ! latitude text version
    Character*60 txt_alt ! alt text version
!
! save message
    write(unit=33,*) '\tCreate output kml line file'
! ind1 = pathnum reference kml file
! ind2 = pathnum output kml
! ind3 = varnum longitude
! ind4 = varnum latitude
!
! read reference kml file
    filename=trim(path(man(iman)%ind1)%path1)
    open(Unit=60, file=trim(filename), form='formatted')
    do irec=1,31
        read(unit=60,fmt='(a69)') kml(irec)
    enddo
    close(60)
!
! open output kml file
    if(ifil==1) then
      filename=trim(path(man(iman)%ind2)%path1)
      open(Unit=611, file=trim(filename), form='formatted')
      fmt='(a250)'
      do irec=1,3
        write(unit=611,fmt) kml(irec)
      enddo
      text='	<name>'//trim(man(iman)%txt1)//'</name>'
      write(unit=611,fmt) text
      do irec=5,15
        write(unit=611,fmt) kml(irec)
      enddo
    endif
!
! write placemark header to kml file
    fmt='(a250)'
    write(unit=611,fmt) kml(16)
    text='               <name>'//trim(file(ifil)%path2)//'</name>'
    write(unit=611,fmt) text
    do irec=18,24
      write(unit=611,fmt) kml(irec)
    enddo
!
! write line elements(points) to kml file
    do irec=1,out%n_rec
      write(txt_lon,*) data_out(man(iman)%ind3,irec)
      write(txt_lat,*) data_out(man(iman)%ind4,irec)
      txt_lon=adjustl(txt_lon)
      txt_lat=adjustl(txt_lat)
	
      text=trim(txt_lon)//','//trim(txt_lat)
      text=adjustl(text)
      write(unit=611,*) trim(text)
    enddo
!
! write placemark footer to kml file
    do irec=27,29
      write(unit=611,fmt) kml(irec)
    enddo
!
! closedouble precision filename and kml file
    if (ifil==n_file) then
      write(unit=611,fmt) kml(30)
      write(unit=611,fmt) kml(31)
      close(unit=611)
    endif

    end subroutine
!
!===================================================
  subroutine kml_wall(ifil,iman)
!===================================================
! Creates a single kml wall file containing all files
!
    use dit_variables
!
    implicit none
!
! input variables
    integer ifil ! data file index
    integer iman ! manipulation number
!
! internal variables
    integer irec  ! output record index
    Character*250 text ! text string
    Character*60 fmt   ! text string format
    Character*250 kml(100) ! kml file
    Character*60 txt_lon   ! longitude text version
    Character*60 txt_lat   ! latitude text version
    Character*60 txt_alt   ! alt text version
!
! save message
    write(unit=33,*) '\tCreate output kml wall file'
!
! ind1 = pathnum reference kml file
! ind2 = pathnum output kml
! ind3 = varnum longitude
! ind4 = varnum latitude
! ind5 = varnum wall height
!
! read reference kml file
    filename=trim(path(man(iman)%ind1)%path1)
    open(Unit=60, file=trim(filename), form='formatted')
    do irec=1,31
        read(unit=60,fmt='(a69)') kml(irec)
    enddo
    close(60)
!
! open output kml file
    if(ifil==1) then
      filename=trim(path(man(iman)%ind2)%path1)
      open(Unit=612, file=trim(filename), form='formatted')
      fmt='(a250)'
      do irec=1,3
        write(unit=612,fmt) kml(irec)
      enddo
      text='	<name>'//trim(man(iman)%txt1)//'</name>'
      write(unit=612,fmt) text
      do irec=5,15
        write(unit=612,fmt) kml(irec)
      enddo
    endif
!
! write placemark header to kml file
    fmt='(a250)'
    write(unit=612,fmt) kml(16)
    text='               <name>'//trim(file(ifil)%path2)//'</name>'
    write(unit=612,fmt) text
    do irec=18,24
      write(unit=612,fmt) kml(irec)
    enddo
!
! write line elements(points) to kml file
    do irec=1,out%n_rec
      if(data_out(man(iman)%ind5,irec)/=miss_val_real) then

        if(irec>1.and.data_out(man(iman)%ind5,irec-1)==miss_val_real) then
          write(txt_lon,*) data_out(man(iman)%ind3,irec-1)
          write(txt_lat,*) data_out(man(iman)%ind4,irec-1)
          txt_lon=adjustl(txt_lon)
          txt_lat=adjustl(txt_lat)
          text=trim(txt_lon)//','//trim(txt_lat)//',0.'
          text=adjustl(text)
          write(unit=612,*) trim(text)
	endif

        write(txt_lon,*) data_out(man(iman)%ind3,irec)
        write(txt_lat,*) data_out(man(iman)%ind4,irec)
	write(txt_alt,*) data_out(man(iman)%ind5,irec)
        txt_lon=adjustl(txt_lon)
        txt_lat=adjustl(txt_lat)
        txt_alt=adjustl(txt_alt)
        text=trim(txt_lon)//','//trim(txt_lat)//','//trim(txt_alt)
        text=adjustl(text)
        write(unit=612,*) trim(text)

        if(irec<out%n_rec.and.data_out(man(iman)%ind5,irec+1)==miss_val_real) then
          write(txt_lon,*) data_out(man(iman)%ind3,irec+1)
          write(txt_lat,*) data_out(man(iman)%ind4,irec+1)
          txt_lon=adjustl(txt_lon)
          txt_lat=adjustl(txt_lat)
          text=trim(txt_lon)//','//trim(txt_lat)//',0.'
          text=adjustl(text)
          write(unit=612,*) trim(text)
	endif
      endif
    enddo
!
! write placemark footer to kml file
    do irec=27,29
      write(unit=612,fmt) kml(irec)
    enddo
!
! close filename and kml file
    if (ifil==n_file) then
      write(unit=612,fmt) kml(30)
      write(unit=612,fmt) kml(31)
      close(unit=612)
    endif

    end subroutine
!
!===================================================
  subroutine make_csv_data_file(ifil,case)
!===================================================
! Writes a standard csv file
!
    use dit_variables
!
    implicit none
!
! input variables
    integer ifil      ! data file index
    Character*20 case ! what to write out as csv
!
! internal variables
    integer ipat  ! path index
    integer irec  ! output record index
    integer ivar  ! output variable index
    integer imap  ! input variable index
    integer iout  ! output variable index
    integer count ! count value
    integer i_val ! integer value
    Character*1000 text  ! text string
    Character*60 temp   ! text string
    Character*60 fmt    ! write format
    character*20 typ    ! variable type
    Character*250 temp_file  ! temporary file name
    Character*250 path_typ ! path type
    logical flg_out     ! flag for writing output array
    double precision, allocatable :: data_wrt(:,:)          ! temp write data array
    Character*50, allocatable :: char_wrt(:,:) ! temp write character array
!
! move what you are writing to local temporary arrays
    select case(case)
      case('in_temp') ! write input arrays to temporary file
        x_dim=in%n_var
        y_dim=in%n_rec
        allocate(data_wrt(x_dim,y_dim))
        allocate(char_wrt(x_dim,y_dim))
        allocate(head1_tmp(x_dim))
        allocate(fmt_tmp(x_dim))
        allocate(typ_tmp(x_dim))
        data_wrt=temp1_d2
        char_wrt=temp1_char2
        head1_tmp=head_in(:,1)
        fmt_tmp=var_in(:)%fmt1
        typ_tmp=var_in(:)%typ
	flg_out=.false.
        path_typ='temp'
	temp_file='temp1'
      case('out_temp') ! write output arrays to temporary file
        x_dim=out%n_var
        y_dim=out%n_rec
        allocate(data_wrt(x_dim,y_dim))
        allocate(char_wrt(x_dim,y_dim))
        allocate(head1_tmp(x_dim))
        allocate(fmt_tmp(x_dim))
        allocate(typ_tmp(x_dim))
        data_wrt=temp1_d2
        char_wrt=temp1_char2
        head1_tmp=head_out(:,1)
        fmt_tmp=var_out(:)%fmt1
        typ_tmp=var_out(:)%typ
	flg_out=.true.
        path_typ='temp'
	temp_file='temp1'
      case('out') ! write output arrays to output directory file
        x_dim=out%n_var
        y_dim=out%n_rec
        allocate(data_wrt(x_dim,y_dim))
        allocate(char_wrt(x_dim,y_dim))
        allocate(head1_tmp(x_dim))
        allocate(fmt_tmp(x_dim))
        allocate(typ_tmp(x_dim))
        data_wrt=data_out
        char_wrt=char_out
        head1_tmp=head_out(:,1)
        fmt_tmp=var_out(:)%fmt1
        typ_tmp=var_out(:)%typ
	flg_out=.true.
        path_typ='outpath'
	temp_file=trim(file(ifil)%path2)//'.csv'
      case('shred_tmp') ! write shredded output arrays to temp directory
        x_dim=tmp%n_var
        y_dim=tmp%n_rec
        allocate(data_wrt(x_dim,y_dim))
        allocate(char_wrt(1,y_dim))
        allocate(head1_tmp(x_dim))
        allocate(fmt_tmp(x_dim))
        allocate(typ_tmp(x_dim))
        data_wrt=temp1_d2(1:x_dim,1:y_dim)
        char_wrt(1,:)=temp1_char1(1:y_dim)
        head1_tmp=head1_tmp(1:x_dim)
        fmt_tmp=var_shd(:)%fmt1
        typ_tmp=var_shd(:)%typ
	flg_out=.true.
        path_typ='temp'
	temp_file='temp1'
      case('shred_out')  ! write shredded output arrays to final directory
        x_dim=tmp%n_var
        y_dim=tmp%n_rec
        allocate(data_wrt(x_dim,y_dim))
        allocate(char_wrt(x_dim,y_dim))
        allocate(head1_tmp(x_dim))
        allocate(fmt_tmp(x_dim))
        allocate(typ_tmp(x_dim))
        data_wrt=temp1_d2(1:x_dim,1:y_dim)
        char_wrt(1,:)=temp1_char1(1:y_dim)
        head1_tmp=head1_tmp(1:x_dim)
        fmt_tmp=var_shd(:)%fmt1
        typ_tmp=var_shd(:)%typ
	flg_out=.true.
        path_typ='outpath'
	temp_file=trim(id)
    end select
!
! find output path
    do ipat = 1, n_path
      if(path(ipat)%typ==trim(path_typ)) exit
    enddo
!
! open output csv file
    filename=trim(path(ipat)%path1)//trim(temp_file)
    print*, '\t\tout csv file: ', trim(filename)
    write(unit=33,*) '\t\tout csv file: ', trim(filename)
    open(unit=70,file=trim(filename),form='formatted')
!
! write header
    text=''
    do ivar=1,x_dim
      text=trim(text)//trim(head1_tmp(ivar))
      if(ivar<x_dim) text=trim(text)//','
    enddo
    write(unit=70,*) trim(text)
!
! write to csv file
    do irec=1,y_dim
      text=''
      do ivar=1,x_dim
	fmt=fmt_tmp(ivar)
	typ=typ_tmp(ivar)

	if(trim(typ)=='integer') then
	  i_val=data_wrt(ivar,irec)
	  write(temp,fmt=fmt) i_val
	  temp=adjustl(temp)
	endif

        if(trim(typ)=='real') then
	  write(temp,fmt=fmt) data_wrt(ivar,irec)
	  temp=adjustl(temp)
	endif

	if(trim(typ)=='char') then
	  temp=trim(char_wrt(ivar,irec))
	  temp=adjustl(temp)
	endif

	text=trim(text)//trim(temp)
	if(ivar<x_dim)text=trim(text)//','
      enddo
      write(unit=70,*) trim(text)
    enddo
    close(unit=70)
!
! deallocate temporary variables
    deallocate(data_wrt)
    deallocate(char_wrt)
    deallocate(head1_tmp)
    deallocate(fmt_tmp)
    deallocate(typ_tmp)
!
    end subroutine
!
!===================================================
  subroutine append_csv_data_file(ifil,iman)
!===================================================
! appends to a standard csv file
!
    use dit_variables
!
    implicit none
!
! input variables
    integer ifil      ! data file index
    integer iman      ! manipulation number
    Character*20 case ! what to write out as csv
!
! internal variables
    integer ipat  ! path index
    integer irec  ! output record index
    integer ivar  ! output variable index
    integer imap  ! input variable index
    integer iout  ! output variable index
    integer count ! count value
    integer i_val ! integer value
    Character*1000 text  ! text string
    Character*60 temp   ! text string
    Character*60 fmt    ! write format
    character*20 typ    ! variable type
    Character*250 temp_file  ! temporary file name
    Character*250 path_typ ! path type
    logical flg_out     ! flag for writing output array
    double precision, allocatable :: data_wrt(:,:)          ! temp write data array
    Character*50, allocatable :: char_wrt(:,:) ! temp write character array
!
! move what you are writing to local temporary arrays
    case='out'
    select case(case)
      case('out') ! write output arrays to output directory file
        x_dim=out%n_var
        y_dim=out%n_rec
        allocate(data_wrt(x_dim,y_dim))
        allocate(char_wrt(x_dim,y_dim))
        allocate(head_tmp(x_dim))
        allocate(fmt_tmp(x_dim))
        allocate(typ_tmp(x_dim))
        data_wrt=data_out
        char_wrt=char_out
        head_tmp=head_out(:,1)
        fmt_tmp=var_out(:)%fmt1
        typ_tmp=var_out(:)%typ
	flg_out=.true.
        path_typ='outpath'
	temp_file=trim(file(ifil)%path2)//'.csv'
    end select
!
! open output csv file
    ipat=man(iman)%ind1
    filename=trim(path(ipat)%path1)
    print*, '\t\tout csv file: ', trim(filename)
    write(unit=33,*) '\t\tout csv file: ', trim(filename)
!
! set up file
    if(ifil==1) then ! open and write header
      open(unit=70,file=trim(filename),form='formatted')
      text=''
      do ivar=1,x_dim
        text=trim(text)//trim(head_tmp(ivar))
        if(ivar<x_dim) text=trim(text)//','
      enddo
      write(unit=70,*) trim(text)
    else ! just open
      open(unit=70,file=trim(filename),form='formatted', status='old', Position='append')
    endif
!
! write to csv file
    do irec=1,y_dim
      text=''
      do ivar=1,x_dim
	fmt=fmt_tmp(ivar)
	typ=typ_tmp(ivar)

	if(trim(typ)=='integer') then
	  i_val=data_wrt(ivar,irec)
	  write(temp,fmt=fmt) i_val
	  temp=adjustl(temp)
	endif

        if(trim(typ)=='real') then
	  write(temp,fmt=fmt) data_wrt(ivar,irec)
	  temp=adjustl(temp)
	endif

	if(trim(typ)=='char') then
	  temp=trim(char_wrt(ivar,irec))
	  temp=adjustl(temp)
	endif

	text=trim(text)//trim(temp)
	if(ivar<x_dim)text=trim(text)//','
      enddo
      write(unit=70,*) trim(text)
    enddo
    close(unit=70)
!
! deallocate temporary variables
    deallocate(data_wrt)
    deallocate(char_wrt)
    deallocate(head_tmp)
    deallocate(fmt_tmp)
    deallocate(typ_tmp)
!
    end subroutine
!
!===================================================
  subroutine shred_reset(irec)
!===================================================
! resets shred counting variables, clears arrays
!
    use dit_variables
!
    implicit none
!
! input variables
    integer irec  ! output record index
!
! clear out arrays
    temp1_d2=miss_val_real
    temp1_d1=miss_val_real
    temp1_char1=miss_val_char
    head1_tmp=miss_val_char
!
! set initial variable and record count
    tmp%n_rec=0   ! initial number records
    tmp%n_var=2   ! initial number columns (1=y value, 2= first x value)
!
! set first site ID
    id=trim(char_out(indx_id,irec))           ! first site ID value
!
! set first x-value (col)
    temp1_d1(tmp%n_var)=data_out(indx_x,irec) ! first x (col) value
!
    end subroutine
!
!===================================================
  subroutine shred_prep_for_write(ifil,iman)
!===================================================
! prepares a shredded file for writing
!
    use dit_variables
!
    implicit none
!
! input variables
    integer ifil ! data file index
    integer iman ! manipulation number
!
! internal variables
    integer irec  ! output record index
    integer ivar  ! output variable index
    integer i_val ! integer value
    integer count ! count value
    Character*1000 text     ! text string
    Character*200 fmt      ! text string format
    Character*20  case     ! what to write/read
    Character*250 file_in  ! input file for python script
    Character*250 file_out ! output file from pythn script
    Character*250 cmd      ! command variable for system call
    Character*60 temp   ! text string
    character*20 typ    ! variable type
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
! allocate shred variable mapping array and header
    allocate(var_shd(tmp%n_var))   ! variable mapping
!
! fill in shred variable mapping file and header
    var_shd(1)=var_out(indx_y)
    head1_tmp(1)=trim(var_shd(1)%txt2)
    do ivar=2,tmp%n_var
      var_shd(ivar)=var_out(indx_x)
      fmt=trim(var_shd(ivar)%fmt1)

      if(trim(var_shd(ivar)%typ)=='integer') then
        i_val=temp1_d1(ivar)
        write(text,fmt=fmt) i_val
        text=adjustl(text)
      endif

      if(trim(var_shd(ivar)%typ)=='real') then
        write(text,fmt=fmt) temp1_d1(ivar)
        text=adjustl(text)
      endif

      var_shd(ivar)%txt2=trim(text)
      head1_tmp(ivar)=trim(text)
    enddo
!
!-------------------------------------------------------
! sort by date
!-------------------------------------------------------
!
! temp file names
    file_in=trim(path(i_pat_tmp)%path1)//'temp1'  ! input file to script
    file_out=trim(path(i_pat_tmp)%path1)//'temp2' ! output file from script
!
! save to temp file for sorting by date
    open(unit=70,file=trim(file_in),form='formatted')
!
! write header
    text=''
    do ivar=1,tmp%n_var
      text=trim(text)//trim(head1_tmp(ivar))
      if(ivar<tmp%n_var) text=trim(text)//','
    enddo
    write(unit=70,*) trim(text)
!
! write to temporary csv file
    do irec=1,tmp%n_rec
      text=''
      do ivar=1,tmp%n_var
	fmt=var_shd(ivar)%fmt1
	typ=var_shd(ivar)%typ

	if(trim(typ)=='integer') then
	  i_val=temp1_d2(ivar,irec)
	  write(temp,fmt=fmt) i_val
	  temp=adjustl(temp)
	endif

        if(trim(typ)=='real') then
	  write(temp,fmt=fmt) temp1_d2(ivar,irec)
	  temp=adjustl(temp)
	endif

	if(trim(typ)=='char') then
	  temp=trim(temp1_char1(irec))
	  temp=adjustl(temp)
	endif

	text=trim(text)//trim(temp)
	if(ivar<tmp%n_var)text=trim(text)//','
      enddo
      write(unit=70,*) trim(text)
    enddo
    close(unit=70)
!
! command to execute python sort script
    cmd=trim(path(i_pat_python)%path1)//'sort_by_columns.py'
    cmd=trim(cmd)//' -i '//trim(file_in)
    cmd=trim(cmd)//' -o '//trim(file_out)
    text=qd//'[(0, '//qs//'dt'//qs//')]'//qd
    cmd=trim(cmd)//' -l '//trim(text)
!
! call system command to sort shredded arrays by date
    call system( trim(cmd) )
!
! read sorted data back in
    allocate(temp2_char1(tmp%n_var))
    temp1_d2=miss_val_real    ! z values
    temp1_char1=miss_val_char ! dates
    open(unit=70,file=trim(file_out),form='formatted')
    read(unit=70,*) temp
    do irec=1,tmp%n_rec
      read(unit=70,*) temp2_char1
      do ivar=1,tmp%n_var
        if(var_shd(ivar)%typ=='char')    temp1_char1(irec)   =trim(temp2_char1(ivar))
        if(var_shd(ivar)%typ=='real')    read(temp2_char1(ivar),*) temp1_d2(ivar,irec)
        if(var_shd(ivar)%typ=='integer') read(temp2_char1(ivar),*) temp1_d2(ivar,irec)
      enddo
    enddo
    close(unit=70)
!
!-------------------------------------------------------
! compress array 
!-------------------------------------------------------
! allocate second set of temporary arrays
    allocate(temp2_d2(max_xvar,out%n_rec))
    allocate(temp2_char1(out%n_rec))
    temp2_d2=miss_val_real
    temp2_char1=miss_val_char
!
! initialize record counter 
    count=1
!
! remove duplicate dates
    temp2_d2(:,1)=temp1_d2(:,1)
    temp2_char1(1)=temp1_char1(1)
    do irec=2,tmp%n_rec
      if(temp1_char1(irec)==temp1_char1(irec-1)) then ! duplicate date
        do ivar=2,tmp%n_var
          if(temp1_d2(ivar,irec)/=miss_val_real) temp2_d2(ivar,count)=temp1_d2(ivar,irec)
        enddo
      else ! new date
        count=count+1
        temp2_d2(:,count)=temp1_d2(:,irec)
        temp2_char1(count)=temp1_char1(irec)
      endif
    enddo
!
! reset number of records
    tmp%n_rec=count
!
! transfer compressed data back to working array
    temp1_d2=temp2_d2
    temp1_char1=temp2_char1
!
! deallocate temp arrays
    deallocate(temp2_d2)
    deallocate(temp2_char1)
!
    end subroutine
!
!===================================================
  subroutine shred_csv_data_files(ifil,iman)
!===================================================
! Shreds the output file into multiple csv GTN-P files
!
    use dit_variables
!
    implicit none
!
! input variables
    integer ifil ! data file index
    integer iman ! manipulation number
!
! internal variables
    integer ipat  ! path index
    integer irec  ! output record index
    integer ivar  ! output variable index
    integer imap  ! input variable index
    integer iout  ! output variable index
    integer count ! count value
    integer inum  ! number index
    integer i_val ! integer value
    Character*250 text ! text string
    Character*60 temp  ! text string
    Character*60 fmt   ! text string format
    Character*20  case     ! what to write/read
!
! save message
    write(unit=33,*) '\tExpand to create multiple output CSV files'
    print*, '\tExpand to create multiple output CSV files'
!
! set x,y,val indeces
! assumes data is already sorted by station ID, x value, and y value
    indx_id=man(iman)%ind1 ! site ID index
    indx_x=man(iman)%ind2  ! x/column value index
    indx_y=man(iman)%ind3  ! y/row value index
    indx_z=man(iman)%ind4  ! z value index
!
! allocate temporary output arrays assuming maximum of 100 x values
    max_xvar=25
    allocate(temp1_d2(max_xvar,out%n_rec)) ! square array
    allocate(temp1_d1(max_xvar))           ! x/column values
    allocate(temp1_char1(out%n_rec))       ! y/row values
    allocate(head1_tmp(max_xvar))          ! header
!
! set initial values
    call shred_reset(1)
!
! loop through records in output array
    do irec=1, out%n_rec
!
! check for change in site ID (new file)
      if(trim(char_out(indx_id,irec))/=trim(id)) then
	call shred_prep_for_write(ifil,iman)
        case='shred_out'
        call make_csv_data_file(ifil,case)
        call shred_reset(irec)
      endif    
!
! increment number of records
      tmp%n_rec=tmp%n_rec+1
!
! Check for change in x value (new column)
      if(data_out(indx_x,irec)/=temp1_d1(tmp%n_var)) then
        tmp%n_var=tmp%n_var+1
        temp1_d1(tmp%n_var)=data_out(indx_x,irec)
      endif
!
! move data to temporary square array
      temp1_d2(tmp%n_var,tmp%n_rec)=data_out(indx_z,irec)
      temp1_char1(tmp%n_rec)=trim(char_out(indx_y,irec))
!
! end of record loop
     enddo
!
! save last file
    call shred_prep_for_write(ifil,iman)
    case='shred_out'
    call make_csv_data_file(ifil,case)
!
! deallocate temporary arrays
    deallocate(temp1_d2)
    deallocate(temp1_d1)
    deallocate(temp1_char1)
    deallocate(head1_tmp)

    end subroutine
!
!===================================================
  subroutine make_json_metadata_file(idat)
!===================================================
! makes a metadata file in json format
!
    use dit_variables
!
    implicit none
!
! input variables
    integer idat ! data file index
!
! internal variables
    integer ipat   ! path index
    integer irec   ! output record index
    integer item   ! template line index
    integer ivar   ! output variable index
    integer imap   ! input variable index
    integer iout   ! output variable index
    integer count  ! count value
    integer i_val  ! integer value
    integer n_line ! number lines in template
    Character*250 text ! text string
    Character*250,allocatable :: template(:) ! json template file
    Character*250,allocatable :: json(:)     ! output json file
    Character*250,allocatable :: json_var(:) ! json template variable names
    Character*250 temp  ! text string
    Character*60 fmt   ! text string format
    integer status ! read status variable
!
! print message
    print*, '\tcreate output json metadata file'
    write(unit=33,*) '\tcreate output json metadata file'
!
! locate template
    ipat=file(idat)%npath4
    filename=trim(path(ipat)%path1)
    print*, '\tjson template: ',trim(filename)
!
! open template and count the lines
    open(unit=70, file=trim(filename), form='formatted', status='old')
    n_line=0
    do item=1,10e26
      read(unit=70,*, iostat=status) text
      if(status<0) exit
      n_line=n_line+1
    enddo
    close(unit=70)
    allocate(template(n_line))
    allocate(json(n_line))
    allocate(json_var(n_line))
!
! read in json template (full text)
    open(unit=70, file=trim(filename), form='formatted', status='old')
    fmt='(a250)'
    do item=1, n_line
      read(unit=70,fmt) template(item)
    enddo
    close(unit=70)
!
! read in json variables
    open(unit=70, file=trim(filename), form='formatted', status='old')
    do item=1, n_line
      read(unit=70,*) json_var(item)
    enddo
    close(unit=70)
!
! open output json file
    ipat=file(idat)%npath2
    filename=trim(trim(path(ipat)%path1))//trim(file(idat)%path2)
    print*, trim(filename)
    open(unit=70, file=trim(filename), form='formatted')
!
! loop through outputd and make a json record for each
    do irec=1,out%n_rec
      json=template
!
! match data_out variables to template variables
      do ivar=1,n_var
        if(var(ivar)%flg2) then
          do imap=1,n_line
	    if(trim(var(ivar)%txt2)==trim(json_var(imap))) then
	      if(trim(var(ivar)%typ)=='char') then
	        temp='\t\t"'//trim(json_var(imap))//'": "'//trim(char_out(var(ivar)%ind2,irec))//'",'
	        json(imap)=temp
	        print*, imap,trim(var(ivar)%txt2),': ',trim(char_out(var(ivar)%ind2,irec))
	      endif
	      if(trim(var(ivar)%typ)=='real') then
	        fmt=trim(var(ivar)%fmt1)
	        write(text,fmt) data_out(var(ivar)%ind2,irec)
	        temp='\t\t"'//trim(json_var(imap))//'": "'//trim(text)//'",'
	        json(imap)=temp
	        print*, imap,trim(var(ivar)%txt2),': ',trim(text)
	      endif
	      if(trim(var(ivar)%typ)=='integer') then
		count=data_out(var(ivar)%ind2,irec)
	        fmt=trim(var(ivar)%fmt1)
	        write(text,fmt) count
	        temp='\t\t"'//trim(json_var(imap))//'": "'//trim(text)//'",'
	        json(imap)=temp
	        print*, imap,trim(var(ivar)%txt2),': ',trim(text)
	      endif
	      exit
	    endif
	  enddo
        endif
      enddo
!
! write json record to output json file
      do item=1, n_line
        write(unit=70,*) json(item)
      enddo
    enddo
!
! close json file
    close(unit=70)

    end subroutine
!
!===================================================
  subroutine construct_output_array
!===================================================
! constructs and fills the output data array
!
    use dit_variables
!
    implicit none
!
! internal variables
    integer ivar ! input variable index
    integer i_in ! input variable index
!
! variable specification key
! var_out(ivar)%num   num
! var_out(ivar)%txt1  In_var
! var_out(ivar)%txt2  Out_var
! var_out(ivar)%flg1  in
! var_out(ivar)%flg2  out
! var_out(ivar)%ind1  o_in
! var_out(ivar)%ind2  o_out
! var_out(ivar)%map   map_typ
! var_out(ivar)%typ   typ
! var_out(ivar)%fmt1  fmt
! var_out(ivar)%txt3  units
! var_out(ivar)%txt4  Description
!
! print message
    write(unit=33,*) '\tConstruct output array'
!
! allocate output data arrays
    allocate(data_out(out%n_var,out%n_rec))
    allocate(char_out(out%n_var,out%n_rec))
    allocate(head_out(out%n_var,out%n_hed))
!
! clear all data and character output
    data_out=miss_val_real
    Char_out=trim(miss_val_char)
    head_out=trim(miss_val_char)
!
! fill output variable header
    do ivar=1,out%n_var
      head_out(ivar,1)=var_out(ivar)%txt2
    enddo
!
! copy from input to output arrays
    do ivar=1,out%n_var
      if(var_out(ivar)%map=='copy') then
        i_in=var_out(ivar)%ind1
        if(var_out(ivar)%typ=='real')    data_out(ivar,:)=data_in(i_in,:)
        if(var_out(ivar)%typ=='integer') data_out(ivar,:)=data_in(i_in,:)
        if(var_out(ivar)%typ=='char')    char_out(ivar,:)=char_in(i_in,:)
      endif
    enddo
!
    end subroutine
!
!===================================================
      subroutine write_data(ifil,iman)
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
    Character*20 case ! what to write out as csv
!
! print output
    print*, '\t',trim(man(iman)%typ)
!
! scan through output options
    select case(man(iman)%typ)
!
!----------------------------------------------------------
! kml point file
!----------------------------------------------------------
      case('kml_point')
        call kml_point(ifil,iman)
!
!----------------------------------------------------------
! kml line file
!----------------------------------------------------------
      case('kml_line')
        call kml_line(ifil,iman)
!
!----------------------------------------------------------
! kml polygon file
!----------------------------------------------------------
      case('kml_sqr')
        call kml_sqr(ifil,iman)
!
!----------------------------------------------------------
! kml wall file
!----------------------------------------------------------
      case('kml_wall')
        call kml_wall(ifil,iman)
!
!----------------------------------------------------------
! shred vector file into multiple square files
!----------------------------------------------------------
      case('shred')
        call shred_csv_data_files(ifil,iman)
!
!----------------------------------------------------------
! write individual csv file
!----------------------------------------------------------
      case('csv')
        case='out'
	call make_csv_data_file(ifil,case)
!
!----------------------------------------------------------
! append to single csv file
!----------------------------------------------------------
      case('csv_app')
	call append_csv_data_file(ifil,iman)
!
!----------------------------------------------------------
! write json file
!----------------------------------------------------------
      case('jsn')
 	call make_json_metadata_file(ifil)
!
! end output options
    end select
!
    end subroutine
