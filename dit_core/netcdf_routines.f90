!
!===================================================
      subroutine read_vecmap_time(filename,varname,dim1,dim2,recnum,outmap)
!===================================================
! reads a 1-D vector of land points and transfers them to a 2-D map
! assumes netcdf file is closed
! assumes unlimited time dimension: multiple maps for each variable
!
! Modifications:
!  Kevin Schaefer created routine (6/3/2003)
!  Kevin Schaefer added deallocation of land vectors (5/12/2009)
!---------------------------------------------------
!
      use netcdf
      use typeSizes
!
      implicit none
!
! input
      Character*100 filename ! netcdf file name
      Character*20 varname   ! netcdf variable name
      integer dim1           ! first dimension of map
      integer dim2           ! second dimension of map
      integer recnum         ! netcdf time record number of variable
!
! input/output
      real outmap(dim1,dim2) ! 2-d map of values read from netcdf file
!
! internal variables
      integer i,j,k,l,m,n  ! generic indeces
      Character*20 subname ! subroutine name for error handling
      integer file_id      ! netcdf file id number
      integer varid        ! netcdf variable id number
      integer dimid        ! netcdf dimension id number
      integer nland        ! number land points
      integer status       ! successful execution status number
      integer start(2)     ! starting index location to read
      real, allocatable :: landvec(:)     ! vector of land point values read from netcdf file
      integer, allocatable :: latindx(:)  ! latitude index locations
      integer, allocatable :: lonindx(:)  ! longitude index locations
!
! set subroutine name
      subname='read_vecmap_time'
!
! open netcdf file and get file id number
      status=nf90_open(trim(filename),0,file_id)
      call Handle_Err(subname,1,status)
!
! get landpoint dimension id number
      status=nf90_inq_dimid(file_id,'subcount',dimid)
      call Handle_Err(subname,2,status)
!
! get dimension (number of land points)
      status=nf90_inquire_dimension(file_id,dimid, len=nland)
      call Handle_Err(subname,3,status)
!
! allocate land vectors
      allocate(landvec(nland))
      allocate(latindx(nland))
      allocate(lonindx(nland))
!
! get variable id number
      status=nf90_inq_varid(file_id,trim(varname),varid)
      call Handle_Err(subname,4,status)
!
! set read starting point (recnum is assumed to be time record)
      start(1)=1      ! vector starting point
      start(2)=recnum ! time record starting point
!
! get vector of land points
      status=nf90_get_var(file_id,varid,landvec,start=start)
      call Handle_Err(subname,5,status)
!
! get lat index id number
      status=nf90_inq_varid(file_id,'latindex',varid)
      call Handle_Err(subname,6,status)
!
! get lat indeces
      status=nf90_get_var(file_id,varid,latindx)
      call Handle_Err(subname,7,status)
!
! get lon index id number
      status=nf90_inq_varid(file_id,'lonindex',varid)
      call Handle_Err(subname,8,status)
!
! get lon indeces
      status=nf90_get_var(file_id,varid,lonindx)
      call Handle_Err(subname,9,status)
!
! close netcdf file
      status=nf90_close(file_id)
      call Handle_Err(subname,10,status)
!
! map vector of values onto 2-D map
      do i=1,nland
        outmap(lonindx(i),latindx(i))=landvec(i)
      enddo
!
! deallocate land vectors
      deallocate(landvec)
      deallocate(latindx)
      deallocate(lonindx)
!
      end subroutine
!
!===================================================
      Subroutine Handle_Err(subname,location,status)
!===================================================
! checks if error ocurred, prints netcdf standard
! error description to the screen, and stops program
!
! Modifications:
!  Kevin Schaefer created routine (2/1/2000)
!---------------------------------------------------
!
      use netcdf
      use typeSizes
!
      implicit none
!
      Integer Status       ! successful execution status number
      Character*20 subname ! subroutine name where error occured
      integer location     ! location of error in subroutine
!
! check to see if error occured
      if (Status/=nf90_noerr) then
        print *, 'error in ', trim(subname), ' at',location
        print *, 'error: ',status,nf90_strerror(STATUS)
        stop 'Stopped'
      endif
!
      return
!
      END subroutine handle_err
!
