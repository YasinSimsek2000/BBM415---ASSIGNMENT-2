    This code includes only one .py files:

- main.py

    main.py file includes some attributes:

- image_sources: it is a source list. The program reads all source images in "photo" folder and record into this array. 
- image_targets = it is a target list. The program reads all target images in "photo" folder and record into this array. 
- sources = it is a list of 3D array. The array form of all source images is recorded while the program is recording source images. 
- targets = it is a list of 3D array. The array form of all target images is recorded while the program is recording target images. 

    And also, main.py file includes some functions:

- get_mean: takes limit values and an array to calculate mean value in given limit. Returns an array of the mean values that includes
  the mean values of all panels. 

- get_std: takes limit values (for regions) and an array to calculate standard deviation value in given region. Returns an array of 
  the standard deviation values that includes the mean values of all panels. 

- get_ssd: takes two arrays and find the SSD between these arrays.

- color_transfer: takes an array as a source, all mean and standard deviation values of the source and the target, and the indexes of
  regions. By using given mean and standard deviation values and Reinhard formula, changes all pixel values with new in given index interval. 

- color_transfer_according_to_ssd: takes source and target images as arrays. It divides the images into four regions. It compares 
  all regions with each other to find the best solution and returns the indices of the best matched regions as an array of "limit".

    The first loop of program runs, and records all images data named "sourceX" and "targetX" within "photos" folder and its 3D array forms. 
The second loop calls the get_mean and the get_std functions that calculates mean and standard deviation values. These functions need limit 
values to calculate, because we need the values of a region instead of the value of all of panel in Part 2. At the end of the second loop, 
"color_transfer" function is called and the color transferring operation is applied to source image. 

    In the third loop, differently from the second loop, the "color_transfer_according_to_ssd" function is called to find the best regions that 
gives the smallest SSD. After that, the mean and the standard deviation values are calculated within found limits. The regions is determined and 
the color_transfer method is called. 