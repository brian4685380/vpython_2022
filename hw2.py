from vpython import *
g = 9.8
size, delta, m = 0.2, 0.002, 1
L, k = 2, 150000
scene = canvas(width = 500, height = 500, center = vec(0, -0.2, 0), background = vec(0.5,0.5,0))
ceiling = box(length = 3, height = 0.05, width = 3, color = color.blue)
dt = 0.0001
t = 0
K_total = 0
U_total = 0
averaged_K_total = 0
averaged_U_total = 0

Et_plot = graph(title = "E-t plot", width = 600, height = 450, x = 0, y = 600,
	xtitle = "t(s)", ytitle = "E(J)")
averaged_Et_plot = graph(title = "averaged_E-t plot", width = 600, height = 450, x = 0, y = 600,
	xtitle = "t(s)", ytitle = "E(J)")
Kt = gcurve(graph = Et_plot, color = color.red)
Ut = gcurve(graph = Et_plot, color = color.blue)
averaged_Kt = gcurve(graph = averaged_Et_plot, color = color.red)
averaged_Ut = gcurve(graph = averaged_Et_plot, color = color.blue)
def af_col_v(m1, m2, v1, v2, x1, x2): # function after collision velocity
	v1_prime = v1 + 2*(m2/(m1+m2))*(x1-x2) * dot (v2-v1, x1-x2) / dot (x1-x2, x1-x2)
	v2_prime = v2 + 2*(m1/(m1+m2))*(x2-x1) * dot (v1-v2, x2-x1) / dot (x2-x1, x2-x1)
	return (v1_prime, v2_prime)

balls = []
for i in range(5) :
	ball = sphere(radius = size, pos = vec(2 * (size + delta) * (i - 2), -L - m*g/k, 0))
	ball.v = vec(0, 0, 0)
	balls.append(ball)
springs = []
for i in range(5) :
	spring = cylinder(radius=0.05, pos = vec(2 * (size + delta) * (i - 2), 0, 0))
	spring.axis = balls[i].pos - spring.pos
	spring.k = k
	springs.append(spring)
N = int(input())
for i in range(N) :
	balls[i].pos += vec(-(2 ** 2 - 1.95 ** 2) ** 0.5, 0.05, 0)
	springs[i].axis = balls[i].pos - springs[i].pos
while True:
	t += dt
	for i in range(5) :
		if (i < 4) :
			if (mag(balls[i].pos - balls[i + 1].pos) <= size * 2) :
				(balls[i].v, balls[i + 1].v) = af_col_v(m, m, balls[i].v, balls[i + 1].v, balls[i].pos, balls[i - 1].pos)
		springs[i].axis = balls[i].pos - springs[i].pos #spring extended from endpoint to ball
		spring_force = - k * (mag(springs[i].axis) - L) * springs[i].axis.norm() # to get spring force vector
		balls[i].a = vector(0, - g, 0) + spring_force / m # ball acceleration = - g in y + spring force /m
		balls[i].v += balls[i].a*dt
		balls[i].pos += balls[i].v*dt
		if (i == 4) :
			for i in range(5) :
				K_total += 0.5 * m * mag2(balls[i].v)
				averaged_K_total = K_total / 5
				U_total += m * g * (balls[i].pos.y + L + m * g / k)
				averaged_U_total = U_total / 5
			Kt.plot(pos = (t, K_total))
			Ut.plot(pos = (t, U_total))
			averaged_Kt.plot(pos = (t, averaged_K_total))
			averaged_Ut.plot(pos = (t, averaged_U_total))
			U_total = 0
			K_total = 0
			averaged_K_total = 0
			averaged_U_total = 0