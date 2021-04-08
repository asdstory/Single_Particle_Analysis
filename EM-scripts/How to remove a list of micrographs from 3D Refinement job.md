
Hi,

> I realised some of my micrographs have only 1-3 particles, which are mostly false positives. I have three questions, does bad particles affect my 
> final reconstructions?

Probably no, unless you have really a lot of bad particles and/or you are at very very
high resolution (see the method section of our atomic resolution paper in Nature last week).

> If not so much, is there a way to verify the signal contribution of those particles in the final constructions?

Look at the "model_groups" data block of run_model.star.

Usually bad micrographs have rlnGroupScaleCorrection values significantly smaller
than 1.0 (say < 0.4).

> Regardless of 
> the two previous questions, how can I remove those micrographs and rerun 3D refinement on the remaining micrographs?
```sh
relion_star_printtable Refine3D/jobXXX/run_model.star data_model_groups rlnGroupName rlnGroupNrParticles _rlnGroupScaleCorrection | awk '$3 < 0.4 || 
$2 < 10 {print $1}'> BAD_MICS.lst
```
This will make the list of bad groups with rlnGroupScaleCorrection < 0.4 and particles less than 10.
Then you can remove such particles from run_data.star as:
```sh
grep -Fvf BAD_MICS.lst Refine3D/jobXXX/run_data.star > filtered.star
```
That being said, such a step is usually not necessary.

Best regards,

Takanori Nakane

########################################################################

To unsubscribe from the CCPEM list, click the following link:
Bad URL Removed - see why - https://ees.sps.nih.gov/services/Pages/Anti-Virus.aspx?SUBED1=CCPEM&A=1

This message was issued to members of www.jiscmail.ac.uk/CCPEM, a mailing list hosted by www.jiscmail.ac.uk, terms & conditions are available at https://www.jiscmail.ac.uk/policyandsecurity/
