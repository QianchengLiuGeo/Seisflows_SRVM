SeisFlows_SRVM
=================

SeisFlows_SRVM is a special version of SeisFlows.

SeisFlows contains SRVM, an additional optimization algorithm, in addition to SD, CG and L-BFGS in the original Seisflows.

SRVM based FWI allows for a posterior uncertainty estimation after the inversion finishes.

Documentation about the algorithm in Seisflows_SRVM is available online at readthedocs.org, except for an addtional option: SRVM. One manuscript about how SRVM works during FWI will be under review in GJI soon.

The codes for uncertainty estimation are written in Matlab. The posterior analysis part includes RSVD-SRVM, standard deviation map, eigenvectors and eigenvalues of the inverse Hessian, 2D Gaussian random samplers, 2D posterior sampling, marginal distributions, and null space.

One manuscript about the theories and methods on uncertainty estimation in Seisflows_SRVM will be under review in GJI soon.

==================================================================================================================================

SeisFlows is an open source seismic inversion package that

    Delivers a complete, customizable waveform inversion workflow

    Provides a framework for research in regional, global, and exploration seismology

Documentation is available online at readthedocs.org. A manuscript is currently under review in Computers and Geosciences.


