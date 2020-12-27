# -*- coding: utf-8 -*-
"""Untitled6.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1msX0uAX-29_vD-vmW8LoOllPiuBhUgq0
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np



import matplotlib.pyplot as plt
# %matplotlib inline



f_w0 = -0.3
f_w1 =  0.5


def f(X, noise_variance):
    '''Linear function plus noise'''
    return f_w0 + f_w1 * X + noise(X.shape, noise_variance)


def g(X, noise_variance):
    '''Sinusoidal function plus noise'''
    return 0.5 + np.sin(2 * np.pi * X) + noise(X.shape, noise_variance)


def noise(size, variance):
    return np.random.normal(scale=np.sqrt(variance), size=size)

def g(X, noise_variance):
    '''Sinusoidal function plus noise'''
    return 0.5 + np.sin(2 * np.pi * X) + noise(X.shape, noise_variance)

def identity_basis_function(x):
    return x


def gaussian_basis_function(x, mu, sigma=0.1):
    return np.exp(-0.5 * (x - mu) ** 2 / sigma ** 2)


def polynomial_basis_function(x, power):
    return x ** power


def expand(x, bf, bf_args=None):
    if bf_args is None:
        return np.concatenate([np.ones(x.shape), bf(x)], axis=1)
    else:
        return np.concatenate([np.ones(x.shape)] + [bf(x, bf_arg) for bf_arg in bf_args], axis=1)

def posterior(Phi, t, alpha, beta, return_inverse=False):
    """Computes mean and covariance matrix of the posterior distribution."""
    S_N_inv = alpha * np.eye(Phi.shape[1]) + beta * Phi.T.dot(Phi)
    S_N = np.linalg.inv(S_N_inv)
    m_N = beta * S_N.dot(Phi.T).dot(t)

    if return_inverse:
        return m_N, S_N, S_N_inv
    else:
        return m_N, S_N


def posterior_predictive(Phi_test, m_N, S_N, beta):
    """Computes mean and variances of the posterior predictive distribution."""
    y = Phi_test.dot(m_N)
    # Only compute variances (diagonal elements of covariance matrix)
    y_var = 1 / beta + np.sum(Phi_test.dot(S_N) * Phi_test, axis=1)
    
    return y, y_var
  
def plot_data(x, t):
    plt.scatter(x, t, marker='o', c="k", s=20)


def plot_truth(x, y, label='Truth'):
    plt.plot(x, y, 'k--', label=label)


def plot_predictive(x, y, std, y_label='Prediction', std_label='Uncertainty', plot_xy_labels=True):
    y = y.ravel()
    std = std.ravel()

    plt.plot(x, y, label=y_label)
    plt.fill_between(x.ravel(), y + std, y - std, alpha = 0.5, label=std_label)

    if plot_xy_labels:
        plt.xlabel('x')
        plt.ylabel('y')
def plot_posterior_samples(x, ys, plot_xy_labels=True):
    plt.plot(x, ys[:, 0], 'r-', alpha=0.5, label='Post. samples')
    for i in range(1, ys.shape[1]):
        plt.plot(x, ys[:, i], 'r-', alpha=0.5)

    if plot_xy_labels:
        plt.xlabel('x')
        plt.ylabel('y')




N_list = [3, 8, 20]

beta = 25.0
alpha = 2.0

# Training observations in [-1, 1)
X = np.random.rand(N_list[-1], 1)

# Training target values
t = g(X, noise_variance=1/beta)

# Test observations
X_test = np.linspace(0, 1, 100).reshape(-1, 1)

# Function values without noise 
y_true = g(X_test, noise_variance=0)
    
# Design matrix of test observations
Phi_test = expand(X_test, bf=gaussian_basis_function, bf_args=np.linspace(0, 1, 9))

plt.figure(figsize=(10, 10))
plt.subplots_adjust(hspace=0.4)

for i, N in enumerate(N_list):
    X_N = X[:N]
    t_N = t[:N]

    # Design matrix of training observations
    Phi_N = expand(X_N, bf=gaussian_basis_function, bf_args=np.linspace(0, 1, 9))

    # Mean and covariance matrix of posterior
    m_N, S_N = posterior(Phi_N, t_N, alpha, beta)
    
    # Mean and variances of posterior predictive 
    y, y_var = posterior_predictive(Phi_test, m_N, S_N, beta)
    
    # Draw 5 random weight samples from posterior and compute y values
    w_samples = np.random.multivariate_normal(m_N.ravel(), S_N, 5).T
    y_samples = Phi_test.dot(w_samples)
    
    plt.subplot(len(N_list), 2, i * 2 + 1)
    plot_data(X_N, t_N)
    plot_truth(X_test, y_true)
    plot_posterior_samples(X_test, y_samples)
    plt.ylim(-1.0, 2.0)
    plt.legend()
    
    plt.subplot(len(N_list), 2, i * 2 + 2)
    plot_data(X_N, t_N)
    plot_truth(X_test, y_true, label=None)
    plot_predictive(X_test, y, np.sqrt(y_var))
    plt.ylim(-1.0, 2.0)
    plt.legend()

f, (ax1,ax2,ax3) = plt.subplots(1,3,figsize=(14,4),sharey=True);

#predict new data points
x_predict = np.concatenate((np.linspace(-5,-1,10),np.linspace(6,15,20)));
y_predict = line(x_predict,mb_ls[0],mb_ls[1]);
#draw
ax1.plot(x_temp,line(x_temp,mb_ls[0],mb_ls[1]),'m--',label='LSE');
ax1.plot(x, y,'k.',markersize=15,label='$y');
); ax1.set_title(‘predictions’); ax1.set_xlabel(‘x’); ax1.set_ylabel(‘y’); ax1.legend(); ); ax1.set_title(‘predictions’); ax1.set_xlabel(‘x’); ax1.set_ylabel(‘y’); ax1.legend(); #stochastic prediction rss_ls = least_square_result[1]; #sum of squared residuals std_ls = np.sqrt(rss_ls/N); y_predict = line(x_predict,mb_ls[0],mb_ls[1]) + np.random.normal(0,std_ls,len(x_predict)); #draw ax2.plot(x_temp,line(x_temp,mb_ls[0],mb_ls[1]),‘m–‘); ax2.plot(x, y,‘k.’,markersize=15); ax2.plot(x_predict,y_predict,‘m.’,markersize=15); ax2.set_title(‘stochastic prediction with $\sigma$ = %2.2f‘ %(std_ls)); ax2.set_xlabel(‘x’); #visualize predictive distribution def variancePolygon(axes,model,xmin,xmax,resolution,std,alpha=1,color=‘r’,drawUpTo=1,label=”): Y = list() X = np.linspace(xmin,xmax,resolution); for x in X: y = model(x) Y.append(y); Y = np.array(Y); for i in range(1,drawUpTo+1): temp_std = std*float(i); temp_alpha = 0.5*float(drawUpTo–i+1)*alpha/(drawUpTo); plt.fill(np.append(X,np.flipud(X)),np.append(Y–temp_std,np.flipud(Y)+temp_std),color,alpha=temp_alpha,label=“%i $\sigma$”%i) axes.legend(); variancePolygon(ax3,lambda x: line(x,mb_ls[0],mb_ls[1]),–5,15,2, std_ls,1.0,‘m’,3,‘MLE’); ax3.plot(x, y,‘k.’,markersize=15,label=‘data points’); ax3.plot(x_predict,y_predict,‘m.’,markersize=15,label=‘predictions’); ax3.set_title(‘predictive distribution’); ax3.set_xlabel(‘x’);




