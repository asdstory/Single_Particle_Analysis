## To get the range for z, to solve the problem of "Z percentage is out of range under current settings!".

- [ ] relion_helix_toolbox --check --boxdim 200 --cyl_outer_diameter 20 --rise_max 50 --sphere_percentage 0.75 --angpix 1.058 --rise 47.7 --twist 0 --z_percentage 0.5

- [ ] relion_helix_toolbox --check --boxdim 200 --cyl_outer_diameter 150 --rise_max 50 --sphere_percentage 0.95 --angpix 1.058 --rise 48.6 --twist 0.75 --z_percentage 0.5

- [ ] relion_helix_toolbox --check --boxdim 200 --cyl_outer_diameter 150 --rise_max 50 --sphere_percentage 0.95 --angpix 1.058 --rise 48.6 --twist 0.75 --z_percentage 0.5

- [ ] `which relion_refine_mpi` --o Class3D/job306/run --i Select/job262/particles.star --ref InitialModel/job263/run_it300_class001.mrc --firstiter_cc --ini_high 15 --dont_combine_weights_via_disc --pool 3 --pad 2  --ctf --ctf_corrected_ref --iter 25 --tau2_fudge 4 --particle_diameter 212 --K 4 --flatten_solvent --zero_mask --strict_highres_exp 12 --oversampling 1 --healpix_order 3 --offset_range 30 --offset_step 2 --sym C6 --norm --scale  --helix --helical_outer_diameter 150 --helical_nr_asu 1 --helical_twist_initial 10 --helical_rise_initial 40 --helical_z_percentage 0.4 --helical_symmetry_search --helical_twist_min 0 --helical_twist_max 10 --helical_twist_inistep 1 --helical_rise_min 20 --helical_rise_max 60 --helical_rise_inistep 1 --sigma_tilt 5 --sigma_psi 3.33333 --sigma_rot 0 --j 1 --gpu "" -dont_check_norm --pipeline_control Class3D/job306/

```

##########################################################
   CHECKING PARAMETERS FOR 3D HELICAL RECONSTRUCTION...
##########################################################
 Pixel size = 1.058 Angstrom(s)
 Box size = 200 pixels = 211.6 Angstroms
 Particle diameter = 150 pixels = 158.7 Angstroms
 Half box size = 99 pixels = 104.742 Angstroms
 Outer tube diameter = 18.9036 pixels = 20 Angstroms
 Helical twist = 0 degree(s)
 Helical rise  = 45.0851 pixel(s) = 47.7 Angstrom(s)
 Z percentage = 0.5 = 50 %
 Z percentage should be > 0.450851 and < 0.74402 (under current settings)
 Number of asymmetrical units = 1, maximum value = 3 (under current settings)
 Done! All the parameters seem OK for 3D helical reconstruction in RELION.

```
