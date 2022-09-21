"""
Author: Ajda Savarin
Created: July 04th 2020
University of Washington
asavarin@uw.edu

Author: Shun-Nan Wu
Modified: July 01 2022
University of Oklahoma
swu@ou.edu

This program is used to retrieve images for the CPEX-AW and CPEX-CV field campaign forecasting template.

Required packages: os, subprocess, time.


NOTE: Read through the True/False switches at the top of the script to make sure the ones you want are selected.

Updates:
 - 2021-07-13: For satellite imagery, included Meteosat, GOES-16 cropped to St. Croix, and the Tropical Atlantic GOES-16. Also added the NHC tropical weather outlook figures for 2 and  5 days ahead. Included marked locations for both Sal Island and St Croix where applicable.
 - 2021-07-15: Trimmed the new CPEX-AW 2021 logo. Merged the Meteosat-11 and GOES-16 satellite imagery for a view of the Tropical Atlantic.
 - 2021-07-26: Added total AOT to files moved to ./figs_final/.
 - 2022-08-20: Changing the highlight point to Sal island
 - 2022-08-27: Adopt to all operating systems
 - 2022-09-12: Change to object oriented version
"""

import os
import subprocess
import time


model_4panel_ul = 'uwincm'
model_4panel_ur = 'uutah'
model_4panel_dl = 'ucdavis'
#model_4panel_dl = 'uutah'
model_4panel_dr = 'mpas'

clearDirectory = False # remove existing files
readSwitches = True
processImages = True
joinSlideAnimations = True
moveFinalImages = True

model_day1 = model_day2 = True

forecastDir = os.getcwd()
saveDir = os.path.join('.','figs')
cropDir = os.path.join('.','figs_cropped')
finDir  = os.path.join('.','figs_final')




nDup_frames = 3


def persistLastImage(fileDir, imageNameRoot, nDup=3):
  """
  persistLastImage(fileDir, imageNameRoot, nDup)

  Will copy the last image in the series nDup times, so it persists a bit longer in animation.

  Parameters:
  - fileDir: the directory where the files are saved
  - imageNameRoot: the complete root of the animation images (e.g. uwincm_anim_day1_)
  - nDup: number of times the last image is duplicated
  """

  fls = sorted([el for el in os.listdir(fileDir) if imageNameRoot in el])
  if len(fls) > 0:
    working = True
    frame_num = [int(el[-6:-4]) for el in fls]
    for fl in range(nDup):
      cmd = ['cp', os.path.join(fileDir,imageNameRoot+'{:02d}'.format(frame_num[-1])+fls[-1][-4:]), os.path.join(fileDir,imageNameRoot+'{:02d}'.format(frame_num[-1]+fl+1)+fls[-1][-4:]) ]
      os.system(' '.join(cmd))
  else:
    working = False

  return working


def createAnimation(fileDir, imageNameRoot, outName, delay=50, loop=0):
  """
  createAnimation(fileDir, imageNameRoot, delay=50, loop=0, outName)

  Will create a .gif animation of the provided images and save it.

  Parameters:
  - fileDir: the directory where the files are saved
  - imageNameRoot: the complete root of the animation images (e.g. uwincm_anim_day1_)
  - outName: the name of the output file (e.g. something.gif)
  - delay: delay in ms
  - loop: 0 means repeating
  """
  cmd = ['convert', '-delay', str(delay), os.path.join(fileDir,imageNameRoot+'*'), '-loop', str(loop), '+repage', os.path.join(fileDir,outName) ]
  os.system(' '.join(cmd))

  return


def animationSteps(fileDir, imageNameRoot, outName):
  """
  animationSteps(fileDir, imageNameRoot, outName)

  Sequentially calls persistLastImage, then createAnimation (if possible), to output an animation.

  Parameters:
  - fileDir: the directory where the files are saved
  - imageNameRoot: the complete root of the animation images (e.g. uwincm_anim_day1_)
  - outName: the name of the output file (e.g. something.gif)
  """

  dl = persistLastImage(fileDir, imageNameRoot)

  if dl:
    createAnimation(fileDir, imageNameRoot, outName)
  else:
    print('... ... Missing images - cannot create animation')

  return





if clearDirectory:
  print('Removing existing files.')
  existing_files = [el for el in sorted(os.listdir(cropDir)) if 'logo_cpexcv.png' not in el]
  for fl in existing_files:
    os.remove( os.path.join(cropDir,fl) )

  print('Copying over CPEX-CV logo.')
  fls = os.listdir(saveDir)
  cmd = ['cp', os.path.join(saveDir,'logo_cpexcv.png'), os.path.join(cropDir,'logo_cpexcv.png') ]
  os.system(' '.join(cmd))
  cmd = ['convert', os.path.join(cropDir,'logo_cpexcv.png'), '-trim',  '-border',  '0',  '+repage', os.path.join(cropDir,'logo_cpexcv.png')]
  os.system(' '.join(cmd))
  cmd = ['cp', os.path.join(cropDir,'logo_cpexcv.png'), os.path.join(finDir,'logo_cpexcv.png') ]
  os.system(' '.join(cmd))
  print('Removing existing files complete.')

  time.sleep(10)

print('Copying over CPEX-CV logo.')
fls = os.listdir(saveDir)
cmd = ['cp', os.path.join(saveDir,'logo_cpexcv.png'), os.path.join(cropDir,'logo_cpexcv.png') ]
os.system(' '.join(cmd))
cmd = ['convert', os.path.join(cropDir,'logo_cpexcv.png'), '-trim',  '-border',  '0',  '+repage', os.path.join(cropDir,'logo_cpexcv.png')]
os.system(' '.join(cmd))
cmd = ['cp', os.path.join(cropDir,'logo_cpexcv.png'), os.path.join(finDir,'logo_cpexcv.png') ]
os.system(' '.join(cmd))

print('')
print('')
print('')
print('')
print('')


if readSwitches:
  print("Reading True/False switches from switches_process.txt")
  fl = open( os.path.join(forecastDir,'supplementary','switches_process.txt'), 'r')
  data = fl.readlines()
  fl.close()
  data = [line.rstrip() for line in data]

  switches = {}
  for line in data:
    if len(line) > 0:
      switch_name, switch_setting = line.split(' = ')

      if switch_setting == 'True':
        switches[switch_name] = True
      elif switch_setting == 'False':
        switches[switch_name] = False


  print("Reading True/False switches complete.")


print('')
print('')
print('')
print('')
print('')

if processImages:
  all_files = sorted([el for el in os.listdir(saveDir)])
  print('Processing images.')


  if switches['nhc_analysis']:
    print('... NHC analysis - cropping image and adding   Sal locations.')
    current_files = [el for el in all_files if 'NHC_surface_analysis.png' in el]

    marker_radius = 5
    for fl in current_files:
      cmd = ['convert', os.path.join(saveDir,fl), '-crop', '1268x648+1100+350', '+repage', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      xPt, yPt = 952, 445
      cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'red', '-stroke', 'black', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))


    current_files = [el for el in all_files if 'NHC_' in el and 'surface_analysis' not in el]

    marker_radius = 5
    for fl in current_files:
      cmd = ['convert', os.path.join(saveDir,fl), '-crop', '900x665+0+0', '+repage', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      xPt, yPt = 775, 445
      cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'blue', '-stroke', 'black', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))



  if switches['mimic_tpw']:
    print('... MIMIC-TPW - cropping image and adding   Sal locations.')
    current_files = sorted([el for el in all_files if 'MIMIC-TPW' in el])

    marker_radius = 4
    for fl in current_files:
      cmd = ['convert', os.path.join(saveDir,fl), '-crop', '990x452+8+18', '+repage', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      xPt, yPt = 665, 323
      cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'white', '-stroke', 'black', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

    current_files_subset = [el for el in current_files if 'animation-' in el]
    frame_number = [int(el.split('-')[-1].split('.')[0]) for el in current_files_subset]
    for num, fl in enumerate(current_files_subset):
      os.rename(os.path.join(cropDir,fl), os.path.join(cropDir,fl[:24]+'{:02d}'.format(frame_number[num])+fl[-4:]))



  if switches['brammer_tropical_waves']:
    print('   ... Tropical wave analysis - cropping image and adding Sal locations.')
    current_files = [el for el in all_files if 'Brammer' in el]

    marker_radius = 4
    for fl in current_files:
      cmd = ['convert', os.path.join(saveDir,fl), '-crop', '990x388+10+0', '+repage', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      xPt, yPt = 662, 243
      cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'red', '-stroke', 'black', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))



  if switches['sal_split']:
    print('   ... SAL dust split image - cropping image and adding Sal location.')
    current_files = [el for el in all_files if 'SAL_dryAir_split' in el]

    marker_radius = 6
    for fl in current_files:
      cmd = ['convert', os.path.join(saveDir,fl), '-crop', '1312x780+230+0', '+repage', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      xPt, yPt = 1120, 488
      cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'white', '-stroke', 'black', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      # # # crop off the color bar
      cmd = ['convert', os.path.join(saveDir,fl), '-crop', '682x38+430+782', '+repage', os.path.join(cropDir,fl[:-4]+'_cbar'+fl[-4:])]
      os.system(' '.join(cmd))

      # # # resize color bar
      cmd = ['convert', os.path.join(cropDir,fl[:-4]+'_cbar'+fl[-4:]), '-resize', '1312x73', '+repage', os.path.join(cropDir,fl[:-4]+'_cbar'+fl[-4:]) ]
      os.system(' '.join(cmd))

      print('      ... Adding a larger version of the color bar.')
      # # # join original image and larger color bar together
      cmd = ['convert', os.path.join(cropDir,fl), os.path.join(cropDir,fl[:-4]+'_cbar'+fl[-4:]), '-append', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))


  if switches['meteosat_sat']:
    print('... Meteosat-11 - cropping image, adding Sal location, and adding a Celsius IR scale.')
    current_files = sorted([el for el in all_files if 'Meteosat' in el])

    marker_radius = 12
    #xPt, yPt = 600, 675
    xPt, yPt = 850, 910
    for fl in current_files:
      cmd = ['convert', os.path.join(saveDir,fl), '-crop', '3000x2000+0+0', '+repage', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'magenta', '-stroke', 'black', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      if 'IRC' in fl:
        print('      ... Color IR - adding Celsius color scale on side.')
        #cmd = []
        cmd = ['convert', os.path.join(cropDir,fl), '-resize', '3100x2000', '-background', 'white', '-gravity', 'west', '-extent', '3100x2000', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))
        # this will add a  color scale

        xPtT, yPtT = 3000, 1775
        cmd = ['convert', os.path.join(cropDir,fl), '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), '-110', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))
        xPtT, yPtT = 3000, 1577
        cmd = ['convert', os.path.join(cropDir,fl), '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), '-90', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))
        xPtT, yPtT = 3000, 1395
        cmd = ['convert', os.path.join(cropDir,fl), '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), '-70', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))
        xPtT, yPtT = 3000, 1215
        cmd = ['convert', os.path.join(cropDir,fl), '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), '-50', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))
        xPtT, yPtT = 3000, 1035
        cmd = ['convert', os.path.join(cropDir,fl), '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), '-30', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))
        xPtT, yPtT = 3000, 855
        cmd = ['convert', os.path.join(cropDir,fl), '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), '-10', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))
        xPtT, yPtT = 3000, 675
        cmd = ['convert', os.path.join(cropDir,fl), '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), ' 10', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))
        xPtT, yPtT = 3000, 495
        cmd = ['convert', os.path.join(cropDir,fl), '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), ' 30', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))
        xPtT, yPtT = 3000, 315
        cmd = ['convert', os.path.join(cropDir,fl), '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), ' 50', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))
        xPtT, yPtT = 3000, 245
        cmd = ['convert', os.path.join(cropDir,fl), '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), 'ºC', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))


  if switches['GOES16_sat']:
    print('... GOES-16 - cropping image, adding St. Croix location, and adding a Celsius IR scale.')
    current_files = sorted([el for el in all_files if 'Goes16' in el])

    marker_radius = 12
    for fl in current_files:
      if ('IRC' or 'RGB') in fl:
        xPt, yPt = 1340, 940
        cmd = ['convert', os.path.join(saveDir,fl), '-crop', '2000x2000+0+0', '+repage', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))

        cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'magenta', '-stroke', 'black', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))

      elif 'VIS' in fl:
        xPt, yPt = 940, 1560
        cmd = ['convert', os.path.join(saveDir,fl), '-crop', '3712x3700+0+0', '+repage', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))

        cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'magenta', '-stroke', 'black', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius*2) + ',' + str(yPt+marker_radius*2) + '\'', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))

      if 'IRC' in fl:
        print('      ... Color IR - adding Celsius color scale on side.')
        #cmd = []
        cmd = ['convert', os.path.join(cropDir,fl), '-resize', '2100x2000', '-background', 'white', '-gravity', 'west', '-extent', '2100x2000', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))
        # this will add a  color scale

        xPtT, yPtT = 2000, 1775
        cmd = ['convert', os.path.join(cropDir,fl), '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), '-110', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))
        xPtT, yPtT = 2000, 1577
        cmd = ['convert', os.path.join(cropDir,fl), '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), '-90', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))
        xPtT, yPtT = 2000, 1395
        cmd = ['convert', os.path.join(cropDir,fl), '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), '-70', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))
        xPtT, yPtT = 2000, 1215
        cmd = ['convert', os.path.join(cropDir,fl), '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), '-50', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))
        xPtT, yPtT = 2000, 1035
        cmd = ['convert', os.path.join(cropDir,fl), '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), '-30', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))
        xPtT, yPtT = 2000, 855
        cmd = ['convert', os.path.join(cropDir,fl), '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), '-10', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))
        xPtT, yPtT = 2000, 675
        cmd = ['convert', os.path.join(cropDir,fl), '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), ' 10', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))
        xPtT, yPtT = 2000, 495
        cmd = ['convert', os.path.join(cropDir,fl), '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), ' 30', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))
        xPtT, yPtT = 2000, 315
        cmd = ['convert', os.path.join(cropDir,fl), '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), ' 50', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))
        xPtT, yPtT = 2000, 245
        cmd = ['convert', os.path.join(cropDir,fl), '-pointsize', '50', '-annotate', '+' + str(xPtT) + '+' + str(yPtT), 'ºC', os.path.join(cropDir,fl)]
        os.system(' '.join(cmd))


  if switches['meteosat_sat'] and switches['GOES16_sat']:
    current_files_met = sorted([el for el in all_files if 'Meteosat' in el])
    current_files_goes = sorted([el for el in all_files if 'Goes16' in el])


    # for IRC image:
    fileName = 'Goes16_Meteosat11_IRC.png'
    currentInd_met = current_files_met.index([fl for fl in current_files_met if '_IRC.' in fl][0])
    currentInd_goes = current_files_goes.index([fl for fl in current_files_goes if '_IRC.' in fl][0])

    # 1. crop off the color bar off of GOES16
    cmd = ['convert', os.path.join(cropDir,current_files_goes[currentInd_goes]), '-crop', '502x2000+0+0', '+repage', os.path.join(cropDir,'temp1.png')]
    os.system(' '.join(cmd))

    # 2. merge met file with goes file
    cmd = ['convert', os.path.join(cropDir,'temp1.png'), os.path.join(cropDir,current_files_met[currentInd_met]), '+append', '+repage', os.path.join(cropDir,fileName)]
    os.system(' '.join(cmd))


    current_fls = [fl for fl in os.listdir(cropDir) if 'temp' in fl and '.png' in fl]
    for fl in current_fls:
      cmd = ['rm', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))


  if switches['uwincm_clouds_animation']:
    print('   ... UWIN-CM - clouds and TPW - cropping image and adding Sal locations.')
    current_files = sorted([el for el in all_files if 'uwincm_clouds' in el])

    marker_radius = 5
    for fl in current_files:
      cmd = ['convert', os.path.join(saveDir,fl), '-crop', '740x450+25+110', '+repage', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      xPt, yPt = 448, 172
      cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'white', '-stroke', 'black', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))


  if switches['uwincm_precipitation_animation']:
    print('   ... UWIN-CM - precipitation - cropping image and adding Sal locations.')
    current_files = sorted([el for el in all_files if 'uwincm_precip' in el])

    marker_radius = 5

    for fl in current_files:
      cmd = ['convert', os.path.join(saveDir,fl), '-crop', '740x500+25+110', '+repage', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      # Cape Verde
      xPt, yPt = 454, 171
      cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'black', '-stroke', 'red', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))



  if switches['uutah_precipitation_animation'] or switches['UTAH_website']:
    print('   ... Unversity of Utah - precipitation - cropping image and adding Sal location.')
    current_files = sorted([el for el in all_files if 'uutah_precip' in el])

    marker_radius = 5
    for fl in current_files:
      #cmd = ['convert', os.path.join(saveDir,fl), '-crop', '800x500+0+0', '+repage', os.path.join(cropDir,fl)]
      cmd = ['cp', os.path.join(saveDir,fl), os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      xPt, yPt = 452, 187
      cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'black', '-stroke', 'red', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      cmd = ['convert', os.path.join(cropDir,fl), '-resize', '750x500', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))


    current_files = sorted([el for el in all_files if 'uutah_clouds' in el])

    marker_radius = 5
    for fl in current_files:
      #cmd = ['convert', os.path.join(saveDir,fl), '-crop', '800x500+0+0', '+repage', os.path.join(cropDir,fl)]
      cmd = ['cp', os.path.join(saveDir,fl), os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      xPt, yPt = 452, 187
      cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'black', '-stroke', 'red', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      cmd = ['convert', os.path.join(cropDir,fl), '-resize', '750x500', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))


  if switches['ucdavis_precipitation_animation']:
    print('   ... Unversity of UCDavis - precipitation - cropping image and adding Sal location.')
    current_files = sorted([el for el in all_files if 'ucdavis_precip' in el])

    marker_radius = 5
    for fl in current_files:
      #cmd = ['convert', os.path.join(saveDir,fl), '-crop', '800x500+0+0', '+repage', os.path.join(cropDir,fl)]
      cmd = ['cp', os.path.join(saveDir,fl), os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      xPt, yPt = 422, 163
      cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'black', '-stroke', 'red', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      cmd = ['convert', os.path.join(cropDir,fl), '-resize', '750x500', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))


  if switches['ECMWF_prediction']:
    print('   ... ECMWF outlook - cropping image and adding Sal locations.')
    current_files = sorted([el for el in all_files if 'ECMWF_midRH_anim' in el])

    marker_radius = 4
    for fl in current_files:
      cmd = ['convert', os.path.join(saveDir,fl), '-crop', '971x547+0+0', '+repage', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      xPt, yPt = 235, 325
      cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'red', '-stroke', 'black', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))


    current_files = sorted([el for el in all_files if 'ECMWF_mslp_pcpn_anim' in el])

    marker_radius = 4
    for fl in current_files:
      cmd = ['convert', os.path.join(saveDir,fl), '-crop', '971x547+0+0', '+repage', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      xPt, yPt = 235, 325
      cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'red', '-stroke', 'black', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

    current_files = sorted([el for el in all_files if 'GFS_midRH_anim' in el])


  if switches['GFS_prediction']:
    print('   ... GFS outlook - cropping image and adding Sal locations.')
    marker_radius = 4
    for fl in current_files:
      #cmd = ['convert', os.path.join(saveDir,fl), '-crop', '825x530+80+85', '+repage', os.path.join(cropDir,fl)]
      cmd = ['cp', os.path.join(saveDir,fl), os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      xPt, yPt = 235, 325
      cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'red', '-stroke', 'black', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

    current_files = sorted([el for el in all_files if 'GFS_mslp_pcpn_anim' in el])

    marker_radius = 4
    for fl in current_files:
      #cmd = ['convert', os.path.join(saveDir,fl), '-crop', '825x530+80+85', '+repage', os.path.join(cropDir,fl)]
      cmd = ['cp', os.path.join(saveDir,fl), os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      xPt, yPt = 235, 325
      cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'red', '-stroke', 'black', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))


  if switches['mpas_outlook_day34']:
    print('   ... MPAS outlook - cropping image and adding Sal locations.')
    current_files = sorted([el for el in all_files if 'mpas_rainr' in el])

    marker_radius = 4
    for fl in current_files:
      cmd = ['convert', os.path.join(saveDir,fl), '-crop', '780x400+0+115', '+repage', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      xPt, yPt = 402, 98
      cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'red', '-stroke', 'black', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))


    current_files = sorted([el for el in all_files if 'mpas_pw_olr' in el])

    marker_radius = 4
    for fl in current_files:
      #cmd = ['convert', os.path.join(saveDir,fl), '-crop', '825x530+80+85', '+repage', os.path.join(cropDir,fl)]
      cmd = ['convert', os.path.join(saveDir,fl), '-crop', '780x400+0+115', '+repage', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      xPt, yPt = 402, 98
      cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'red', '-stroke', 'black', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))


  if switches['mpas_precipitation']:
    current_files = sorted([el for el in all_files if 'mpas_precip' in el])

    marker_radius = 4
    for fl in current_files:
      #cmd = ['convert', os.path.join(saveDir,fl), '-crop', '825x530+80+85', '+repage', os.path.join(cropDir,fl)]
      cmd = ['convert', os.path.join(saveDir,fl), '-crop', '780x400+0+115', '+repage', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      xPt, yPt = 402, 98
      cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'red', '-stroke', 'black', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      cmd = ['convert', os.path.join(cropDir,fl), '-resize', '750x500', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))


  if switches['nasa_geos']:
    print('   ... NASA GEOS images - cropping image and adding Sal locations.')
    current_files = sorted([el for el in all_files if 'GEOS_700mb_outlook' in el])

    marker_radius = 5
    for fl in current_files:
      cmd = ['convert', os.path.join(saveDir,fl), '-crop', '984x688+0+80', '+repage', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      xPt, yPt = 685, 335
      cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'red', '-stroke', 'black', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))


    current_files = sorted([el for el in all_files if ('GEOS_dust' in el) and ('vert' not in el)])

    marker_radius = 5
    for fl in current_files:
      cmd = ['convert', os.path.join(saveDir,fl), '-crop', '984x688+0+80', '+repage', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      xPt, yPt = 360, 325
      cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'white', '-stroke', 'black', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
      #os.system(' '.join(cmd))

      xPt, yPt = 685, 335
      cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'white', '-stroke', 'black', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))


    current_files = sorted([el for el in all_files if ('GEOS_dust' in el) and ('N.png' in el)])

    marker_radius = 8
    xPt, yPt = 385, 619
    for fl in current_files:
      cmd = ['convert', os.path.join(saveDir,fl), '-crop', '1021x654+2+57', '+repage', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      xPt, yPt = 750, 619
      cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'white', '-stroke', 'black', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))


    current_files = sorted([el for el in all_files if ('GEOS_dust' in el) and ('W.png' in el)])

    marker_radius = 8
    for fl in current_files:
      cmd = ['convert', os.path.join(saveDir,fl), '-crop', '1019x681+0+57', '+repage', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      xPt, yPt = 495, 619
      cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'white', '-stroke', 'black', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))


    current_files = sorted([el for el in all_files if ('GEOS_total_aot' in el)])

    marker_radius = 5
    for fl in current_files:
      cmd = ['convert', os.path.join(saveDir,fl), '-crop', '984x688+0+80', '+repage', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      xPt, yPt = 685, 335
      cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'blue', '-stroke', 'black', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

    current_files = sorted([el for el in all_files if ('GEOS_' in el) and ('CloudFraction' in el)])

    marker_radius = 5
    for fl in current_files:
      cmd = ['convert', os.path.join(saveDir,fl), '-crop', '984x688+0+80', '+repage', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))

      xPt, yPt = 685, 335
      cmd = ['convert', os.path.join(cropDir,fl), '-fill', 'red', '-stroke', 'black', '-draw', '\''+'circle '+ str(xPt) + ',' + str(yPt) + ' ' + str(xPt+marker_radius) + ',' + str(yPt+marker_radius) + '\'', os.path.join(cropDir,fl)]
      os.system(' '.join(cmd))



  print('Processing images complete.')
  time.sleep(5)

print('')
print('')
print('')
print('')
print('')



if joinSlideAnimations:
  print('Creating joint animations.')

  if switches['ECMWF_prediction'] and switches['GFS_prediction']:
      print('... ECMWF & GFS midRH')
      fls_left = sorted([el for el in os.listdir(cropDir) if 'ECMWF_midRH_anim_day1' in el])
      fls_right = sorted([el for el in os.listdir(cropDir) if 'GFS_midRH_anim_day1' in el])
      if len(fls_left) <= len(fls_right):
        for num, fl in enumerate(fls_left):
          cmd = ['convert', '+append', os.path.join(cropDir,fl), os.path.join(cropDir,fls_right[num]), os.path.join(cropDir,'ECMWF_GFS_midRH_day1_anim_' + '{:02d}'.format(num) + '.jpg')]
          os.system(' '.join(cmd))
      else:
        print('... ... The numbers of images for fields do not match.')

      animationSteps(cropDir, 'ECMWF_GFS_midRH_day1_anim_', 'ECMWF_GFS_midRH_day1.gif')

      fls_left = sorted([el for el in os.listdir(cropDir) if 'ECMWF_midRH_anim_day2' in el])
      fls_right = sorted([el for el in os.listdir(cropDir) if 'GFS_midRH_anim_day2' in el])
      if len(fls_left) <= len(fls_right):
        for num, fl in enumerate(fls_left):
          cmd = ['convert', '+append', os.path.join(cropDir,fl), os.path.join(cropDir,fls_right[num]), os.path.join(cropDir,'ECMWF_GFS_midRH_day2_anim_' + '{:02d}'.format(num) + '.jpg')]
          os.system(' '.join(cmd))
      else:
        print('... ... The numbers of images for fields do not match.')

      animationSteps(cropDir, 'ECMWF_GFS_midRH_day2_anim_', 'ECMWF_GFS_midRH_day2.gif')


      fls_left = sorted([el for el in os.listdir(cropDir) if 'ECMWF_midRH_anim_day3' in el])
      fls_right = sorted([el for el in os.listdir(cropDir) if 'GFS_midRH_anim_day3' in el])
      if len(fls_left) <= len(fls_right):
        for num, fl in enumerate(fls_left):
          cmd = ['convert', '+append', os.path.join(cropDir,fl), os.path.join(cropDir,fls_right[num]), os.path.join(cropDir,'ECMWF_GFS_midRH_day3_anim_' + '{:02d}'.format(num) + '.jpg')]
          os.system(' '.join(cmd))
      else:
        print('... ... The numbers of images for fields do not match.')

      animationSteps(cropDir, 'ECMWF_GFS_midRH_day3_anim_', 'ECMWF_GFS_midRH_day3.gif')

      print('... ECMWF & GFS precipitation')
      fls_left = sorted([el for el in os.listdir(cropDir) if 'ECMWF_mslp_pcpn_anim_day1' in el])
      fls_right = sorted([el for el in os.listdir(cropDir) if 'GFS_mslp_pcpn_anim_day1' in el])
      if len(fls_left) <= len(fls_right):
        for num, fl in enumerate(fls_left):
          cmd = ['convert', '+append', os.path.join(cropDir,fl), os.path.join(cropDir,fls_right[num]), os.path.join(cropDir,'ECMWF_GFS_mslp_pcpn_day1_anim_' + '{:02d}'.format(num) + '.jpg')]
          os.system(' '.join(cmd))
      else:
        print('... ... The numbers of images for fields do not match.')

      animationSteps(cropDir, 'ECMWF_GFS_mslp_pcpn_day1_anim_', 'ECMWF_GFS_mslp_pcpn_day1.gif')

      fls_left = sorted([el for el in os.listdir(cropDir) if 'ECMWF_mslp_pcpn_anim_day2' in el])
      fls_right = sorted([el for el in os.listdir(cropDir) if 'GFS_mslp_pcpn_anim_day2' in el])
      if len(fls_left) <= len(fls_right):
        for num, fl in enumerate(fls_left):
          cmd = ['convert', '+append', os.path.join(cropDir,fl), os.path.join(cropDir,fls_right[num]), os.path.join(cropDir,'ECMWF_GFS_mslp_pcpn_day2_anim_' + '{:02d}'.format(num) + '.jpg')]
          os.system(' '.join(cmd))
      else:
        print('... ... The numbers of images for fields do not match.')

      animationSteps(cropDir, 'ECMWF_GFS_mslp_pcpn_day2_anim_', 'ECMWF_GFS_mslp_pcpn_day2.gif')


      fls_left = sorted([el for el in os.listdir(cropDir) if 'ECMWF_mslp_pcpn_anim_day3' in el])
      fls_right = sorted([el for el in os.listdir(cropDir) if 'GFS_mslp_pcpn_anim_day3' in el])
      if len(fls_left) <= len(fls_right):
        for num, fl in enumerate(fls_left):
          cmd = ['convert', '+append', os.path.join(cropDir,fl), os.path.join(cropDir,fls_right[num]), os.path.join(cropDir,'ECMWF_GFS_mslp_pcpn_day3_anim_' + '{:02d}'.format(num) + '.jpg')]
          os.system(' '.join(cmd))
      else:
        print('... ... The numbers of images for fields do not match.')

      animationSteps(cropDir, 'ECMWF_GFS_mslp_pcpn_day3_anim_', 'ECMWF_GFS_mslp_pcpn_day3.gif')


  if switches['mpas_outlook_day34']:
      print('... MPAS TPW & precipitation')
      fls_left = sorted([el for el in os.listdir(cropDir) if 'pw_olr' in el])
      fls_right = sorted([el for el in os.listdir(cropDir) if 'rainr' in el])
      if len(fls_left) <= len(fls_right):
        for num, fl in enumerate(fls_left):
          cmd = ['convert', '+append', os.path.join(cropDir,fl), os.path.join(cropDir,fls_right[num]), os.path.join(cropDir,'MPAS_outlook_day3_anim_' + '{:02d}'.format(num) + '.jpg')]
          os.system(' '.join(cmd))
      else:
        print('... ... The numbers of images for fields do not match.')


      animationSteps(cropDir, 'MPAS_outlook_day3_anim_', 'MPAS_outlook_day3.gif')

  if switches['uwincm_clouds_animation'] and switches['uwincm_precipitation_animation']:

    if model_day1:
      print('... UWINCM TPW and OLR & precipitation - model day 1.')

      fls_left = sorted([el for el in os.listdir(cropDir) if 'uwincm_clouds_day1_anim' in el])
      fls_right = sorted([el for el in os.listdir(cropDir) if 'uwincm_precip_day1_anim' in el])
      if len(fls_left) <= len(fls_right):
        for num, fl in enumerate(fls_left):
          cmd = ['convert', '+append', os.path.join(cropDir,fl), os.path.join(cropDir,fls_right[num]), os.path.join(cropDir,'uwincm_joint_clouds_precipitation_day1_anim_' + '{:02d}'.format(num) + '.jpg')]
          os.system(' '.join(cmd))
      else:
        print('... ... The numbers of images for fields do not match.')


      animationSteps(cropDir, 'uwincm_joint_clouds_precipitation_day1_anim_', 'joint_clouds_precipitation_day1_movie.gif')

    if model_day2:
      print('... UWINCM TPW and OLR & precipitation - model day 2.')

      fls_left = sorted([el for el in os.listdir(cropDir) if 'uwincm_clouds_day2_anim' in el])
      fls_right = sorted([el for el in os.listdir(cropDir) if 'uwincm_precip_day2_anim' in el])
      if len(fls_left) <= len(fls_right):
        for num, fl in enumerate(fls_left):
          cmd = ['convert', '+append', os.path.join(cropDir,fl), os.path.join(cropDir,fls_right[num]), os.path.join(cropDir,'uwincm_joint_clouds_precipitation_day2_anim_' + '{:02d}'.format(num) + '.jpg')]
          os.system(' '.join(cmd))
      else:
        print('... ... The numbers of images for fields do not match.')


      animationSteps(cropDir, 'uwincm_joint_clouds_precipitation_day2_anim_', 'joint_clouds_precipitation_day2_movie.gif')

  if switches['UTAH_website']:

    if model_day1:
      print('... UTAH TPW and OLR & precipitation - model day 1.')

      fls_left = sorted([el for el in os.listdir(cropDir) if 'uutah_clouds_day1_anim' in el])
      fls_right = sorted([el for el in os.listdir(cropDir) if 'uutah_precip_day1_anim' in el])
      if len(fls_left) <= len(fls_right):
        for num, fl in enumerate(fls_left):
          cmd = ['convert', '+append', os.path.join(cropDir,fl), os.path.join(cropDir,fls_right[num]), os.path.join(cropDir,'uutah_joint_clouds_precipitation_day1_anim_' + '{:02d}'.format(num) + '.jpg')]
          os.system(' '.join(cmd))
      else:
        print('... ... The numbers of images for fields do not match.')


      animationSteps(cropDir, 'uutah_joint_clouds_precipitation_day1_anim_', 'joint_clouds_precipitation_day1_movie.gif')

    if model_day2:
      print('... UTAH TPW and OLR & precipitation - model day 2.')

      fls_left = sorted([el for el in os.listdir(cropDir) if 'uutah_clouds_day2_anim' in el])
      fls_right = sorted([el for el in os.listdir(cropDir) if 'uutah_precip_day2_anim' in el])
      if len(fls_left) <= len(fls_right):
        for num, fl in enumerate(fls_left):
          cmd = ['convert', '+append', os.path.join(cropDir,fl), os.path.join(cropDir,fls_right[num]), os.path.join(cropDir,'uutah_joint_clouds_precipitation_day2_anim_' + '{:02d}'.format(num) + '.jpg')]
          os.system(' '.join(cmd))
      else:
        print('... ... The numbers of images for fields do not match.')


      animationSteps(cropDir, 'uutah_joint_clouds_precipitation_day2_anim_', 'joint_clouds_precipitation_day2_movie.gif')


  print('Creating joint animations complete.')

#convert -size 500x500 xc:white canvas.png
#convert canvas.png in.png -geometry +200+200 -composite out.png

  if switches['model_4panel']:
    cmd = ['convert -size 780x400 xc:white', os.path.join(cropDir,'logo_cpexcv.png'), '-gravity center -composite', os.path.join(cropDir,'logo_cpexcv_cp.png')]
    os.system(' '.join(cmd))
    for num in range(12):
        cmd = ['cp', os.path.join(cropDir,'logo_cpexcv_cp.png'), os.path.join(cropDir,'logo_cpexcv_anim_'+'{:02d}'.format(num)+'.png')]
        os.system(' '.join(cmd))


    if switches['uwincm_precipitation_animation']: model_1 = model_4panel_ul+'_precip_day1_anim'
    else: model_1 = 'logo_cpexcv_anim_'

    if switches['uutah_precipitation_animation']: model_2 = model_4panel_ur+'_precip_day1_anim'
    else: model_2 = 'logo_cpexcv_anim_'

    if switches['ucdavis_precipitation_animation']: model_3 = model_4panel_dl+'_precip_day1_anim'
    else: model_3 = 'logo_cpexcv_anim_'

    if switches['mpas_precipitation']: model_4 = model_4panel_dr+'_precip_day1_anim'
    else: model_4 = 'logo_cpexcv_anim_'

    if 'model_4' in locals():
      fls_left = sorted([el for el in os.listdir(cropDir) if model_1 in el])
      fls_right = sorted([el for el in os.listdir(cropDir) if model_2 in el])

      for num, fl in enumerate(fls_left[:12]):
          cmd = ['convert', '+append', os.path.join(cropDir,fl), os.path.join(cropDir,fls_right[num]), os.path.join(cropDir,'temp1_anim_' + '{:02d}'.format(num) + '.jpg')]
          os.system(' '.join(cmd))

      fls_left = sorted([el for el in os.listdir(cropDir) if model_3 in el])
      fls_right = sorted([el for el in os.listdir(cropDir) if model_4 in el])

      for num, fl in enumerate(fls_left[:12]):
          cmd = ['convert', '+append', os.path.join(cropDir,fl), os.path.join(cropDir,fls_right[num]), os.path.join(cropDir,'temp2_anim_' + '{:02d}'.format(num) + '.jpg')]
          os.system(' '.join(cmd))

      fls_up = sorted([el for el in os.listdir(cropDir) if 'temp1_anim_' in el])
      fls_down = sorted([el for el in os.listdir(cropDir) if 'temp2_anim_' in el])
      if len(fls_up) <= len(fls_down):
          for num, fl in enumerate(fls_up[:12]):
              cmd = ['convert', '-append', os.path.join(cropDir,fl), os.path.join(cropDir,fls_down[num]), os.path.join(cropDir,'Four_model_joint_anim_day1_' + '{:02d}'.format(num) + '.jpg')]
              os.system(' '.join(cmd))

      animationSteps(cropDir, 'Four_model_joint_anim_day1_', 'Four_model_joint_movie_day1.gif')

    if switches['uwincm_precipitation_animation']: model_1 = model_4panel_ul+'_precip_day2_anim'
    else: model_1 = 'logo_cpexcv_anim_'

    if switches['uutah_precipitation_animation']: model_2 = model_4panel_ur+'_precip_day2_anim'
    else: model_2 = 'logo_cpexcv_anim_'

    if switches['ucdavis_precipitation_animation']: model_3 = model_4panel_dl+'_precip_day2_anim'
    else: model_3 = 'logo_cpexcv_anim_'

    if switches['mpas_precipitation']: model_4 = model_4panel_dr+'_precip_day2_anim'
    else: model_4 = 'logo_cpexcv_anim_'

    if 'model_4' in locals():
      fls_left = sorted([el for el in os.listdir(cropDir) if model_1 in el])
      fls_right = sorted([el for el in os.listdir(cropDir) if model_2 in el])

      for num, fl in enumerate(fls_left[:12]):
          cmd = ['convert', '+append', os.path.join(cropDir,fl), os.path.join(cropDir,fls_right[num]), os.path.join(cropDir,'temp1_anim_' + '{:02d}'.format(num) + '.jpg')]
          os.system(' '.join(cmd))

      fls_left = sorted([el for el in os.listdir(cropDir) if model_3 in el])
      fls_right = sorted([el for el in os.listdir(cropDir) if model_4 in el])

      for num, fl in enumerate(fls_left[:12]):
          cmd = ['convert', '+append', os.path.join(cropDir,fl), os.path.join(cropDir,fls_right[num]), os.path.join(cropDir,'temp2_anim_' + '{:02d}'.format(num) + '.jpg')]
          os.system(' '.join(cmd))

      fls_up = sorted([el for el in os.listdir(cropDir) if 'temp1_anim' in el])
      fls_down = sorted([el for el in os.listdir(cropDir) if 'temp2_anim' in el])
      if len(fls_up) <= len(fls_down):
          for num, fl in enumerate(fls_up[:12]):
              cmd = ['convert', '-append', os.path.join(cropDir,fl), os.path.join(cropDir,fls_down[num]), os.path.join(cropDir,'Four_model_joint_anim_day2_' + '{:02d}'.format(num) + '.jpg')]
              os.system(' '.join(cmd))

      animationSteps(cropDir, 'Four_model_joint_anim_day2_', 'Four_model_joint_movie_day2.gif')


  time.sleep(10)

print('')
print('')
print('')
print('')
print('')

if moveFinalImages:
  print('Moving final images and animations to ./figs_final.')


  list_of_images = ['logo_cpexcv.png',
                    'NHC_surface_analysis.png',
                    'MIMIC-TPW_latest.png',
                    'SAL_dryAir_split.jpg',
                    'AEW_Brammer.jpg',
                    'Goes16_Meteosat11_IRC.png',
                    'NHC_2day_outlook.png',
                    'NHC_5day_outlook.png',
                    'GEOS_dust_aot_day1.png',
                    'GEOS_total_aot_day1.png',
                    'GEOS_dust_aot_day1_vert_15N.png',
                    'GEOS_dust_aot_day1_vert_20W.png',
                    'GEOS_dust_aot_day2.png',
                    'GEOS_total_aot_day2.png',
                    'GEOS_dust_aot_day2_vert_15N.png',
                    'GEOS_dust_aot_day2_vert_20W.png',
                    'GEOS_total_aot_day3.png',
                    'GEOS_total_aot_day4.png',
                    'ECMWF_GFS_midRH_day1.gif',
                    'ECMWF_GFS_midRH_day2.gif',
                    'ECMWF_GFS_midRH_day3.gif',
                    'ECMWF_GFS_mslp_pcpn_day1.gif',
                    'joint_clouds_precipitation_day1_movie.gif',
                    'Four_model_joint_movie_day1.gif',
                    'ECMWF_GFS_mslp_pcpn_day2.gif',
                    'joint_clouds_precipitation_day2_movie.gif',
                    'Four_model_joint_movie_day2.gif',
                    'ECMWF_GFS_mslp_pcpn_day3.gif',
                    'MPAS_outlook_day3.gif'
                    ]

    # additional images, when they become available:
    # 'AEW_Brammer.jpg'

  for fl in list_of_images:
    if os.path.isfile(os.path.join(cropDir,fl)):
      os.system('cp ' + os.path.join(cropDir,fl) + ' ' + os.path.join(finDir,fl))
    else:
      print('... ... ' + fl + ' not present and cannot be copied over.')


  print('Moving final images and animations complete.')
  time.sleep(10)


  rename_of_images = ['logo_cpexcv.png',
                    '03_NHC_surface_analysis.png',
                    '04_MIMIC-TPW_latest.png',
                    '04_SAL_dryAir_split.jpg',
                    '04_AEW_Brammer.jpg',
                    '04_Goes16_Meteosat11_IRC.png',
                    '05_NHC_2day_outlook.png',
                    '05_NHC_5day_outlook.png',
                    '06_GEOS_dust_aot_day1.png',
                    '06_GEOS_total_aot_day1.png',
                    '06_GEOS_dust_aot_day1_vert_15N.png',
                    '06_GEOS_dust_aot_day1_vert_20W.png',
                    '07_GEOS_dust_aot_day2.png',
                    '07_GEOS_total_aot_day2.png',
                    '07_GEOS_dust_aot_day2_vert_15N.png',
                    '07_GEOS_dust_aot_day2_vert_20W.png',
                    '08_GEOS_total_aot_day3.png',
                    '08_GEOS_total_aot_day4.png',
                    '10_ECMWF_GFS_midRH_day1.gif',
                    '11_ECMWF_GFS_midRH_day2.gif',
                    '12_ECMWF_GFS_midRH_day3.gif',
                    '14_ECMWF_GFS_mslp_pcpn_day1.gif',
                    '15_joint_clouds_precipitation_day1_movie.gif',
                    '16_Four_model_joint_day1_movie.gif',
                    '17_ECMWF_GFS_mslp_pcpn_day2.gif',
                    '18_joint_clouds_precipitation_day2_movie.gif',
                    '19_Four_model_joint_day2_movie.gif',
                    '20_ECMWF_GFS_mslp_pcpn_day3.gif',
                    '21_MPAS_outlook_day3.gif'
                    ]

  for fl, fl_r in zip(list_of_images, rename_of_images):
      if os.path.isfile( os.path.join(finDir,fl) ):
        os.system('mv ' + os.path.join(finDir,fl) + ' ' + os.path.join(finDir,fl_r) )
      else:
        print('... ... ' + fl + ' not present and cannot be copied over.')

  #GEOS_dust_aot.png is used twice in the slide
  #os.system( 'cp ' + os.path.join(finDir,'04_GEOS_dust_aot.png') + ' ' + os.path.join(finDir,'12_GEOS_dust_aot.png') )

  print('Rename final images and animations complete.')
