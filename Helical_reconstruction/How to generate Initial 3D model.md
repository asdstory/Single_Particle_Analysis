# Featureless cylinders

### Featureless cylinders are unbiased initial models that are also non-polar, and they are often a good choice for simple helices. A cylindrical reference can be generated using the following command: 

- [ ] relion_helix_toolbox --cylinder --o out.mrc --boxdim 400 --cyl_innner_diameter 50 --cyl_outer_diameter 150 --angpix 1.058 --sphere_percentage 0.9 --width 5 

# Simulated lattices

### Simulated helical lattices are better initial models for complicated symmetries compared to featureless cylinders as they provide helical lattice information for the alignment. 

- [ ] relion_helix_toolbox --simulate_helix --o out.mrc --subunit_diameter 30 --cyl_outer_diameter 150 --angpix 1.058 --rise 1.408 --twist 0 --boxdim 400 --sym_Cn 1 --sphere_percentage 0.9 --width 5

# Initial model from a single 2D large class averages

- [ ] relion_image_handler --i 180@Class2D/job051/run_it025_classes.mrcs --o bigclass.mrc
- [ ] relion_project --i bigclass.mrc --o bigclass_ali.mrc --psi -0.67
- [ ] relion_image_handler --i bigclass_ali.mrc --o bigclass_ali.mrc --shift_y -5
- [ ] relion_star_loopheader rlnReferenceImage > bigclass.star
- [ ] echo "bigclass_ali.mrc" >> bigclass.star
- [ ] relion_helix_inimodel2d --i Select/job382/class_averages.star --iter 1 --sym 2 --crossover_distance 800 --angpix 1.058 --o Select/job382/ref --mask_diameter 400
- [ ] relion_image_handler --i IniModel/bigclass_class001_rec3d.mrc --o IniModel/bigclass_class001_rec3d_box256.mrc --angpix 3.45 --rescale_angpix 1.058 --new_box 256

# Initial model from multiple smaller 2D class averages

- [ ] relion_stack_create --i Select/job060/class_averages.star --o IniModel/smallclasses_box256 --ignore_optics
- [ ] relion_image_handler --i IniModel/smallclasses_box256.mrcs --new_box 400 --o IniModel/smallclasses_box400.mrcs
- [ ] relion_helix_inimodel2d --i IniModel/smallclasses_box220.star --iter 10 --crossover_distance 700 --angpix 1.058 --o IniModel/smallclasses --mask_diameter 150 --search_shift 3 --search_angle 1 --step_angle 1 --sym 2 --maxres 5 --j 12
- [ ] relion_image_handler --i IniModel/smallclasses_class001_rec3d.mrc --o IniModel/smallclasses_class001_rec3d_box256.mrc --new_box 256
