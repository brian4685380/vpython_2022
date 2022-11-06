from vpython import *

t = 0
g = 9.8 # g = 9.8 m/s^2
size = 0.25 # ball radius = 0.25 m
height = 15.0 # ball center initial height = 15 m
C_drag = 0.9
times = 0
trip_dis = 0;
vt_plot = graph(title="v-t plot", width=600, height=450,
            x=0, y=600, xtitle="t(s)", ytitle="v(m/s)")
vt = gcurve(graph=vt_plot, color=color.red)
scene = canvas(width=600, height=600, center =vec(0,height/2,0), background=vec(0.5,0.5,0))
floor = box(length=30, height=0.01, width=10, color=color.blue)
ball = sphere(radius = size, color=color.red, make_trail = True)
ball.pos = vec(-15, size, 0)
ball.v = vec(10*sqrt(2), 10*sqrt(2), 0)# ball initial velocity
velocity_arrow = arrow(shaftwidth = 0.3, pos = ball.pos, axis = ball.v, length = mag(ball.v))
max_height = 0
dt = 0.001 # time step
while times < 3: # until the ball hit the ground
	rate(500) # run 1000 times per real second
	t += dt
	ball.v += vec(0, -g, 0) * dt - C_drag*ball.v*dt
	trip_dis += mag(ball.v) * dt
	ball.pos += ball.v*dt
	velocity_arrow.pos = ball.pos
	velocity_arrow.axis = ball.v
	velocity_arrow.length = mag(ball.v)

	vt.plot(pos=(t, mag(ball.v)))
	if ball.pos.y > max_height:
		max_height = ball.pos.y
	if ball.pos.y <= size:
		ball.v.y = -ball.v.y
		times = times + 1 
msg1 = text(text = 'final displacement = ' + str(ball.pos-vec(-15, size, 0)) 
	, pos = vec(-15, 15, 0))
msg2 = text(text = 'total trip distence = ' + str(trip_dis)
	, pos = vec(-15, 13.5, 0))
msg3 = text(text = 'the largest height of the ball= ' + str(max_height)
	, pos = vec(-15, 12, 0))


