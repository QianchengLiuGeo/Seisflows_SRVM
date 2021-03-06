import sys
import numpy as np

from seisflows.tools import unix
from seisflows.tools.array import loadnpy, savenpy
from seisflows.tools.tools import savetxt, exists
from seisflows.tools.math import angle, dot

PATH = sys.modules['seisflows_paths']

class SRVM(object):
    """ Square root variable metric algorithm

        Includes optional safeguards: periodic restarting and descent
        conditions.

        To conserve memory, most vectors are read from disk rather than 
        passed from a calling routine.
    """

    def __init__(self, path='.', load=loadnpy, save=savenpy, memory=5, thresh=0., maxiter=np.inf, precond=None):
        assert exists(path)
        unix.cd(path)
        unix.mkdir('SRVM')

        self.path = path
        self.load = load
        self.save = save
        self.thresh = thresh
        self.maxiter = maxiter
        self.precond = precond
        self.memory = memory

        self.iter = 0
        self.memory_used = 0


    def __call__(self):
        """ Returns SRVM search direction
        """
        self.iter += 1

        #unix.cd(self.path)
	#unix.cp('../../model_true/proc000000_hessian.npy','./proc000000_hessian')

        hess = self.load('g_new')
        hess = 1.0
	#hess = self.load('proc000000_hessian')
        g = self.load('g_new') * hess
        self.save('g_new',g)
        if self.iter == 1:
	    #ShatT_ghat = g
	    #self.save('ShatT_ghat',g)
	    #print 'max(ShatT_ghat)',max(ShatT_ghat)
            #return -g, 0
            g = self.load('g_new')
            norm_g = max(abs(g))

	    m_init = self.load('m_new')
	    norm_m = max(abs(m_init))
	    self.save('m_init',m_init)
	  
	    baln = norm_m / norm_g * 0.05
	    self.savetxt('baln',baln)


	    g *= baln
            self.save('g_new',g)


        elif self.iter > self.maxiter:
            print 'restarting SRVM... [periodic restart]'
            self.restart()
            return -g, 1

	#baln = self.loadtxt('baln')
	r = self.load('m_init') * 0.5
	r = r * r

	print 'max_r', max(r)

        g = self.load('g_new') + (self.load('m_new') - self.load('m_init')) / r

	print 'max g,m_new,m_init',max(self.load('g_new')),max(self.load('m_new')),max(self.load('m_init'))

	kk = self.iter - 1

	ShatT_ghat = self.update(g,kk,1)

	self.save('ShatT_ghat',ShatT_ghat)

	q = self.update(ShatT_ghat,kk,0)

	m_init = self.load('m_init')

	tq_ratio = max(abs(q))/max(abs(m_init))
	#if tq_ratio > 0.2:
		#q = q * 0.2


	if self.iter == 1:
	    self.savetxt('R',0)
	    return -g, 0

        status = self.check_status(g,q)
	print 'status',status
	#status = 0
        if status != 0:
            self.restart()
	    self.savetxt('R',1)
            return -g, status
        else:
	    self.savetxt('R',0)
            return -q, status


    def update(self,chi,kk,tflag):
        """ Updates SRVM algorithm history
        """
        unix.cd(self.path)
		
	Shat_chi = chi

	mm = 500

	if tflag == 1:
            for ii in range(mm):
		jj = ii + 1 + kk - mm
		
		if jj > 0 :

    	            unix.cp('a_%04d' % jj,'A')
	            a = self.loadtxt('A')

		    unix.cp('nu_%04d' % jj,'Nu')
	    	    nu = self.loadtxt('Nu')

		    unix.cp('w_%04d' % jj,'W')
	            wtemp = self.load('W')

		#print 'A,nu', A,nu

	            xtemp = dot(wtemp,Shat_chi)
		    Shat_chi = Shat_chi - xtemp * nu / a * wtemp

	elif tflag == 0:
            for ii in range(mm):
		jj = kk - ii

		if jj > 0 :
	            unix.cp('a_%04d' % jj,'A')
	            a = self.loadtxt('A')

		    unix.cp('nu_%04d' % jj,'Nu')
		    nu = self.loadtxt('Nu')

		    unix.cp('w_%04d' % jj,'W')
	            wtemp = self.load('W')

		#print 'A,nu', A,nu

	            xtemp = dot(wtemp,Shat_chi)
		    Shat_chi = Shat_chi - xtemp * nu / a * wtemp

	return	Shat_chi
					

    def restart(self):
        """ Discards history and resets counters
        """
        #self.iter = 1


    def check_status(self, g, r):
        theta = 180.*np.pi**-1*angle(g,r)
	print 'theta =', theta
        if not 0. < theta < 90.:
            print 'restarting SRVM... [not a descent direction]'
            return 1
        elif theta > 90. - self.thresh:
            print 'restarting SRVM... [practical safeguard]'
            return 1
        else:
            return 0


    def dot(self,x,y):
        """ Computes inner product between vectors
        """
        return np.dot(
            np.squeeze(x),
            np.squeeze(y))

    def load(self, filename):
        return loadnpy(PATH.OPTIMIZE+'/'+filename)

    def save(self, filename, array):
        savenpy(PATH.OPTIMIZE+'/'+filename, array)


    def loadtxt(self, filename):
        return float(np.loadtxt(filename))

    def savetxt(self, filename, scalar):
        np.savetxt(PATH.OPTIMIZE+'/'+filename, [scalar], '%11.6e')


