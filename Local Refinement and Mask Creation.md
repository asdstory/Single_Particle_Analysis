# Mask Creation: 

Once you have identified a region of interest that you would like to refine further, you can use a few methods to extract a mask from it. The recommended tool to use here is Chimera, and you can take any of the following three tools. Note that your mask should be the saved on an identical grid as the original structure, and should have an origin of [0,0,0]. To force Chimera to save your map on the same grid as your original map, you can run the vop resample #1 onGrid #2 command where #1 is your off-grid mask and #2 is your original structure.


## Volume Eraser: 
The Chimera Volume Eraser tool is fairly self-explanatory. You can use a variable-sized sphere to delete chunks off the original structure to leave you with the region of interest


## Segment Map: 
You can use the built-in segmentation tool in Chimera to algorithmically segment your volume, and group the subvolumes together until you have your region of interest in one segment. Then, you can save this segment as a .mrc file.


## Fit in Map: 
If you already have an atomic model of the region of the structure you want to refine, you can open it in the same session as your original structure and use the Fit in Map tool to align it. Then, you can use the molmap command to create a new volume from the atomic model that can serve as a mask.
Mask Processing: Use the Volume Tools job to dilate your masks, add soft padding, and fill holes. This mask will be used to select a region of the structure to refine, but a dynamically generated mask will be used at each iteration of alignment.

## Fulcrum: 

Instead of doing a naive search that extends uniformly in each direction from the original pose, cryoSPARC gives the option to account for rotations around the connection point between the subvolume and the original structure. Note that the fulcrum is indexed from the corner of the structure, not the center ([0,0,0] will correspond a corner of the structure, not the center). Leaving the fulcrum option unset in the job builder will default to using the center of the structure as the rotation point. If it is hard to choose an exact fulcrum, or you are unsure about your selection, it may improve results to increase the "Local shift search extent" parameter.

## Branch and Bound: 

cryoSPARC's GPU-accelerated Branch and Bound algorithm accurately searches over a range of poses and shifts to find the best alignment of each image. The poses are forced to remain close to the original pose - how far it can stray away from the original pose is governed by the search extent parameters. The rotation extent (in radians) limits the magnitude of the angle of each rotation, the algorithm will search over rotations in all directions within the extent. The shift extent in pixels limits the diameter of the circle over which the shift is searched.

## Non-Uniform Refinement BETA: 

The Non-Uniform Refinement job, which is particularly useful for particles that have non-uniform structural characteristics, like membrane proteins or other macromolecules with unresolved peripheral structure, is also available as a feature in local refinement. This can often improve the quality of the map in your region of interest.

## FSC Calculation: 

The FSC plots will show the Global FSC, spherical masked FSC as well as the locally masked FSC. It it typical for the local FSCs (tight & loose mask) to be significantly better than the global values, since they are calculated using a dynamic mask around the computed structure.

## Gold Standard: 

The local refinement job follows the Gold-Standard FSC assumptions the same way a typical refinement job does. Particles are split into two halves using the splits from the previous refinement jobs, and the alignments are computed on independent halfmaps.

## New output plots!: 

The local refinement job will output heatmaps showing the magnitude of the change in poses and shifts for each initial position. Also, you will be able to see the distribution of the magnitude of changes for poses and shifts in the form of histograms.


