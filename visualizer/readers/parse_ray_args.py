#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 17:21:18 2022

@author: nick
"""

import argparse
import os
import shutil

def call_parser():
        
    """Collects the information included as commandline arguments. 
    """

    print('Parsing Rayleigh Fit arguments...')
    
    parser = argparse.ArgumentParser(
    	description='arguments ')
    
    parser.add_argument('-i', '--input_file', metavar = 'input_file', 
                        type = str, nargs = '?', 
                        help = 'The path to the input file ')

    parser.add_argument('-o', '--output_folder', metavar = 'output_folder', 
                        type = str, nargs = '?', 
                        help = 'The path to the output folder where the results and plots subfolders will be placed ')

    parser.add_argument('-d', '--delete', metavar = 'delete',
                        type = bool, default = False, 
                        action = argparse.BooleanOptionalAction,
                        help = 'If called then the input file will be DELETED after processing in order to save space. Use with care! ')

    parser.add_argument('--dpi', metavar = 'dpi',
                        type = int, nargs = '?', default = 300, 
                        help = 'The dots per inch (dpi) resolution of the exported figures. Defaults to 100 ')

    parser.add_argument('--color_reduction', metavar = 'color_reduction',
                        type = bool, default = True, 
                        action = argparse.BooleanOptionalAction,
                        help = 'If set to True, and provided that Imagemagick is installed, an adaptive color reduction will be applied to save space when exporting the figures. Defaults to True. A warning will be raised if Imagemagick is not installed. ')

    parser.add_argument('--use_lin_scale', metavar = 'use_lin_scale',
                        type = bool, default = False, 
                        action = argparse.BooleanOptionalAction,
                        help = 'If called, a linear scale will be used for the x axis (signal) ')

    parser.add_argument('--use_range', metavar = 'use_range',
                        type = bool, default = True, 
                        action = argparse.BooleanOptionalAction,
                        help = 'If called, the y axis of the quicklook will correspond to the distance between the laser pulse and the telescope (vertical range) ')

    parser.add_argument('-c', '--channels', metavar = 'channels',
                        type = str, nargs = '+', default = None, 
                        help = 'Type one or more channel names (e.g. xpar0355) here in order to open the figures in interactive mode ')

    parser.add_argument('--exclude_telescope_type', metavar = 'exclude_telescope_type',
                        type = str, nargs = '+', default = [], 
                        help = 'Provide all the channel field types that you want to EXCLUDE (None: None, x: unspecified, n: near field, f: far field ). Nothing is excluded by default in ATLAS preprocessor ')

    parser.add_argument('--exclude_acquisition_mode', metavar = 'exclude_acquisition_mode',
                        type = str, nargs = '+', default = [], 
                        help = 'Provide all the channel detection mode types that you want to EXCLUDE (None: None, a: analogue, p: photon). Nothing is excluded by default in ATLAS preprocessor ')

    parser.add_argument('--exclude_channel_type', metavar = 'exclude_channel_type',
                        type = str, nargs = '+', default = [], 
                        help = 'Provide all the channel scattering types that you want to EXCLUDE (None: None, p: co-polar linear analyzer, c: cross-polar linear analyzer, t: total (no depol), o: co-polar circular analyzer, x: cross-polar circular analyzer, v: vibrational Raman, r: rotational Raman, a: Cabannes, f: fluorescence). Nothing is excluded by default in ATLAS preprocessor ')

    parser.add_argument('--exclude_channel_subtype', metavar = 'exclude_channel_subtype',
                        type = str, nargs = '+', default = ['b', 's', 'a', 'w', 'c'], 
                        help = 'Provide all the channel scattering types that you want to EXCLUDE (None: None, r: Signal Reflected from a PBS, t: Signal Transmitted through a PBS, n: N2 Ramal line, o: O2 Ramal line, w: H2O Ramal line, c: CH4 Ramal line, h: High Rotational Raman, l: Low Rotational Raman, a: Mie (aerosol) HSRL signal, m: Molecular HSRL signal, b: Broadband Fluorescence, s: Spectral Fluorescence, x: No specific subtype). The following subtyoes are excluded by default in ATLAS (b, s, a, w, c) ')
    
    parser.add_argument('--y_lims', metavar = 'y_lims',
                        type = float, nargs = 2, default = [None, None], 
                        help = 'The y axis limits (lower and upper) of the normalized RC signal. Defaults to 0 (lower) 1.2 (upper) when use_lin_scale is True. If use_lin_scale is true then the lower limit becomes 1E-5 ')

    parser.add_argument('--x_lims', metavar = 'x_lims',
                        type = float, nargs = 2, default = [0., 20.], 
                        help = 'The x axis limits in km (lower and upper). If use_range is called, the limits correspond to distance. Defaults to 0 km (lower) and 20 km (upper) If values below 0 or above the maximum signal altitude/distance are used, they will be ignored')

    parser.add_argument('--x_tick', metavar = 'x_tick',
                        type = int, nargs = '?', default = 2, 
                        help = 'The x axis finest tick in km. Defaults to 2km ')

    parser.add_argument('--normalization_region', metavar = 'normalization_region',
                        type = float, nargs = 2, default = [8.5, 9.5],
                        help = 'The lower and upper limits of the region used for normalizing the signal in the Rayleigh fit. If use_range is called, the limits correspond to distance. If auto_fit is set to True and the automatic identification is successful for a specific channel, the normalization_region values will e ignored. Defaults to: 8.5, 9.5')

    parser.add_argument('--auto_fit', metavar = 'auto_fit',
                        type = bool, default = True, 
                        action = argparse.BooleanOptionalAction,
                        help = 'If set to True an automatic identification of the molecular regions will be attempted. If the automatic procedure is successful, the normalization_region variable will be ignored. If the procedure is not successful or auto_fit is set to False, the manually-provided/default normalization will be used. Defaults to True')

    parser.add_argument('--cross_check_lim', metavar = 'cross_check_lim',
                        type = float, nargs = '?', default = 2, 
                        help = 'Lower limit applied for the cross-check criterion for the calculation of the Rayleigh fit mask. Use in case a high distance of full overlap is causing the cross-check test to fail. Defaults to 2km ')

    parser.add_argument('--smooth', metavar = 'smooth',
                        type = bool, default = True, 
                        action = argparse.BooleanOptionalAction,
                        help = 'Refer to the smooth option in the quicklook section. Defaults to: True')

    parser.add_argument('--smoothing_range', metavar = 'smoothing_range',
                        type = float, nargs = 2, default = [0., 20.], 
                        help = 'Refer to the smooth option in the quicklook section Defaults to: 0.05, 14.')

    parser.add_argument('--smoothing_window', metavar = 'smoothing_window',
                        type = float, nargs = "?", default = 500., 
                        help = 'The full smoothing window in the first and last bin of the smoothing region, in m. The widow progressively changes between from the first to the last value. Use the only one value twice to apply a constant window. Defaults to: smoothing_window = 100.')

    parser.add_argument('--smooth_exponential', metavar = 'smooth',
                        type = bool, default = False, 
                        action = argparse.BooleanOptionalAction,
                        help = 'Refer to the smooth option in the quicklook section. Defaults to: False.')

    args = vars(parser.parse_args())

    return(args)

def check_parser(args):
    
    mandatory_args = ['input_file']

    mandatory_args_abr = ['-i']
    
    for i in range(len(mandatory_args)):
        if not args[mandatory_args[i]]:
            raise Exception(f'---- Error: The mandatory argument {mandatory_args[i]} is not provided! Please provide it with: {mandatory_args_abr[i]} <path>')            

    if not os.path.exists(args['input_file']):
        raise Exception(f"---- Error: The path to the input file does not exists. Please provide a valid input file path. Current Path: {args['input_file']}")  
    
    if '_ray_' not in os.path.basename(args['input_file']):
        raise Exception('---- Error: Measurement filename not understood! The filename should contain the _ray_ field (quicklook)')
    
    if args['color_reduction'] == True:
        if shutil.which('convert') == None:
            raise Warning("---- Color_reduction was set tot True for the Rayleigh fit test but Imagemagick was not found. No color reduction will be performed. ")
            args['color_reduction'] = False
            
    if args['output_folder'] == None:
        out_path = os.path.join(os.path.dirname(args['input_file']),'..','..')
        args['output_folder'] = out_path
        os.makedirs(os.path.join(args['output_folder'], 'plots'), exist_ok = True)
        os.makedirs(os.path.join(args['output_folder'], 'ascii'), exist_ok = True)
    elif not os.path.exists(args['output_folder'] ):
        raise Exception(f"The provided output folder {args['output_folder']} does not exist! Please use an existing folder or don't provide one and let the the parser create the default output folder ") 
        
    return(args)

def view_parser(args):
    
    print(" ")
    print("-- Rayleigh Fit arguments!")
    print("-------------------------------------------------------------------")
    for key in args.keys():
        print(f"{key} = {args[key]}")
    print("-------------------------------------------------------------------")
    print("")
    
    return()