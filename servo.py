from time import sleep

# Adjust the pulse values to set rotation range
min_pulse = 0.000544	# Library default = 1/1000
max_pulse = 0.0024		# Library default = 2/1000
# Initial servo position
pos = 0
test = 0

servo = Servo(11, pos, min_pulse, max_pulse, 20/1000, None)

while True:
	# For statement example
	for pos in range(0, 20):
		pos = pos * 0.1 - 1
		servo.value = pos
		print(pos)
		sleep(0.05)

	for pos in range(20, -1, -1):
		pos = pos * 0.1 - 1
		servo.value = pos
		print(pos)
		sleep(0.05)

	# While statement example
	"""
	while test < 20:
		pos = test * 0.1 - 1
		servo.value = pos
		print(pos)
		test = test + 1
		sleep(0.05)

	while test > 0:
		pos = test * 0.1 - 1
		servo.value = pos
		print(pos)
		test = test - 1
		sleep(0.05)
	"""
