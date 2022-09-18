# CPEX-CV_forecasting

Forecasting template and tools for creating daily weather forecasts for the CPEX-CV field experiment.

To run the scripts in this directory, you will need to following:

1. ImageMagick (for image processing).
2. Python v3.x (I use 3.7.4) with following modules:
    - bs4 (HTML parsing; if python yells at you about "Couldn't find a tree builder ", you may have to conda/pip install lxml)
    - datetime (dealing with dates)
    - numpy (number stuff)
    - PIL (Create gif files)
    - os (reading existing files)
    - subprocess (executing code outside python)
    - urllib (retrieving images)
    - time
3. Microsoft Powerpoint.
4. **Access to a Mac/Linux computer.  These OSs reliably run the scripts successfully, while there are some lingering bugs for Windows users.  If you are a lead forecaster with a Windows computer, coordinate with your support forecasters to run the scripts on a Mac/Linux machine.  There is at least one Mac/Linux user in every forecast team.**

- Google Drive with forecasting resources: https://drive.google.com/drive/u/0/folders/1DC6AGeQbo8y9StU1wO9NbwBCahSa66BF
- Google Drive link:  https://drive.google.com/drive/u/0/folders/14g2MU2wh6fWceYqPDgEeQqtZ734wW_zm
- Zoom Meeting: https://uwmadison.zoom.us/j/96904936558?pwd=SFh2aHFKR3FHcGVxaVVnbnFQYzZ3dz09

-------------------------------------------
# Steps for automatically downloading the figures

1. Go to https://orca.atmos.washington.edu/models_cpex_aw/models.php and click yesterday's date in the calendar, located in the upper right portion of the screen.  Confirm that UWIN-CM, U of Utah WRF, and UC-Davis WRF models run out to at least 23Z of the day 2 forecast date.  If not, see "Potential Script Errors" section before proceeding to Step 2.
2. In your computer's terminal, enter into the "CPEX-CV_object_oriented" directory
3. Then, type **python ./run_forecast_scripts.py**, which will run all of the necessary steps/scripts automatically for you
    -   For manual download (which should be unnecessary), see "Steps for manually downloading the figures" section below

If the script runs successfully, you're done!  Proceed to "Steps for creating the Microsoft PowerPoint template" and other lead forecaster steps in the Forecaster Responsibilities Google Doc (see Google Drive link above).

If the script does not run successfully, proceed to the "Potential Script Errors" section.

-------------------------------------------
# Steps for creating the Microsoft PowerPoint template
Make sure you have successfully downloaded image/animation files and cropped them before starting this.

1. Copy the CPEX-CV_Forecast_2022-09-XX.pptx file and replace XX with the current date. Move this renamed file to the _./forecast_files/_ folder, and open the new file.

2. Manually insert the _./figs_final/_ figures into the PowerPoint. This might vary from machine to machine, or from one PowerPoint version to another. But in general, here's what you need to do **for each image in the template**:
- Right click on the image and select **Format Picture...**.  In the _Format Picture_ pop-up window, click on the paint can (_Fill & Line_), then click on the _Fill_ dropdown menu, then click _Insert..._  Navigate to the _./figs_final/_ directory and double click on the appropriate image.  Images will be labeled with a prefix that coincides with the slide that the image should be pasted on.

3. After manually inserting the figures into the PowerPoint, confirm that the dates in the figures match their appropriate forecast day (when included in the figure). For example, model images have a timestamp on the top right.

4. Once the figures are updated, update the header dates and forecaster names in the PowerPoint
- The dates in the footer of each slide are automatically updated to the current day, so you do not need to update these
- In slides 3-4, update each figure header’s times (the ones with “(XXZ)” in the title) to reflect the times of the "current" imagery
    - For the surface analysis plot on slide 3 and MIMIC TPW plot on slide 4, the times can be found in the _./figs_ folder on the _NHC_surface_analysis.png_ and _MIMIC-TPW_latest.png_ images, respectively.  The times for the satellite image can be found in the _./figs_final_ folder on the _04_Goes16_Meteosat11_IRC_ image in red text in the upper left part of the figure.  There are 2 separate times listed, which should be within around 30 minutes of each other.  Just take the average of these times and put that in the MIMIC TPW header.
    - The times for the other plots on slide 4 can be found on the imagery already in the PowerPoint

5. Right before the final summary slide, copy and paste in Roman’s satellite tracks slides for the current day, day 1, and day 2 (if they’re available)

6. After the last slide, go to https://drive.google.com/drive/folders/1InAiHzAHk1MRn-5Qev_-MXcIGpVYwLFZ and copy and paste in the previous day’s (and current day’s, if available) radiosonde soundings from the hotel

7. Upload the PowerPoint presentation to the Google Drive (https://drive.google.com/drive/u/0/folders/14g2MU2wh6fWceYqPDgEeQqtZ734wW_zm) by the beginning of the forecast prep discussion time

8. Proceed to other lead forecaster steps in the Forecaster Responsibilities Google Doc (see Google Drive link above)

-------------------------------------------
# Potential Script Errors

1. Per Step 1 in "Steps for automatically downloading the figures", if any of the 3 models' runs are not complete out to the day 2 forecast, open _./supplementary/switches_download.txt_ and change the model's associated switches to False.  Then, go into _./supplementary/crop_edit_daily_images.py_ and set the model's assigned "model_4panel_XX" variable equal a repeat of one of the other model's names (preferably MPAS, unless MPAS is the problem).
 - If the U of Utah WRF model is not finished updating on the UW website, it may be finished updating on its own website (https://home.chpc.utah.edu/~pu/cpexaw/).  If it's finished, then all you need to do is set _uutah_precipitation_animation = False_ and _UTAH_website = False_.  You don't need to edit anything in _./supplementary/crop_edit_daily_images.py_
    - If the U of Utah WRF 12Z model run isn't finished on either website, then open _./supplementary/download_daily_images_all.py_ and change ” utah_ini_time = ‘12’ ” to ” utah_ini_time = ‘00’ ”.  You should just have to comment and uncomment these lines, respectively.
    - If both the UWIN-CM and U of Utah WRF models are not working, follow the steps above, and also delete the day 1/2 TPW/Rain joint animation slides from the PowerPoint presentation.

2. KeyError: '.......'
 - If you get a KeyError for an "if switches['......']:" line of code, then set the appropriate switch in _./supplementary/switches_download.txt_ to False.  If the KeyError is for the UWIN-CM, U of Utah WRF, UC-Davis WRF, or NCAR MPAS model, then refer to #1 in Potential Script Errors.

3. If you encounter any other issues that you can't resolve, then message Shun-Nan and Ben together on Slack, and they will do their best to help you.  If they are not available, then you will need to figure out a solution.  That may be just using some of the forecast websites directly in your presentation, rather than having their imagery be in a PowerPoint.

-------------------------------------------
# Steps for manually downloading the figures

These should be run from the main directory.

1. Archiving previous day's images: (**python ./supplementary/archive_yesterdays_images.py**)

 - This will take all the images from _./figs_final/_ and move them into _./forecast_archive/_, labeled under yesterday's date.
 - It will then remove all the images from _./figs/_, _./figs_cropped/_, and _./figs_final/_

2. Download updated images for the forecast: **python ./supplementary/download_daily_images_master.py**

This will:
    - download images for the forecasting template.
    - reports on status of images (e.g. tells you if they are not available).
    - saves all the available images in the _./figs/_ directory.

3. Create basic animations: **python ./supplementary/create_animations.py**

This will:
    - extend the last frame of each future animations by 3 frames, so a looping animation will stay longer at the last frame.

4. Crop, process, and annotate downloaded images: **python ./supplementary/crop_edit_daily_images.py**

This reads in _switches_process.txt_ that was created in 2. It's automatic, so no need for any changes. It:
    - adds the locations of Sal wherever applicable.
    - crops images.
    - joins images together for animations.
    - creates final animations.
    - puts all intermediate imagery to _./figs_cropped/_.
    - puts all final imagery (for the .pptx template) to _./figs_final/_.
