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
4. **Access to a Mac/Linux computer.  These OSs reliably run the scripts successfully, while there are some lingering bugs for Windows users.  If you are a lead forecaster with a Windows computer, coordinate with your support forecasters to run the scripts on a Mac/Linux machine.  There is at least one Mac/Linux user in every forecast group.**

- Google Drive with forecasting resources: https://drive.google.com/drive/u/0/folders/1DC6AGeQbo8y9StU1wO9NbwBCahSa66BF
- Google Drive link:  https://drive.google.com/drive/u/0/folders/14g2MU2wh6fWceYqPDgEeQqtZ734wW_zm
- Zoom Meeting: https://uwmadison.zoom.us/j/96904936558?pwd=SFh2aHFKR3FHcGVxaVVnbnFQYzZ3dz09

-------------------------------------------
# Steps for automatically downloading the figures

1. In your computer's terminal, enter into the "cpex_cv_night_shift" directory
2. Then, type **python ./run_forecast_scripts.py**, which will run all of the necessary steps/scripts automatically for you
    -   For manual download (which should be unnecessary), see "Steps for manually downloading the figures" section below

3. If the script runs successfully, proceed to "Steps for creating the Microsoft PowerPoint template" and other lead forecaster steps in the Forecaster Responsibilities Google Doc (see Google Drive link above).  
    -   If the script does not run successfully, proceed to the "Potential Script Errors" section.

-------------------------------------------
# Steps for creating the Microsoft PowerPoint template
Make sure you have successfully downloaded image/animation files and cropped them before starting this.

1. Copy the CPEX-CV_Forecast_2022-09-XX.pptx file and replace XX with the current date. Move this renamed file to the _./forecast_files/_ folder, and open the new file.

2. Manually insert the _./figs_final/_ figures into the PowerPoint. This might vary from machine to machine, or from one PowerPoint version to another. But in general, here's what you need to do **for each image in the template**:
- Right click on the image and select **Format Picture...**.  In the _Format Picture_ pop-up window, click on the paint can (_Fill & Line_), then click on the _Fill_ dropdown menu, then click _Insert..._  Navigate to the _./figs_final/_ directory and double click on the appropriate image.  Images will be labeled with a prefix that coincides with the slide that the image should be pasted on.
    - There will be no _Insert..._ option for the ECMWF/GFS animations from Tropical Tidbits.  You will just have to delete the animation that is in the template, then drag and drop in the appropriate animation from the _./figs_final/_ directory.

3. After manually inserting the figures into the PowerPoint, confirm that the dates in the figures match their appropriate forecast day (when included in the figure). For example, model images have a timestamp on the top right.

4. Once the figures are updated, update the header dates and forecaster names in the PowerPoint
- The dates in the footer of each slide are automatically updated to the current day, so you do not need to update these
- In slides 3-4, update each figure header’s times (the ones with “(XXZ)” in the title) to reflect the times of the "current" imagery
    - For the surface analysis plot on slide 3 and MIMIC TPW plot on slide 4, the times can be found in the _./figs_ folder on the _NHC_surface_analysis.png_ and _MIMIC-TPW_latest.png_ images, respectively.  The times for the satellite image can be found in the _./figs_final_ folder on the _04_Goes16_Meteosat11_IRC_ image in red text in the upper left part of the figure.  There are 2 separate times listed, which should be within around 30 minutes of each other.  Just take the average of these times and put that in the MIMIC TPW header.
    - The times for the other plots on slide 4 can be found on the imagery already in the PowerPoint

5. Right before the final summary slide, copy and paste in Roman’s satellite tracks slides for the current day, day 1, and day 2 (if they’re available)

6. After the last slide, go to https://drive.google.com/drive/folders/1InAiHzAHk1MRn-5Qev_-MXcIGpVYwLFZ and copy and paste in the previous day’s radiosonde soundings from the hotel.

7. Upload the PowerPoint presentation to the Google Drive (https://drive.google.com/drive/u/0/folders/14g2MU2wh6fWceYqPDgEeQqtZ734wW_zm) by the beginning of the forecast prep discussion time

8. Right before the briefing time, execute **python ./run_model_4panel.py** with the appropriate _precipitation_animation_ switches set in _./supplementary/switches_download_model_4panel.txt_ (based on mesoscale model availability; the mesoscale models should be finished running by ~6am).
    - To confirm UWIN-CM and UC-Davis models have run, go to https://orca.atmos.washington.edu/models_cpex_aw/models.php and click yesterday's date in the calendar, located in the upper right portion of the screen.  To confirm that U of Utah WRF model has run, go to https://home.chpc.utah.edu/~pu/cpexaw/ and select yesterday's 00Z time.  To confirm that the NCAR MPAS model has run, go to https://www2.mmm.ucar.edu/projects/real-time-forecasts/ and select yesterday's 12Z time.  Confirm that UWIN-CM, UC-Davis WRF, U of Utah WRF, and NCAR MPAS models run out to at least 23Z of the day 2 forecast date.  If not, see "Potential Script Errors" section before proceeding to Step 2.
    - While you're presenting the briefing, this script will run in the background and create the 4-panel animations that we have included in the briefing in the past.  **You do not need to discuss them during the briefing.**  However, after the briefing, put these 1- and 2-day 4-panel animations in the appropriate "skipped" convection slide in the PowerPoint and "unskip" the slide.  **You do not need to add text to these slides.**. During the flight planning, you can then pull up these animations for the flight planners, as they are very useful when making flight plans. 
    - If the script crashes for some reason (other than you forgot to change one of the _precipitation_animation_ switches in _./supplementary/switches_download_model_4panel.txt_), then don't worry about it.

9. Proceed to other lead forecaster steps in the Forecaster Responsibilities Google Doc (see Google Drive link above)

-------------------------------------------
# Potential Script Errors

1. If any of the models' runs are not completed yet, open _./supplementary/switches_download_main.txt_ and _./supplementary/switches_download_model_4panel.txt_ and change the model's associated switches to False. 
    - If both the UWIN-CM and U of Utah WRF models are not working, follow the steps above, and also delete the day 1/2 TPW/Rain joint animation slides from the PowerPoint presentation.

2. KeyError: '.......'
 - If you get a KeyError for an "if switches['......']:" line of code, then set the appropriate switch in _./supplementary/switches_download_main.txt_ to False.  If the KeyError is for the UWIN-CM, U of Utah WRF, UC-Davis WRF, or NCAR MPAS model, then refer to #1 in Potential Script Errors.

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
