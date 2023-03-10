'''
Answer to 8.1

d[E]/dt = -k1 [E][S] + (k2+k3) [ES]
d[S]/dt = k2 [ES] - k1[E][S]
d[ES]/dt = k1 [E][S] - (k2+k3) [ES]
d[P]/dt = k3 [ES]
'''
import numpy as np
from matplotlib import pyplot as plt

# (uM / min)
k1, k2, k3 = 100, 600, 150

# (min)
t = 1
dt = 0.0002
time = np.arange(0, t, dt)
num_iteration = int(np.ceil(t / dt))

# (uM)
E = np.zeros(num_iteration)
S = np.zeros(num_iteration)
ES = np.zeros(num_iteration)
P = np.zeros(num_iteration)
V = np.zeros(num_iteration)
E[0] = 1
S[0] = 10
ES[0] = 0
P[0] = 0

def get_dE(t, E, S, ES):
	return -k1 * E * S + (k2 + k3) * ES

def get_dS(t, E, S, ES):
	return k2 * ES - k1 * E * S

def get_dES(t, E, S, ES):
	return k1 * E * S - (k2 + k3) * ES

def get_dP(t, ES):
	return k3 * ES

def get_euler_updated(t, dt, E, S, ES, P):
	dE = get_dE(t, E, S, ES)
	dS = get_dS(t, E, S, ES)
	dES = get_dES(t, E, S, ES)
	dP = get_dP(t, ES)
	E_next = E + dE * dt
	S_next = S + dS * dt
	ES_next = ES + dES * dt
	P_next = P + dP * dt
	return E_next, S_next, ES_next, P_next

def get_rungekutta_updated(t, dt, E, S, ES, P):
	dE_1 = get_dE(t, E, S, ES)
	dE_2 = get_dE(t, E + dE_1 * dt/2, S, ES)
	dE_3 = get_dE(t, E + dE_2 * dt/2, S, ES)
	dE_4 = get_dE(t, E + dE_3 * dt, S, ES)
	dE = (dE_1 + dE_2 * 2 + dE_3 * 2 + dE_4) / 6
	E_next = E + dE * dt

	dS_1 = get_dS(t, E, S, ES)
	dS_2 = get_dS(t, E, S + dS_1 * dt / 2, ES)
	dS_3 = get_dS(t, E, S + dS_2 * dt / 2, ES)
	dS_4 = get_dS(t, E, S + dS_3 * dt, ES)
	dS = (dS_1 + dS_2 * 2 + dS_3 * 2 + dS_4) / 6
	S_next = S + dS * dt

	dES_1 = get_dES(t, E, S, ES)
	dES_2 = get_dES(t, E, S, ES + dES_1 * dt / 2)
	dES_3 = get_dES(t, E, S, ES + dES_2 * dt / 2)
	dES_4 = get_dES(t, E, S, ES + dES_3 * dt)
	dES = (dES_1 + dES_2 * 2 + dES_3 * 2 + dES_4) / 6
	ES_next = ES + dES * dt 

	dP_1 = get_dP(t, ES)
	dP_2 = get_dP(t, ES)
	dP_3 = get_dP(t, ES)
	dP_4 = get_dP(t, ES)
	dP = (dP_1 + dP_2 * 2 + dP_3 * 2 + dP_4) / 6
	P_next = P + dP * dt

	return E_next, S_next, ES_next, P_next

if __name__ == '__main__':
	for k, t in enumerate(time[1:]):
		V[k+1] = get_dP(t, ES[k])
		# E[k+1], S[k+1], ES[k+1], P[k+1] = get_euler_updated(t, dt, E[k], S[k], ES[k], P[k])
		E[k+1], S[k+1], ES[k+1], P[k+1] = get_rungekutta_updated(t, dt, E[k], S[k], ES[k], P[k])

	# plot for 8.2
	plt.plot(time, E, label='$E$')
	plt.plot(time, S, label='$S$')
	plt.plot(time, ES, label='$ES$')
	plt.plot(time, P, label='$P$')
	plt.annotate('%.3fmol' % E[-1], xy=(time[-1], E[-1]))
	plt.annotate('%.3fmol' % S[-1], xy=(time[-1], S[-1]))
	plt.annotate('%.3fmol' % ES[-1], xy=(time[-1], ES[-1]))
	plt.annotate('%.3fmol' % P[-1], xy=(time[-1], P[-1]))
	plt.xlabel('time $t$ (minute)')
	plt.ylabel('concentration (uM)')
	plt.legend()
	plt.title('concentration of $E$, $S$, $ES$ and $P$ according to time $t$')
	plt.show()

	# plot for 8.3
	plt.plot(S, V, label='velocity of S')
	plt.axhline(y=V.max(), ls=':')
	plt.plot(S[V.argmax()], V.max(), marker='.', markersize=20, zorder=-1, color='#FB2')
	plt.annotate('(%.2f, %.2f)' % (S[V.argmax()], V.max()), xy=(S[V.argmax()], V.max()))
	plt.title('velocity $V$ according to time $t$')
	plt.xlabel('time $t$ (minute)')
	plt.ylabel('concentration (uM)')
	plt.show()
