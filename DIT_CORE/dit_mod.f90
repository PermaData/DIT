!
!===================================================
      module dit_variables
!===================================================
! defines variables common to all routines in the
! Data Integration Tool (dit) program
!
! Modifications
!  Kevin Schaefer created module (12/24/14)
!  Kevin Schaefer added in/out dimension variable tree (1/11/15)
!---------------------------------------------------
!
      implicit none
!
! filenames
      Character*200 filename ! generic file name
!
! data variables
      real, allocatable :: data_in(:,:)           ! input data
      real, allocatable :: data_out(:,:)          ! output data
      Character*200, allocatable :: char_in(:,:)  ! input character data
      Character*200, allocatable :: char_out(:,:) ! output character data
      Character*200, allocatable :: head_in(:,:)  ! header in
      Character*200, allocatable :: head_out(:,:) ! header out
      Character*200, allocatable :: head_tmp(:)   ! temp header
      Character*200, allocatable :: head1_tmp(:)  ! temp header
      Character*200, allocatable :: head2_tmp(:)  ! temp header
      Character*200, allocatable :: fmt_tmp(:)    ! temporary write format for arrays
      Character*200, allocatable :: typ_tmp(:)    ! temporary variable type for arrays
      integer, allocatable :: indx_map(:,:)       ! var index mapping between input and output data
      real miss_val_real         ! standard missing value
      Character*20 miss_val_char ! standard missing value
!
! data dimension variables
      type dimension
        integer n_var    ! number of variables (number columns)
        integer n_rec    ! number of data records (number rows)
        integer n_hed    ! number of header records (number rows in header)
        integer strt_rec ! record start index
        integer stop_rec ! record end index
      end type dimension
      type(dimension) :: in  ! dimensions input data
      type(dimension) :: out ! dimensions output data
      type(dimension) :: tmp ! dimensions temporary data
      integer x_dim ! x dimension
      integer y_dim ! y dimension
!
! temporary variables
      real, allocatable :: temp1_d1(:)         ! temporary 1D variable #1
      real, allocatable :: temp2_d1(:)         ! temporary 1D variable #2
      real, allocatable :: temp3_d1(:)         ! temporary 1D variable #3
      real, allocatable :: temp1_d2(:,:)       ! temporary 2D variable #1
      real, allocatable :: temp2_d2(:,:)       ! temporary 2D variable #2
      real, allocatable :: temp3_d2(:,:)       ! temporary 2D variable #3
      real, allocatable :: temp1_d3(:,:,:)     ! temporary 3D variable #1
      real, allocatable :: temp2_d3(:,:,:)     ! temporary 3D variable #2
      real, allocatable :: temp3_d3(:,:,:)     ! temporary 3D variable #3
      integer, allocatable :: temp_int1(:)     ! temporary 1D integer variable
      integer, allocatable :: temp_int2(:,:)   ! temporary 2D integer variable
      integer, allocatable :: temp_int3(:,:,:) ! temporary 3D integer variable
      Character*50, allocatable :: temp1_char1(:)     ! temporary 1D character variable
      Character*200, allocatable :: temp2_char1(:)     ! temporary 1D character variable
      Character*200, allocatable :: temp3_char1(:)     ! temporary 1D character variable
      Character*200, allocatable :: temp1_char2(:,:)   ! temporary 2D character variable
      Character*200, allocatable :: temp2_char2(:,:)   ! temporary 2D character variable
      Character*200, allocatable :: temp3_char2(:,:)   ! temporary 2D character variable
      Character*200, allocatable :: temp_char3(:,:,:)  ! temporary 3D character variable
!
! Time variables
      integer day_per_mon(12)      ! (day) days per month
      integer day_per_mon_leap(12) ! (day) days per month for leap year
      integer doy1_mon(12)         ! (day) day of year (DOY) for first on month
      integer doy1_mon_leap(12)    ! (day) day of year (DOY) for first on month for leap year
      real mid_mon_doy(12)         ! (day) mid month day of year real version
      real mid_mon_doy_leap(12)    ! (day) mid month day of year real version for leap year
      character*20 mid_month(12)   ! (dd hh:mm) mid month day of month character version
      real day_per_yr              ! (day) number of days per year
      real day_per_yr_leap         ! (day) number of days per year for leap year
!
! Misc character variables
      character*1 qd   ! double quote character string
      character*1 qs   ! single quote character string
!
! generic index variables that do not change
      integer i_pat_out    ! path index for output directory
      integer i_pat_tmp    ! path index for temporary working data directory
      integer i_pat_python ! path index python script library
!
! count variables
      integer n_path  ! number of input/output paths
      integer n_file  ! number of input data files
      integer n_man   ! number of data manipulations
      integer n_var   ! number of variables defined in varmap file
      integer n_map   ! number of variables mapped from input to output data array
!
! file shredding variables to separate into multiple output files
      integer indx_id    ! index of variable used to map to column (usually depth)
      integer indx_x     ! index of x/column variable
      integer indx_y     ! index of y/row variable
      integer indx_z     ! z variable
      integer max_xvar   ! max number of x/column variables
      Character*250 id   ! text string site ID
!
! generic specifications variable tree
      type manipulation
        integer num         ! number
        logical doit        ! perform the operation
        logical saveit      ! save to file
        character*20 map    ! type of mapping
        character*20 typ    ! variable type
        character*20 cat    ! variable category
        logical flg1        ! logical flag 1
        logical flg2        ! logical flag 2
        logical flg3        ! logical flag 3
        logical flg4        ! logical flag 4
        real val1           ! 1st value
        real val2           ! 2nd value
        real val3           ! 3rd value
        real val4           ! 4th value
        integer ind1        ! index value 1
        integer ind2        ! index value 2
        integer ind3        ! index value 3
        integer ind4        ! index value 4
        integer ind5        ! index value 4
        integer ind6        ! index value 4
        integer npath1      ! path number 1
        integer npath2      ! path number 2
        integer npath3      ! path number 3
        integer npath4      ! path number 4
        Character*200 path1 ! 1st path
        Character*200 path2 ! 2st path
        Character*200 path3 ! 3st path
        Character*200 path4 ! 4th path
        character*200 txt1  ! text string 1
        character*200 txt2  ! text string 2
        character*200 txt3  ! text string 3
        character*200 txt4  ! text string 4
        character*200 fmt1  ! format 1
        character*200 fmt2  ! format 2
        character*200 fmt3  ! format 3
        character*200 fmt4  ! format 4
        integer  dim1       ! dimension 1
        integer  dim2       ! dimension 2
        integer  dim3       ! dimension 3
        integer  dim4       ! dimension 4
      end type manipulation
      type(manipulation), allocatable :: man(:)     ! manipulation specifications
      type(manipulation), allocatable :: path(:)    ! i/o path names
      type(manipulation), allocatable :: file(:)    ! data file names
      type(manipulation), allocatable :: var(:)     ! variable specifications
      type(manipulation), allocatable :: var_in(:)  ! input array variable specifications
      type(manipulation), allocatable :: var_out(:) ! output array variable specifications
      type(manipulation), allocatable :: var_tmp(:) ! temporary array variable specifications
      type(manipulation), allocatable :: var_shd(:) ! shredded output array variable specifications
!
! grid variables
      type grid_variables
        character*20 name ! grid name
        character*20 type ! grid type
        double precision lonmin       ! minimum longitude
        double precision latmin       ! minimum latitude
        double precision Dlon         ! longitude increment
        double precision Dlat         ! latitude increment
        double precision lon_offset   ! offset to locate position in grid cell
        double precision lat_offset   ! offset to locate position in grid cell
        integer nlon      ! number of longitude points
        integer nlat      ! number of latitude points
      end type grid_variables
      type(grid_variables) grid_r   ! grid variables for reading
!
      end module dit_variables
!
