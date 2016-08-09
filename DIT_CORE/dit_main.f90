!=========================================================================
      program data_integration_tool
!=========================================================================
! The Data Integration Tool (DIT) reformats and processes generic
! datasets into a common format
!
! Modifications:
!  Kevin Schaefer created program from the grid program (12/12/14)
!
    use dit_variables
!
    implicit none
!
! define variables
    integer ifil ! data file index
    integer iman ! manipulation index
    integer ipat ! path index
    logical temp_flag ! generic flag
    Character*20 case ! input/output case
!
! print message
    print*, 'Process Data Files'
!
! read program inputs
    call read_inputs
!
! process inpiut data files
    do ifil=1,n_file
!
! print file name
      print*, ifil, trim(file(ifil)%path1)
      open(unit=33, file='./output/'//trim(file(ifil)%path1))
      write(unit=33,*) '----------------------------------------'
      write(unit=33,*) ifil, trim(file(ifil)%path1)
      write(unit=33,*) '----------------------------------------'
!
! read in mapping file
      call read_variable_mapping_file(ifil)
!
! read data
      if(trim(file(ifil)%typ)=='ascii') then
         temp_flag=.false.
	 call read_ascii_data(ifil,temp_flag)
      endif
      if(trim(file(ifil)%typ)=='ascii_fil') call read_ascii_filter(ifil)
      if(trim(file(ifil)%typ)=='python') call read_python_data(ifil)
!
! manipulate input data
      do iman=1,n_man
        if(man(iman)%doit.and.man(iman)%num==1) call manipulate_data(ifil,iman)
      enddo
!
! construct output data array
      call construct_output_array
!
! manipulate output data
      do iman=1,n_man
        if(man(iman)%doit.and.man(iman)%num==2) call manipulate_data(ifil,iman)
      enddo
!
! write output file(s)
      do iman=1,n_man
        if(man(iman)%doit.and.man(iman)%num==3) call write_data(ifil,iman)
      enddo
!
! deallocate variables
      deallocate(var)
      deallocate(data_in)
      deallocate(data_out)
      deallocate(head_in)
    enddo
!
    end program data_integration_tool
