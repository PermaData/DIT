!
!===================================================
      subroutine read_3d_closed(filename,varname,dim1,dim2,dim3,array)
!===================================================
! reads a 3-D array from a closed netcdf file
! assumes netcdf file is closed
! assumes unlimited time dimension: multiple values for each variable
!
      use netcdf
      use typeSizes
!
      implicit none
!
! input
      Character*200 filename  ! netcdf file name
      Character*20 varname    ! variable name number for netcdf file type
      integer dim1   ! 1st dimension of variable (num land pts)
      integer dim2   ! 2nd dimension of variable (num time) 
      integer dim3   ! 3rd dimension of variable (num time) 
!
! output
      real array(dim1,dim2,dim3)  ! array of values read from netcdf file
!
! internal variables
      Character*20 subname ! subroutine name for error handling
      integer file_id      ! netcdf file id number
      integer varid        ! variable id number
      integer status       ! successful execution status number
!
! set subroutine name
      subname='read_3d_closed'
!
! open netcdf file and get file id number
      status=nf90_open(trim(filename),0,file_id)
      call Handle_Err(subname,1,status)
!
! get variable id number
      status=nf90_inq_varid(file_id,trim(varname),varid)
      call Handle_Err(subname,2,status)
!
! get array
      status=nf90_get_var(file_id,varid,array)
      call Handle_Err(subname,3,status)
!
! close netcdf file
      status=nf90_close(file_id)
      call Handle_Err(subname,4,status)
!
      end subroutine
!
!===================================================
      subroutine read_2d_closed_ascii(filename,varname,dim1,dim2,nhead,array)
!===================================================
! reads a 2-D array from a closed netcdf file
! assumes netcdf file is closed
!
      implicit none
!
! input
      Character*200 filename  ! netcdf file name
      Character*20 varname    ! variable name number for netcdf file type
      integer dim1   ! 1st dimension of variable
      integer dim2   ! 2nd dimension of variable 
      integer nhead  ! number header lines 
!
! output
      real array(dim1,dim2)  ! array of values read from netcdf file
!
! internal variables
      integer i,j,k,l,m,n  ! indeces
      Character*20 subname ! subroutine name for error handling
      Character*100 junk ! subroutine name for error handling
      integer file_id      ! netcdf file id number
      integer varid        ! variable id number
      integer status       ! successful execution status number
      real temp(dim1)  ! array of values read from netcdf file
!
! set subroutine name
      subname='read_2d_closed'
!
! open netcdf file and get file id number
      open(unit=99,file=trim(filename),form='formatted')
!
! read header
      do i=1,nhead
        read(unit=99,*) junk
      enddo
!
! read data
      do i=1,dim2
         read(unit=99,*) temp
	 array(:,i)=temp
      enddo
!
! close file
      close(unit=99)
      
      end subroutine
!
!===================================================
      subroutine read_2d_closed(filename,varname,dim1,dim2,array)
!===================================================
! reads a 2-D array from a closed netcdf file
! assumes netcdf file is closed
!
      use netcdf
      use typeSizes
!
      implicit none
!
! input
      Character*200 filename  ! netcdf file name
      Character*20 varname    ! variable name number for netcdf file type
      integer dim1   ! 1st dimension of variable (num land pts)
      integer dim2   ! 2nd dimension of variable (num time) 
!
! output
      real array(dim1,dim2)  ! array of values read from netcdf file
!
! internal variables
      Character*20 subname ! subroutine name for error handling
      integer file_id      ! netcdf file id number
      integer varid        ! variable id number
      integer status       ! successful execution status number
!
! set subroutine name
      subname='read_2d_closed'
!
! open netcdf file and get file id number
      status=nf90_open(trim(filename),0,file_id)
      call Handle_Err(subname,1,status)
!
! get variable id number
      status=nf90_inq_varid(file_id,trim(varname),varid)
      call Handle_Err(subname,2,status)
!
! get array
      status=nf90_get_var(file_id,varid,array)
      call Handle_Err(subname,3,status)
!
! close netcdf file
      status=nf90_close(file_id)
      call Handle_Err(subname,4,status)
!
      end subroutine
!
!===================================================
      subroutine read_n80_weather(filename,varname,dim1,nland,vector)
!===================================================
! reads a 2-D map from a closed netcdf file
! assumes netcdf file is closed
! assumes no time dimension: only a single map for each variable
!
      use netcdf
      use typeSizes
!
      implicit none
!
! input
      Character*200 filename  ! netcdf file name
      Character*20 varname    ! variable name number for netcdf file type
      integer dim1   ! first dimension of variable
      integer recnum ! time record number of variable
!
! input/output
      real vector(dim1,3)  ! vector of lat/lon values read from netcdf file
!
! internal variables
      integer, i, j, k, l, m, n ! indeces
      Character*20 subname ! subroutine name for error handling
      integer file_id      ! netcdf file id number
      integer varid        ! variable id number
      integer dimid        ! variable id number
      integer status       ! successful execution status number
      real, allocatable :: latvec(:)  ! vector of land points
      real, allocatable :: lonvec(:)  ! vector of land points
      real, allocatable :: maskvec(:)  ! vector of land points
      integer nland
!
! set subroutine name
      subname='read_n80_weather'
!
! open netcdf file and get file id number
      status=nf90_open(trim(filename),0,file_id)
      call Handle_Err(subname,1,status)
!
! dimension id number
      status=nf90_inq_dimid(file_id,'ngpts',dimid)
      call Handle_Err(subname,2,status)
!
! dimension lenth
      status=nf90_inquire_dimension(file_id,dimid, len=nland)
      call Handle_Err(subname,3,status)
      allocate(latvec(nland))
      allocate(lonvec(nland))
      allocate(maskvec(nland))
!
! get land mask id number
      status=nf90_inq_varid(file_id,trim(varname),varid)
      call Handle_Err(subname,2,status)
!
! get land mask
      status=nf90_get_var(file_id,varid,maskvec)
      call Handle_Err(subname,3,status)
!
! transfer to vector
      do i=1,nland
        vector(i,3)=maskvec(i)
      enddo
!
! close netcdf file
      status=nf90_close(file_id)
      call Handle_Err(subname,4,status)
!
      end subroutine
!
!===================================================
      subroutine read_n80_land_mask(filename,dim1,nland,vector)
!===================================================
! reads a 2-D map from a closed netcdf file
! assumes netcdf file is closed
! assumes no time dimension: only a single map for each variable
!
      use netcdf
      use typeSizes
!
      implicit none
!
! input
      Character*200 filename  ! netcdf file name
      integer dim1   ! first dimension of variable
      integer recnum ! time record number of variable
!
! input/output
      real vector(dim1,3)  ! vector of lat/lon values read from netcdf file
!
! internal variables
      integer, i, j, k, l, m, n ! indeces
      Character*20 subname ! subroutine name for error handling
      integer file_id      ! netcdf file id number
      integer varid        ! variable id number
      integer dimid        ! variable id number
      integer status       ! successful execution status number
      real, allocatable :: latvec(:)  ! vector of land points
      real, allocatable :: lonvec(:)  ! vector of land points
      real, allocatable :: maskvec(:)  ! vector of land points
      integer nland
!
! set subroutine name
      subname='read_n80_land_mask'
!
! open netcdf file and get file id number
      status=nf90_open(trim(filename),0,file_id)
      call Handle_Err(subname,1,status)
!
! dimension id number
      status=nf90_inq_dimid(file_id,'ngpts',dimid)
      call Handle_Err(subname,2,status)
!
! dimension lenth
      status=nf90_inquire_dimension(file_id,dimid, len=nland)
      call Handle_Err(subname,3,status)
      allocate(latvec(nland))
      allocate(lonvec(nland))
      allocate(maskvec(nland))
!
! get latitude id number
      status=nf90_inq_varid(file_id,'LAT',varid)
      call Handle_Err(subname,4,status)
!
! get latitudes
      status=nf90_get_var(file_id,varid,latvec)
      call Handle_Err(subname,5,status)
!
! get longitude id number
      status=nf90_inq_varid(file_id,'LON',varid)
      call Handle_Err(subname,6,status)
!
! get longitudes
      status=nf90_get_var(file_id,varid,lonvec)
      call Handle_Err(subname,7,status)
!
! get land mask id number
      status=nf90_inq_varid(file_id,'LSM',varid)
      call Handle_Err(subname,8,status)
!
! get land mask
      status=nf90_get_var(file_id,varid,maskvec)
      call Handle_Err(subname,9,status)
!
! transfer to vector
      do i=1,nland
        vector(i,1)=latvec(i)
        vector(i,2)=lonvec(i)
        vector(i,3)=maskvec(i)
      enddo
!
! close netcdf file
      status=nf90_close(file_id)
      call Handle_Err(subname,4,status)
!
      end subroutine
!
!===================================================
      subroutine read_vecmap_multi(filename,varname,dim1,dim2,dim3,outmap)
!===================================================
! reads a 1-D vectors of land points and transfers them to a 2-D map
! assumes netcdf file is closed
! assumes a time dimension for each variable
!
      use netcdf
      use typeSizes
!
      implicit none
!
! input
      Character*200 filename  ! netcdf file name
      Character*20 varname    ! variable name number for netcdf file type
      integer dim1   ! first dimension of output map (lon)
      integer dim2   ! second dimension of output map (lat)
      integer dim3   ! third dimension of output map (time)
!
! output
      real outmap(dim1,dim2)  ! 2-d map of values read from netcdf file
!
! internal variables
      integer i,j,k,l,m,n  ! generic indeces
      integer start(3)     ! starting index location to read
      Character*20 subname ! subroutine name for error handling
      integer file_id      ! netcdf file id number
      integer varid        ! variable id number
      integer dimid        ! dimension id id number
      integer nland        ! number land points
      integer status       ! successful execution status number
      real, allocatable :: landvec(:)  ! vector of land points
      integer, allocatable :: latindx(:)  ! latitude index locations
      integer, allocatable :: lonindx(:)  ! longitude index locations
!
! set subroutine name
      subname='read_vecmap_multi'
!
! open netcdf file and get file id number
      status=nf90_open(trim(filename),0,file_id)
      call Handle_Err(subname,1,status)
!
! landpoint dimension id number
      status=nf90_inq_dimid(file_id,'subcount',dimid)
      call Handle_Err(subname,2,status)
!
! get dimension
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
! get vector of land points
      start(1)=1
      start(2)=dim3
      start(3)=1
      status=nf90_get_var(file_id,varid,landvec, start=start)
      call Handle_Err(subname,5,status)
!
! get lat index id number
      status=nf90_inq_varid(file_id,'latindex',varid)
      call Handle_Err(subname,6,status)
!
! get vector of lat indeces
      status=nf90_get_var(file_id,varid,latindx)
      call Handle_Err(subname,7,status)
!
! get lon index id number
      status=nf90_inq_varid(file_id,'lonindex',varid)
      call Handle_Err(subname,8,status)
!
! get vector of lat indeces
      status=nf90_get_var(file_id,varid,lonindx)
      call Handle_Err(subname,9,status)
!
! close netcdf file
      status=nf90_close(file_id)
      call Handle_Err(subname,10,status)
!
! map vectors onto map
      do i=1,nland
        outmap(lonindx(i),latindx(i))=landvec(i)
      enddo
!
      end subroutine
!
!===================================================
      subroutine read_restart_2d(filename,varname,dim1,dim2,outmap)
!===================================================
! reads a 1-D vector of land points and transfers them to a 2-D map
! assumes netcdf file is closed
! assumes no time dimension: single map for each variable
!
      use netcdf
      use typeSizes
!
      implicit none
!
! input
      Character*200 filename  ! netcdf file name
      Character*20 varname    ! variable name number for netcdf file type
      integer dim1   ! first dimension of output map
      integer dim2   ! second dimension of output map
!
! output
      real outmap(dim1,dim2)  ! 2-d map of values read from netcdf file
!
! internal variables
      integer i,j,k,l,m,n  ! generic indeces
      Character*20 subname ! subroutine name for error handling
      integer file_id      ! netcdf file id number
      integer varid        ! variable id number
      integer ndims        ! number of dimensions
      integer dimid        ! dimension ID
      integer nsib         ! total number of possible land points
      integer subcount     ! total number land points
      integer status       ! successful execution status number
      real, allocatable :: landvec(:)  ! vector of land points
      integer, allocatable :: latindx(:)  ! latitude index locations
      integer, allocatable :: lonindx(:)  ! longitude index locations
      integer, allocatable :: subset(:)  ! sib vector index locations
!
! set subroutine name
      subname='read_restart_2d'
!
! open netcdf file and get file id number
      status=nf90_open(trim(filename),0,file_id)
      call Handle_Err(subname,1,status)
!
! subcount dimension 
      status=nf90_inq_dimid(file_id,'subcount',dimid)
      call Handle_Err(subname,2,status)
      status=nf90_inquire_dimension(file_id,dimid, len=subcount)
      call Handle_Err(subname,3,status)
!
! nsib dimension 
      status=nf90_inq_dimid(file_id,'nsib',dimid)
      call Handle_Err(subname,2,status)
      status=nf90_inquire_dimension(file_id,dimid, len=nsib)
      call Handle_Err(subname,3,status)
!
! allocate vectors
      allocate(landvec(nsib))
      allocate(latindx(subcount))
      allocate(lonindx(subcount))
      allocate(subset(subcount))
!
! get variable
      status=nf90_inq_varid(file_id,trim(varname),varid)
      call Handle_Err(subname,4,status)
      status=nf90_get_var(file_id,varid,landvec)
      call Handle_Err(subname,5,status)
!
! get lat indeces
      status=nf90_inq_varid(file_id,'latindex',varid)
      call Handle_Err(subname,6,status)
      status=nf90_get_var(file_id,varid,latindx)
      call Handle_Err(subname,7,status)
!
! get lon indeces
      status=nf90_inq_varid(file_id,'lonindex',varid)
      call Handle_Err(subname,8,status)
      status=nf90_get_var(file_id,varid,lonindx)
      call Handle_Err(subname,9,status)
!
! get subset indeces
      status=nf90_inq_varid(file_id,'subset',varid)
      call Handle_Err(subname,8,status)
      status=nf90_get_var(file_id,varid,subset)
      call Handle_Err(subname,9,status)
!
! close netcdf file
      status=nf90_close(file_id)
      call Handle_Err(subname,10,status)
!
! map vectors onto map
      do i=1,subcount
        outmap(lonindx(i),latindx(i))=landvec(subset(i))
      enddo
!
      end subroutine
!
!===================================================
      subroutine read_restart_3d(filename,varname,dim1,dim2,nlayer,layernum,outmap)
!===================================================
! reads a 1-D vector of land points and transfers them to a 2-D map
! assumes netcdf file is closed
!
      use netcdf
      use typeSizes
!
      implicit none
!
! input
      Character*200 filename  ! netcdf file name
      Character*20 varname    ! variable name number for netcdf file type
      integer dim1     ! first dimension of output map
      integer dim2     ! second dimension of output map
      integer nlayer   ! number of layers in output map
      integer layernum ! layer of output map
!
! output
      real outmap(dim1,dim2)  ! 2-d map of values read from netcdf file
!
! internal variables
      integer i,j,k,l,m,n  ! generic indeces
      Character*20 subname ! subroutine name for error handling
      integer file_id      ! netcdf file id number
      integer varid        ! variable id number
      integer ndims        ! number of dimensions
      integer dimid        ! dimension ID
      integer nsib         ! total number of possible land points
      integer subcount     ! total number land points
      integer npool       ! total number layers
      integer status       ! successful execution status number
      integer, allocatable :: latindx(:)  ! latitude index locations
      integer, allocatable :: lonindx(:)  ! longitude index locations
      integer, allocatable :: subset(:)   ! sib vector index locations
      real, allocatable :: landvec(:,:)   ! 3-d map of values read from netcdf file
!
! set subroutine name
      subname='read_restart_3d'
!
! open netcdf file and get file id number
      status=nf90_open(trim(filename),0,file_id)
      call Handle_Err(subname,1,status)
!
! subcount dimension 
      status=nf90_inq_dimid(file_id,'subcount',dimid)
      call Handle_Err(subname,2,status)
      status=nf90_inquire_dimension(file_id,dimid, len=subcount)
      call Handle_Err(subname,3,status)
!
! nsib dimension 
      status=nf90_inq_dimid(file_id,'nsib',dimid)
      call Handle_Err(subname,2,status)
      status=nf90_inquire_dimension(file_id,dimid, len=nsib)
      call Handle_Err(subname,3,status)
!
! allocate vectors
      allocate(landvec(nsib,nlayer))
      allocate(latindx(subcount))
      allocate(lonindx(subcount))
      allocate(subset(subcount))
!
! get variable
      status=nf90_inq_varid(file_id,trim(varname),varid)
      call Handle_Err(subname,4,status)
      status=nf90_get_var(file_id,varid,landvec)
      call Handle_Err(subname,5,status)
!
! get lat indeces
      status=nf90_inq_varid(file_id,'latindex',varid)
      call Handle_Err(subname,6,status)
      status=nf90_get_var(file_id,varid,latindx)
      call Handle_Err(subname,7,status)
!
! get lon indeces
      status=nf90_inq_varid(file_id,'lonindex',varid)
      call Handle_Err(subname,8,status)
      status=nf90_get_var(file_id,varid,lonindx)
      call Handle_Err(subname,9,status)
!
! get subset indeces
      status=nf90_inq_varid(file_id,'subset',varid)
      call Handle_Err(subname,8,status)
      status=nf90_get_var(file_id,varid,subset)
      call Handle_Err(subname,9,status)
!
! close netcdf file
      status=nf90_close(file_id)
      call Handle_Err(subname,10,status)
!
! map vectors onto map
      do i=1,subcount
        outmap(lonindx(i),latindx(i))=landvec(subset(i),layernum)
      enddo
!
      end subroutine
!
!===================================================
      subroutine read_vecmap_single(filename,varname,dim1,dim2,outmap)
!===================================================
! reads a 1-D vector of land points and transfers them to a 2-D map
! assumes netcdf file is closed
! assumes no time dimension: single map for each variable
!
      use netcdf
      use typeSizes
!
      implicit none
!
! input
      Character*200 filename  ! netcdf file name
      Character*20 varname    ! variable name number for netcdf file type
      integer dim1   ! first dimension of output map (lon)
      integer dim2   ! second dimension of output map (lat)
!
! output
      real outmap(dim1,dim2)  ! 2-d map of values read from netcdf file
!
! internal variables
      integer i,j,k,l,m,n  ! generic indeces
      Character*20 subname ! subroutine name for error handling
      integer file_id      ! netcdf file id number
      integer varid        ! variable id number
      integer dimid        ! dimension id id number
      integer nland        ! number land points
      integer status       ! successful execution status number
      real, allocatable :: landvec(:)  ! vector of land points
      integer, allocatable :: latindx(:)  ! latitude index locations
      integer, allocatable :: lonindx(:)  ! longitude index locations
!
! set subroutine name
      subname='read_vecmap_single'
!
! open netcdf file and get file id number
      status=nf90_open(trim(filename),0,file_id)
      call Handle_Err(subname,1,status)
!
! landpoint dimension id number
!      status=nf90_inq_dimid(file_id,'landpoints',dimid)
!      status=nf90_inq_dimid(file_id,'subcount',dimid)
      status=nf90_inq_dimid(file_id,'nsib',dimid)
      call Handle_Err(subname,2,status)
!
! get dimension
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
! get vector of land points
      status=nf90_get_var(file_id,varid,landvec)
      call Handle_Err(subname,5,status)
!
! get lat index id number
      status=nf90_inq_varid(file_id,'latindex',varid)
      call Handle_Err(subname,6,status)
!
! get vector of lat indeces
      status=nf90_get_var(file_id,varid,latindx)
      call Handle_Err(subname,7,status)
!
! get lon index id number
      status=nf90_inq_varid(file_id,'lonindex',varid)
      call Handle_Err(subname,8,status)
!
! get vector of lat indeces
      status=nf90_get_var(file_id,varid,lonindx)
      call Handle_Err(subname,9,status)
!
! close netcdf file
      status=nf90_close(file_id)
      call Handle_Err(subname,10,status)
!
! map vectors onto map
      do i=1,nland
        outmap(lonindx(i),latindx(i))=landvec(i)
      enddo
!
      end subroutine
!
!===================================================
      subroutine read_ndvivec(filename,varname,dim1,dim2,recnum,outmap)
!===================================================
! reads a 1-D vector of land points and transfers them to a 2-D map
! assumes netcdf file is closed
! assumes unlimited time dimension: multiple maps for each variable
!
      use netcdf
      use typeSizes
!
      implicit none
!
! input
      Character*200 filename  ! netcdf file name
      Character*20 varname    ! variable name number for netcdf file type
      integer dim1   ! first dimension of variable
      integer dim2   ! second dimension of variable
      integer recnum ! time record number of variable
!
! output
      real outmap(dim1,dim2)  ! 2-d map of values read from netcdf file
!
! internal variables
      integer i,j,k,l,m,n  ! generic indeces
      Character*20 subname ! subroutine name for error handling
      integer file_id      ! netcdf file id number
      integer varid        ! variable id number
      integer dimid        ! dimension id id number
      integer nland        ! number land points
      integer status       ! successful execution status number
      integer start(2)     ! starting index location to read
      real, allocatable :: landvec(:,:)  ! vector of land points
      integer, allocatable :: latindx(:)  ! latitude index locations
      integer, allocatable :: lonindx(:)  ! longitude index locations
!
! set subroutine name
      subname='read_ndvivec'
!
! open netcdf file and get file id number
      status=nf90_open(trim(filename),0,file_id)
      call Handle_Err(subname,1,status)
!
! landpoint dimension id number
      status=nf90_inq_dimid(file_id,'nsib',dimid)
      call Handle_Err(subname,2,status)
!
! get dimension
      status=nf90_inquire_dimension(file_id,dimid, len=nland)
      call Handle_Err(subname,3,status)
!
! allocate land vectors
      allocate(landvec(12,nland))
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
      status=nf90_get_var(file_id,varid,landvec)
      call Handle_Err(subname,5,status)
!
! get lat index id number
      status=nf90_inq_varid(file_id,'latindex',varid)
      call Handle_Err(subname,6,status)
!
! get vector of lat indeces
      status=nf90_get_var(file_id,varid,latindx)
      call Handle_Err(subname,7,status)
!
! get lon index id number
      status=nf90_inq_varid(file_id,'lonindex',varid)
      call Handle_Err(subname,8,status)
!
! get vector of lat indeces
      status=nf90_get_var(file_id,varid,lonindx)
      call Handle_Err(subname,9,status)
!
! close netcdf file
      status=nf90_close(file_id)
      call Handle_Err(subname,10,status)
!
! map vectors onto map
      do i=1,nland
        outmap(lonindx(i),latindx(i))=landvec(recnum,i)
      enddo
!
      end subroutine
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
      Character*200 filename ! netcdf file name
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
      subroutine read_dim(filename,dim_name,dim_len)
!===================================================
! gets time dimension from a closed netcdf file
! assumes netcdf file is closed
! assumes unlimited time dimension: multiple values for each variable
!
      use netcdf
      use typeSizes
!
      implicit none
!
! input
      Character*200 filename  ! netcdf file name
!
! internal variables
      Character*20 subname ! subroutine name for error handling
      integer file_id      ! netcdf file id number
      integer status       ! successful execution status number
      integer dimid
      integer dim_len
      Character*20 dim_name ! subroutine name for error handling
!
! set subroutine name
      subname='read_dim'
!
! open netcdf file and get file id number
      status=nf90_open(trim(filename),0,file_id)
      call Handle_Err(subname,1,status)
!
! dimension id number
      status=nf90_inq_dimid(file_id,trim(dim_name),dimid)
      call Handle_Err(subname,2,status)
!
! get dimension
      status=nf90_inquire_dimension(file_id,dimid, len=dim_len)
      call Handle_Err(subname,3,status)
!
! close netcdf file
      status=nf90_close(file_id)
      call Handle_Err(subname,4,status)!
!
      end subroutine
!
!===================================================
      subroutine read_time_dim(filename,time_dim)
!===================================================
! gets time dimension from a closed netcdf file
! assumes netcdf file is closed
! assumes unlimited time dimension: multiple values for each variable
!
      use netcdf
      use typeSizes
!
      implicit none
!
! input
      Character*200 filename  ! netcdf file name
!
! internal variables
      Character*20 subname ! subroutine name for error handling
      integer file_id      ! netcdf file id number
      integer status       ! successful execution status number
      integer dimid, time_dim
      Character*20 name ! subroutine name for error handling
!
! set subroutine name
      subname='read_time_dim'
!
! open netcdf file and get file id number
      status=nf90_open(trim(filename),0,file_id)
      call Handle_Err(subname,1,status)
!
! dimension id number
      status=nf90_inq_dimid(file_id,'time',dimid)
      call Handle_Err(subname,2,status)
!
! get dimension
      status=nf90_inquire_dimension(file_id,dimid, len=time_dim)
      call Handle_Err(subname,3,status)
!
! close netcdf file
      status=nf90_close(file_id)
      call Handle_Err(subname,4,status)
!
      end subroutine
!===================================================
      subroutine read_time(filename,varname,dim1,array)
!===================================================
! reads a 1-D array from a closed netcdf file
! assumes netcdf file is closed
! assumes unlimited time dimension: multiple values for each variable
!
      use netcdf
      use typeSizes
!
      implicit none
!
! input
      Character*200 filename  ! netcdf file name
      Character*20 varname    ! variable name number for netcdf file type
      integer dim1   ! first dimension of variable
      integer dim2 ! time record number of variable
!
! output
      real array(dim1)  ! 1-d array of values read from netcdf file
!
! internal variables
      Character*20 subname ! subroutine name for error handling
      integer file_id      ! netcdf file id number
      integer varid        ! variable id number
      integer status       ! successful execution status number
      integer start(2)     ! starting index location to read
!
! set subroutine name
      subname='read_time'
!
! open netcdf file and get file id number
      status=nf90_open(trim(filename),0,file_id)
      call Handle_Err(subname,1,status)
!
! get variable id number
      status=nf90_inq_varid(file_id,trim(varname),varid)
      call Handle_Err(subname,2,status)
!
! get array
      status=nf90_get_var(file_id,varid,array)
      call Handle_Err(subname,3,status)
!
! close netcdf file
      status=nf90_close(file_id)
      call Handle_Err(subname,4,status)
!
      end subroutine
!
!
!===================================================
      subroutine read_line_c(filename,varname,dim1,dim2,array)
!===================================================
! reads a 1-D array from a closed netcdf file
! assumes netcdf file is closed
! assumes unlimited time dimension: multiple values for each variable
!
      use netcdf
      use typeSizes
!
      implicit none
!
! input
      Character*200 filename  ! netcdf file name
      Character*20 varname    ! variable name number for netcdf file type
      integer dim1   ! first dimension of variable
      integer dim2 ! time record number of variable
!
! output
      real array(dim1,dim2)  ! 2-d array of values read from netcdf file
!
! internal variables
      Character*20 subname ! subroutine name for error handling
      integer file_id      ! netcdf file id number
      integer varid        ! variable id number
      integer status       ! successful execution status number
      integer start(2)     ! starting index location to read
!
! set subroutine name
      subname='read_line_c'
!
! open netcdf file and get file id number
      status=nf90_open(trim(filename),0,file_id)
      call Handle_Err(subname,1,status)
!
! get variable id number
      status=nf90_inq_varid(file_id,trim(varname),varid)
      call Handle_Err(subname,2,status)
!
! set read starting point (recnum is assumed to be time record)
      start(1)=1      ! dim1 starting point
      start(2)=1      ! dim2 starting point
!
! get array
      status=nf90_get_var(file_id,varid,array)
      call Handle_Err(subname,3,status)
!
! close netcdf file
      status=nf90_close(file_id)
      call Handle_Err(subname,4,status)
!
      end subroutine
!
!===================================================
      subroutine close_netcdf(file_id)
!===================================================
! closes a netcdf file
! assumes netcdf file is already open
!
      use netcdf
      use typeSizes
!
      implicit none
!
! input
      integer file_id ! netcdf file id number
!
! internal variables
      Character*20 subname ! subroutine name for error handling
      integer status       ! successful execution status number
!
! set subroutine name
      subname='close_netcdf'
!
! close netcdf file
      status=nf90_close(file_id)
      call Handle_Err(subname,1,status)
!
      end subroutine
!
!===================================================
      subroutine open_netcdf(filename,varname,file_id,varid)
!===================================================
! opens a netcdf file and gets a file and variable number
! assumes netcdf file is not already open
!
      use netcdf
      use typeSizes
!
      implicit none
!
! input
      Character*200 filename  ! netcdf file name
      Character*20 varname    ! variable name number for netcdf file type
      Character*20 subname    ! subroutine name for error handling
!
! output
      integer file_id ! netcdf file id number
      integer varid   ! variable id number
!
! internal variables
      integer status  ! successful execution status number
!
! set subroutine name
      subname='open_netcdf'
!
! open netcdf file and get file id number
      status=nf90_open(trim(filename),ior(nf90_write,nf90_share),file_id)
      call Handle_Err(subname,1,status)
!
! get variable id number
      status=nf90_inq_varid(file_id,trim(varname),varid)
      call Handle_Err(subname,2,status)
!
      end subroutine
!
!===================================================
      subroutine read_netcdf_o(file_id,varid,dim1,dim2,recnum,map)
!===================================================
! reads a 2-D map from an open netcdf file
! assumes netcdf file is already open (faster when reading multiple maps)
! allows read/write/sharing privilages
! assumes unlimited time dimension
!
      use netcdf
      use typeSizes
!
      implicit none
!
! input
      integer file_id ! netcdf file id number
      integer varid   ! variable id number
      integer dim1    ! first dimension of variable
      integer dim2    ! second dimension of variable
      integer recnum  ! time record number of variable
!
! output
      real map(dim1,dim2) ! 2-d map of values read from netcdf file
!
! internal variables
      Character*20 subname ! subroutine name for error handling
      integer status       ! successful execution status number
      integer start(3)     ! starting index location to read
!
! set subroutine name
      subname='read_netcdf_o'
!
! set read starting point (recnum is assumed to be time record)
      start(1)=1      ! dim1 starting point
      start(2)=1      ! dim2 starting point
      start(3)=recnum ! time record starting point
!
! get map
      status=nf90_get_var(file_id,varid,map,start=start)
      call Handle_Err(subname,1,status)
!
      end subroutine
!
!===================================================
      subroutine read_netcdf_c(filename,varname,dim1,dim2,recnum,map)
!===================================================
! reads a 2-D map from a closed netcdf file
! assumes netcdf file is closed
! assumes unlimited time dimension: multiple maps for each variable
!
      use netcdf
      use typeSizes
!
      implicit none
!
! input
      Character*200 filename  ! netcdf file name
      Character*20 varname    ! variable name number for netcdf file type
      integer dim1   ! first dimension of variable
      integer dim2   ! second dimension of variable
      integer recnum ! time record number of variable
!
! output
      real map(dim1,dim2)  ! 2-d map of values read from netcdf file
!
! internal variables
      Character*20 subname ! subroutine name for error handling
      integer file_id      ! netcdf file id number
      integer varid        ! variable id number
      integer status       ! successful execution status number
      integer start(3)     ! starting index location to read
!
! set subroutine name
      subname='read_netcdf_c'
!
! open netcdf file and get file id number
!print*, trim(filename)
      status=nf90_open(trim(filename),0,file_id)
      call Handle_Err(subname,1,status)
!
! get variable id number
      status=nf90_inq_varid(file_id,trim(varname),varid)
      call Handle_Err(subname,2,status)
!
! set read starting point (recnum is assumed to be time record)
      start(1)=1      ! dim1 starting point
      start(2)=1      ! dim2 starting point
      start(3)=recnum ! time record starting point
!
! get map
      status=nf90_get_var(file_id,varid,map,start=start)
      call Handle_Err(subname,3,status)
!
! close netcdf file
      status=nf90_close(file_id)
      call Handle_Err(subname,4,status)
!
      end subroutine
!
!===================================================
      subroutine read_single_netcdf_c(filename,varname,dim1,dim2,map)
!===================================================
! reads a 2-D map from a closed netcdf file
! assumes netcdf file is closed
! assumes no time dimension: only a single map for each variable
!
      use netcdf
      use typeSizes
!
      implicit none
!
! input
      Character*200 filename  ! netcdf file name
      Character*20 varname    ! variable name number for netcdf file type
      integer dim1   ! first dimension of variable
      integer dim2   ! second dimension of variable
      integer recnum ! time record number of variable
      integer i,j
!
! output
      real map(dim1,dim2)  ! 2-d map of values read from netcdf file
      real value
!
! internal variables
      Character*20 subname ! subroutine name for error handling
      integer file_id      ! netcdf file id number
      integer varid        ! variable id number
      integer status       ! successful execution status number
!
! set subroutine name
      subname='read_single_netcdf_c'
!
! open netcdf file and get file id number
! print*, trim(filename)
      status=nf90_open(trim(filename),0,file_id)
      call Handle_Err(subname,1,status)
!
! get variable id number
      status=nf90_inq_varid(file_id,trim(varname),varid)
      call Handle_Err(subname,2,status)
!
! get map
      status=nf90_get_var(file_id,varid,map)
      call Handle_Err(subname,3,status)
!
! close netcdf file
      status=nf90_close(file_id)
      call Handle_Err(subname,4,status)
!
      end subroutine
!
!===================================================
      subroutine write_netcdf_o(file_id,varid,dim1,dim2,recnum,map)
!===================================================
! writes a 2-D map from an open netcdf file
! assumes netcdf file is already open (faster when writing multiple maps)
! assumes unlimited time dimension
!
      use netcdf
      use typeSizes
!
      implicit none
!
! input
      integer file_id ! netcdf file id number
      integer varid   ! variable id number
      integer dim1    ! first dimension of variable
      integer dim2    ! second dimension of variable
      integer recnum  ! time record number of variable
!
! output
      real map(dim1,dim2) ! 2-d map of values read from netcdf file
!
! internal variables
      Character*20 subname ! subroutine name for error handling
      integer status       ! successful execution status number
      integer start(3)     ! starting index location to read
      integer count(3)     ! length of record to write
!
! set subroutine name
      subname='write_netcdf_o'
!
! set read starting point (recnum is assumed to be time record)
      start(1)=1      ! dim1 starting point
      start(2)=1      ! dim2 starting point
      start(3)=recnum ! time record starting point
!
! set length of record
      count(1)=dim1     ! dim1 length
      count(2)=dim2    ! dim2 length
      count(3)=1 ! time record length
!
! write map
      status=nf90_put_var(file_id,varid,map,start=start,count=count)
      call Handle_Err(subname,1,status)
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
